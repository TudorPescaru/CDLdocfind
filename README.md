# docfind

A document parser that attempts to find certain words given as input via a 
logical query.

Implementation
-----

The algorithm used uses an inverted-index-like scheme to keep track of whether 
a word appears or not in each of the scanned files. This is sotred as 
True/False values in a database. The database has a column for all words and a
column for each file in which the words are searched. All these values are then
loaded in lists. All logical operations are executed in the given order on
these value lists so as to reach a final one in which the True values corespond
to files which match the given query.

Given documentation
-----

https://drive.google.com/file/d/1LXAwPBsveZi2_Q3YI9bAosmyj-Xja1Op/view

Usage
-----

Pyhton as well as make are required to be installed for the program to run.

```
	$ cd < dir with documents to be scanned >
	$ wget https://raw.githubusercontent.com/TudorPescaru/CDLdocfind/master/Makefile
	$ make
	$ ./docfind.py
```

Planned updates
-----

* ~~Add a GUI~~
* ~~Implement databases to store word values~~
* Improve search engine efficiency by implementing tf-idf

