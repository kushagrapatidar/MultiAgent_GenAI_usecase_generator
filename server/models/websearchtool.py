import requests
from bs4 import BeautifulSoup
import time


class WebSearchTool:
    """
    Dynamic Web Search Tool with retry logic, user-agent support,
    and optional API key for production use.
    Currently scrapes Bing search results.
    """

    def __init__(self, api_key=None, max_retries=3, delay=1.0):
        self.api_key = api_key
        self.max_retries = max_retries
        self.delay = delay
        self.headers = {"User-Agent": "Mozilla/5.0 (compatible; Bot/1.0)"}

    def search(self, queries):
        results = {'links': []}
        for query in queries:
            for attempt in range(self.max_retries):
                try:
                    url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
                    resp = requests.get(url, headers=self.headers, timeout=10)
                    if resp.status_code == 200:
                        soup = BeautifulSoup(resp.text, 'html.parser')
                        for item in soup.find_all('li', {'class': 'b_algo'}):
                            title_tag = item.find('h2')
                            link_tag = title_tag.find('a') if title_tag else None
                            if title_tag and link_tag:
                                title = title_tag.get_text()
                                link = link_tag.get('href')
                                # Avoid duplicates
                                if not any(l['url'] == link for l in results['links']):
                                    results['links'].append({'title': title, 'url': link})
                                if len(results['links']) >= 10:
                                    break
                        break  # success, break retry loop
                    else:
                        time.sleep(self.delay)
                except requests.RequestException:
                    time.sleep(self.delay)
            if len(results['links']) >= 10:
                break
        return results