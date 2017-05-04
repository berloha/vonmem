#!/usr/bin/python
#coding: utf8

import re
import sys
import urllib2
from datetime import datetime  

def Download(url, proxies = None) :
	if proxies :
		proxy = urllib2.ProxyHandler(proxies)
		opener = urllib2.build_opener(proxy)
		urllib2.install_opener(opener)
	loader = urllib2.urlopen(url)
	chunk = 4096
	data = ''
	while 1:
		d = loader.read(chunk)
		data += d
		if not d : break

 	return data


def GetReadings(date) :	
#	page = ''
	page = Download('https://azbyka.ru/days/' + date.strftime('%Y-%m-%d'))
	page = re.findall('<div class="brif readings">.+?<span[^>]*>', page, re.DOTALL)[0]
	page = page.decode('utf-8')
	page = re.sub('<.+?>', '', page)
	page = re.sub('[ \t\r\n]+', ' ', page)

#	page = u" Утр. - Ев. 7-е, Ин. XX:1-10 (зач. 63). Лит. - Кол. III:4-11 (Недели 29-й) (зач. 257). Лк. XIV:16-24 (Недели 28-й) (зач. 76)."
	page = page.strip()
	page = re.sub(r' [IVX0-9,\- ]+:[IVX0-9,\- ]+ ', '', page)
	page = re.sub(u'\(зач. (\d+)[а-я ]*\)', r'ZA\1', page)
	page = re.sub(u'Утр. -', 'UT:', page)
	page = re.sub(u'Лит. -', '\nLT:', page)
	page = re.sub(u'Ев\\..+?, ', '', page)
	page = re.sub(u'Мф\\.', 'MF', page)
	page = re.sub(u'Мк\\.', 'MK', page)
	page = re.sub(u'Лк\\.', 'LK', page)
	page = re.sub(u'Ин\\.', 'IN', page)
	page = re.sub(r'(IN|MF|MK|LK)(.*?)ZA(\d+)', r'\1\3 \2', page)
	return page

if __name__ == "__main__" :         

	sd = '24.12.2017'

	if len(sys.argv) > 1 : 
		sd = sys.argv[1]

	date = datetime.strptime(sd, '%d.%m.%Y')
	print GetReadings(date)