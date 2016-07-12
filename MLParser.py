#! /usr/bin/python
import sys
import os
from lxml import html
import requests
from statistics import mean
from statistics import mode
from statistics import median
from statistics import stdev
from statistics import median_grouped

def removeOutliers(priceList, mean, stdev):
	for price in priceList:
		if (abs(((price - mean)/stdev)) > 1):
			priceList.remove(price)

	return(priceList)


def ParseMLPrice(url):
	adPrices = []
	statusCode = 200
	counter = 1
	header = {
				'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
				'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
				'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
				'Accept-Encoding': 'none',
				'Accept-Language': 'en-US,en;q=0.8',
				'Connection': 'keep-alive'
				}

	while (statusCode == 200):
		try:
			page = requests.get(url)
			tree = html.fromstring(page.content)
		except requests.exceptions.Timeout as t:
			# Maybe set up for a retry, or continue in a retry loop
			print('ERROR: URL Timeout! Skipping...')
		except requests.exceptions.TooManyRedirects as r:
			# Tell the user their URL was bad and try a different one
			print('ERROR: Too Many Redirects! Skipping...')
		except requests.exceptions.ConnectionError as c:
			# Tell the user their URL isn't found
			print('ERROR: Connection Error!')
			sys.exit(1)
		except requests.exceptions.RequestException as e:
			# catastrophic error. bail.
			print ('ERROR: Request Exception')
			sys.exit(1)

		prices = tree.xpath("//div[2]/div/strong/text()")

		for price in prices:
			if price.strip():
				value = (''.join(s for s in price if s.isdigit()))
				if value.strip():
					adPrices.append(int(value))

		counter += 50

		url = url + "_Desde_" + str(counter)

		statusCode = page.status_code

	return (adPrices)	


def main():
	adPrices = ParseMLPrice(sys.argv[1])

	meanPrice = mean(adPrices)
	stdevPrice = stdev(adPrices)

	adPrices = removeOutliers(adPrices, meanPrice, stdevPrice)

	print('Average: ' + str(mean(adPrices)))
	print('Mode: ' + str(mode(adPrices)))
	print('Median: ' + str(median(adPrices)))
	print('Standard Deviation: ' + str(stdev(adPrices)))
	print('Median Grouped: ' + str(median_grouped(adPrices)))
	print('Minimum: ' + str(min(adPrices)))
	print('Maximum: ' + str(max(adPrices)))


if __name__ == '__main__':
		sys.exit(main())