import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji
import os

def remove_stop_words(message):

    '''''''''''''''
    args: string 
    return : string with no stop_words

    '''''''''''''''
    
    f1 = open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "hindi_stopwords.txt"),'r',encoding="utf8")
    stop1 = f1.read()
    stop1 = stop1.split()
    f2 = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'hinglish+english_stop_words.txt'),'r',encoding="utf8")
    stop2 = f2.read()
    stop2 = stop2.split()

    words = []
    for word in message.lower().split():
        if word not in stop1:
            if word not in stop2:
                if len(word) > 3:
                    words.append(word)

    return " ".join(words)

def word_cloud(opted_user,df):
    '''''''''''''''
    args: user on which analysis is to be done or the whole group ,,,, the dataframe 
    return : word cloud of the messages sent

    '''''''''''''''
    if opted_user != 'Overall Analysis':
        df = df[df['users']==opted_user]

    df = df[df['messages']!='<Media omitted>\n']
    df = df[df['messages']!='This message was deleted\n']        

    ch_df = df.copy()
    ch_df['messages'] = df['messages'].apply(remove_stop_words)
    if len(ch_df['messages'])==0:
        ch_df['messages'] = ['Not_so_active']
    wc = WordCloud(height=1000, width=1400, min_font_size=12, background_color = 'pink')
    msg_wc = wc.generate(ch_df['messages'].str.cat(sep=" "))
    
    return msg_wc


def stats(opted_user,df):
    '''''''''''''''
    args: user on which analysis is to be done or the whole group ,,,, the dataframe 
    return : stats including msg count, word count , count of media shared , number of url shared

    '''''''''''''''
    if opted_user != 'Overall Analysis':
        df = df[df['users']==opted_user]

    msg_count = df.shape[0]
    words = []
    for message in df['messages']:
        words.extend(message.split())

    media_count = df[df['messages']=='<Media omitted>\n'].shape[0]

    url_ext = URLExtract()
    urls = []
    for message in df['messages']:
        urls.extend(url_ext.find_urls(message))

    return {'msg_count':msg_count, 'word_count':len(words), 'media_count':media_count, 'url_count':len(urls)}

def top_charts(df):

    '''''''''''''''
    args: dataframe 
    return : stats including msg count, word count , count of media shared , number of url shared

    '''''''''''''''

    active_data = round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'Users','users':'Percentage'})
    active_users = df['users'].value_counts().head()
            
    return active_data , active_users


def common_words(opted_user, df):
    '''''''''''''''
    args: selected user, dataframe 
    return : 30 Most frequently used words

    '''''''''''''''
    if opted_user != 'Overall Analysis':
        df = df[df['users']==opted_user]

    mod_df = df[df['messages']!='<Media omitted>\n']
    mod_df = mod_df[mod_df['messages']!='This message was deleted\n']
    ch_df = mod_df.copy()
    ch_df['messages'] = mod_df['messages'].apply(remove_stop_words)

    words = []
    for message in ch_df['messages']:
        for word in message.lower().split():
            if word[0] not in emoji.UNICODE_EMOJI['en']:
                words.append(word)
    if len(words)==0:
        words.append('No text message')
    new_df = pd.DataFrame(Counter(words).most_common(10))
    
    new_df.columns=['Word','Frequency']
    return new_df

def common_emoji(opted_user,df):

    '''''''''''''''
    args: selected user, dataframe 
    return : Most common Emojis

    '''''''''''''''

    if opted_user != 'Overall Analysis':
        df = df[df['users']==opted_user]
    
    emojis = []
    for message in df['messages']:
        emojis.extend([e for e in message if e in emoji.UNICODE_EMOJI['en']])

    if len(emojis)==0:
        emojis.append('No emojis')

    new_df = pd.DataFrame(Counter(emojis).most_common(10))
    new_df.columns=['Emoji','Frequency']
    
    return new_df

def m_timeline(opted_user,df):
    '''''''''''''''
    args: selected user, dataframe 
    return : monthly activity df

    '''''''''''''''

    if opted_user != 'Overall Analysis':
        df = df[df['users'] == opted_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def d_timeline(opted_user,df):
    '''''''''''''''
    args: selected user, dataframe 
    return : daily activity df 

    '''''''''''''''
    if opted_user != 'Overall Analysis':
        df = df[df['users'] == opted_user]

    timeline = df.groupby(['the_date']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['the_date'][i])

    timeline['time'] = time

    return timeline    
    
def weekly_activity(opted_user,df):
    '''''''''''''''
    args: selected user, dataframe 
    return : weekly sent messages

    '''''''''''''''

    if opted_user != 'Overall Analysis':
        df = df[df['users'] == opted_user]

    df['day_name'] = df['date'].dt.day_name()
    counts = df['day_name'].value_counts()
    
    return counts

if __name__ == '__main__':
    print('ok')
    