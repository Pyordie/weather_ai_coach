import streamlit as st
from Cli import get_weather, generate_email, send_email
from openai import OpenAI


st.title("Weather AI Coach")
st.write("with few clicks, get your daily update on the weather !")

name = st.text_input("Enter your Name:")
email = st.text_input("Enter your Email:")
city = st.text_input("Enter your city:")

check = st.button("Get Updates")

if check:
    try:
        weather_data = get_weather(city)

        client = OpenAI(
            api_key="",                 #INSERT YOUR API_KEY FROM OPEN AI
        )

        email_content = generate_email(weather_data, name)

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": email_content,
                }
            ],
            model="gpt-3.5-turbo",
        )

        send_email(email, chat_completion.choices[0].message.content.encode("utf-8"))
        st.warning("Email sent successfully !")
    except KeyError:
        st.warning("Please make sure to fill all your information !")