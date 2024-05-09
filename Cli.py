import requests, smtplib, ssl
from datetime import date
from openai import OpenAI

API_KEY = "" #INSERT YOUR API_KEY FROM OPENWEATHERMAP.ORG

def get_weather(city):
    api_location = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid={API_KEY}"
    response = requests.get(api_location)
    location_data = response.json()

    latitude = float(location_data[1]["lat"])
    longitude = float(location_data[1]['lon'])
    today_date = date.today()
    api_weather = (f"https://api.openweathermap.org/data/3.0/onecall?lat={latitude}&lon={longitude}&units=metric&date={today_date}&exclude=hourly,"
                   f"current,minutely,alerts&appid={API_KEY}")
    weather_response = requests.get(api_weather)
    return weather_response.json()


def generate_email(weather_data, name):
    email_content = ("use the data given to you and write an email describing the weather in a user-friendly way"
                     f" in the different phases of the day and give advice about clothes that should be worn. address the reciever as {name} "
                     f"and the sender as AI weather coach.\n"
                     f"Data: {weather_data}")
    return email_content

def send_email(receiver_email, message):
    host = "smtp.gmail.com"
    port = 465
    context = ssl.create_default_context()
    sender_email = ""  # Insert Email and password for the smtp server
    sender_password = ""

    with smtplib.SMTP_SSL(host,port,context=context) as server :
        server.login(sender_email,sender_password)
        server.sendmail(sender_email,receiver_email,message )

def main():
    print("Welcome to TWA!")

    email = input("Enter your email: ")
    name = input("Enter your name: ")
    city = input("Enter your city: ").capitalize()

    weather_data = get_weather(city)

    client = OpenAI(
        api_key="",
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

    send_email(email,chat_completion.choices[0].message.content.encode("utf-8"))

if __name__ == "__main__":
    main()
