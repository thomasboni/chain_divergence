# chain_divergence

![platform](https://img.shields.io/badge/python-3.X-blue.svg)

Analysis of blockchain masternode divergences: simple python script which parse files containing block in input and print blocks with divergences.

* Input: folder hierarchy containing one directory per node with all blocks
* Ouptut: json data of all blocks containing divergences

## Platform and requirements

* Python version: 3.X

## Getting started

```
git clone git@gitlab.pikcio.com:diaas/diaas_api.git
python parse.py -p <blocks_folder> -d
```
    
## Usage 

```
usage: parser.py [-h] --path PATH [-v] [-d]

Parse pengine blocks tree

optional arguments:
  -h, --help            show this help message and exit
  --path PATH, -p PATH  root path of the directory tree
  -v, --verbose         display INFO logging messages
  -d, --debug           display DEBUG logging messages
```
