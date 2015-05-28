#!/usr/bin/env python
#user-agent comparison tool

#props to joff tyher which rir tool i used as a basis and the security weekly crew!
#https://bitbucket.org/jsthyer/rirtools/src/658e628a3c813b6bdef3003997915eaa977e40d3/riracl.py?at=master


import argparse
import os
import sys
import sqlite3

class Database:

	def __init__(self):
		
		dbhome = '%s/.useragentdb' % (os.path.expanduser('~'))
		if not os.path.exists(dbhome):
			os.mkdir(dbhome)
		self.dbname = '%s/useragent.db' % (dbhome)
		self.lastfetch = '%s/lastfetchdate' % (dbhome)
		self.dbh = self._sqlite3_connect()

	def _sqlite3_connect(self):
		dbh = sqlite3.connect(self.dbname)
		dbh.text_factory = str
		cur = dbh.cursor()
		sql = """\
CREATE TABLE IF NOT EXISTS useragents
(
	useragent TEXT, comment TEXT, count INT
)
"""
		cur.execute(sql)
		dbh.commit()
		return dbh	

	def import_useragents(self, comment, uastring, count):
		cur = self.dbh.cursor()
		
		sql = """\
SELECT * FROM useragents WHERE useragent = ?
"""
		cur.execute(sql, [uastring])
		
		i = cur.fetchone()
		if i is None:
		
			print 'inserting ' + comment + ' ' + uastring + ' ' + count
			sql = "INSERT INTO useragents (useragent, comment, count) VALUES (?, ?, ?)"
			cur.execute(sql, [uastring, comment, count])
			self.dbh.commit()
			print 'db inserted'
		else:
			print 'adding count of ' + count + ' to the useragent ' + 'uastring '
			sql = "UPDATE useragents SET count = count + ? WHERE useragent = ?"
			cur.execute(sql, [count, uastring])
			self.dbh.commit()
			
		print 'db inserted'



	def print_db(self):
		cur = self.dbh.cursor()
		cur.execute("SELECT * FROM useragents")
		for row in cur.fetchall():
			print row

	def run(self):
		if options.csvname:
			#print options.csvname
			f = open (options.csvname, 'r')
			for line in f:
				#print line
				elements = line.split(",")
				#print elements[2]
				comment = elements[0]
				uastring = elements[1]
				count = elements[2]
				self.import_useragents(comment, uastring, count)
			return
		if options.printua:
			#print 'print'
			self.print_db()
			return



if __name__ == '__main__':

	VERSION = '20150528_1'
	desc = """
[*] ---------------------------------------------
[*] %s version %s
[*] Author: Sebastian Brabetz
[*] http://itunsecurity.wordpress.com
[*] ---------------------------------------------
""" % (os.path.basename(sys.argv[0]), VERSION)
	parser = argparse.ArgumentParser(
		formatter_class=argparse.RawDescriptionHelpFormatter,
	description=desc
	)
	#parser.add_argument(
	#	'--http', action='store_true',
	#	default=False, help='Retrieve RIR data over HTTP'
	#)


	parser.add_argument(
		'--importcsv', action='store', dest='csvname',
		help='Retrieve RIR data over HTTP'
	)

	parser.add_argument(
		'--printua', action='store_true',
		default=False, help='Print UserAgents'
	)
	options = parser.parse_args()

	print '%s' % (desc)


	db = Database()
	db.run()
