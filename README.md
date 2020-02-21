# docfind

A document parser that attempts to find certain words given as input via a 
logical query.

Implementation
-----

The algorithm used uses an inverted-index-like scheme to keep track of whether 
a word appears or not in each of the scanned files. Then applies all logical
operations in the given order on these value sets.

Given documentation
-----

https://drive.google.com/file/d/1LXAwPBsveZi2_Q3YI9bAosmyj-Xja1Op/view

Usage
-----

```
	$ cd < dir with documents to be scanned >
	$ wget curl https://github.com/TudorPescaru/CDLdocfind/blob/master/docfind.py
	$ ./docfind.py #needs to be run again after each query
```

Planned updates
-----

* ~~Add a GUI~~
* Implement databases to store word values
* Create custom set of tests
* Improve search engine efficiency by implementing tf-idf

