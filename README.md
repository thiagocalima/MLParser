#MLParser
Price parser for MercadoLivre/MercadoLibre ads
This script is very simple and (at this moment) is able to return the following metrics:
- Average;
- Mode;
- Median;
- Standard Deviation;
- Median Grouped;
- Minimum;
- Maximum.

This scrip must be called with the MercadoLivre/Mercadolibre query URL as an argument as follows:
- python MLParser.py http://celulares.mercadolivre.com.br/iphone/iphone-5s/cinza-espacial/32gb/_ItemTypeID_U

The URL will contain the desired query made on the MercadoLivre/MercadoLibre search engine and the desire categorization and filtering. This is good because you can search for better customized results and make better statistics.

#ToDo List:
- Make dynamic the zScore;
- Implement some intelligence to wait for an interval between the queries (to avoid blocking);
- Other improvements yet not pictured.

#Known Issues:
- This isn't working for queries of car advertisements.


This script was born because my sister wanted to sell her used iPhone and asked me how much should she ask for it! :)
