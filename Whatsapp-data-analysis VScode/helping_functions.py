
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
import matplotlib as plt
from matplotlib import font_manager 

extractor = URLExtract()

# Fetching_Stats
def fetch_stats(option,data):
    if option != 'Overall':
        data = data[data['users']== option]
    # Total Number of Messages
    num_messages = data.shape[0]
    
    # Total Number of Words in Messages
    words = []
    for message in data['messages']:
        words.extend(message.split())
    
    # Total Number of Media Files in Messages
    media = data[data['messages'] == '<Media omitted>\n']  

    # Total links in messages
    links = []
    for message in data['messages']:
        links.extend(extractor.find_urls(message))  

    return num_messages,len(words),len(media),len(links)

# Busy_Users
def Busy_users(data):
    x = data['users'].value_counts().head()
    y = round((data['users'].value_counts()/data.shape[0])*100,2).reset_index().rename(columns={'users':'Name','count':'Percent'})
    return x,y


# Word_Cloud
def Generate_WordCloud(option,data):

    if option != 'Overall':
        data = data[data['users']== option]


    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate(data['messages'].str.cat(sep=" ")) 

    return df_wc

# Most_Common_Words
def Most_common_words(option,data):
    f = open('stop_hinglish.txt','r')
    stop_words = f.read()


    if option != 'Overall':
        data = data[data['users']== option]

    data = data[data['users'] != 'group_notification']
    data = data[data['messages'] != '<Media omitted>\n']
    data = data[data['messages'] != 'Waiting for this message\n']
    data = data[data['messages'] != '<this edited>\n']

    
    words = []
    for message in data['messages']:
        for word in message.lower().split():
            if word.isalpha():
                if word not in stop_words:
                    words.append(word)

    df_Cw = pd.DataFrame(Counter(words).most_common(20)).rename(columns ={0:'Words',1:'Count_Frequency'})

    return df_Cw

# Emoji extract
def Emoji_Count(option,data):
    if option != 'Overall':
        data = data[data['users']== option]


    emojis = []
    for message in data['messages']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA]) 

    a = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return a    

def monthly_timeline(option,data):
    if option != 'Overall':
        data = data[data['users']== option]

    data['num_month'] = data['date'].dt.month
    timeline = data.groupby(['year','num_month','month']).count()['messages'].reset_index()
    time = []
    for i in range(len(timeline)):
        time.append(timeline['month'][i]+ "-" +str(timeline['year'][i]))  

    timeline['time'] = time

    return timeline      

def daily_timeline(option,data):
    if option != 'Overall':
        data = data[data['users']== option]

    daily_timeline = data.groupby('only_dates').count()['messages'].reset_index() 

    return daily_timeline  

def week_activity_map(option,data):
    if option != 'Overall':
        data = data[data['users']== option]
    
    z = data['weekday_name'].value_counts()


    return z  

def month_activity_map(option,data):
    if option != 'Overall':
        data = data[data['users']== option]
    
    z = data['month'].value_counts()


    return z  

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    user_heatmap = df.pivot_table(index='weekday_name', columns='period', values='messages', aggfunc='count').fillna(0)

    return user_heatmap