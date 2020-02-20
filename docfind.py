#!/usr/bin/env python3

import os
from tkinter import *

"""GUI code"""

program = Tk()
program.title("docfind")

here = Label(program, text="Input query here:", width=18, borderwidth=5)
here.grid(row=0, column=0)

inp = Entry(program, width=50, borderwidth=5)
inp.grid(row=0, column=1, padx=10, pady=10)

out = Text(program, width=70, height=10, borderwidth=5)
out.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

"""Function that attempts to find word in file"""

def find(file, word):
	with open(file, 'r') as f:
		for line in f:
			if word in line.split() or word.casefold() in line.split():
				return True
	return False

"""Function for NOT operation"""

def query_not(query):
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

def query_or(query):
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

def query_and(query):
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

def clear_par(query):
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

def run():

	"""Getting query input as well as files in dir"""

	global inp
	global out
	out.delete('1.0', END)
	query = inp.get()
	if len(query) > 0:
		ls = os.popen("ls").read()
		files = list(ls.split('\n'))
		del files[files.index("docfind.py")]
		del files[files.index('')]
		# files = files[:-2]
		out.insert(INSERT, "Documents scanned: ")
		out.insert(INSERT, files[0])
		for doc in files[1:]:
			out.insert(INSERT, ", " + doc)
		out.insert(INSERT, '\n')
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
			clear_par(query)
			query_not(query)
			query_or(query) 
			query_and(query)
			# query_or() Not sure if operation order matters here

		"""Print files that match query"""

		has_printed = 0
		for i in range(len(query[0])):
			if query[0][i] is True:
				out.insert(INSERT, files[i] + " matches query.\n")
				has_printed = 1
		if has_printed == 0:
			out.insert(INSERT, "No file matches query.\n")
	else:
		out.insert(INSERT, "No query given!\n")

go = Button(program, text="GO!", padx=10, pady=10, borderwidth=5, command=run)
go.grid(row=0, column=2)

program.mainloop()
