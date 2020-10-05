#!/usr/bin/env python3

import csv
import fnmatch
import glob
import os
import re
import requests
import shutil
import string

from bs4 import BeautifulSoup
from lxml import html, etree
from urllib.parse import urlparse

# Set to Taste
urlbase = "https://dr.library.brocku.ca"
csv_file = open("url_list.csv", encoding='utf-8-sig')
url_list = csv.reader(csv_file)


def build_ftp_folder(page_url):

    #Grabs the page and parses the HTML
    page = requests.get(page_url+"?show=full")
    soup = BeautifulSoup(page.content, 'html.parser')

    #This part makes a folder with the name of the DSpace item
    narrowed_title = "blank"

    for x in soup.find('title'):
        narrowed_title = x.extract()

    stripped_title = page_url.split("/")[-1]
    os.mkdir(stripped_title)


    #This part grabs the files from the page and downloads them to the folder
    narrowed_file = soup.find_all('div', class_='file-link' )
    link = []

    for narrowed_file in narrowed_file:
        link.append(narrowed_file.find('a')['href'])

    file_num = 0

    for link in link:
        file_num = file_num + 1
        url = (urlbase + link)

        parsed_url = urlparse(link)
        parsed_name_of_file = os.path.basename(parsed_url.path)

        r = requests.get(url, allow_redirects=True)
        open(parsed_name_of_file, 'wb').write(r.content)
        shutil.move(parsed_name_of_file, stripped_title)

    #This part creates and populates the metatada.yml file
    metafile = open("metadata.yml","a")
    
    
    narrowed_title = narrowed_title.replace('"', "'")
    metafile.write("title: " + '"' + narrowed_title +'"\n')




    try:
        description_text = (soup.find(text="dc.description").findNext('td').contents[0])
    except:
        description_text = ""



    try:
        description_text = (soup.find(text="dc.description.abstract").findNext('td').contents[0])
    except:
        description_text = ""
    
    
  
    description_text = description_text.replace('"', "'").replace('\r','').replace('\n',' ').replace("’","'").replace("‘","'").replace("“","'").replace("”","'").replace('£','').replace('½','.5').replace('[','(').replace(']',')')
    metafile.write("description: " + description_text + "\n")


    metafile.write("physical_description: ''"  + "\n")
    metafile.write("document_history: ''"  + "\n")
    metafile.write("permission_description: ''"  + "\n")
    metafile.write("location_of_composition: ''"  + "\n")



    try:
        author_name = (soup.find(text="dc.contributor.author").findNext('td').contents[0])
    except:
        author_name = ""
    
    author_name = author_name.replace('"', "'")
    metafile.write("author: " + author_name + "\n")

    metafile.write("transcription_conventions: ''"  + "\n")
    metafile.write("scribes_can_edit_titles: true"  + "\n")
    metafile.write("supports_translation: true"  + "\n")
    metafile.write("translation_instructions: ''"  + "\n")
    metafile.write("pages_are_meaningful: true"  + "\n")

    metafile.write("slug: '" + stripped_title.replace(" ", "_") + "'\n")

    metafile.close()

    shutil.move("metadata.yml", stripped_title)



def batch_bundle():
    folders = os.listdir()
    os.mkdir("bundled_items")
    
    placeholder = requests.get("https://raw.githubusercontent.com/BrockDSL/BrockDSL.github.io/master/dsl_logo.png", allow_redirects=True)
    open("dsl_logo.png", 'wb').write(placeholder.content)
    shutil.move("dsl_logo.png", "bundled_items")
    
    for dir in folders:
        if os.path.isdir(dir) and dir[0] != "." :
            shutil.move(dir, "bundled_items")



def bundle_files():
    for dir in os.listdir():
        if os.path.isdir(dir) and dir[0] != "." :
            shutil.make_archive(dir, 'zip', dir)
            shutil.rmtree(dir, ignore_errors=True)


if __name__ == "__main__":

    #scrape and clean data
    for row in url_list:
        build_ftp_folder(row[0])
    
    
    #Uncomment this to have all of the files be combined into a single .zip for upload.  Good for if all items will be put into a single collection.
    #batch_bundle()


    #process into zips
    bundle_files()
