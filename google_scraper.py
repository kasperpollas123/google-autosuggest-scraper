import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import streamlit as st

# Function to get Google autosuggestions
def get_google_autosuggestions(query):
    url = "https://www.google.com/complete/search"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    params = {
        'q': query,
        'client': 'chrome',
        'hl': 'en'
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()[1]
    else:
        st.error(f"Failed to fetch suggestions for '{query}'. Status code: {response.status_code}")
        return []

# Function to fetch all suggestions
def fetch_all_suggestions(seed_keyword):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    queries = [f"{seed_keyword} {letter}" for letter in alphabet] + [f"{letter} {seed_keyword}" for letter in alphabet]
    all_suggestions = set()
    for query in queries:
        suggestions = get_google_autosuggestions(query)
        all_suggestions.update(suggestions)
    return sorted(all_suggestions)

# Function to scrape SERP for a keyword
def scrape_serp(keyword):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    url = f"https://www.google.com/search?q={keyword}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        st.error(f"Failed to fetch SERP for '{keyword}'. Status code: {response.status_code}")
        return []
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    for result in soup.select("div.g")[:10]:  # Limit to first 10 results
        try:
            title = result.select_one("h3").text
            snippet = result.select_one("div.IsZvec").text
            results.append({"Keyword": keyword, "Title": title, "Snippet": snippet})
        except AttributeError:
            continue
    return results

# Streamlit UI
st.title("Google Autosuggest Keyword Expander with SERP Results")
seed_keyword = st.text_input("Enter a seed keyword:", "dog training")

if st.button("Generate Keywords and Scrape SERP"):
    if seed_keyword:
        # Fetch all suggestions
        with st.spinner("Fetching suggestions..."):
            suggestions = fetch_all_suggestions(seed_keyword)
        
        # Scrape SERP for each suggestion
        serp_data = []
        for keyword in suggestions:
            with st.spinner(f"Scraping SERP for '{keyword}'..."):
                results = scrape_serp(keyword)
                serp_data.extend(results)  # Add all results for this keyword
                time.sleep(5)  # Add a delay to avoid detection
        
        # Display the suggestions
        if serp_data:
            st.write(f"Found {len(suggestions)} unique keywords with SERP results:")
            df = pd.DataFrame(serp_data)
            st.write(df)
            
            # Option to download the results as an Excel file
            excel_file = "keywords_with_serp.xlsx"
            df.to_excel(excel_file, index=False)
            with open(excel_file, "rb") as f:
                st.download_button(
                    label="Download Results as Excel",
                    data=f,
                    file_name=excel_file,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.write("No SERP results found.")
    else:
        st.warning("Please enter a seed keyword.")
