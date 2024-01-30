# Import the necessary libraries
from bs4 import BeautifulSoup as bs
import urllib.request
import csv
import re

def main():
    # Open the file in write mode
    with open('scrap.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        # Write the headers to the CSV file
        writer.writerow(['Name', 'Year release', 'Kms', 'Box', 'Energy', 'Price'])

        # Loop through the pages to scrape
        for i in range(1, 11):
            # Build the URL for the page to scrape
            url = "https://www.lacentrale.fr/listing?makesModelsCommercialNames=&options=&page={}".format(i)
            # Open the URL and create a BeautifulSoup object to parse the HTML
            page = urllib.request.urlopen(url, timeout=5)
            soup = bs(page, 'html.parser')
            # Scrape the name, motor, and price of the car
            name = scrap_name(soup)
            price = scrap_price(soup)
            # Sort the remaining characteristics of the car and return them as separate lists
            year, kms_str, box, energy = sorting(soup)
            # Write the scraped data to the CSV file
            csv_create(name, year, kms_str, box, energy, price, writer)

def forming(var):
    # Create a list of text from a list of BeautifulSoup elements
    var_tab = []
    for e in var:
        e = e.text
        var_tab.append(e)
    return var_tab

def scrap_name(soup):
    # Scrape the name of the car
    return forming(soup.find_all('h3', {'class': 'Text_Text_subtitle2'}))

def scrap_characteristics(soup):
    # Scrape the characteristics of the car
    return forming(soup.find_all('div', {'class': 'Vehiculecard_Vehiculecard_characteristicsItems'}))

def scrap_price(soup):
    # Scrape the price of the car
    return forming(soup.find_all('span', {'class': 'Text_Text_subtitle2'}))

def sorting(soup):
    # Create a table for all the scrap_caracteristics
    elements = []
    # Scrape the characteristics of the car
    caracteristics = scrap_characteristics(soup)
    # Put all the informations into the table
    for caractere in caracteristics:
        elements.append(caractere)
    # Pad elements with empty strings if it has less than 16 elements
    while len(elements) < 16:
        elements.append("")
    x = 0
    # Create tables for all the information category we get
    years = []
    kms = []
    box = []
    energy = []
    while x < 16 * 4:
        # Put all information from element into our new tables
        years.append(elements[x])
        kms_value = elements[x+1]
        # Use regex to extract digits and convert to int
        kms_match = re.search(r'\d+', kms_value)
        kms.append(int(kms_match.group()) if kms_match else 0)
        box.append(elements[x + 2])
        energy.append(elements[x + 3])
        x += 4
    # Return the sorted lists of characteristics
    return years, kms, box, energy


def csv_create(name, year, kms_str, box, energy, price, writer) :
    y = 1
    while y < 16:
        """ Show the elements get in the colomns"""
        writer.writerow([name[y], year[y], kms_str[y], box[y], energy[y], price[y]]) 
        y += 1
    """ Validate if the file is create """
    print("Page chargée")


main()
