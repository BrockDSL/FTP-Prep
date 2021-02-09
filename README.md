
# DSpace to From The page

This utility will download [DSpace](https://dspace.org) items and prep them for Upload into [From the Page](http://zebrapedia.psu.edu/static/faq). Creates zip file of digital object and `metadata.yml` file.


## Prerequisites
- Python 3
- BeautifulSoup
- lxml

## Usage

- set `urlbase` to relevant DSpace site
- add urls to items into .csv files and place csv's into the Input folder
- run script `batch_parse_and_build.py` in the build folder if you want all of the works in each csv to be bundled together into a single zip file.
- run script `individual_parse_and_build.py` in the build folder if you want all of the works in each csv to be bundled into seperate zip files.
- retreive zip files from the Output folder

Project written and maintained by Brock University [Digital Scholarship Lab](https://brocku.ca/library/dsl)
