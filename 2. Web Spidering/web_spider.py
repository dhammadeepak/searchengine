import requests
from bs4 import BeautifulSoup
import sqlite3

def crawler(start_url, max_pages = 10):
    #response = requests.get("https://www.bbc.co.uk/news/topics/c4y26wwj72zt")
    #print(response)
    #print(response.content)
    conn = sqlite3.connect('crawled_pages.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS pages (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              url TEXT UNIQUE,
              content TEXT
              )
    '''
    )
    conn.commit()

    url_frontier = [start_url]

    visited_pages = set()

    while url_frontier and len(visited_pages) < max_pages:

        url = url_frontier.pop(0)

        if url in visited_pages:
            continue

        print(f"Crawling {url}")
        response = requests.get(url)

        if response.status_code != 200:
            continue
        soup = BeautifulSoup(response.content,'html.parser')
        c.execute('INSERT OR IGNORE INTO pages (url,content) VALUES(?,?)',(url, str(soup)))
        conn.commit()

        links = soup.find_all('a')
        #print(links)

        for link in links:
            href = link.get("href")
            #print(href)
            if href and 'http' in href and href not in visited_pages:
                url_frontier.append(href)
                print(href)
        visited_pages.add(url)
    conn.close()
    print("Crawling complete")

seed_urls =["https://www.bbc.co.uk/news/topics/c4y26wwj72zt"]
crawler(seed_urls[0])