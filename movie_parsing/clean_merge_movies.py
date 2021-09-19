import pandas as pd
import os


# =============================================================================
# Clean and merge all movies into single csv
# =============================================================================

#
# Save cleaned data to movies.csv
#
def save_to_csv(result):
    outputdir = './source'
    if not os.path.exists(outputdir):
        os.mkdir(outputdir)
        
    # Write DataFrame to movies.csv
    result.to_csv('./source/movies.csv', sep=',', index=False, encoding='utf-8')
    print('movies.csv created!')  
    
    
#
# Load dataframe from movies.csv
#    
def load_years_csv():
    outputdir = '../year_parsing/source/csv/'
    if not os.path.exists(outputdir):
        print('years_table.csv does not exist!')
        return None
        
    csv_files = os.listdir(outputdir)
    
    df = pd.DataFrame()
    
    for file in csv_files:
        if file == '.DS_Store':
            continue
        
        temp_df = pd.read_csv(outputdir + file)
        temp_df['year'] = file.split('.')[0]
        temp_df['plot'] = 'Not Available'
        temp_df['rating'] = '0'
        df = df.append(temp_df)
        
    print(df[:5])
    return df
    

df = load_years_csv()
# Sort rows by year
df = df.sort_values(by ='year')
save_to_csv(df)