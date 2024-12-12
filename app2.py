import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import BytesIO

def scrape_data(url):
    """Scrape data from the provided URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Example: Extract table data
        tables = soup.find_all('table')
        if not tables:
            return pd.DataFrame(), "No tables found on the page."
        
        table_data = pd.read_html(str(tables))
        # Combine all tables into one DataFrame if multiple tables are found
        combined_df = pd.concat(table_data, ignore_index=True)
        return combined_df, "Scrape successful!"
    except Exception as e:
        return pd.DataFrame(), str(e)

# Streamlit UI
st.title("Dark Eden Web Scraper")

# User input for URL
url = st.text_input("Enter the URL to scrape:", placeholder="https://example.com")

# Button to start scraping
if st.button("Scrape Data"):
    if url:
        # Scrape the data
        data, message = scrape_data(url)
        st.write(message)

        if not data.empty:
            # Display data as a table
            st.dataframe(data)

            # Allow user to download the data
            csv_buffer = BytesIO()
            data.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)

            xml_buffer = BytesIO()
            data.to_xml(xml_buffer, index=False)
            xml_buffer.seek(0)

            st.download_button("Download as CSV", data=csv_buffer, file_name="scraped_data.csv", mime="text/csv")
            st.download_button("Download as XML", data=xml_buffer, file_name="scraped_data.xml", mime="application/xml")
        else:
            st.error("No data found to scrape.")
    else:
        st.error("Please enter a valid URL.")
