from requests_html import HTMLSession
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import random

# List of proxies
proxies = [
    'us-ca.proxymesh.com:31280',
    'us-wa.proxymesh.com:31280',
    'fr.proxymesh.com:31280',
    'jp.proxymesh.com:31280',
    'au.proxymesh.com:31280',
    'de.proxymesh.com:31280',
    'nl.proxymesh.com:31280',
    'sg.proxymesh.com:31280',
    'us-il.proxymesh.com:31280',
    'us-tx.proxymesh.com:31280',
    'us-dc.proxymesh.com:31280',
    'us-ny.proxymesh.com:31280',
    'uk.proxymesh.com:31280',
    'ch.proxymesh.com:31280',
    'us-fl.proxymesh.com:31280',
    'open.proxymesh.com:31280',
    'world.proxymesh.com:31280'
    # Add more proxies as needed
]

url = 'https://www.amazon.com/s?k=camera&ref=nb_sb_noss'
# url_reviews = 1

count = 0
review_list = []

s = HTMLSession()


def get_random_proxy():
    return random.choice(proxies)


def get_soup(url1):
    try:
        proxy = get_random_proxy()
        r = s.get(url1, proxies={'http': proxy})
        r.html.render(sleep=100)
        soup = BeautifulSoup(r.html.html, 'html.parser')
        return soup
    except:
        pass


def get_helpful_votes(item):
    if item.find('span', {'data-hook': 'helpful-vote-statement'}):
        return item.find('span', {'data-hook': 'helpful-vote-statement'}).text.replace('One person found this helpful', '1').replace('people found this helpful', '')
    else:
        return '0'


def get_verified_purchase_status(item):
    if item.find('span', {'data-hook': 'avp-badge'}):
        return item.find('span', {'data-hook': 'avp-badge'}).text.strip()
    else:
        return 'Not a verified purchase'


def get_date(item):
    date_string = item.find('span', {'data-hook': 'review-date'}).text.replace('Reviewed in the United States on ', '').replace('Reviewed in the United States 🇺🇸 on ', '').strip()
    print(date_string)
    date_format = "%B %d, %Y"
    return datetime.strptime(date_string, date_format).date()


def get_all_reviews(profile_page):
    reviews = profile_page.find_all('div', {'class': 'your-content-card-top'})
    all_review_list = []
    for item in reviews:
        review = {
         'title': item.find('h1').text.strip(),
         'review': item.find('span').text.strip(),
        }
        all_review_list.append(review)
    return all_review_list


def get_profile_data(profile_url):
    profile_page = get_soup(profile_url)
    all_review_list = get_all_reviews(profile_page)
    profile_info = {}
    try:
        profile_info = {
            'profile_name': profile_page.find('span', {'class': 'card-title'}).text.strip(),
            'helpful_votes': profile_page.find('div', {'class': 'impact-cell'}).find('span', {'class': 'impact-text'}).text.strip(),
            'all_reviews': all_review_list
        }
    except:
        pass

    return profile_info


def get_link(link):
    return 'https://www.amazon.com' + str(link)


def get_reviews(soup, asin):
    reviews = soup.find_all('div', {'data-hook': 'review'})
    try:
        for item in reviews:
            review = {
                'product_identifier': asin,
                'product_name': soup.title.text.replace('Amazon.com: Customer reviews:', '').strip(),
                'review_title': item.find('a', {'data-hook': 'review-title'}).text.strip(),
                'review_date': get_date(item),
                'reviewer_name': item.find('span', {'class': 'a-profile-name'}).text.strip(),
                'reviewer_profile_link': item.find('a', {'class': 'a-profile'})['href'],
                'profile_data': get_profile_data(get_link(item.find('a', {'class': 'a-profile'})['href'])),
                'rating':  float(item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
                'full_review': item.find('span', {'data-hook': 'review-body'}).text.strip(),
                'helpful_votes': get_helpful_votes(item),
                'verified_purchase': get_verified_purchase_status(item),
            }
            print(review)
            review_list.append(review)
    except:
        pass


# def get_next_review_page(soup):
#     try:
#         pages = soup.find('div', {'data-hook': 'pagination-bar'})
#         if not pages.find('li', {'class': 'a-disabled a-last'}):
#             div = pages.find('li', {'class': 'a-last'})
#             return 'https://www.amazon.com' + str(div.find('a')['href'])
#         else:
#             return False
#     except:
#         pass


df = pd.read_excel('asinlist.xlsx', skiprows=291)
asin_list = df.iloc[:, 0].tolist()

for asin in asin_list:
    print(asin)
    url_reviews = f'https://www.amazon.com/product-reviews/{asin}/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews'
    data = get_soup(url_reviews)
    get_reviews(data, asin)
    df = pd.DataFrame(review_list)
    df.to_excel('camera9.xlsx',index=False)


df = pd.DataFrame(review_list)
df.to_excel('camera2.xlsx', index=False)
print('Fin.')