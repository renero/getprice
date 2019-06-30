# getprice

Connects to a set of URLs to extract the price value in them,
performing currency conversion (if applies), and printing a CSV-like formatted
output with the result.

A file called '.getprice.yaml' must be present in the
home directory, following the structure:

    item_name:
        url: https://my.store.com/path/to/the/article
        tag_id: priceblock             # the HTML tag you want to capture
        site_name: your site name      # simply for tracking purposes
        currency: EUR                  # default is EUR. Other values will be 
                                       # converted to EUR (i.e.: GBP)

If the currency is other than the default currency or not present, then 
it is converted using the latest available change rate.
