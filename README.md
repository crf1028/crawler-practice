Bloomberg crawler
-------------
- This tool is able to take a bloomberg public company page and parse some useful data
- After crawling information on bloomberg it will redirect to glassdoor page of that company and parse information 
- It sleeps for 5 seconds each time it requesting for html content to reduce burden on server and avoid being detected as robot


- Example Input:

    print crawl_main_content("http://www.bloomberg.com/quote/AAPL:US")

- Example Output

    {'Website': u'http://www.apple.com', 'YTD Return': u'3.23%', 'Name': u'Apple Inc', 'Competitors': 'Unknown', 
    'Industry': u'Hardware', 'Price/Sales': u'2.62', 'Revenue': u'$10+ billion (USD) per year', 
    '52Wk Range': u'92.00 - 134.54', 'Size': u'10000+ Employees', 'Sector': u'Technology', 
    'Sub-Industry': u'Communications Equipment', 'Shares Outstanding': u'5.545', 'Exchange': u'NASDAQ GS', 
    'Market Cap': u'602.474', 'Dividend Indicated Gross Yield': u'1.91%', 'Founded': u'1976', 
    '1 Yr Return': u'-12.93%', 'Volume': u'23,581,740', 'Phone': '1-408-996-1010', 
    'glassdoor Page': u'https://www.glassdoor.com/Overview/Working-at-Apple-EI_IE1138.11,16.htm', 
    'Address': ['1 Infinite Loop', 'Cupertino, CA 95014', 'United States\n    '], 
    'Current P/E Ratio': u'11.59', 'Ticker': u'AAPL:US', 'Earnings per Share': u'9.38'}