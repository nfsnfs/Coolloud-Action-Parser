#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import datetime
import json
import re
import urllib2
from calendar import monthrange


class CoolloudAction:

	month_conversion = {'1': u"一月", '2': u"二月", '3': u"三月", '4': u"四月", '5': u"五月", '6': u"六月",
			    '7': u"七月", '8': u"八月", '9': u"九月", '10': u"十月", '11': u"十一月", '12': u"十二月"}

	def __init__(self, time):

		url = 'http://www.coolloud.org.tw/action/%d/%d' % (time.year, time.month)

		print url

		self.date = time
		self.html = urllib2.urlopen(url).read()
		self.soup = BeautifulSoup(self.html)
		

	def getYearMonth(self):
		month_action = self.soup.find('a', {'class': '1 active'})['href']
		split = month_action.split('/')

		year = split[2]
		month = split[3]

		return year, month


	def getDayEvent(self, date = ''):

		result = []

		if date is '':
			date = self.date

		day = self.soup.find('td', {'id': self.month_conversion[str(date.month)] + str(date.day)})
		events = day.findAll('div', {'class': 'calendar monthview'})
	
		for event in events:
			temp = event.find('a')

			title = temp.contents[0]
			link = 'http://www.coolloud.org.tw' + temp['href']
			start = event.find('div', {'class': 'start'})
			if start is not None:
				start = start.contents[0]
			
			end = event.find('div', {'class': 'end'})
			if end is not None:
				end = end.contents[0]
			

			single_event = {'title': unicode(title).encode('utf-8').replace('\r\n', ''), 
				'link': link,
				'start': start,
				'end': end,
				}

			result.append(single_event)

		return result

	def getMonthEvent(self, date = ''):

		result = {}

		if date is '':
			date = self.date

		weekday, number_days = monthrange(date.year, date.month)

		for day in range(1, number_days):
			temp_date = datetime.date(date.year, date.month, day)

			result[str(temp_date)] = self.getDayEvent(temp_date)

		return result



if __name__ == '__main__':
	
	d = datetime.date.today()
	
	cool = CoolloudAction(d)

	print 'Coolload Action Module'
	print cool.getDayEvent(d)
	print cool.getMonthEvent(d)


