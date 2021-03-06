#!/usr/bin/env python3

import os
from tkinter import *
import sqlite3
import string

# Database setup

db = sqlite3.connect('words.db')

if db is None:
	print("Error accessing DB")
	exit(-1)

cursor = db.cursor()

# Create primary key column for words

cursor.execute(""" SELECT name FROM sqlite_master WHERE type='table' AND name='WORDVAL'; """)
if cursor.fetchall() is None:
	try:
		cursor.execute("CREATE TABLE WORDVAL (WORD VARCHAR(50) PRIMARY KEY NOT NULL);")
		db.commit()
	except Exception:
		print("Database table error.")
		db.rollback()

# GUI code

program = Tk()
program.title("docfind")

# Text Lables

here = Label(program, text="Input query here:", width=18, borderwidth=5)
here.grid(row=0, column=0)

fs = Label(program, text="Select files to scan:", width=21, borderwidth=5)
fs.grid(row=2, column=0)

# Scrollbars for Text and Listbox widgets

scroll1 = Scrollbar(program, orient=VERTICAL)
scroll2 = Scrollbar(program, orient=VERTICAL)

# Entry widget for user input

inp = Entry(program, width=50, borderwidth=5)
inp.grid(row=0, column=1, padx=10, pady=10)

# Text widget for displaying search results

out = Text(program, width=70, height=10, borderwidth=5, yscrollcommand=scroll1.set)
out.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
out.configure(state='disabled')

scroll1.place(in_=out, relx='1.0', relheight='1.0', bordermode='outside')
scroll1.config(command=out.yview)

# Listbox widget for allowing the user to select files to be scanned

filelist = Listbox(program, width=48, height=10, borderwidth=5, selectmode=MULTIPLE, yscrollcommand=scroll2.set)
filelist.grid(row=2, column=1, columnspan=2, rowspan=2, padx=10, pady=10)

scroll2.place(in_=filelist, relx='1.0', relheight='1.0', bordermode='outside')
scroll2.config(command=filelist.yview)

# Getting list of files in the local dir

ls = os.popen("ls").read()
files = list(ls.split('\n'))
del files[files.index("words.db")]
del files[files.index("docfind.py")]
del files[files.index('')]
for file in files:
	filelist.insert(END, file)

	# Create a column to store the find value for each file

	try:
		cursor.execute("""ALTER TABLE WORDVAL ADD COLUMN "%s" INT;""" % str(file))
		db.commit()
	except Exception:
		db.rollback()
		print("Column already exists.")

# Function for the select/deselect all button

isClicked = False


def onselect(evt):
	global isClicked
	isClicked = True
	sel_txt.set("Deselect all")


filelist.bind('<<ListboxSelect>>', onselect)


def de_sel():
	global isClicked
	if isClicked is False:
		filelist.select_set(0, END)
		isClicked = True
		sel_txt.set("Deselect all")
	else:
		filelist.selection_clear(0, END)
		isClicked = False
		sel_txt.set("Select all")


# Function that attempts to find word in file

def find(file, word):
	with open(file, 'r') as f:
		for line in f:
			line = line.translate(str.maketrans('', '', string.punctuation))
			line = line.lower()
			if word in line.split():
				return True
			elif word.casefold() in line.split():
				return True
	return False

# Function for NOT operation

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

# Function for OR operation

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


# Function for AND opertaion

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

# Function that removes useless parentheses

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

# Main function that is called when the GO! button is pressed

def run():

	# Getting query input

	out.configure(state='normal')
	out.delete('1.0', END)
	out.configure(state='disabled')
	query = inp.get()

	if len(query) > 0:

		# Getting list of selected files and converting the query for use

		select = filelist.curselection()
		fileselect = [filelist.get(i) for i in select]
		query = query.replace('(', ' ( ')
		query = query.replace(')', ' ) ')
		query = list(query.split())

		if len(fileselect) > 0:

			# Separation of query args and creating inverted index values

			for i in range(len(query)):
				if query[i].isalpha():

					# Making sure each word in query exists in DB

					cursor.execute("SELECT WORD FROM WORDVAL;")
					words = cursor.fetchall()
					words = [words[i][0] for i in range(len(words))]
					if query[i] not in words:
						cursor.execute("""INSERT INTO WORDVAL (WORD) VALUES ("%s");""" % query[i])
					for file in fileselect:

						# Populating DB with values for each word

						val = 1 if find(file, query[i]) is True else 0
						cursor.execute("""UPDATE WORDVAL SET "%s" = "%d" WHERE WORD = "%s";""" % (file, val, query[i]))

			# Generating processing-ready list from DB

			for i in range(len(query)):
				if query[i].isalpha():
					word = query[i]
					query[i] = []
					for file in fileselect:
						cursor.execute("""SELECT "%s" FROM WORDVAL WHERE WORD = "%s";""" % (file, word))
						data = cursor.fetchall()
						query[i].append(True if data[0][0] == 1 else False)

			# Determine final value list

			while len(query) > 1:
				clear_par(query)
				query_not(query)
				query_or(query)
				query_and(query)

			# Print files that match query

			out.configure(state='normal')
			has_printed = 0
			for i in range(len(query[0])):
				if query[0][i] is True:
					out.insert(INSERT, fileselect[i] + " matches query.\n")
					has_printed = 1
			if has_printed == 0:
				out.insert(INSERT, "No file matches query.\n")
		else:
			out.configure(state='normal')
			out.insert(INSERT, "Please select files!\n")
	else:
		out.configure(state='normal')
		out.insert(INSERT, "No query given!\n")
	out.configure(state='disabled')

# Buttons for various actions

go = Button(program, text="GO!", borderwidth=5, command=run)
go.grid(row=0, column=2, padx=10, pady=10)

sel_txt = StringVar()
sel = Button(program, textvariable=sel_txt, borderwidth=5, command=de_sel)
sel.grid(row=3, column=0, padx=10, pady=10)
sel_txt.set("Select all")

program.mainloop()

db.commit()
db.close()
