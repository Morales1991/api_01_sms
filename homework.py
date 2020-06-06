import time
import os

import requests
from twilio.rest import Client
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env') 
load_dotenv(dotenv_path) #если убрать path - ругается что потерян один аргумент

vk_token = os.getenv('access_token')
user_id = os.getenv('id')

account_sid = os.getenv('account_sid')
auth_token = os.getenv('auth_token')
number_from = os.getenv('NUMBER_FROM')
number_to = os.getenv('NUMBER_TO')


def get_status(user_id):
    params = {
        'access_token': vk_token,
        'user_ids': user_id,
        'fields': 'online',
        'v': 5.92
    }
    response = requests.post('https://api.vk.com/method/users.get', params=params)
    #response.raise_for_status() # Ругаются тесты'MockResponsePOST' object has no attribute 'raise_for_status'
    status = response.json()['response'][0]['online'] 
    return status


def sms_sender(sms_text):
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=sms_text,
        from_=number_from,
        to=number_to,
    )
    return message.sid


if __name__ == '__main__':
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
        