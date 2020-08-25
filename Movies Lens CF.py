import pandas as pd
import joblib

ratings = pd.read_csv('ratings.csv')
movies = pd.read_csv('movies.csv')
posters = pd.read_csv('movie_posters.csv',header=None,names=['movieId','poster_url'],index_col=0)
ratings = pd.merge(movies,ratings).drop(['genres','timestamp'],axis=1)
ratings.head()


#Removing Movies which have less than 10 users who rated it. and fill remaining NaN with 0
user_ratings = ratings.dropna(thresh=10,axis=1).fillna(0)
user_ratings.head()

user_ratings = ratings.pivot_table(index=['userId'],columns=['title'],values='rating')
user_ratings.head()

#Building our Similarity Matrix
item_similarity_df = user_ratings.corr(method='pearson')
item_similarity_df.head(50)


joblib.dump(item_similarity_df,"item_similarity_df")

def get_similar_movies(movie_name,user_rating):
    similar_score = item_similarity_df[movie_name]*(user_rating-2.5)
    similar_score = similar_score.sort_values(ascending=False)
    return similar_score


action_lover = [("Catch Me If You Can (2002)",5),
                ("12 Years a Slave (2013)",3),("2012 (2009)",3),
               ("(500) Days of Summer (2009)",5),("28 Days Later (2002)",4),("Deadpool 2 (2018)",4),("Blood Diamond (2006)",4),
                ("Up in the Air (2009)",4),("I Am Legend (2007)",5),("Titanic (1997)",5),("Up (2009)",4),("Kung Fu Panda (2008)",4),
               ("I Am Legend (2007)",5),("Sherlock Holmes (2009)",4),("Da Vinci Code, The (2006)",4),("Casino Royale (2006)",4),
                ("300 (2007)",2),("War of the Worlds (2005)",2),("Scott Pilgrim vs. the World (2010)",3),("Casino Royale (2006)",4),
                ("Prestige, The (2006)",4),("Wrestler, The (2008)",4),("Mad Max: Fury Road (2015)",5),("King Kong (2005)",5),
                ("Minority Report (2002)",4),("Edge of Tomorrow (2014)",4),("Django Unchained (2012)",3),("Troy (2004)",3),
                ("Star Trek (2009)",4),("Kung Fu Panda (2008)",4),("Black Hawk Down (2001)",4),("Social Network, The (2010)",4),
                ("V for Vendetta (2006)",2)
               
               ]


def check_seen(movie,seen_movies):
    for item,rating in seen_movies:
        if item == movie:
            return True
    return False
        
    
romantic_lover = [("Titanic (1997)",5),("Up (2009)",4),("Up (2009)",4),("Kung Fu Panda (2008)",4)]
similar_movies = pd.DataFrame()

for movie,rating in action_lover:
    similar_movies = similar_movies.append(get_similar_movies(movie,rating),ignore_index=True)
    all_recommend = similar_movies.sum().sort_values(ascending=False)

for movie,score in all_recommend.iteritems():
    if not check_seen(movie,action_lover):
         print(movie)
