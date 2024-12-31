import requests
import streamlit as st

def get_google_autosuggestions(query):
    # Google's autosuggest URL
    url = "https://www.google.com/complete/search"
    
    # Headers to mimic a real browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # Parameters for the request
    params = {
        'q': query,          # The query you want suggestions for
        'client': 'chrome',  # Mimic a Chrome browser
        'hl': 'en'           # Language (English)
    }
    
    # Send the request
    response = requests.get(url, headers=headers, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        suggestions = response.json()[1]
        return suggestions
    else:
        st.error(f"Failed to fetch suggestions. Status code: {response.status_code}")
        return []

# Streamlit UI
st.title("Google Autosuggest Scraper")
st.write("Enter a keyword to get Google's autosuggestions.")

# Input field for the keyword
keyword = st.text_input("Enter a keyword:", "python")

# Button to trigger the scraper
if st.button("Get Suggestions"):
    if keyword:
        # Get autosuggestions
        suggestions = get_google_autosuggestions(keyword)
        
        # Display the suggestions
        if suggestions:
            st.write(f"Autosuggestions for '{keyword}':")
            for suggestion in suggestions:
                st.write(f"- {suggestion}")
        else:
            st.write("No suggestions found.")
    else:
        st.warning("Please enter a keyword.")
