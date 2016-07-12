#! /usr/bin/python
import sys
import urllib2
import os
from lxml import html
import requests


def ParseMLPrice(url):
	ads = []
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
			print(t)
			# Maybe set up for a retry, or continue in a retry loop
		except requests.exceptions.TooManyRedirects as r:
			print(r)
			# Tell the user their URL was bad and try a different one
		except requests.exceptions.ConnectionError as c:
			print("erro")
			sys.exit(1)
			# Tell the user their URL isn't found
		except requests.exceptions.RequestException as e:
			# catastrophic error. bail.
			print e
			sys.exit(1)

		prices = tree.xpath("//div[2]/div/strong/text()")

		for price in prices:
			if price.strip():
				value = (''.join(s for s in price if s.isdigit()))
				if value.strip():
					print(value)

		counter += 50

		url = url + "_Desde_" + str(counter)

		statusCode = page.status_code


def main():
	ParseMLPrice(sys.argv[1])

if __name__ == '__main__':
		sys.exit(main())