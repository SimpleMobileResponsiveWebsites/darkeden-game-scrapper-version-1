import streamlit as st
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin

class WebScraper:
    @staticmethod
    def scrape_all(url):
        """
        Scrapes HTML, CSS, JS, and other resources from a webpage.

        :param url: URL to scrape
        :return: Dictionary with scraped data
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

            # Extract HTML
            html_content = soup.prettify()

            # Extract CSS and JS links
            css_links = [urljoin(url, link['href']) for link in soup.find_all('link', rel='stylesheet', href=True)]
            js_links = [urljoin(url, script['src']) for script in soup.find_all('script', src=True)]

            # Extract images
            img_links = [urljoin(url, img['src']) for img in soup.find_all('img', src=True)]

            return {
                "html": html_content,
                "css": css_links,
                "js": js_links,
                "images": img_links
            }
        except requests.RequestException as e:
            st.error(f"Error fetching webpage: {e}")
            return {}
        except Exception as e:
            st.error(f"Unexpected error during scraping: {e}")
            return {}


def main():
    # Set page configuration
    st.set_page_config(
        page_title="Enhanced Web Scraper",
        page_icon="🔍",
        layout="wide"
    )

    # Title and description
    st.title("Enhanced Web Scraper")
    st.write("Enter a URL to scrape HTML, CSS, JavaScript, and image data.")

    # URL Input
    url = st.text_input(
        "Enter Website URL",
        placeholder="https://example.com",
        help="Paste the full URL of the webpage you want to scrape."
    )

    # Scrape Button
    if st.button("Scrape Website", type="primary"):
        # Validate URL
        if not url:
            st.warning("Please enter a valid URL.")
            return

        # Progress indicators
        with st.spinner("Scraping website... Please wait"):
            scraped_data = WebScraper.scrape_all(url)

        # Display results
        if scraped_data:
            st.success("Scraping completed successfully!")

            # Display HTML
            st.subheader("HTML Content")
            st.code(scraped_data.get("html", "No HTML content found"), language="html")

            # Display CSS Links
            st.subheader("CSS Files")
            st.write(scraped_data.get("css", "No CSS files found"))

            # Display JS Links
            st.subheader("JavaScript Files")
            st.write(scraped_data.get("js", "No JavaScript files found"))

            # Display Image Links
            st.subheader("Image Files")
            st.write(scraped_data.get("images", "No images found"))

            # Download raw HTML
            st.download_button(
                label="Download HTML",
                data=scraped_data.get("html", ""),
                file_name="scraped_page.html",
                mime="text/html",
                help="Download the scraped HTML content."
            )

        else:
            st.error("Failed to scrape any data. Please check the URL and try again.")


# Run the Streamlit app
if __name__ == "__main__":
    main()
