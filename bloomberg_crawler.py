from bs4 import BeautifulSoup
from urllib2 import urlopen, Request
import time
import re

main_domain = "http://www.bloomberg.com/research/common/symbollookup/"
start_url = "http://www.bloomberg.com/research/common/symbollookup/symbollookup.asp?region=US&letterIn=A&searchType=coname&x=7&y=15&lookuptype=public&firstrow=0"
bloomberg2glassdoor_domain_head = 'http://www.glassdoor.com/api/api.htm?version=1&action=all-in-one&t.s=w-m&t.a=i&t.p=21163&responseType=embed&utm_medium=synd&utm_source=Bloomberg&utm_campaign=21163&utm_content=all-in-one&ticker='

hdr = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36(KHTML, like Gecko) Chrome",
"Accept":"text/html,application/xhtml+xml,application/xml;q = 0.9, image / webp, * / *;q = 0.8"}


def get_paging_links(start_url):
    url = start_url
    html = urlopen(url)
    time.sleep(5)
    soup = BeautifulSoup(html, "html.parser")
    to_return = [start_url]

    anchor = soup.find("span", {"class": "onLink"}).parent
    while True:
        try:
            anchor = anchor.next_sibling
            to_return.extend([main_domain + anchor.find("a", {"class": "link"}).get('href')])
        except:
            break
    return to_return


def get_table_content_links(lst_to_crawl):
    to_return = []
    for i in lst_to_crawl:
        html = urlopen(i)
        time.sleep(5)
        soup = BeautifulSoup(html, "html.parser")
        for k in soup.find("tbody").find_all("a"):
            to_return.extend([k.get('href')])
    return to_return


def crawl_main_content(url2crawl):
    url = url2crawl
    html = urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    time.sleep(5)

    com_name = soup.find("h1", {"class", "name"}).get_text().lstrip().rstrip()
    com_ticker = soup.find("div", {"class", "ticker"}).get_text().lstrip().rstrip()
    com_exchange = soup.find("div", {"class", "exchange"}).get_text().lstrip().rstrip()

    com_volume = soup.find('div', text=re.compile("Volume"), attrs={'class': 'cell__label'}).parent.find("div", {
        "class": "cell__value"}).get_text().lstrip().rstrip()
    com_52wk_range = soup.find('div', text=re.compile("52Wk Range"), attrs={'class': 'cell__label'}).parent.find("div",
                                                                                                                 {
                                                                                                                     "class": "cell__value"}).get_text().lstrip().rstrip()
    try:
        com_one_year_return = soup.find('div', text=re.compile("1 Yr Return"),
                                        attrs={'class': 'cell__label'}).parent.find("div",
                                                                                    {"class": "cell__value"}).get_text().lstrip().rstrip()
    except:
        com_one_year_return = None
    com_ytd_return = soup.find('div', text=re.compile("YTD Return"), attrs={'class': 'cell__label'}).parent.find("div",
                                                                                                                 {
                                                                                                                     "class": "cell__value"}).get_text().lstrip().rstrip()
    com_pe_r = soup.find('div', text=re.compile("Current P/E Ratio*"), attrs={'class': 'cell__label'}).parent.find(
        "div", {"class": "cell__value"}).get_text().lstrip().rstrip()
    com_eps = soup.find('div', text=re.compile("Earnings per Share*"), attrs={'class': 'cell__label'}).parent.find(
        "div", {"class": "cell__value"}).get_text().lstrip().rstrip()
    com_market_cap = soup.find('div', text=re.compile("Market Cap*"), attrs={'class': 'cell__label'}).parent.find("div",
                                                                                                                  {
                                                                                                                      "class": "cell__value"}).get_text().lstrip().rstrip()
    com_shares_outstanding = soup.find('div', text=re.compile("Shares Outstanding*"),
                                       attrs={'class': 'cell__label'}).parent.find("div",
                                                                                   {"class": "cell__value"}).get_text().lstrip().rstrip()
    com_p2s = soup.find('div', text=re.compile("Price/Sales*"), attrs={'class': 'cell__label'}).parent.find("div", {
        "class": "cell__value"}).get_text().lstrip().rstrip()
    com_id_ye = soup.find('div', text=re.compile("Dividend Indicated Gross Yield"),
                          attrs={'class': 'cell__label'}).parent.find("div", {"class": "cell__value"}).get_text().lstrip().rstrip()
    com_sector = soup.find('div', text=re.compile("Sector"), attrs={'class': 'cell__label'}).parent.find("div", {
        "class": "cell__value"}).get_text().lstrip().rstrip()
    com_industry = soup.find('div', text=re.compile("Industry"), attrs={'class': 'cell__label'}).parent.find("div", {
        "class": "cell__value"}).get_text().lstrip().rstrip()
    com_sub_industry = soup.find('div', text=re.compile("Sub-Industry"), attrs={'class': 'cell__label'}).parent.find(
        "div", {"class": "cell__value"}).get_text().lstrip().rstrip()


    com_address = ''
    try:
        for i in soup.find('div', text=re.compile("Address"), attrs={'class': 'profile__detail__label'}).next_siblings:
            com_address += str(i).lstrip().rstrip()
        com_address = com_address.replace("</br>", '').split("<br>")
    except:
        com_address = 'Unknown'
    try:
        com_tel = str(soup.find('div', text=re.compile("Phone"), attrs={'class': 'profile__detail__label'}).next_sibling.lstrip().rstrip())
    except:
        com_tel = 'Unknown'
    try:
        com_website = soup.find('div', text=re.compile("Website"), attrs={'class': 'profile__detail__label'}).parent.find(
        "a", {"class", "profile__detail__website_link"}).get('href').lstrip().rstrip()
    except:
        com_website = 'Unknown'
    glassdoor_page = glass_door_domain(com_name, com_ticker)

    dict2return = {"Name": com_name, "Ticker": com_ticker, "Exchange": com_exchange, "Volume": com_volume,
                   "52Wk Range": com_52wk_range, "1 Yr Return": com_one_year_return, "YTD Return": com_ytd_return,
                   "Current P/E Ratio": com_pe_r, "Earnings per Share": com_eps, "Market Cap": com_market_cap,
                   "Shares Outstanding": com_shares_outstanding, "Price/Sales": com_p2s,
                   "Dividend Indicated Gross Yield": com_id_ye, "Sector": com_sector, "Industry": com_industry,
                   "Sub-Industry": com_sub_industry, "Address": com_address, "Phone": com_tel, "Website": com_website,
                   "glassdoor Page": glassdoor_page}

    if glassdoor_page:
        dict2return.update(glassdoor_data(glassdoor_page))
        return dict2return
    else:
        return dict2return


def glass_door_domain(name, ticker):
    c_name = name
    c_ticker = ticker
    com_name_encoded = c_name.encode("utf-8").lstrip().rstrip()
    com_ticker_encoded = c_ticker.encode("utf-8").lstrip().rstrip()
    com_name_encoded = com_name_encoded.replace(" ", "%20").replace("&", "%26").replace("'", "%27")
    com_ticker_encoded = com_ticker_encoded.replace(":", "%3A")
    glass_door_job_domain = bloomberg2glassdoor_domain_head + com_ticker_encoded + '&employer=' + com_name_encoded

    try:
        soup2 = BeautifulSoup(urlopen(Request(glass_door_job_domain, headers=hdr)), "html.parser")
        time.sleep(5)
        tail = soup2.find("div", {"class": "tbl fill borderBot"}).find("a").get('href')
    except:
        glassdoor_job_page = None
    else:
        if tail is not None:
            glassdoor_job_page = "https://www.glassdoor.com" + tail
        else:
            glassdoor_job_page = None

    if glassdoor_job_page:
        soup3 = BeautifulSoup(urlopen(Request(glassdoor_job_page, headers=hdr)), "html.parser")
        time.sleep(5)
        return "https://www.glassdoor.com"+ soup3.find("a", {"class": "eiCell cell overviews"}).get('href')
    else:
        return None


def glassdoor_data(gd_url):
    try:
        soup = BeautifulSoup(urlopen(Request(gd_url, headers=hdr)), "html.parser")
        time.sleep(5)
        com_size = soup.find("strong", text="Size").parent.find("span", {"class":"empData"}).get_text().lstrip().rstrip()
        com_found = soup.find("strong", text="Founded").parent.find("span", {"class":"empData"}).get_text().lstrip().rstrip()
        com_revenue = soup.find("strong", text="Revenue").parent.find("span", {"class":"empData"}).get_text().lstrip().rstrip()
        try:
            com_competitor = soup.find("strong", text="Competitors").parent.find("span", {"class":"empData"}).get_text().lstrip().rstrip()
        except:
            com_competitor = "Unknown"

        return {"Size": com_size, "Founded":com_found, "Revenue":com_revenue, "Competitors": com_competitor}
    except:
        print "blocked by galssdoor"
        return {}

print crawl_main_content("http://www.bloomberg.com/quote/AAPL:US")