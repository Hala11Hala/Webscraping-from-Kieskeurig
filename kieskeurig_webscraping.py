'''import'''
from bs4 import BeautifulSoup
import requests
from email.message import EmailMessage
import smtplib
import re
import time

'''Receive notifications about deals on kieskeurig'''

class Product_kieskeurig:
  def __init__ (self, url, productname, store = '', price = 0, link = ''):
    self.url = url
    self.productname = productname
    self.store = store
    self.price = price
    self.link = link

    website = requests.get(url).text
    self.soup = BeautifulSoup(website, 'lxml')


  def get_price(self):
    price = self.soup.find('span', class_ = 'price').contents[0].strip()
    price = re.sub(r'[^\d]', '', price)
    price = float(price)/100
    return int(price)

  def get_store(self):
    store = self.soup.find('span', class_ = 'customer').text.strip()
    return store

  def get_link(self):
    link = self.soup.find('a', href=re.compile('https://log.kieskeurig.nl/click'))
    return link['href'] if link else None

  def collect_data(self):
    return('Current lowest price for {}: €{} at {}. Check this link: {}'.format(self.productname, self.get_price(), self.get_store(), self.get_link()))

'''Mail function'''

def mail_alert(subject, body, to):
  msg = EmailMessage()
  msg.set_content(body)
  msg['subject'] = subject
  msg ['to'] = to

  username = #gmail-address that will notify the user
  appkey = # gmail appkey
  msg['from'] = username

  # Gmail server setup
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login(username, appkey)
  server.send_message(msg)

  server.quit()

def main():
   # Ask the user some info
  product_link = input('product link (kieskeuring link): ')
  product_name = input('Product name: ')
  
  product = Product_kieskeurig(product_link, product_name)
  starting_price = product.get_price()
  print('---------------------------------------------------------------------------------------------')
  print('Note: This bot will only send notifications if the price is below €{}.'.format(starting_price))
  print('---------------------------------------------------------------------------------------------')
  receive_mail_address = input('Mailaddress on which you want to be notified: ')
  interval = int(input('How many minutes between price checks: '))
  
  while True:
   # Notify mail if price is lower, otherwise wait
    if starting_price > product.get_price():
      mail_alert('Lowest price '+ product_name, product.collect_data(), receive_mail_address)
      starting_price = product.get_price()

      print('Mail sended to {}'.format(receive_mail_address))
      print("I'll check again in about {} minute(s)!".format(interval))
      time.sleep(interval*60)
    
    else:
      print('No lower price found.')
      print("I'll check again in about {} minute(s)!".format(interval))
      time.sleep(interval*60)

if __name__ == '__main__':
  main()
