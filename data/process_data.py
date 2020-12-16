import sys
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    '''
    Load the message and category .csv data files
    Input: the filepath of the two .csv files
    Output: return the two data frames
    '''
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    return messages,categories


def clean_data(messages,categories):
    '''
    merge and clean the dataframe for further ML model
    Input: the message and category dataframes
    Output: the final clean, merged dataframe
    '''
    
    df= messages.merge(categories,how='outer',on=['id'])
    # create a dataframe of the 36 individual category columns
    categories = df['categories'].str.split(";",expand=True)
    # select the first row of the categories dataframe
    row = categories.iloc[0]
    # use this row to extract a list of new column names for categories.
    # one way is to apply a lambda function that takes everything 
    # up to the second to last character of each string with slicing
    category_colnames=row.map(lambda x: x[:-2])
    # rename the columns of `categories`
    categories.columns = category_colnames
    
    # Convert category values to just numbers 0 or 1.
    for column in categories:
        # set each value to be the last character of the string
        categories[column] = categories[column].astype(str).str[-1]
        # convert column from string to numeric  
        categories[column]=categories[column].map(lambda x:int(x))
    # drop the original categories column from `df`
    df=df.drop(['categories'],axis=1)
    # concatenate the original dataframe with the new `categories` dataframe
    df = pd.concat([df,categories],axis=1)
    # drop duplicates
    df = df.drop_duplicates()
    # replace the label2 in category related with 1
    df['related']=np.where(df['related']==2,1,0)
    
    return df


def save_data(df, database_filename):
    '''
    save the data into a sql table
    Input: the dataframe to be saved and the filepath to save the table
    '''
    engine = create_engine('sqlite:///'+database_filename, echo=False)
    df.to_sql('DisasterData', engine, if_exists='replace', index=False) 


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('step1: Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        messages,categories = load_data(messages_filepath, categories_filepath)

        print('step2: Cleaning data...')
        df = clean_data(messages,categories)
        
        print('step3: Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('step4: Cleaned data saved to database!')
    
    else:
        print('Warning: Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__': 
    main()