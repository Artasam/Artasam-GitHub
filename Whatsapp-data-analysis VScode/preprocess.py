import re 
import pandas as pd

def remove_urdu_words(text):
    # Urdu characters range in Unicode: \u0600 to \u06FF
    return re.sub(r'[\u0600-\u06FF]+', '', text)


def preprocess(data):

    # data = data.read()

    data = data.replace('am ','')
    data = data.replace('pm ','')
        
    data = data.replace('AM ','')
    data = data.replace('PM ','')
         

    #regex101.com
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    cleaned_dates = []
    for i in dates:
         cleaned_dates.append(i.replace('\u202f',' '))

    df = pd.DataFrame({'user_message': messages, 'message_date': cleaned_dates})
    # convert message_date type
    # Define the two possible formats
    format1 = '%m/%d/%y, %H:%M - '
    format2 = '%d/%m/%Y, %H:%M - '

    # Function to convert the date format
    def convert_date(date_str):
        try:
            # Try the first format
            return pd.to_datetime(date_str, format=format1)
        except ValueError:
            try:
                # If the first format fails, try the second format
                return pd.to_datetime(date_str, format=format2)
            except ValueError:
                # Handle cases where neither format works
                return pd.NaT  # Not a Time (NaT) represents missing or null date

    # Apply the conversion function to the 'message_date' column
    df['message_date'] = df['message_date'].apply(convert_date)


    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['users'] = users
    df['messages'] = messages
    df.drop(columns='user_message',inplace=True)  


    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()      
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['weekday_name']=df['date'].dt.day_name()
    df['only_dates'] = df['date'].dt.date

    period = []
    for hour in df[['weekday_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    df['messages'] = df['messages'].apply(remove_urdu_words)

    return df

# file = open('WhatsApp Chat with Chala ja bsdk.txt','r',encoding='utf-8')
# print(preprocess(file))