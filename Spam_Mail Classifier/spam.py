import streamlit as st
import pickle
import nltk
from nltk.corpus import stopwords
import string
from nltk.stem.porter import PorterStemmer

tfidf = pickle.load(open('Vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

ps = PorterStemmer()

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)
    c=[]
    for i in text:
        if i.isalnum():
            c.append(i)
    text = c[:]
    c.clear()
    
    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            c.append(i)
    
    text = c[:]
    c.clear()
    
    for i in text:
        c.append(ps.stem(i))
    
    
    return " ".join(c)

st.title("SMS Spam Prediction")

input_sms = st.text_area("Enter Message")


if st.button("predict"):
     #Transform sms
    Transformed_Sms = transform_text(input_sms)

#Vectorize
    vector = tfidf.transform([Transformed_Sms])

#Predict
    result = model.predict(vector.toarray())[0]
#Display    
    if result == 1:
       st.header("Spam")
    else:
       st.header('Not Spam')

    

