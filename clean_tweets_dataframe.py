import pandas as pd


class Clean_Tweets:
    """
    A class dedicated to return a clean data frame
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df
        print('Automation in Action...!!!')

    def drop_unwanted_column(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Remove rows that has column name, occured at data collection stage
        """
        unwanted_rows = self.df[self.df['retweet_count']
                                == 'retweet_count'].index
        self.df.drop(unwanted_rows, inplace=True)
        self.df = self.df[self.df['polarity'] != 'polarity']

        return self.df

    def drop_duplicate(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        drop duplicate rows
        """
        self.df = self.df.drop_duplicates().drop_duplicates(subset='original_text')

        return self.df

    def convert_to_datetime(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        convert column to datetime
        """
        self.df['created_at'] = pd.to_datetime(
            self.df['created_at'], errors='coerce')

        self.df = self.df[self.df['created_at'] >= '2020-12-31']

        return self.df

    def convert_to_numbers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        columns: polarity, retweet_count, favorite_count represented numerical
        """
        self.df['polarity'] = pd.to_numeric(
            self.df['polarity'], errors='coerce')
        self.df['retweet_count'] = pd.to_numeric(
            self.df['retweet_count'], errors='coerce')
        self.df['favorite_count'] = pd.to_numeric(
            self.df['favorite_count'], errors='coerce')

        return self.df

    def remove_non_english_tweets(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        remove non english tweets from lang
        """
        self.df = self.df.query("lang == 'eng' ")

        return self.df


if __name__ == 'main':
    data_frame = pd.read_csv('/data/processed_tweet_data.csv')
    cleaner = Clean_Tweets(data_frame)

    data_frame = cleaner.drop_duplicate(data_frame)
    data_frame = cleaner.remove_non_english_tweets(data_frame)
    data_frame = cleaner.convert_to_datetime(data_frame)
    data_frame = cleaner.convert_to_numbers(data_frame)
    data_frame = cleaner.drop_unwanted_column(data_frame)

    data_frame.to_csv('/data/clean_processed_tweet_data.csv')
    print('You have now a clean tweet data frame.')
