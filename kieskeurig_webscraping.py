''' Use this bot to send mail notifications about the lowest price, scraping from Kieskeurig.nl'''


'''import'''
from bs4 import BeautifulSoup
import requests
from email.message import EmailMessage
import smtplib
import re
import time

'''Product information'''

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
    return('At {}, the {} priced as low as €{}. Check this link: {}'.format(self.get_store(), self.productname, self.get_price(), self.get_link()))

'''Mail setup'''

def mail_alert(subject, body, to):
  msg = EmailMessage()
  msg.set_content(body)
  msg['subject'] = subject
  msg ['to'] = to

  username = 'SENDINGMAILADDRESS' # Insert your 'sending from' gmail address 
  appkey = 'APPKEY' # Insert it's app password
  msg['from'] = username

  # Gmail server setup
  server = smtplib.SMTP('smtp.gmail.com', 587)
  server.starttls()
  server.login(username, appkey)
  server.send_message(msg)

  server.quit()

def main():
  # Vraag gegevens aan gebruiker
  starting_price  = int(input('Product starting price: €'))
  linkje = input('kieskeurig.nl link for this product: ')
  product_name = input('Product name: ')

  product = Product_kieskeurig(linkje, product_name)

  while True:
   # Send mail if the price is lowered, or wait. Check every 8 hours
    if starting_price > product.get_price():
      receive_mail_address = input('Receiving mail address: ')
      mail_alert('Lower price! '+ product_name, product.collect_data(), receive_mail_address) # Change MAILTOADDRESS to the emailaddress you want to receive the bot notifications
      starting_price = product.get_price()
     
      #wait 8 uur
      time.sleep(28800)
    else:
      time.sleep(28800)

if __name__ == '__main__':
  main()
