import pandas as pd
import pickle

movies = pd.read_csv(r"C:\Users\hridd\Documents\ml-latest-small\movies.csv")
links = pd.read_csv(r"C:\Users\hridd\Documents\ml-latest-small\links.csv")
tags = pd.read_csv(r"C:\Users\hridd\Documents\ml-25m\genome-scores.csv")
ratings = pd.read_csv(r"C:\Users\hridd\Documents\ml-latest-small\ratings.csv")

movies = movies.loc[:, ['movieId', 'title']] # Removing the genres column as more detailed descriptors are available in the tags dataframe
links = pd.merge (movies, links, on = 'movieId')
pickle.dump(links, open('movies.pkl', 'wb'))
ratings = ratings.loc[:, ['userId', 'movieId', 'rating']] # Removing the timestamp column as it is of no importance to us

tagData = pd.merge(movies, tags, on = 'movieId') # Merging the movies and tags dataframes
pickle.dump(tagData, open('tagData.pkl', 'wb'))
tagTable = tagData.pivot_table(index = 'tagId', columns = 'title', values = 'relevance', fill_value=0.00001) # Creating a pivot table with fill_value = 0.00001 to avoid NaN values
pickle.dump(tagTable, open('tagTable.pkl', 'wb'))

userData = pd.merge(movies, ratings, on = 'movieId') # Merging the movies and ratings dataframes
pickle.dump(userData, open('userData.pkl', 'wb'))
userTable = userData.pivot_table(index = 'userId', columns = 'title', values = 'rating', fill_value=0.00001) # Creating a pivot table with fill_value = 0.00001 to avoid NaN values
pickle.dump(userTable, open('userTable.pkl', 'wb'))