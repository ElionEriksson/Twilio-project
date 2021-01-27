from twilio.rest import Client
import Authorization as auth
import requests
from bs4 import BeautifulSoup
from datetime import date
import matplotlib.pyplot as plt

URL = 'https://www.blocket.se/annonser/hela_sverige/fordon/bilar?cb=40&cbl1=6&cg=1020&fu=4&mye=2017'

# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36'}

page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

#Enter price point
price = 150000

#all objoekts that fits the search

dates = []
prices = []
years = []
milage = []

def get_cars():
    ad_elems = soup.find_all("article", class_="hidZFy")
    today = date.today()
    cuurent_date = today.strftime("%d/%m/%Y")
    for cars in ad_elems:
        # hitta namn, pris och url
        dates.append(cuurent_date)
        # car_price = cars.find("div", class_ = "bNwNaE").text
        # prices.append(int(car_price[:-3].replace(' ', '')))

        #to get more info on the car
        car_URL = 'https://www.blocket.se' + cars.find("a", class_="enigRj")["href"]
        car_page = requests.get(car_URL)
        car_soup = BeautifulSoup(car_page.content, 'html.parser')
        car_price = int(car_soup.find('div', class_= 'EkzGO').text[0:-3].replace(' ', ''))
        if car_price <= price:
            send_sms(car_URL, car_price)
        prices.append(car_price)
        car_info_unfiltered = car_soup.find_all('div', class_= 'eZCCwh')

        car_info_filtered = []
        for item in car_info_unfiltered:
            car_info_filtered.append(item.text)
        
        car_year = None
        car_milage = None
        #find milage
        for info in car_info_filtered:
            if len(info) == 5:
                car_year = int(info[0:-1])
                years.append(car_year)
            if len(info) > 9 and car_milage is None:
                car_milage = int(info[-6:-1].replace(' ', '').replace('-', ''))
                milage.append(car_milage)

def plot_graph():
    plt.plot(prices, milage, 'ro')
    plt.ylabel('Miltal')
    plt.xlabel('Pris')
    plt.show()

def statistics():
    medel = sum(prices) / len(prices)
    print(f'Medelvärde: {medel}')

def send_sms(Car_URL, car_price):
    # Your Account SID from twilio.com/console
    account_sid = auth.account_sid
    # Your Auth Token from twilio.com/console
    auth_token  = auth.auth_token

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+460708163050", 
        from_="+19704328522",
        body= f"New car found!! the car costs: {car_price} and can be found at URL: {Car_URL}")

    print(message.sid)
    
if __name__ == "__main__":
    get_cars()
    # plot_graph()
    statistics()

