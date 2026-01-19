import os
import pandas as pd
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI

# Lets get the api key from the enviornment
gemini_api_key = os.getenv('GOOGLE_API_KEY1')

# Lets configure the model 

model = ChatGoogleGenerativeAI(
    model = 'gemini-2.5-flash-lite',
    api_key = gemini_api_key,
    temperature = 0.7
)

# Design the UI of application 

st.title(':orange[HeathifyMe] :blue[Your Personal Health Assistant]')
st.markdown('''
This application will assist you to get better and customized Health advice. You can ask you health related issues and get 
the personalized guidance.''')

st.write('''
Follow these steps:
* Enter your details in sidebar
* Rate your activity and fitness on the scale of 0-5
* submit your details.
* Ask your question on the main page.
* Click generate and relax''')

# Design the sidebar for all the user parameters
st.sidebar.header(':red[Enter Your Details]')
name = st.sidebar.text_input('Enter your Name')
gender = st.sidebar.selectbox('Select your Gender', ['select','M','F','other'])
age = st.sidebar.text_input('Enter your Age')
Weight = st.sidebar.text_input('Enter your Weight in Kgs')
Height = st.sidebar.text_input('Enter your Height in Cms')
BMI = pd.to_numeric(Weight)/((pd.to_numeric(Height)/100)**2)
active = st.sidebar.slider('Rate your activity (0-5)',0,5,step=1)
fitness = st.sidebar.slider('Rate your fitness (0-5)', 0,5,step=1)
if st.sidebar.button('Submit'):
    st.sidebar.write(f'{name}, your BMI is {round(BMI,2)} kg/m^2')

# Lets use the Gemini Model to generate the report 

user_input = st.text_input('Ask me your Question.')
prompt = f'''
<Role> You are an expert in health and wellness and has 10+ years experience in Guiding peoples.
<Goal> Generate the customized report addressing the problem the user has asked. Here is the question that user has asked: {user_input}.
<Context> Here are the details of the user has provided.
name = {name}
age={age}
gender={gender}
weight={Weight}
height={Height}
bmi={BMI}
activity rating (0-5)={active}
fitness rating (0-5)={fitness}

<Format> Following should be outline of the report, in the sequence provided.
* Start with the 2-3 line of comment on the details that user has provided.
* Explain what the real problem could be on the basis of input the user has provided.
* Suggest the possible reasons for th problem.
* What are the possible solutions.
* Mention the doctor from which specialization can be visited if required
* Mention any change in the diet which is required
* In last create a final summary of all the things that has been discussed in the report.


<Instructions>
* Use bullet points where ever possible.
* Create tables to represent any data where ever possible
* Strictly do not advice any medicine.'''

if st.button('Generate Report'):
    response = model.invoke(prompt)
    st.write(response.content)
