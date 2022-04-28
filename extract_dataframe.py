import json
import pandas as pd
from textblob import TextBlob
import re

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
    for tweets in open(json_file,'r'):
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

    #function that returns the status
    def find_statuses_count(self)->list:
        statuses_count = []

        for i in range(len(self.tweets_list)):
            statuses_count.append((self.tweets_list[i]['user']['statuses_count']))

        return statuses_count
        
        
    def find_full_text(self)->list:
        org_txt = []
        clean = []
        for txt in range(len(self.tweets_list)):
            org_txt.append((self.tweets_list[txt]['text']))
            clean.append(re.sub("^RT.*:","",self.tweets_list[txt]['text']))

        return org_txt, clean
       
    #functions that returns lists of polarity and subjectivity
    def find_sentiments(self, text: list)->list:
        text = [txt.get('retweeted_status', {}) for txt in self.tweets_list]
        extended_tweet = [ext_txt.get('extended_tweet', {}) for ext_txt in text]
        full_text = [full.get('full_text', '') for full in extended_tweet]

        sentimentedText = [TextBlob(full) for full in full_text]
        polarity = []
        subjectivity = []

        for feels in range(len(sentimentedText)):
            polarity.append(sentimentedText[feels].sentiment.polarity)
            subjectivity.append(sentimentedText[feels].sentiment.subjectivity)

        return polarity, subjectivity

    #function that returns lists of created_at
    def find_created_time(self)->list:
        created_at = []
        for created in range(len(self.tweets_list)):
            created_at.append(self.tweets_list[created]['created_at'])
       
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
            friends_count.append((self.tweets_list[count]['user']['friends_count']))

        return friends_count

    
    def is_sensitive(self)->list:
        is_sensitive = [x.get('possibly_sensitive', None) for x in self.tweets_list]

        return is_sensitive

    #functions that returns likes in list
    def find_favourite_count(self)->list:
        favorite_count = []

        for fav in range(len(self.tweets_list)):
            favorite_count.append((self.tweets_list[fav]['user']['favourites_count']))
            
        return favorite_count

    #function that returns the language
    def find_lang(self)->list:
        lang = []
        for lg in range(len(self.tweets_list)):
            lang.append(self.tweets_list[lg]['lang'])

        return lang
    
    #function that returns tweet count
    def find_retweet_count(self)->list:
        retweet_count = []
        for r_twt in range(len(self.tweets_list)):
            retweet_count.append(self.tweets_list[r_twt]['retweet_count'])

        return retweet_count

    def find_hashtags(self)->list:
        hashtags = []
        for h in range(len(self.tweets_list)):
            hashtags.append(self.tweets_list[h]['entities']['hashtags'])

        return hashtags
    
    def find_mentions(self)->list:
        # retun list of all None
        mentions = [x.get('mentions', None) for x in self.tweets_list]


        return mentions
    
    def find_location(self)->list:
        #returns list of location
        location = [x.get('retweeted_status', {}).get('user', {}).get('location', None) for x in self.tweets_list]
        return location

    
        
        
    def get_tweet_df(self, save=False)->pd.DataFrame:
        """required column to be generated you should be creative and add more features"""
        
        columns = ['created_at', 'source', 'original_text', 'polarity', 'subjectivity', 'lang', 'favorite_count', 'retweet_count', 'original_author', 'followers_count', 'possibly_sensitive', 'hashtags', 'place', 'friends_count']
         
        created_at = self.find_created_time()
        source = self.find_source()
        clean_txt, text = self.find_full_text()
        polarity, subjectivity = self.find_sentiments(clean_txt)
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

        data = zip(created_at, source, text, polarity, subjectivity, lang, fav_count, retweet_count, screen_name, follower_count, sensitivity, hashtags, location, friends_count)
        
        df = pd.DataFrame(data=data, columns=columns)

        if save:
            df.to_csv('processed_tweet_data.csv', index=False)
            print('File Successfully Saved.!!!')
        
        return df

                
if __name__ == "__main__":
    # required column to be generated you should be creative and add more features
    columns = ['created_at', 'source', 'original_text','clean_text', 'sentiment','polarity','subjectivity', 'lang', 'favorite_count', 'retweet_count', 
    'original_author', 'screen_count', 'followers_count','friends_count','possibly_sensitive', 'hashtags', 'user_mentions', 'place', 'place_coord_boundaries']
    _, tweet_list = read_json("./data/Economic_Twitter_Data.json")
    tweet = TweetDfExtractor(tweet_list)
    tweet_df = tweet.get_tweet_df(True) 

    # use all defined functions to generate a dataframe with the specified columns above
