from bs4 import BeautifulSoup
import requests
import re
import statistics as s
import string


url = 'https://www.allrecipes.com/recipe/15183/carrot-patties/'

def get_soup(url):
    result = requests.get(url)
    doc = result.text # html
    soup = BeautifulSoup(doc, 'html.parser')

    # removes all HTML tag attributes
    def _remove_attrs(soup): # from https://gist.github.com/bradmontgomery/673417
        for tag in soup.findAll(True): 
            tag.attrs = None
        return soup
    soup_refine = _remove_attrs(soup)
    return soup_refine

# returns string of HTML title in snake_case
def get_title(soup):
    file_title = soup.title.string.lower()
    file_title = file_title.replace(' ', '_')
    for x in range(len(file_title)):
        if file_title[x] not in string.ascii_letters and file_title[x] != '_':
            file_title = file_title[:x - 1]
            break
    return file_title

# returns section of soup containing all contents between section title and next section title, delineated
# by header tags
def get_section(soup, section_title):
    soup_str = str(soup)
    headers_all = soup.find_all(re.compile('^h[1-6]$'))
    for i in range(len(headers_all)):
        contents = str(headers_all[i].contents).lower()
        if section_title in contents:
            header = headers_all[i]
            header_i = soup_str.find(str(header))
            header_following = headers_all[i + 1]
            header_i_following = soup_str.find(str(header_following))
            break # what if 2 'title' headers?
            
    section_str = soup_str[header_i:header_i_following]
    section_soup = BeautifulSoup(section_str, "html.parser")
    return section_soup

soup = get_soup(url)
title = get_title(soup)
soup_ingredients = get_section(soup, 'ingredients')


# --------- TO DO ---------------------------------------------------------------------------------------------------
# except get_section index error if title not found in header tags
# get directions
# save soup as html
# build side app to run through list of urls to extract recipes
# style saved soup html
# build django(?) app to display recipes


# --------- TESTING ---------------------------------------------------------------------------------------------------
# with open(f'./temp.txt', 'w') as f:
#     f.write(str(soup))