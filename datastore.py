import sqlite3

from datetime import datetime

class DataStore():
	def __init__(self, db_path, schema_path):
		"""Creates a new instance of the data store using the specified schema

		Args:
			db_path (str): The path where the database should be stored
			schema_path (str): The path to the SQL schema of the database
		"""
		self.db_path = db_path
		self.schema_path = schema_path
		self.connection = sqlite3.connect(db_path)

		self.create_schema()

	def __exit__(self):
		self.connection.close()

	def create_schema(self):
		"""Open the specified schema file and execute the contained SQL"""
		with open(self.schema_path) as schema_file:
			cursor = self.connection.cursor()
			schema_sql = schema_file.read()
			cursor.executescript(schema_sql)

	def channel_from_row(self, row):
		"""Transform a database row into a channel representation

		Args:
			row (list): The database row
		"""
		channel = dict()
		channel['id'] = row[0]
		channel['username'] = row[1]
		channel['title'] = row[2]
		channel['added_on'] = row[3]
		channel['last_checked'] = row[4]
		return channel

	def row_from_channel(self, channel):
		"""Transform a channel object into a database row

		Args:
			channel (dict): The channel object
		"""
		return (channel['id'], channel['username'], channel['title'], channel['added_on'], channel['last_checked'])

	def store_channel(self, channel):
		"""Insert the provided channel object into the database"""
		cursor = self.connection.cursor()
		cursor.execute('INSERT INTO channel VALUES (?, ?, ?, ?, ?)', self.row_from_channel(channel))
		self.connection.commit()

	def get_channel_by_id(self, id):
		"""Retrieve a channel from the database by its ID

		Args:
			id (str): The channel ID
		"""
		cursor = self.connection.cursor()
		cursor.execute('SELECT * FROM channel WHERE id = ?', (id,))
		result = cursor.fetchone()
		if result is not None:
			return self.channel_from_row(result)
		return None

	def get_channel_by_username(self, username):
		"""Retrieve a channel from the database by its username

		Args:
			id (str): The username of the channel owner
		"""
		cursor = self.connection.cursor()
		cursor.execute('SELECT * FROM channel WHERE username = ?', (username,))
		result = cursor.fetchone()
		if result is not None:
			return self.channel_from_row(result)
		return None

	def get_channels(self):
		"""Retrieve all channels from the database"""
		cursor = self.connection.cursor()
		for row in cursor.execute('SELECT * FROM channel'):
			yield self.channel_from_row(row)
		return None

	def remove_channel(self, channel):
		"""Remove a channel from the database

		Args:
			channel (dict): The channel to be removed (by key 'id')
		"""
		cursor = self.connection.cursor()
		cursor.execute('DELETE FROM channel WHERE id = ?', (channel['id'],))
		self.connection.commit()

	def update_last_checked(self, channel_id):
		"""Update the last_checked value of a specific channel

		Args:
			channel_id (str): The channel to be updated
		"""
		cursor = self.connection.cursor()
		cursor.execute('UPDATE channel SET last_checked = ? WHERE id = ?', (datetime.utcnow().isoformat(), channel_id))
		self.connection.commit()
