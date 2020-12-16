# Udacity_DisasterPipeline
## Table of Contents

1. [Project description](#description)

2. [File descriptions](#files)

3. [Project steps](#steps)
   
   i. [Packages](##pack)
   
   ii.[Program scripts](##pro)
   
   iii.[Deployment](###deploy)

4. [Licensing, Authors, and Acknowledgements](#terms)

<a name = "description"></a>

## Project description
The current project is part of my Data Scientist Nanodegree of the Udacity. The goal of the project is to create a machine learning pipeline to categorize different disaster events, so that the messages can be sent to an appropriate disaster relief agency. The project will finally build a web app that a new message can be input and then get classification results in several categories. 

Overall, the project includes an ETL Pipeline, a Machine learning pipeline, and a web app.

<a name = "files"></a>

## File description

The following files were included in the current project：

- The jupyter files for ETL and ML pipelines (i.e. ETL Pipeline Preparation & ML Pipeline Preparation)
- The data folder: includes the raw message and category data files (.csv files), the python file of the ETL pipeline (process_daya.py)
- The models folder: includes the python file of the ML pipeline (train_classifier.py)
- The app folder: includes the deployment script (run.py) and template

<a name = "steps"></a>

## Project steps

<a name = "pack"></a>

### Packages

- Python 3.5+
- Jupyter notebook
- Natural language process libraries: nltk
- SQLite database library: SQLalchemy
- Web app: Flask, Plotly
- CSS, HTML

<a name = "pro"></a>

### Program scripts

- ETL pipeline: Load data file. Data wrangling, clean data, re-name the categories dataframe, merge message and categories into one dataframe, save the data in a SQLite database.
- ML Pipeline: Load data from SQLite database; split dataset into training and test sets;builds a text processing and machine learning pipeline;Trains and tunes a model using GridSearchCV;Outputs results on the test set;Exports the final model as a pickle file.
- Flask web App: The main function of the web app was provided by Udacity already. Just need modify the file paths for database and models needed. 

<a name = "deploy"></a>

### Deployment

- In the data directory, run: `python process_data.py disaster_messages.csv disaster_categories.csv DisasterResponse.db`
- In the models directory, run: `python train_classifier.py ../data/DisasterResponse.db classifier.pkl`
- In the app diretory, run python `run.py`
- Check the web visualization in http://0.0.0.0:3001/

<a name = "terms"></a>

## Licensing, Authors, and Acknowledgements

The project is finished by [Zhuo Fang](https://github.com/Lydiafz). Partial of the codes was provided by Udacity.

I would like to thank Udacity for providing the dataset and the project supports.



