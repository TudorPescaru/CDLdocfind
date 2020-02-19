#!/usr/bin/env python3

import os
	
"""Function that attempts to find word in file"""

def find(file, word):
	with open(file, 'r') as f:
		for line in f:
			if word in line.split() or word.casefold() in line.split():
				return True
	return False

"""Function for NOT operation"""

def query_not():
	if '!' in query and len(query) > 1:
		index = []
		for i in range(len(query)):
			if query[i - 1] == '!'and type(query[i]) == list:
				index.append(i)
		if len(index) > 0:
			for i in range(len(index)):
				index = [x - 1 for x in index]
				del query[index[i]]
				for j in range(len(query[index[i]])):
					if query[index[i]][j] is True:
						query[index[i]][j] = False
					else:
						query[index[i]][j] = True

"""Function for OR operation"""

def query_or():
	if '||' in query and len(query) > 1:
		index = []
		for i in range(len(query)):
			if query[i] == '||' and type(query[i - 1]) == list and type(query[i + 1]) == list:
				index.append(i)
		if len(index) > 0:
			for i in range(len(index)):
				index = [x - 1 for x in index]
				for j in range(len(query[index[i]])):
					query[index[i]][j] = query[index[i]][j] or query[index[i] + 2][j]
				del query[index[i] + 1]
				index = [x - 1 for x in index]
				del query[index[i] + 2]


"""Function for AND opertaion"""

def query_and():
	if '&&' in query and len(query) > 1:
		index = []
		for i in range(len(query)):
			if query[i] == '&&' and type(query[i - 1]) == list and type(query[i + 1]) == list:
				index.append(i)
		if len(index) > 0:
			for i in range(len(index)):
				index = [x - 1 for x in index]
				for j in range(len(query[index[i]])):
					query[index[i]][j] = query[index[i]][j] and query[index[i] + 2][j]
				del query[index[i] + 1]
				index = [x - 1 for x in index]
				del query[index[i] + 2]

"""Function that removes useless parentheses"""

def clear_par():
	if '(' in query and len(query) > 1:
		index = []
		for i in range(len(query)):
			if query[i - 1] == '(' and query[i + 1] == ')' and type(query[i]) == list:
				index.append(i)
		if len(index) > 0:
			for i in range(len(index)):
				index = [x - 1 for x in index]
				del query[index[i]]
				index = [x - 1 for x in index]
				del query[index[i] + 2]

"""Getting query input as well as files in dir"""

query = input("Please input a query:\n")
ls = os.popen("ls").read()
files = list(ls.split('\n'))
files = files[:-2]
query = query.replace('(', ' ( ')
query = query.replace(')', ' ) ')
query = list(query.split())

"""Separation of query args and creating inv index values"""

for i in range(len(query)):
	if query[i].isalpha():
		values = []
		for file in files:
			values.append(find(file, query[i]))
		query[i] = values

"""Determine final value list"""

while len(query) > 1:
	clear_par()
	query_not()
	query_or() 
	query_and()
	# query_or() Not sure if operation order matters here

"""Print files that match query"""

has_printed = 0
for i in range(len(query[0])):
	if query[0][i] is True:
		print(files[i] + " matches query.")
		has_printed = 1
if has_printed == 0:
	print("No file matches query.")
