import requests
from bs4 import BeautifulSoup
from time import sleep
from telegram import Bot

bot = Bot(token='5830451746:AAGNvcvXOLHCbwXsGUH5ts4wxzSyYP29Bq0')  # Replace 'YOUR_BOT_TOKEN' with your Bot's API token

url = "https://eomisae.co.kr/os"

# Initial state of the website
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

cards = soup.find_all('div', {'class': 'card_el n_ntc clear'})
products = []
sent_list = []
counter = 0

while True:
    for card in cards:
        product = {}
        product['img_url'] = card.find('img', {'class': 'tmb'}).get('src')  # Image URL
        product['title'] = card.find('a', {'class': 'pjax'}).get_text()  # Title of the product
        product['url'] = card.find('a', {'class': 'pjax'}).get('href')  # Product URL
        product['comment'] = int(
            card.find('i', {'class': 'ion-ios-chatbubble'}).parent.get_text(strip=True))  # number of comments
        product['heart'] = int(
            card.find('i', {'class': 'ion-ios-heart'}).parent.get_text(strip=True))  # number of hearts

        # Check if the product is already in the sent list
        if product['url'] not in sent_list:
            # If the number of hearts exceeds 3 or the number of comments exceeds 5
            if product['heart'] > 3 or product['comment'] > 5:
                try:
                    bot.send_message(chat_id='1905923211', text=str(product['title'] + '\n' + product['url']))
                except Exception as e:
                    print(f"Error sending message: {e}")

                sent_list.append(product['url'])
                print(product['title'])

    # Refresh the page and update the list of products every minute
    sleep(60)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.find_all('div', {'class': 'card_el n_ntc clear'})

    counter +=1 # 1분에 하나씩 증가
    if counter == 1440:
        sent_list = []
        counter = 0