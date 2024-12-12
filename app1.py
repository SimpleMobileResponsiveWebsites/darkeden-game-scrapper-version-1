import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

class DarkEdenScraper:
    @staticmethod
    def scrape_website(url):
        """
        Generic web scraping method with error handling
        
        :param url: URL to scrape
        :return: Pandas DataFrame with scraped data
        """
        try:
            # Add headers to mimic browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Fetch the webpage
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract table data (generic approach)
            table = soup.find('table')
            
            if not table:
                st.warning("No table found on the page. Unable to scrape data.")
                return pd.DataFrame()
            
            # Extract headers
            headers = [header.text.strip() for header in table.find_all('th')]
            
            # Extract rows
            rows = []
            for row in table.find_all('tr')[1:]:  # Skip header row
                cols = row.find_all('td')
                row_data = [col.text.strip() for col in cols]
                
                # Only add row if it has data
                if row_data:
                    rows.append(row_data)
            
            # Create DataFrame
            if headers and rows:
                df = pd.DataFrame(rows, columns=headers[:len(rows[0])])
                return df
            else:
                st.warning("Could not extract meaningful data from the table.")
                return pd.DataFrame()
        
        except requests.RequestException as e:
            st.error(f"Error fetching webpage: {e}")
            return pd.DataFrame()
        except Exception as e:
            st.error(f"Unexpected error during scraping: {e}")
            return pd.DataFrame()

def main():
    # Set page configuration
    st.set_page_config(
        page_title="DarkEden Web Scraper",
        page_icon="🕸️",
        layout="wide"
    )
    
    # Title and description
    st.title("🌐 DarkEden Web Scraper")
    st.write("Enter a URL to scrape tabular data from a webpage")
    
    # URL Input
    url = st.text_input(
        "Enter Website URL", 
        placeholder="https://example.com/darkeden/data",
        help="Paste the full URL of the webpage containing the data you want to scrape"
    )
    
    # Scrape Button
    if st.button("Scrape Website 🚀", type="primary"):
        # Validate URL
        if not url:
            st.warning("Please enter a valid URL")
            return
        
        # Progress indicators
        with st.spinner("Scraping website... Please wait"):
            # Perform scraping
            scraped_df = DarkEdenScraper.scrape_website(url)
        
        # Display results
        if not scraped_df.empty:
            # Display DataFrame
            st.success("Scraping completed successfully!")
            
            # Data Preview
            st.subheader("Scraped Data Preview")
            st.dataframe(scraped_df)
            
            # Download Button
            csv = scraped_df.to_csv(index=False)
            st.download_button(
                label="Download CSV 📥",
                data=csv,
                file_name='scraped_data.csv',
                mime='text/csv',
                help="Download the scraped data as a CSV file"
            )
            
            # Additional DataFrame insights
            st.subheader("Data Insights")
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Total Rows", len(scraped_df))
            
            with col2:
                st.metric("Total Columns", len(scraped_df.columns))
        else:
            st.error("No data could be scraped. Please check the URL and webpage structure.")

# Run the Streamlit app
if __name__ == "__main__":
    main()
