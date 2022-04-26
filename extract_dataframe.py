import json
import pandas as pd
from textblob import TextBlob

def read_json(json_file: str)->list:
    """
    json file reader to open and read json files into a list
    Args:
    -----
    json_file: str - path of a json file
    
    Returns
    -------
    length of the json file and a list of json
    """
    
    tweets_data = []
    for tweets in open("Economic_Twitter_Data.json",'r'):
        tweets_data.append(json.loads(tweets))
    
    
    return len(tweets_data), tweets_data

class TweetDfExtractor:
    """
    this function will parse tweets json into a pandas dataframe
    
    Return
    ------
    dataframe
    """
    def __init__(self, tweets_list):
        
        self.tweets_list = tweets_list

    # an example function
    def find_statuses_count(self)->list:
        statuses_count = []

        for i in range(len(self.tweets_list)):
            statuses_count.append((self.tweets_list[i]['user']['statuses_count']))

        return statuses_count
        
        
    def find_full_text(self)->list:
        org_txt = []
        clean = []
        for txt in range(len(self.tweets_list)):
            org_txt.append((tweets_list[txt]['text']))
            clean.append(re.sub("^RT.*:","",tweets_list[txt]['text']))

        return org_txt, clean
       
    #functions that returns lists of polarity and subjectivity
    def find_sentiments(self, text: list)->list:
        polarity = []
        self.subjectivity = []
        for sentiment in range(len(text)):
            self.subjectivity.append(TextBlob(items).sentiment.subjectivity)
            polarity.append(TextBlob(items).sentiment.polarity)

        return polarity, self.subjectivity

    #function that returns lists of created_at
    def find_created_time(self)->list:
        created_at = []
        for created in range(len(self.tweets_list)):
            created_at.append(created['created_at'])
       
        return created_at

    #function that returns the lists of sources
    def find_source(self)->list:
        source = []
        for src in range(len(self.tweets_list)):
            source.append((self.tweets_list[src]['source']))

        return source
    
    #function that returns lists of screen_name/author name
    def find_screen_name(self)->list:
        screen_name = []

        for name in range(len(self.tweets_list)):
            screen_name.append((self.tweets_list[name]['user']['screen_name']))

        return screen_name

    #function that returns lists of followers
    def find_followers_count(self)->list:
        followers_count = []

        for follow in range(len(self.tweets_list)):
            followers_count.append((self.tweets_list[follow]['user']['followers_count']))

        return followers_count

    #function that returns number of friends
    def find_friends_count(self)->list:
        friends_count = []

        for count in range(len(self.tweets_list)):
            text.append((tweets_list[count]['user']['friends_count']))

    
    def is_sensitive(self)->list:
        try:
            is_sensitive = [x['possibly_sensitive'] for x in self.tweets_list]
        except KeyError:
            is_sensitive = None

        return is_sensitive

    #functions that returns likes in list
    def find_favourite_count(self)->list:
        favorite_count = []

        for fav in range(len(self.tweets_list)):
            favorite.append((self.tweets_list[fav]['retweeted_status']['favorite_count']))
            
        return favorite_count

    #function that returns tweet count
    def find_retweet_count(self)->list:
        retweet_count = 

    def find_hashtags(self)->list:
        hashtags =

    def find_mentions(self)->list:
        mentions = 


    def find_location(self)->list:
        try:
            location = self.tweets_list['user']['location']
        except TypeError:
            location = ''
        
        return location

    
        
        
    def get_tweet_df(self, save=False)->pd.DataFrame:
        """required column to be generated you should be creative and add more features"""
        
        columns = ['created_at', 'source', 'original_text','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
            'original_author', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place']
        
        created_at = self.find_created_time()
        source = self.find_source()
        text = self.find_full_text()
        polarity, subjectivity = self.find_sentiments(text)
        lang = self.find_lang()
        fav_count = self.find_favourite_count()
        retweet_count = self.find_retweet_count()
        screen_name = self.find_screen_name()
        follower_count = self.find_followers_count()
        friends_count = self.find_friends_count()
        sensitivity = self.is_sensitive()
        hashtags = self.find_hashtags()
        mentions = self.find_mentions()
        location = self.find_location()
        data = zip(created_at, source, text, polarity, subjectivity, lang, fav_count, retweet_count, screen_name, follower_count, friends_count, sensitivity, hashtags, mentions, location)
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')
        
        return df

                
if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
    'original_author', 'screen_count', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']
    _, tweet_list = read_json("../Economic_Twitter_Data.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df() 

    # use all defined functions to generate a dataframe with the specified columns above
