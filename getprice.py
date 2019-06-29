"""
Connects to a URL and extract the price of an article,
performing currency conversion (if applies), and prints a CSV-like formatted
output with the result.

A file called '.getprice.yaml' must be present in the
working directory, following the structure:

item_name:
    url: https://my.store.com/path/to/the/article
    tag_id: priceblock
    site_name: amazon
    currency: EUR

If the currency is other than the default currency, then it is converted
using the latest available change rate.
"""

import string
import warnings
from datetime import date

import urllib3
import yaml
from bs4 import BeautifulSoup
from forex_python.converter import CurrencyRates

warnings.simplefilter('ignore')


def read_params():
    """
    Read the parameters from a default filename
    :return:
    """
    default_params_file = '.getprice.yaml'
    params = {}
    with open(default_params_file, 'r') as config:
        try:
            params = yaml.safe_load(config)
        except yaml.YAMLError as exc:
            print(exc)

    return params


def remove_non_numeric(captured_string: string):
    """
    Remove non numeric characters from argument.
    :type captured_string: string
    """
    caption = captured_string
    non_numeric_chars = ''.join(
        set(string.printable).union({'€', '£', '\xa0'}) - set(
            string.digits) - {',', '.'})

    # Loop over non numeric chars to remove them from string.
    for c in non_numeric_chars:
        caption = caption.replace(c, '')

    # If comma separator is ',' replace it by '.'
    caption = caption.replace(',', '.')

    return caption


def retrieve_price(html_code: bytes, tag_id: string):
    """
    Access the HTML code, searching for a specific ID tag, and treat it as
    a number, returning its float value.
    :param html_code: the HTML page
    :param tag_id: The HTML tag we're looking for.
    :return: The price in float value
    """
    soup = BeautifulSoup(html_code, 'lxml')
    item_price = soup.find(id=tag_id).get_text().strip()
    item_price = remove_non_numeric(item_price)
    item_price = float(item_price)
    return item_price


# Prepare common data structures.
params = read_params()
date_string = date.today()
http = urllib3.PoolManager()

# Loop over items
for item in params.keys():
    # Fetch page
    request = http.request('GET', params[item]['url'])

    # Access HTML tag
    price = retrieve_price(request.data, params[item]['tag_id'])

    # Currency conversion, if applicable.
    if params[item]['currency'] != 'EUR':
        converter = CurrencyRates()
        price = converter.convert(params[item]['currency'], 'EUR', price)

    # Printout everything.
    print('{},{},{},{:.2f}'.format(item, params[item]['site_name'],
                                   date_string, price))
