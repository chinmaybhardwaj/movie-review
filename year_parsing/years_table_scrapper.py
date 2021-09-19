from bs4 import BeautifulSoup
import requests
import pandas as pd
import os


# =============================================================================
# Parse HTML and get links for each year.
# URL: https://en.wikipedia.org/wiki/Lists_of_films
# =============================================================================

#
# Request HTML page for url
#
def get_html_page(url=''):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    
    return soup

#
# Save HTML response to Lists_of_films.html file in source directory
#
def save_html(soup):
    outputdir = './source'
    if not os.path.exists(outputdir):
        os.mkdir(outputdir)
        
    # Write HTML String to Lists_of_films.html
    with open("./source/Lists_of_films.html", "w") as file:
        file.write(str(soup.encode("utf-8")))
        print('Lists_of_films.html created!')  
    
    
#
# Load HTML response from Lists_of_films.html
#
def load_html():
    outputdir = './source/Lists_of_films.html'
    if not os.path.exists(outputdir):
        print('Lists_of_films.html does not exist!')
        return None
        
    # Read HTML String from Lists_of_films.html
    with open(outputdir, "r") as file:
        soup = BeautifulSoup(file, features="html.parser")
        print('Loading Lists_of_films.html !')  
        
    return soup


#
# Parse HTMl to get list of all years and their links
#
def parse_html(divs):
    href = []
    text = []
    for mydiv in divs:
#        dls = mydiv.find_all("dl")
        dt_a = mydiv.find_all("a", href=True)
        print(mydiv)
        for a in dt_a:
            print(a.text, '-------', a["href"])
            href.append(a["href"])
            text.append(a.text)
        
    return text, href


#
# Save Years and Links to years_table.csv
#
def save_to_csv(text=[], href=[]):
    outputdir = './source'
    if not os.path.exists(outputdir):
        os.mkdir(outputdir)
        
    # Write DataFrame to years_table.csv
    df = pd.DataFrame()
    df['year'] = text
    df['link'] = href
    df.to_csv('./source/years_table.csv', sep=',', index=False, encoding='utf-8')
    print('years.csv created!')  
    
    
    
#
# Load dataframe from years_table.csv
#    
def load_years_csv():
    outputdir = './source/years_table.csv'
    if not os.path.exists(outputdir):
        print('years_table.csv does not exist!')
        return None
        
    # Read DataFrame from years_table.csv
    with open(outputdir, "r") as file:
        df = pd.read_csv(file)
        print('Loading years_table.csv !') 
        
    return df
    

#
# Main function to check if csv/html file exists or not.
# If file does not exist request html page and parse response
#
def get_years():
    
    df = load_years_csv()
    
    if df is None:
        soup = load_html()
        if soup is None:
            soup = get_html_page(url = 'https://en.wikipedia.org/wiki/Lists_of_films') 
            save_html(soup)
        
        mydivs = soup.findAll("div", {"class": "hlist"})
        text, href = parse_html(mydivs)
        save_to_csv(text=text, href=href)
        get_years()
    else:
        print('CSV ready to use!')
        return df

        
