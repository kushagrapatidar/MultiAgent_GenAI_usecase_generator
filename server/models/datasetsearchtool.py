import requests
from bs4 import BeautifulSoup
import time

class DatasetSearchTool:
    """
    Dynamic Dataset Search Tool scraping Kaggle, HuggingFace, and GitHub dataset search pages.
    Consolidates and deduplicates results from all sources.
    """

    def __init__(self, max_retries=3, delay=1.0):
        self.max_retries = max_retries
        self.delay = delay
        self.headers = {"User-Agent": "Mozilla/5.0 (compatible; Bot/1.0)"}

    def _search_kaggle(self, query):
        results = []
        url = f"https://www.kaggle.com/search?q={query.replace(' ', '+')}"
        for attempt in range(self.max_retries):
            try:
                resp = requests.get(url, headers=self.headers, timeout=10)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    for card in soup.find_all('div', {'class': 'block-link--hover'})[:10]:
                        a_tag = card.find('a')
                        if a_tag:
                            title = a_tag.get_text(strip=True)
                            link = 'https://www.kaggle.com' + a_tag.get('href')
                            results.append({'title': title, 'url': link})
                    break
                else:
                    time.sleep(self.delay)
            except requests.RequestException:
                time.sleep(self.delay)
        return results

    def _search_huggingface(self, query):
        results = []
        url = f"https://huggingface.co/datasets?search={query.replace(' ', '%20')}"
        for attempt in range(self.max_retries):
            try:
                resp = requests.get(url, headers=self.headers, timeout=10)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    # Each dataset is in an <a> tag under some container, inspect site for precise class if needed
                    for a_tag in soup.select('a[data-testid="dataset-card-link"]')[:10]:
                        title = a_tag.get_text(strip=True)
                        link = 'https://huggingface.co' + a_tag.get('href')
                        results.append({'title': title, 'url': link})
                    break
                else:
                    time.sleep(self.delay)
            except requests.RequestException:
                time.sleep(self.delay)
        return results

    def _search_github(self, query):
        results = []
        url = f"https://github.com/search?q={query.replace(' ', '+')}+dataset&type=repositories"
        for attempt in range(self.max_retries):
            try:
                resp = requests.get(url, headers=self.headers, timeout=10)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    # Search repos with "dataset" in description or name, picks repo titles and URLs
                    repo_list = soup.find_all('li', class_='repo-list-item')[:10]
                    for repo in repo_list:
                        a_tag = repo.find('a', {'class': 'v-align-middle'})
                        if a_tag:
                            title = a_tag.get_text(strip=True)
                            link = 'https://github.com' + a_tag.get('href')
                            results.append({'title': title, 'url': link})
                    break
                else:
                    time.sleep(self.delay)
            except requests.RequestException:
                time.sleep(self.delay)
        return results

    def search(self, query):
        consolidated_results = []
        seen_urls = set()

        # Search Kaggle datasets
        kaggle_results = self._search_kaggle(query)
        for item in kaggle_results:
            if item['url'] not in seen_urls:
                consolidated_results.append(item)
                seen_urls.add(item['url'])

        # Search HuggingFace datasets
        huggingface_results = self._search_huggingface(query)
        for item in huggingface_results:
            if item['url'] not in seen_urls:
                consolidated_results.append(item)
                seen_urls.add(item['url'])

        # Search GitHub repos (dataset repos)
        github_results = self._search_github(query)
        for item in github_results:
            if item['url'] not in seen_urls:
                consolidated_results.append(item)
                seen_urls.add(item['url'])

        # Limit total results to 15 combined
        consolidated_results = consolidated_results[:15]

        return {'links': consolidated_results}
