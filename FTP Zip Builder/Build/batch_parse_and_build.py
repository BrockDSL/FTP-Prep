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


input_files = os.listdir("../Input")
print(input_files)


def build_ftp_folder(page_url):

    #Checks if user provided URI instead of URL and fixes
    if page_url[0:21]=="http://hdl.handle.net":
        url_start = "https://dr.library.brocku.ca/handle/"
        url_end = page_url[22:]
        page_url = url_start + url_end
    
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
        
                
        #Renames image to remove bad characters
        img_name_cleaned = parsed_name_of_file.replace("%20","_").replace("&","AND").replace("%2c","").replace("%e2","").replace("%80","").replace("%99","").replace("%27","").replace("%","")
        os.rename(str(parsed_name_of_file),str(img_name_cleaned))

        
        
        shutil.move(img_name_cleaned, stripped_title)

    #This part creates and populates the metatada.yml file
    metafile = open("metadata.yml","a")
    
    
    narrowed_title = narrowed_title.replace('"', "'").replace('\r','').replace('\n',' ').replace("’","'").replace("‘","'").replace("“","'").replace("”","'").replace('£','').replace('½','.5').replace('[','(').replace(']',')').replace('–',' ').replace('-',' ').replace('%',' ').replace("…","").replace("¼","0.25").replace("—"," ")

    metafile.write("title: " + '"' + narrowed_title[0:250] +'"\n')




    try:
        description_text = (soup.find(text="dc.description").findNext('td').contents[0])
    except:
        description_text = ""



    try:
        description_text = (soup.find(text="dc.description.abstract").findNext('td').contents[0])
    except:
        description_text = ""
    
    
  
    description_text = description_text.replace('"', "'").replace('\r','').replace('\n',' ').replace("’","'").replace("‘","'").replace("“","'").replace("”","'").replace('£','').replace('½','.5').replace('[','(').replace(']',')').replace('–',' ').replace('-',' ').replace('%',' ').replace("…","").replace("¼","0.25").replace("—"," ")
    metafile.write("description: " + '"' + description_text + '"\n')


    metafile.write('physical_description: ""'  + "\n")
    metafile.write('document_history: ""'  + "\n")
    metafile.write('permission_description: ""'  + "\n")
    metafile.write('location_of_composition: ""'  + "\n")



    try:
        author_name = (soup.find(text="dc.contributor.author").findNext('td').contents[0])
    except:
        author_name = ""
    
    author_name = author_name.replace('"', "'").replace('\r','').replace('\n',' ').replace("’","'").replace("‘","'").replace("“","'").replace("”","'").replace('£','').replace('½','.5').replace('[','(').replace(']',')').replace('–',' ').replace('-',' ').replace('%',' ').replace("…","").replace("¼","0.25").replace("—"," ")
    metafile.write('author: "' + author_name + '"\n')

    metafile.write('transcription_conventions: ""'  + '\n')
    metafile.write('scribes_can_edit_titles: true'  + '\n')
    metafile.write('supports_translation: true'  + '\n')
    metafile.write('translation_instructions: ""'  + '\n')
    metafile.write('pages_are_meaningful: true'  + '\n')

    metafile.write('slug: "' + stripped_title.replace(" ", "_") + '"\n')

    metafile.close()

    shutil.move("metadata.yml", stripped_title)

def batch_bundle():
    folders = os.listdir()
    os.mkdir("bundled_items")
    
    for dir in folders:
        if os.path.isdir(dir) and dir[0] != "." :
            shutil.move(dir, "bundled_items")

def bundle_files():
    for dir in os.listdir():
        if os.path.isdir(dir) and dir[0] != "." :
            shutil.make_archive(dir, 'zip', dir)
            shutil.rmtree(dir, ignore_errors=True)

if __name__ == "__main__":

    for file in input_files:
        
        print("Currently building "+file)
        
        #Pull file into build folder and rename to url_list
        shutil.move("../Input/"+file, "../Build")
        os.rename(file, "url_list.csv")
        
        #Read in file
        csv_file = open("url_list.csv", encoding='utf-8-sig')
        url_list = csv.reader(csv_file)
        
        
        #Scrape and clean data
        for row in url_list:
            build_ftp_folder(row[0])
        
        
        #Combine into a single .zip for upload.  Good for if all items will be put into a single collection.
        batch_bundle()
        
        
        #process into zips
        bundle_files()
        
        #Rename the bundle and file to filename
        csv_file.close()
        os.rename("bundled_items.zip", "bundled_"+file+".zip")
        os.rename("url_list.csv", file)
        shutil.move("bundled_"+file+".zip", "../Output")
        shutil.move(file, "../Output")
        
