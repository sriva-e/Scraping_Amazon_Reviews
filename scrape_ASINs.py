import pandas as pd
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime


url = 'https://www.amazon.com/s?k=camera&rh=p_36%3A1253506011&dc&qid=1691890354&rnid=386442011&ref=sr_nr_p_36_4&ds=v1%3A7dle2xlGpHBQvqSlTFDrwlOBUmaQeIoXcVbZ3w8ljQs'
url_reviews = 1

count = 0
asinlist = []
reviewlist = []

s = HTMLSession()

#
# def random_values(d_lists):
#     """
#     Returns a random value from a list.
#
#     Args
#     """
#     idx = secrets.randbelow(len(d_lists))
#     return d_lists[idx]


# def user_agents():
#     """
#     Returns a random user agent string from a file containing a list of user agents.
#
#     Args:
#         -None
#
#     Returns:
#         -A string representing a random user agent.
#     """
#     with open('user-agents.txt') as f:
#         agents = f.read().split("\n")
#         return random_values(agents)

#
# headers = {
#     'user-agent':  user_agents()
# }


def get_soup(url):
    r = s.get(url, )
    r.html.render(sleep=15)
    soup = BeautifulSoup(r.html.html, 'html.parser')
    return soup


def get_next_page(soup):
    # this will return the next page URL
    try:
        pages = soup.find('span', {'class': 's-pagination-strip'})
        if not pages.find('span', {'class': 's-pagination-item s-pagination-next s-pagination-disabled'}):
            return 'https://www.amazon.com' + str(pages.find('a', {'class': 's-pagination-item s-pagination-next s-pagination-button s-pagination-separator'})['href'])
        else:
            return
    except:
        pass


def get_data_asin(soup):
    data = soup.find_all('div', {'data-asin': True})
    try:
        for item in data:
            asin = item.get('data-asin')
            asinlist.append(asin)
            print(asin)
    except:
        pass


while count != 20:
    count = count + 1
    data = get_soup(url)
    get_data_asin(data)
    url = get_next_page(data)
    if not url:
        break
    print(url)

asinlist = list(set(asinlist))
df = pd.DataFrame(asinlist)
#print(len(asinlist))
df.to_excel("./asin_new.xlsx", index=False)
print('Fin.')