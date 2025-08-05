import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import streamlit as st

st.set_page_config(page_title="Kenalytics", layout="centered")

st.title("🎯 Kenalytics: Cold Number Finder")

st.markdown("This app scans recent Keno results and shows the top 10 longest undrawn number pairs.")

URL = "https://www.lottoland.com/au/keno-results"

@st.cache_data(show_spinner=False)
def fetch_keno_draws():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    draw_sections = soup.find_all("ul", class_="lottoBalls")

    draws = []
    for section in draw_sections:
        balls = section.find_all("li")
        if len(balls) >= 20:
            numbers = sorted([int(b.text) for b in balls if b.text.strip().isdigit()])
            draws.append(numbers)
    return draws[:100]

def get_undrawn_pairs(draws):
    pair_streaks = defaultdict(int)
    last_seen = {}

    all_pairs = [(i, j) for i in range(1, 80) for j in range(i+1, 81)]

    for idx, draw in enumerate(draws):
        draw_set = set(draw)
        for pair in all_pairs:
            if pair[0] in draw_set and pair[1] in draw_set:
                last_seen[pair] = idx

    for pair in all_pairs:
        last = last_seen.get(pair, len(draws))
        pair_streaks[pair] = len(draws) - last

    sorted_pairs = sorted(pair_streaks.items(), key=lambda x: x[1], reverse=True)
    return sorted_pairs[:10]

draws = fetch_keno_draws()
top_pairs = get_undrawn_pairs(draws)

st.subheader("📊 Top 10 Coldest Number Pairs")

for idx, (pair, streak) in enumerate(top_pairs, start=1):
    st.write(f"**{idx}. {pair[0]} & {pair[1]}** — not drawn together in the last **{streak}** games.")
