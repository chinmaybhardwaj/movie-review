import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import imdb

    
    
#
# Load dataframe from movies.csv
#    
def load_movies_csv():
    outputdir = './source/movies.csv'
    if not os.path.exists(outputdir):
        print('get_movie_detail.py:', outputdir, ' does not exist!')
        return None
        
    # Read DataFrame from year.csv
    with open(outputdir, "r") as file:
        df = pd.read_csv(file)
        print('get_movie_detail.py:', 'Loading', 'movies.csv !') 
        
    return df


def visualize_data():
    df = load_movies_csv()
    df.dropna(inplace=True) 

    count = 0
    
    for index, movie in df.iterrows():
        
        if count < 3:
            if len(movie['title']) > 0: 
                get_imdb_details(index, movie['title'], df.loc[index])
        count = count + 1    

        

def get_imdb_details(index, movie_name, df_row):
    
    print('-------->', movie_name)
    search_results = ia.search_movie(movie_name)

    if search_results:
     movieID = search_results[0].movieID
     movie = ia.get_movie(movieID)
     
     if movie:
         cast = movie.get('cast')
         topActors = 5
         actors = ''
         for actor in cast[:topActors]:

             if len(actors) == 0:
                 actors = actor['name']
             else:
                 actors = actors + ', ' + actor['name']
                 
         df_row['cast'] =  actors
         
         genres = ''
         for genre in movie['genres']:
             if len(genres) == 0:
                 genres = genre
             else:
                 genres = genres + ', ' + genre

         df_row['genre'] =  genres
         df_row['rating'] =  movie['rating']         
         df_row['plot'] = movie['plot']  
         
         print('Rating:', movie['rating'])
         print('ROW:', df_row)
         
         final_df.append(df_row, ignore_index=True)
         
    return df_row



ia = imdb.IMDb()

final_df = pd.DataFrame()
visualize_data()

print(final_df)







