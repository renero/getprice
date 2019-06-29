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
