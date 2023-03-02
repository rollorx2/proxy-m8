import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# list of websites to scrape
websites = ['https://www.socks-proxy.net/',
            'https://www.hide-my-ip.com/proxylist.shtml',
            'https://www.proxy-list.download/SOCKS5/',
            'https://www.proxydocker.com/en/socks5-proxy-list/',
            'https://free-proxy-list.net/']

# set up the selenium webdriver
options = webdriver.ChromeOptions()
options.add_argument('headless')
driver = webdriver.Chrome(options=options)

# scrape proxies from each website
proxies = []
for site in websites:
    try:
        response = requests.get(site)
        soup = BeautifulSoup(response.text, 'html.parser')
        if site == 'https://www.hide-my-ip.com/proxylist.shtml':
            table = soup.find('table', attrs={'id': 'listable'})
            rows = table.find_all('tr')
            for row in rows[1:]:
                cols = row.find_all('td')
                ip = cols[0].text.strip()
                port = cols[1].text.strip()
                proxies.append(f'{ip}:{port}')
        elif site == 'https://www.proxy-list.download/SOCKS5/':
            proxies.extend(soup.text.splitlines())
        elif site == 'https://www.proxydocker.com/en/socks5-proxy-list/':
            driver.get(site)
            content = driver.find_element_by_css_selector('.table-responsive').text
            proxies.extend(content.splitlines()[1:])
        elif site == 'https://free-proxy-list.net/':
            table = soup.find('table', attrs={'id': 'proxylisttable'})
            rows = table.find_all('tr')
            for row in rows[1:]:
                cols = row.find_all('td')
                ip = cols[0].text.strip()
                port = cols[1].text.strip()
                proxies.append(f'{ip}:{port}')
        else:
            rows = soup.find_all('tr')
            for row in rows[1:]:
                cols = row.find_all('td')
                ip = cols[0].text.strip()
                port = cols[1].text.strip()
                proxies.append(f'{ip}:{port}')
    except:
        pass

# check the validity of each proxy
valid_proxies = []
for proxy in proxies:
    try:
        response = requests.get('https://www.google.com', proxies={'socks5': proxy}, timeout=5)
        if response.status_code == 200:
            valid_proxies.append(proxy)
    except:
        pass

# write the working proxies to a text file
with open('working_proxies.txt', 'w') as f:
    for proxy in valid_proxies:
        f.write(f'{proxy}\n')
