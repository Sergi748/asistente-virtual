import os
import requests
from PIL import Image
from openai import OpenAI
from subprocess import call


class SearchGoogle:

    @staticmethod
    def open_website(website):
        if 'www.' not in website:
            website = f'wwww.{website}'
        call("C:/Program Files/Google/Chrome/Application/chrome.exe " + website)

    @staticmethod
    def search_chrome(search):
        search = "" if search is None else search
        google_page = f"https://www.google.com/search?q={search.replace(' ', '+')}"
        call("C:/Program Files/Google/Chrome/Application/chrome.exe " + google_page)


class Weather:

    def __init__(self):
        self.api_weather = 'xxxxxxxxxxxxxx'

    def get_weather(self, city):

        response = requests.get(f"http://api.weatherapi.com/v1/current.json?key={self.api_weather}&q={city}&aqi=no")
        if response.status_code:
            temp = response.json()["current"]["temp_c"]
            humidity = response.json()["current"]["humidity"]
            txt = f'La temperatura actual en {city} es de {temp}ºC, con una humedad del {humidity}%'
        else:
            txt = 'No se ha podido obtener la información de la api del tiempo.'

        return txt


class ImagesGenerator:

    @staticmethod
    def create_images(prompt):
        client = OpenAI()
        resp_img = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            quality='standard',
            size="1024x1024",
            n=1
        )

        message_img = f'Generando la imagen "{prompt}"'
        img_url = resp_img.data[0].url
        img = Image.open(requests.get(img_url, stream=True).raw)

        path_save = "C:/Users/47796528k/Documents/SERGIO/asistente-virtual/images"
        img.save(os.path.join(path_save, f'photo.jpg'), 'JPEG')
        return message_img, img


class FunctionsCalls:

    def __init__(self, message, function_name, arg):
        self.message = message
        self.function_name = function_name
        self.arg = arg

    def process_functions(self):

        message_complete = self.message

        if self.function_name == 'search_chrome':
            SearchGoogle().search_chrome(search=self.arg['search'])
            message_search = f"Búsqueda en google de {self.arg['search']}"
            message_complete.append({"role": "assistant", "content": message_search})
            return message_complete, message_search
        elif self.function_name == 'open_website':
            SearchGoogle().open_website(website=self.arg['website'])
            message_website = f"Abierta página web {self.arg['website']}"
            message_complete.append({"role": "assistant", "content": message_website})
            return message_complete, message_website
        elif self.function_name == 'get_weather':
            message_weather = Weather().get_weather(city=self.arg['city'])
            message_complete.append({"role": "assistant", "content": message_weather})
            return message_complete, message_weather
        elif self.function_name == 'create_images':
            message_img, img = ImagesGenerator().create_images(prompt=self.arg['prompt'])
            message_complete.append({"role": "assistant", "content": message_img})
            return message_complete, message_img
