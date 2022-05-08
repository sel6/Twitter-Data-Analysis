# -*- coding: utf-8 -*-
"""
Created on Sun May  8 12:02:25 2022

@author: Selu
"""

# Importing module
import os
import pandas as pd
from mysql.connector import Error
import mysql.connector as cu

def DBConnect(dbName=None):
    mydb = cu.connect(host='localhost', user='root',
                      password='Selam@0102.',
                         database=dbName, buffered=True)
    cursor = mydb.cursor()
    return mydb, cursor


def createDB(dbName: str) -> None:
    mydb, cursor = DBConnect()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbName};")
    mydb.commit()
    cursor.close()
    
def createTables(dbName: str) -> None:
    mydb, cursor = DBConnect(dbName)
    sqlFile = 'schema.sql'
    fd = open(sqlFile, 'r')
    readsqlFile = fd.read()
    fd.close()
    sqlCommands = readsqlFile.split(';')
    for command in sqlCommands:
        try:
            result = cursor.execute(command)
        except Exception as e:
            print('command skipped: ', command)
            print(e)
    mydb.commit()
    cursor.close()
    
def preprocess_df(df: pd.DataFrame) -> pd.DataFrame:
    try:
        df = df.fillna(0)
    except KeyError as e:
        print('Error: ', e)
    
    return df
        
def insert_into_tweet_table(dbName: str, df: pd.DataFrame, table_name: str) -> None:
    mydb, cursor = DBConnect(dbName)
    df = preprocess_df(df)
    for _, row in df.iterrows():
        sqlQuery = f"""INSERT INTO {table_name} 
        (created_at, source, original_text, polarity, subjectivity, lang,
                    favorite_count, retweet_count, original_author, followers_count, friends_count,
                    hashtags, place)
              VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
       
        data = (row[0], row[1], row[2], row[3], (row[4]), (row[5]), row[6], row[7], row[8], row[9], row[10], row[11],
          row[12])
        try:
            cursor.execute(sqlQuery, data)
            mydb.commit()
            print('Data inserted successfully')
        except Exception as e:
            mydb.rollback()
            print('Error: ', e)
            
def fetch_data(table_name):
    mydb, cursor= DBConnect()
    column = []
    query = "SELECT * FROM {table_name}"
    value = cursor.execute(query)
    for items in cursor.description:
        column.append(items[0])
        mydb.commit()
        df = pd.DataFrame(value, columns=column)
        cursor.close()
        return df
            
if __name__=="__main__":
    createDB(dbName='tweets')
    df = pd.read_csv('processed_tweet_data.csv')
    createTables(dbName='tweets')
    insert_into_tweet_table(dbName = 'tweets', df = df, table_name='TweetInformation')
