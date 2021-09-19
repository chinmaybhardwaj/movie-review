import os
import pandas as pd
from year_scrapper import get_year



def get_url(df):
  
    if df is not None:
        
        for index, row in df.iterrows():
            name = row['year']
            url = row['link']
            # Get HTML page for given year URL
            get_year(str(name), url)
    else:
        print('year_parser.py:','Error in parsing DataFrame')


#
# Create years.csv with cleaned data
#
def save_to_csv(df):
    outputdir = './dataset'
    if not os.path.exists(outputdir):
        os.mkdir(outputdir)
        
    # Write DataFrame to years.csv
    df.to_csv('./dataset/years.csv', sep=',', index=False, encoding='utf-8')
    print('year_parser.py:','years.csv created!')
    
    
#
# Load dataframe from years.csv
#    
def load_years_csv():
    outputdir = './dataset/years.csv'
    if not os.path.exists(outputdir):
        print('year_parser.py:','years.csv does not exist!')
        return None
        
    # Read DataFrame from years_table.csv
    with open(outputdir, "r") as file:
        df = pd.read_csv(file)
        print('year_parser.py:','Loading years.csv !') 
        
    return df
#
# Load dataframe from csv
#
df = load_years_csv()

get_url(df)

