import requests
import streamlit as st

def get_google_autosuggestions(query, country_code="us", language_code="en"):
    # Google's autosuggest URL (using country-specific domain)
    google_domain = f"https://www.google.com"  # Default to global domain
    if country_code:
        google_domain = f"https://www.google.{country_code}"
    
    url = f"{google_domain}/complete/search"
    
    # Headers to mimic a real browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Parameters for the request
    params = {
        'q': query,          # The query you want suggestions for
        'client': 'chrome',  # Mimic a Chrome browser
        'hl': language_code, # Language (e.g., "en" for English)
        'gl': country_code   # Country (e.g., "us" for the United States)
    }
    
    # Send the request
    response = requests.get(url, headers=headers, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        suggestions = response.json()[1]
        return suggestions
    else:
        st.error(f"Failed to fetch suggestions for '{query}'. Status code: {response.status_code}")
        return []

def fetch_all_suggestions(seed_keyword, country_code="us", language_code="en"):
    # Alphabet for appending/prepending letters
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    
    # Generate queries
    queries = [f"{seed_keyword} {letter}" for letter in alphabet] + [f"{letter} {seed_keyword}" for letter in alphabet]
    
    # Fetch suggestions for all queries
    all_suggestions = set()
    for query in queries:
        suggestions = get_google_autosuggestions(query, country_code, language_code)
        all_suggestions.update(suggestions)
    
    return sorted(all_suggestions)

# Streamlit UI
st.title("Google Autosuggest Keyword Expander")
st.write("Enter a seed keyword to generate an extensive list of related keywords.")

# Input field for the seed keyword
seed_keyword = st.text_input("Enter a seed keyword:", "dog training")

# Dropdown for country selection
countries = {
    "United States": "us",
    "United Kingdom": "uk",
    "Canada": "ca",
    "Australia": "au",
    "France": "fr",
    "Germany": "de",
    "Spain": "es",
    "India": "in"
}
selected_country = st.selectbox("Select a country:", list(countries.keys()))
country_code = countries[selected_country]

# Dropdown for language selection
languages = {
    "English": "en",
    "Spanish": "es"
}
selected_language = st.selectbox("Select a language:", list(languages.keys()))
language_code = languages[selected_language]

# Button to trigger the keyword expansion
if st.button("Generate Keywords"):
    if seed_keyword:
        # Fetch all suggestions
        with st.spinner("Fetching suggestions..."):
            suggestions = fetch_all_suggestions(seed_keyword, country_code, language_code)
        
        # Display the suggestions
        if suggestions:
            st.write(f"Found {len(suggestions)} unique keywords:")
            st.write(suggestions)
            
            # Option to download the results as a text file
            st.download_button(
                label="Download Keywords",
                data="\n".join(suggestions),
                file_name="keywords.txt",
                mime="text/plain"
            )
        else:
            st.write("No suggestions found.")
    else:
        st.warning("Please enter a seed keyword.")
