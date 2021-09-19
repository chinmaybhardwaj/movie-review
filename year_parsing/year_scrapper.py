from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
#from requests.adapters import HTTPAdapter
#from requests.packages.urllib3.util.retry import Retry
import time

# =============================================================================
# Parse HTML and get title, link, production, cast and other details of each movie.
# URL: https://en.wikipedia.org/wiki/name_of_movie
# =============================================================================


base_url = 'https://en.wikipedia.org'

#
# Request HTML page for url
#
def get_year_page(url=''):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")

    return soup

#
# Save HTML response to year_name.html file in source directory
#
def save_html(name, soup):
    outputdir = './source/html'
    if not os.path.exists(outputdir):
        os.mkdir(outputdir)
        
    # Write HTML String to .html file
    filename = outputdir + '/' + name + '.html'
    with open(filename, "w") as file:
        file.write(str(soup.encode("utf-8")))
        print('year_scrapper.py:', name,'html created!')  
    
    
#
# Load HTML response from year_name.html if present
#
def load_html(name):
    outputdir = './source/html/' + name + '.html'
    if not os.path.exists(outputdir):
        print('year_scrapper.py:', name, 'html does not exist!')
        return None
        
    # Read HTML String from year_name.html and convert it to bs object
    with open(outputdir, "r") as file:
        soup = BeautifulSoup(file, features="html.parser")
        print('year_scrapper.py:', 'Loading', name, 'html !')  
        
    return soup


#
# Parse HTMl to get list of all movies and their title, link, cast, genre, production
#
def parse_html(divs):    
    data = []    
    for mydiv in divs:
        table_rows = mydiv.find_all("tr")
        for tr in table_rows:

            td_a = tr.find_all("a", href=True)
           
            movie = {}
            count = 0
            movie['cast'] = ''
            for a in td_a:              
                if count == 0:
                    movie['title'] = a.text
                    movie['link'] = a['href']
                    movie['detail'] = td_a
                elif count == 1:
                    movie['production'] = a.text
                elif count == 3:
                    pass 
                elif count == len(td_a)-2:
                    movie['genre'] = a.text
                elif count == len(td_a)-1:
                    pass
                else:
                    if len(movie['cast']) == 0:
                        movie['cast'] = a.text
                    else:
                        movie['cast'] = movie['cast'] + ', ' + a.text
                        
                count = count + 1
            data.append(movie)
    print('----------------\n\n', data[:2])


    return data


#
# Save the movie details in year_name.csv
#
def save_to_csv(name, result):
    outputdir = './source/csv/'
    if not os.path.exists(outputdir):
        os.mkdir(outputdir)
        
    # Convert list to dataframe and rearrange the columns
    cols = ['title', 'link', 'genre', 'production', 'cast', 'detail']
    df = pd.DataFrame(result)
    df = df[cols]
    # Write DataFrame to years_name.csv
    csv_name = outputdir + name + '.csv'
    df.to_csv(csv_name, sep=',', index=False, encoding='utf-8')
    print('year_scrapper.py:', name, 'csv created!')  
    
    
    
#
# Load dataframe from year_name.csv
#    
def load_years_csv(name):
    outputdir = './source/csv/' + name + '.csv'
    if not os.path.exists(outputdir):
        print('year_scrapper.py:', name, 'csv does not exist!')
        return None
        
    # Read DataFrame from year.csv
    with open(outputdir, "r") as file:
        df = pd.read_csv(file)
        print('year_scrapper.py:', 'Loading', name, 'csv !') 
        
    return df
    

#
# Main function to check if csv/html file exists or not.
# If file does not exist request html page and parse response
#
def get_year(name='', url=''):

    df = load_years_csv(name)
    
    if df is None:
        soup = load_html(name)
        if soup is None:
            soup = get_year_page(url = base_url + url) 
            save_html(name, soup)
        
        mydivs = soup.findAll("table",{"class":"wikitable sortable"})
        result = parse_html(mydivs)
        save_to_csv(name, result)
        time.sleep(2)
    else:
        print('year_scrapper.py:', 'CSV ready to use!')
        return df

        
