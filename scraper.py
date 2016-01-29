# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import scraperwiki
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup
import csv
import re


def connect(url):
    # print url
    report_soup = ''
    try:
        report_html = urllib2.urlopen(url)
        report_soup = BeautifulSoup(report_html, 'lxml')
    except:
        # print url
        connect(url)
    if not report_soup:
        connect(url)
    else:
        return report_soup
st_time = str(datetime.now())
directoryUrl = "http://www.cqc.org.uk/content/how-get-and-re-use-cqc-information-and-data#directory"
# html = urllib2.urlopen(directoryUrl)
# soup = BeautifulSoup(html)
soup = connect(directoryUrl)

block = soup.find('div',{'id':'directory'})
csvA = block.find('a',href=True)
csvUrl = csvA['href']
print csvUrl
response = urllib2.urlopen(csvUrl)
csv_file = csv.reader(response)
p = 0
for row in csv_file:

    if 'http' not in row[12]:
        continue
    print p
    location_url = row[12].replace('https://admin.cqc.org.uk', 'http://www.cqc.org.uk')
    name = row[0]
    # add3 = row[10]
    report_soup = connect(location_url)
    report_date = ''
    try:
        report_date = report_soup.find('div', 'overview-inner latest-report').find('h3').text.strip()
    except:
        pass
    print name
    todays_date = str(datetime.now())           
    scraperwiki.sqlite.save(unique_keys=['d'], data={"d": todays_date, "name": unicode(name), "val": unicode(report_date)})
end_time = str(datetime.now())
print st_time
print end_time
