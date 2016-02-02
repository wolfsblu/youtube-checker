#!/bin/env python3

import sys
import argparse

from youtubeapi import YouTube
from datastore import DataStore

def pretty_print(headers, data):
	if (len(data) == 0):
		return

	separators = []
	for word in headers:
		separators.append('-' * len(word))

	output = [headers, separators] + data

	col_widths = [0] * len(headers)
	for row in output:
		for idx, column in enumerate(row):
			if len(column) > col_widths[idx]:
				col_widths[idx] = len(column)

	for row in output:
		for idx, column in enumerate(row):
			print("".join(column.ljust(col_widths[idx])), end = ' ' * 2)
		print()

def get_parser():
	parser = argparse.ArgumentParser()
	parser.add_argument('-i', '--id', help = 'Channel ID', default = None)
	parser.add_argument('-u', '--username', help = 'Username', default = None)
	parser.add_argument('action', help = 'Perform the specified action', default = 'check',
		nargs = '?', choices = ['add', 'check', 'list', 'remove'])
	return parser

def main():
	parser = get_parser()
	args = parser.parse_args()

	youtube = YouTube()
	store = DataStore('%s-data.sqlite3' % sys.argv[0], 'schema.sql')

	channel = None
	if args.username is not None:
		channel = youtube.get_channel_by_username(args.username)
	elif args.id is not None:
		channel = youtube.get_channel_by_id(args.id)

	if args.action == 'add':
		store.store_channel(channel)
	elif args.action == 'remove':
		store.remove_channel(channel)
	elif args.action == 'list':
		data = []
		for item in store.get_channels():
			data.append([item['id'], item['title'], item['added_on'], item['last_checked']])

		pretty_print(['ID', 'Title', 'Added On', 'Last Checked'], data)
	elif args.action == 'check':
		channels = []
		if channel is not None:
			channels.append(store.get_channel_by_id(channel['id']))
		else:
			channels = store.get_channels()

		data = []
		to_check = dict()
		for channel_item in channels:
			to_check[channel_item['id']] = channel_item['last_checked']

		uploads = youtube.get_uploads(to_check)
		for upload in uploads:
			video_url = 'https://youtube.com/watch?v=%s' % (upload['id'],)
			data.append([channel_item['title'], upload['title'], upload['published_at'], video_url])

		pretty_print(['Channel', 'Title', 'Published At', 'Link'], data)

		for channel_id in to_check.keys():
			store.update_last_checked(channel_id)

if __name__ == '__main__':
	main()
