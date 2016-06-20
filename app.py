#!/usr/bin/python

import requests
from lxml import html
import re
import sys

def get_ebooks( start, end):

  # Urls for website
  baseUrl = 'http://www.it-ebooks.info/book'

  # Regex expression to find download link
  regex_exp = "http://filepi.com/*"
  regex = re.compile(regex_exp).search

  global count
  for counter in range( start, end, 1):
    count = counter
    booksUrl = baseUrl + '/{0}/'.format(counter)
    print '\n'
    print 'Url: %s' %booksUrl
    book_details(booksUrl, regex)

  print '\nDownloading Completed... \n{0} ebooks downloaded'.format(end-start)

def book_details(bookUrl, regex):
  tree = html.fromstring(requests.get(bookUrl).text)
  bookName = tree.xpath('//h1[@itemprop="name"]/text()')[0]
  a_links = tree.xpath('//td[@class="justify link"]//tr/td/a/@href')
  download_link = filterPick(a_links, regex)[0]

  # Staring Download
  print bookName + ' Downloading...'
  rp = requests.get(download_link, headers = {'Referer':bookUrl}, allow_redirects = False)
  r = requests.get(rp.headers['location'])
  
  # Start writting
  bookName = '{0} - {1}.pdf'.format(count, bookName)
  open(bookName, 'w')
  with open(bookName, "wb") as code:
    code.write(r.content)

def filterPick(list,filter):
  return [ l for l in list if filter(l)]

if __name__ == '__main__':
  get_ebooks( int(sys.argv[1]), int(sys.argv[2])+1)