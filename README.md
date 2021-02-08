
# DSpace to From The page

This utility will download [DSpace](https://dspace.org) items and prep them for Upload into [From the Page](http://zebrapedia.psu.edu/static/faq). Creates zip file of digital object and `metadata.yml` file.


## Prerequisites
- Python 3
- BeautifulSoup
- lxml

## Usage

<iframe src="https://h5p.org/h5p/embed/1104294" width="1090" height="677" frameborder="0" allowfullscreen="allowfullscreen" allow="geolocation *; microphone *; camera *; midi *; encrypted-media *"></iframe><script src="https://h5p.org/sites/all/modules/h5p/library/js/h5p-resizer.js" charset="UTF-8"></script>


- set `urlbase` to relevant DSpace site
- add urls to items into .csv files and place csv's into the Input folder
- run script `batch_parse_and_build.py` in the build folder if you want all of the works in each csv to be bundled together into a single zip file.
- run script `individual_parse_and_build.py` in the build folder if you want all of the works in each csv to be bundled into seperate zip files.
- retreive zip files from the Output folder

Project written and maintained by Brock University [Digital Scholarship Lab](https://brocku.ca/library/dsl)
