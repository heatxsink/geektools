#!/usr/bin/env python
# encoding: utf-8
 
# Copyright (c) 2009 Nicholas Granado
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

import sys
import socket
import urllib
import urllib2
import cookielib
import re
import os
import simplejson
import textwrap
import string
import time
import unicodedata
import rfc822
import calendar

USERNAME = "your_username_here"
PASSWORD = "your_password_here"
NUMBER_OF_TWEETS = 5

SCREEN_NAMES = []
SCREEN_NAMES.append('twitter')
SCREEN_NAMES.append('thatkevinsmith')
SCREEN_NAMES.append('kevinrose')

def massage_timestamp(created_at, utc_offset):
	utc_offset_hours = int(utc_offset) / 3600
	timestamp = calendar.timegm(rfc822.parsedate(created_at))
	return time.strftime("%a %b %d %I:%M:%S %p", time.localtime(timestamp))

def get_top_n_tweets(username):
	tweet = twitter(USERNAME, PASSWORD)
	statuses = tweet.user_timeline(username)
	for i in range(0, NUMBER_OF_TWEETS):
		status = statuses[i]
		timestamp = massage_timestamp(status['created_at'], status['user']['utc_offset'])
		text = unicode(status['text']).encode('utf-8')
		pre = "%s\t%s%s" % (string.ljust(timestamp, 5), string.ljust(status['user']['screen_name'], 22), text)
		print textwrap.fill(pre,width=200,initial_indent="",subsequent_indent="                      ")

def main():
	for screen_name in SCREEN_NAMES:
		get_top_n_tweets(screen_name)
		print

class twitter:
		UPDATE_URI = "http://twitter.com/statuses/update.xml"
		USER_TIMELINE = "http://twitter.com/statuses/user_timeline/%s.json"
		def __init__(self, username, password):
				self.username = username
				self.password = password
				self.realm = None
				self.toplevel = 'http://twitter.com/statuses/'
				auth = urllib2.HTTPPasswordMgrWithDefaultRealm()
				auth.add_password(self.realm, self.toplevel, self.username, self.password)
				authHandler = urllib2.HTTPBasicAuthHandler(auth)
				opener = urllib2.build_opener(authHandler)
				urllib2.install_opener(opener)
				socket.setdefaulttimeout(60)
		def truncate(self, string, target):
				if len(string) > target:
						return string[:(target-3)] + "..."
				return string
		def update(self, status):
				status = self.truncate(status, 140)
				data = self.url_encode_status_message(status)
				response = self.send_update_request(data)
				return response
		def url_encode_status_message(self, status):
				data = {'type' : 'post', 'status' : status, 'source' : 'lensherr'}
				return urllib.urlencode(data)
		def update_status(self, data):
				request = urllib2.Request(twitter.UPDATE_URI, data)
				return urllib2.urlopen(request).read()
		def user_timeline(self, username):
			user_timeline_url = twitter.USER_TIMELINE % (username)
			request = urllib2.Request(user_timeline_url)
			return simplejson.loads(urllib2.urlopen(request).read())

main()
