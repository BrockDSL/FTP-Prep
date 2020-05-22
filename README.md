
# DSpace to From The page

This utility will download [DSpace](https://dspace.org) items and prep them for Upload into [From the Page](http://zebrapedia.psu.edu/static/faq). Creates zip file of digital object and `metadata.yml` file.

## Still to do
- escape characters from scrapped data 

## Prerequisites
- Python 3
- BeautifulSoup
- lxml

## Usage
- set `urlbase` to relevant DSpace site
- add urls to items in the `uls_list.csv` file
- run script `parse_and_build.py`

Project written and maintained by Brock University [Digital Scholarship Lab](https://brocku.ca/library/dsl)
