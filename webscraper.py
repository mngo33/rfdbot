import requests
from bs4 import BeautifulSoup

class RedFlagDeals:
    def __init__(self):
        self.base_url = 'https://forums.redflagdeals.com/search.php?keywords='
        self.url_end = '&sf=titleonly'
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}



    def key_words_search_words(self, user_message):
        words = user_message.split()[1:]
        keywords = '+'.join(words)
        search_words = ' '.join(words)
        return keywords, search_words

    def search(self, keywords):
        response = requests.get(self.base_url + keywords + self.url_end, headers=self.headers)
        content = response.content
        soup = BeautifulSoup(content, 'html.parser')
        result_links = soup.findAll('a')
        return result_links

    def send_link(self, result_links, search_words):
        send_link = []
        for link in result_links:
            text = link.text.lower()
            if search_words in text:
                send_link.append(link.get('href'))
        return send_link