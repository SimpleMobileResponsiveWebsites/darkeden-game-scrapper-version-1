import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

class DarkEdenScraper:
    def __init__(self, base_url):
        """
        Initialize the scraper with the base URL of the DarkEden website
        
        :param base_url: Base URL of the DarkEden website to scrape
        """
        self.base_url = base_url
        self.session = requests.Session()
        # Add headers to mimic a browser request
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def get_page(self, url):
        """
        Fetch a webpage and return its BeautifulSoup object
        
        :param url: Full URL to scrape
        :return: BeautifulSoup object of the page
        """
        try:
            response = self.session.get(url)
            response.raise_for_status()  # Raise an exception for bad status codes
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching page {url}: {e}")
            return None

    def scrape_player_rankings(self, rankings_url):
        """
        Scrape player rankings from the specified URL
        
        :param rankings_url: URL of the rankings page
        :return: DataFrame with player ranking information
        """
        soup = self.get_page(rankings_url)
        if not soup:
            return pd.DataFrame()

        rankings = []
        # This is a placeholder - you'll need to adjust the selector based on the actual website structure
        ranking_rows = soup.find_all('tr', class_='ranking-row')
        
        for row in ranking_rows:
            try:
                rank = row.find('td', class_='rank').text.strip()
                player_name = row.find('td', class_='player-name').text.strip()
                level = row.find('td', class_='level').text.strip()
                
                rankings.append({
                    'Rank': rank,
                    'Player': player_name,
                    'Level': level
                })
            except Exception as e:
                print(f"Error parsing row: {e}")
        
        return pd.DataFrame(rankings)

    def scrape_game_servers(self, servers_url):
        """
        Scrape information about game servers
        
        :param servers_url: URL of the servers page
        :return: DataFrame with server information
        """
        soup = self.get_page(servers_url)
        if not soup:
            return pd.DataFrame()

        servers = []
        # This is a placeholder - adjust selectors based on actual website structure
        server_elements = soup.find_all('div', class_='server-info')
        
        for server in server_elements:
            try:
                name = server.find('span', class_='server-name').text.strip()
                population = server.find('span', class_='population').text.strip()
                status = server.find('span', class_='server-status').text.strip()
                
                servers.append({
                    'Server Name': name,
                    'Population': population,
                    'Status': status
                })
            except Exception as e:
                print(f"Error parsing server info: {e}")
        
        return pd.DataFrame(servers)

    def run_scraper(self, rankings_url, servers_url):
        """
        Run the full scraping process
        
        :param rankings_url: URL for player rankings
        :param servers_url: URL for server information
        """
        print("Starting DarkEden Web Scraper...")
        
        # Scrape player rankings
        print("Scraping Player Rankings...")
        rankings_df = self.scrape_player_rankings(rankings_url)
        if not rankings_df.empty:
            rankings_df.to_csv('darkeden_player_rankings.csv', index=False)
            print(f"Saved {len(rankings_df)} player rankings")
        
        # Scrape server information
        print("Scraping Server Information...")
        servers_df = self.scrape_game_servers(servers_url)
        if not servers_df.empty:
            servers_df.to_csv('darkeden_servers.csv', index=False)
            print(f"Saved {len(servers_df)} server entries")
        
        print("Scraping complete!")

# Example usage
if __name__ == "__main__":
    # Replace these URLs with the actual DarkEden game website URLs
    RANKINGS_URL = "https://example.com/darkeden/rankings"
    SERVERS_URL = "https://example.com/darkeden/servers"
    
    scraper = DarkEdenScraper("https://example.com/darkeden")
    scraper.run_scraper(RANKINGS_URL, SERVERS_URL)
