import sqlite3

from datetime import datetime

class DataStore():
	def __init__(self, db_path, schema_path):
		self.db_path = db_path
		self.schema_path = schema_path
		self.connection = sqlite3.connect(db_path)

		self.create_schema()

	def __exit__(self):
		self.connection.close()

	def create_schema(self):
		with open(self.schema_path) as schema_file:
			cursor = self.connection.cursor()
			schema_sql = schema_file.read()
			cursor.executescript(schema_sql)

	def channel_from_row(self, row):
		channel = dict()
		channel['id'] = row[0]
		channel['username'] = row[1]
		channel['title'] = row[2]
		channel['added_on'] = row[3]
		channel['last_checked'] = row[4]
		return channel

	def row_from_channel(self, channel):
		return (channel['id'], channel['username'], channel['title'], channel['added_on'], channel['last_checked'])

	def store_channel(self, channel):
		cursor = self.connection.cursor()
		cursor.execute('INSERT INTO channel VALUES (?, ?, ?, ?, ?)', self.row_from_channel(channel))
		self.connection.commit()

	def get_channel_by_id(self, id):
		cursor = self.connection.cursor()
		cursor.execute('SELECT * FROM channel WHERE id = ?', (id,))
		result = cursor.fetchone()
		if result is not None:
			return self.channel_from_row(result)
		return None

	def get_channel_by_username(self, username):
		cursor = self.connection.cursor()
		cursor.execute('SELECT * FROM channel WHERE username = ?', (username,))
		result = cursor.fetchone()
		if result is not None:
			return self.channel_from_row(result)
		return None

	def get_channels(self):
		cursor = self.connection.cursor()
		for row in cursor.execute('SELECT * FROM channel'):
			yield self.channel_from_row(row)
		return None

	def remove_channel(self, channel):
		cursor = self.connection.cursor()
		cursor.execute('DELETE FROM channel WHERE id = ?', (channel['id'],))
		self.connection.commit()

	def update_last_checked(self, channel_id):
		cursor = self.connection.cursor()
		cursor.execute('UPDATE channel SET last_checked = ? WHERE id = ?', (datetime.utcnow().isoformat(), channel_id))
		self.connection.commit()
