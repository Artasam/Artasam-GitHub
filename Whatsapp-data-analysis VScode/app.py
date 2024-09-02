import streamlit as st
from preprocess import preprocess
import helping_functions
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

st.sidebar.title('Whatsapp-Data-Analyzer')
uploaded_files = st.sidebar.file_uploader(
    "Choose a file",accept_multiple_files=False
)
if uploaded_files is not None:
    bytes_data = uploaded_files.read()
    data = bytes_data.decode("utf-8")
    data = preprocess(data)
    # st.write(data)
    # st.dataframe(data)
    # st.text(data.shape)

    users = data['users'].unique().tolist()
    users.remove('group_notification')
    users.sort()
    users.insert(0,"Overall")
    option = st.sidebar.selectbox(
    "Show Analysis wrt",
     users)
    # stats of Data
    if st.sidebar.button("Show_Analysis"):
        TM,TW,TMS,TL = helping_functions.fetch_stats(option,data)
        st.title("Statistics")
        col1, col2, col3, col4 = st.columns([5,4,5,4])

        with col1:
            st.subheader("Total Messages")
            st.subheader(TM)

        with col2:
            st.subheader("Total Words")
            st.subheader(TW)    
        
        with col3:
            st.subheader("Media Shared")
            st.subheader(TMS)

        with col4:
            st.subheader("Links Shared")
            st.subheader(TL)


        # Monthly_Timeline
        df_MT = helping_functions.monthly_timeline(option,data)
        st.title('Monthly_Timeline')
        fig, ax = plt.subplots()
        ax.plot(df_MT['time'],df_MT['messages'],color='purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily_timeline
        df_dT = helping_functions.daily_timeline(option,data)
        st.title('Daily_Timeline')
        fig, ax = plt.subplots()
        ax.plot(df_dT['only_dates'],df_dT['messages'],color='darkgreen')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        # active_users on day
        map_week = helping_functions.week_activity_map(option,data)
        map_month = helping_functions.month_activity_map(option,data)
        st.title('Activity_map')
        fig, ax = plt.subplots()
        
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy week-day")
            fig, ax = plt.subplots()
            ax.bar(map_week.index,map_week.values,color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            fig, ax = plt.subplots()
            ax.bar(map_month.index,map_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
    
        # Activity heatmap
        st.title("Weekly Activity Map")
        user_heatmap = helping_functions.activity_heatmap(option,data)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)


        # Finding busiest person in group    
        if option == 'Overall':
            st.title("Most Busy_users")
            x,d = helping_functions.Busy_users(data)
            fig, ax = plt.subplots()

            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color= 'green')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
            with col2:
                # d = pd.DataFrame({'Names':x.index,'Messages_Count':x.values,'Percentage':(x.values/data.shape[0])*100})
                st.dataframe(d) 


        #WordCloud
        st.title("Word_Cloud")
        try:
            df_wc = helping_functions.Generate_WordCloud(option,data)
            fig, ax = plt.subplots()
            ax.imshow(df_wc) 
            st.pyplot(fig) 
        except Exception as e:
            print(e)    

        # Most Common Words
        try:  
            st.title("Most_Common_Words")
            df_MCW =helping_functions.Most_common_words(option,data)
            fig, ax = plt.subplots()
            
            ax.barh(df_MCW['Words'],df_MCW['Count_Frequency'])
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
        except Exception as e:
            st.error("No Words for showing Chart!") 


        # Emojis Count
        st.title('Emojis Count')
        df_EC = helping_functions.Emoji_Count(option,data)
        fig, ax = plt.subplots()
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(df_EC)

        with col2:
            try:
               ax.pie(df_EC[1].head(),labels=df_EC[0].head(),autopct='%0.2f')
               st.pyplot(fig)
            except Exception as e:
                st.error(f"No values for showing Pie Chart!")
        
            