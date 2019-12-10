## Post-Here Subreddit Recommender

### Overview:
The scope of this application is to take a potential reddit post from a user and provide a list of subreddits that are relevant to said post. This application will use Machine Learning and Natural Language Processing (NLP) techniques to provide the best possible results to our users.

### Project Architecture:
Our team of full-stack web developers created an application on React that interfaces with our Data Science API. The Data Science API accepts text from the React app and then sends the text to our model. The model first vectorizes the text input using a TFIDF Vectorizer that we fit to our Subreddit data. The model then computes the cosine similarity between our vectorized text input and our vectorized training data. Finally, our model returns the most relevant Subreddit ID’s based on the computation.

Once our application has the relevant Subreddit ID’s, it queries more subreddit information from our NoSQL Database and returns the Subreddit name, link, title, description, number of subscribers, active subscribers, and the subreddit score to the React app.

![alt text](https://github.com/BuildWeek-PostHere-Subreddit/MachineLearning/blob/master/Pics/api_logicr.png "Architecture")

## Collecting Subreddit Data:

### Gathering subreddit names
We found a [site the keeps track of the 5000 top subreddits](http://redditlist.com/sfw) so we scraped all the subreddit names and saved them in a CSV file.

~~~
from bs4 import BeautifulSoup as bs
import requests
import lxml
import pandas as pd
import numpy as np

def get_text(num):
    get = requests.get(f'http://redditlist.com/all?page={num}')
    soup = bs(get.content, 'lxml')
    items = soup.find_all('div', class_='listing-item')
    text = [i.find('span',class_='subreddit-url').a.text for i in items]
    return(text)

df = pd.DataFrame([], columns=['names'])

for i in range(41):
    text = get_text(i)
    dfa = pd.DataFrame(text, columns=['names'])
    df = df.append(dfa)
    if i % 5 == 0:
        print(f"Page {i} of 40.")

df = df.drop_duplicates(subset=None, keep='first')

df.to_csv('subreddit_names.csv')
~~~

### Pulling Millions of Posts
We then used the Subreddit names to pull data from the Reddit API. This script pulls 1000 subreddit posts from each Subreddit along with other relevant data and saves it to a Dataframe.

~~~
import pandas as pd
import praw

redd = praw.Reddit(client_id='', client_secret='', username='', password='', user_agent='testagent')

df = pd.read_csv('subreddit_namesn.csv')

def df_range(mindf,maxdf, df):
    req_list = df.values[mindf:maxdf].tolist()
    return(req_list)

names = df_range(3001, 4990, df)

df = pd.DataFrame([], columns=['name', 'title', 'url', 'banner_url', 'subscribers', 'active_accounts', 'score', 'text'])


counter = 0
for i in names:
    name = i[0]
    sub = redd.subreddit(name)
    title = sub.title
    url = sub.url
    banner_url = sub.banner_img
    subscribers = sub.subscribers
    active_accounts = sub.accounts_active
    score = 0
    data = sub.hot(limit=1000)
    text = ''
    for words in data:
        text = text + words.title
        score = score + words.score
    dfa = pd.DataFrame([[name, title, url, banner_url, subscribers, active_accounts, score, text]], columns=['name', 'title', 'url', 'banner_url', 'subscribers', 'active_accounts', 'score', 'text'])
    df = df.append(dfa)
    if counter % 20 == 0:
        print(f'Call {counter} of 4990')
    counter = counter + 1
    df.to_csv('all_data2.csv')
~~~


## Model Exploration:

We explored dozens of different models and techniques that would allow us to maintain a relatively small model while producing good results. We had to cut back on the size of our training data due to hosting limitations so we decided to use a Tfidf Vectorizer to transform our data and then compare the Cosine Similarities. 

### Handling the Data:
![alt text](https://github.com/BuildWeek-PostHere-Subreddit/MachineLearning/blob/master/Pics/handledata.png "handle data")

### Fitting the Model:
![alt text](https://github.com/BuildWeek-PostHere-Subreddit/MachineLearning/blob/master/Pics/fitting.png "fitting")

### Transforming the Training Data:
![alt text](https://github.com/BuildWeek-PostHere-Subreddit/MachineLearning/blob/master/Pics/transformtrain.png "transform training")

### Vectorizing the Data:
![alt text](https://github.com/BuildWeek-PostHere-Subreddit/MachineLearning/blob/master/Pics/vectorizetrain.png "vectorize train")

### Transforming Test Data:
![alt text](https://github.com/BuildWeek-PostHere-Subreddit/MachineLearning/blob/master/Pics/transtest.png "transform test")

### Computing the Cosines:
![alt text](https://github.com/BuildWeek-PostHere-Subreddit/MachineLearning/blob/master/Pics/cosines.png "compute cosines")

### Checking the Results:
![alt text](https://github.com/BuildWeek-PostHere-Subreddit/MachineLearning/blob/master/Pics/checkingres.png "checking results")

### Export the Model:
![alt text](https://github.com/BuildWeek-PostHere-Subreddit/MachineLearning/blob/master/Pics/export.png "export model")
