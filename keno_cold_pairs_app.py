
import streamlit as st
import requests
from itertools import combinations
from collections import defaultdict

# Function to fetch Keno results using the keno-api wrapper
def fetch_keno_results(n=500):
    url = f"https://kenoapi.netlify.app/.netlify/functions/api/games?limit={n}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return [game["numbers"] for game in data["games"]]
    else:
        st.error("Failed to fetch Keno results.")
        return []

# Function to find cold number pairs
def find_coldest_pairs(games):
    pair_latest_seen = defaultdict(lambda: -1)

    for i, numbers in enumerate(reversed(games)):
        for pair in combinations(sorted(numbers), 2):
            if pair_latest_seen[pair] == -1:
                pair_latest_seen[pair] = i

    sorted_pairs = sorted(pair_latest_seen.items(), key=lambda x: -x[1])
    return sorted_pairs[:10]

# Streamlit UI
st.title("ðŸ“‰ Top 10 Coldest Number Pairs")

games = fetch_keno_results(500)

if games:
    coldest_pairs = find_coldest_pairs(games)
    for i, (pair, count) in enumerate(coldest_pairs, 1):
        st.markdown(f"**{i}. {pair[0]} & {pair[1]}** â€” not drawn together in the last **{count}** games.")
