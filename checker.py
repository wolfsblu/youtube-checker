#!/bin/env python3

import sys
import argparse
import dateutil.parser

from datetime import datetime, timezone
from youtubeapi import YouTube
from datastore import DataStore

def pretty_print(header, data):
	if (len(data) == 0):
		return

	separator = []
	for word in header:
		separator.append('-' * len(word))

	output = [header, separator] + data

	max_lens = [0] * len(header)
	for row in output:
		for idx, column in enumerate(row):
			if len(column) > max_lens[idx]:
				max_lens[idx] = len(column)

	for row in output:
		for idx, column in enumerate(row):
			print("".join(column.ljust(max_lens[idx])), end = ' ' * 2)
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
		for channel_item in channels:
			last_checked = dateutil.parser.parse(channel_item['last_checked'])
			last_checked = last_checked.replace(tzinfo = timezone.utc)
			uploads = youtube.get_uploads_by_id(channel_item['id'], last_checked)
			store.update_last_checked(channel_item['id'])

			for upload in uploads:
				video_url = 'https://youtube.com/watch?v=%s' % (upload['id'],)
				data.append([channel_item['title'], upload['title'], upload['published_at'], video_url])

		pretty_print(['Channel', 'Title', 'Published At', 'Link'], data)

if __name__ == '__main__':
	main()
