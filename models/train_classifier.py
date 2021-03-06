import sys
import nltk
nltk.download(['punkt','wordnet','stopwords'])
import pandas as pd
import numpy as np
import re
import joblib
from sqlalchemy import create_engine 

from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.metrics import confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.feature_extraction.text import CountVectorizer,TfidfTransformer
from sklearn.multioutput import MultiOutputClassifier
from nltk.corpus import stopwords
from sklearn.metrics import classification_report
from sklearn.metrics import precision_recall_fscore_support
from sklearn.utils.multiclass import type_of_target

def load_data(database_filepath):
    '''
    Load and read the sql table generated from the ETL pipeline
    Input: SQL engine and database_filepath
    Output: return X,Y varaibles for the further ML model
   
    '''
    engine = create_engine('sqlite:///'+database_filepath)
    df = pd.read_sql_table('DisasterData', engine)
    
    X=df.iloc[:,1]
    Y=df.iloc[:,4:]
    category_names=Y.columns.values
    return X,Y,category_names


def tokenize(text):
    '''
    Clean the text data using tokenize and lemmatizer, and remove stop words
    Input: text data
    Output: lemmatized, clean text data
    '''
    # remove punctuations
    text = re.sub(r"[^a-zA-Z0-9]"," ",text)
    # tokenize text into words
    tokens = nltk.word_tokenize(text)
    # remove stop words
    tokens = [x for x in tokens if x not in stopwords.words("english")]
    lemmatizer=WordNetLemmatizer()
    clean_tokens=[]
    for tok in tokens:
        clean_tok=lemmatizer.lemmatize(tok).lower().strip()
        clean_tokens.append(clean_tok)
    return clean_tokens


def build_model():
    '''
    Build ML pipeline model and GridSearch CV
    Output: improved ML model using GridSearch
    '''
    pipeline = Pipeline([('vect',CountVectorizer(tokenizer=tokenize)),
                    ('tfidf',TfidfTransformer()),
                   ('clf',MultiOutputClassifier(RandomForestClassifier()))])
    parameters = {'vect__ngram_range':((1,1),(1,2)),
              'vect__max_df':(0.5,0.75,1.0)}
    model = GridSearchCV(estimator=pipeline,param_grid=parameters)
    return model


def evaluate_model(model, X_test, Y_test, category_names):
    '''
    model. sklearn ML model
    Evalute the ML model using the disaster data
    input: X, the feature variables; Y, the predict variables, category names, the target names
    output: the results of the ML model, including prevision, recall, f1-score, and support
    '''
    Y_pred = model.predict(X_test)
    print(classification_report(Y_test,Y_pred,target_names=category_names))


def save_model(model, model_filepath):
    '''
    save the model and dump into a pickl file
    Input: the ML el built in the previous steps; the filepath and name to save the model
    '''
    import pickle
    filename=model_filepath
    with open(filename,'wb') as file:
        pickle.dump(model,file)


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        load_data(database_filepath)
       
        X, Y, category_names = load_data(database_filepath)
        
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()
 