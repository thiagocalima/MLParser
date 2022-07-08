#! /usr/bin/python
import sys
from lxml import html
import requests
from statistics import mean, mode, median, stdev, median_grouped


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

	if "_DisplayType_LF" not in url:
		url = url + "_DisplayType_LF"

	while (statusCode == 200):
		try:
			page = requests.get(url)
			tree = html.fromstring(page.content)
		except requests.exceptions.Timeout as t:
			# Maybe set up for a retry, or continue in a retry loop
			print('ERROR: URL Timeout! URL = ' + url)
		except requests.exceptions.TooManyRedirects as r:
			# Tell the user their URL was bad and try a different one
			print('ERROR: Too Many Redirects! URL = ' + url)
		except requests.exceptions.ConnectionError as c:
			# Tell the user their URL isn't found
			print('ERROR: Connection Error! URL = ' + url)
			sys.exit(1)
		except requests.exceptions.RequestException as e:
			# catastrophic error. bail.
			print ('ERROR: Request Exception! URL = ' + url)
			sys.exit(1)
		except lxml.etree.XMLSyntaxError as l:
			print ('ERROR: XML Syntax Error! URL = ' + url)

		prices = tree.xpath("/html/body/main/div/div[2]/section/ol/li[1]/div/div/div[2]/div[2]/div[1]/div[1]/div/div/div/span[1]/span[2]/span[2]/text()")

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

	print('Average: ' + str(round(mean(adPrices),2)))
	
	try:
		print('Mode: ' + str(round(mode(adPrices))))
	except:
		print('ERROR: Unable to print Mode!')

	print('Median: ' + str(round(median(adPrices))))
	print('Standard Deviation: ' + str(round(stdev(adPrices))))
	print('Median Grouped: ' + str(round(median_grouped(adPrices))))
	print('Minimum: ' + str(round(min(adPrices))))
	print('Maximum: ' + str(round(max(adPrices))))


if __name__ == '__main__':
		sys.exit(main())
