

import HTMLParser
import requests
from bs4 import BeautifulSoup

import urlparse
from pprint import pprint
import re

crawled_or_queued = set()
to_crawl = []

index = {}

print '--------'

def normalize(url):
    return url if url.endswith('/') else url + '/'

def crawl(url):
    r = requests.get(url)
    try:
        s = BeautifulSoup(r.text)
    except HTMLParser.HTMLParseError:
        return
    for link in s.findAll('a'):
        abs_link_url = normalize(urlparse.urljoin(url, link.get('href')))
        if not abs_link_url in crawled_or_queued:
            crawled_or_queued.add(abs_link_url)
            to_crawl.append(abs_link_url)
    elements = []
    for tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'p']:
        elements.extend(s.findAll(tag))
    for element in elements:
        text = element.getText()
        for w in set([''.join(re.findall(r'\w', x)).lower() for x in text.split()]):
            index.setdefault(w, []).append(url)


if __name__ == '__main__':
    try:
        to_crawl.append('http://www.nytimes.com/')
        while True:
            crawl(to_crawl.pop(0))
    except KeyboardInterrupt:
        pprint(index)
        print index.keys()

    while True:
        word = raw_input('enter search term!')
        if word in index:
            print "\n".join(set(index[word]))
        else:
            print 'sorry, no hits'


