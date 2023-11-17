import os
import time
from chatbot import *
from openai import OpenAI
from record_audio import *
client = OpenAI()


def app(method_used, session, path_audio, path_context, functions):

    try:
        if method_used == 'voz':
            if keyboard.is_pressed(hotkey='right'):
                name_audio = 'prueba_audio'
                get_audio(path_save=path_audio, name_audio=name_audio)
                audio_file = open(os.path.join(path_audio, f"{name_audio}.wav"), "rb")
                transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file)
                prompt = transcript.text
                print(f"\033[92m{prompt}\033[0m")  # Para hacer el print verde

                resp = chat_functions(prompt=prompt, id_session=session,
                                      path_context=path_context, functions_calls=functions, return_resp=True)
                print(resp)
        elif method_used == 'texto':
            print('Envie un mensaje')
            prompt = input()
            resp = chat_functions(prompt=prompt, id_session=session,
                                  path_context=path_context, functions_calls=functions, return_resp=True)
            print(resp)
    except Exception as e:
        print(e)
        return


if __name__ == '__main__':

    path = os.getcwd()
    pathProject = os.path.dirname(os.path.abspath(path))
    pathAudioTmp = os.path.join(pathProject, 'audios', 'tmp')
    pathContext = os.path.join(pathProject, 'contexto')

    id_session = round(time.time())
    with open(os.path.join(path, 'functions_calls.json'), encoding='utf-8') as json_file:
        functions_calls = json.load(json_file)

    print('¿Asistente virtual a través de voz o texto? (respuestas validas: [voz, texto])')
    method = input()
    method = method.lower()

    if method not in ['voz', 'texto']:
        raise ValueError('El método utilizado solo puede ser voz o escrito')

    if method == 'voz':
        print('Presione el botón a la derecha cada vez que quiera enviar un mensaje')

    while True:
        if keyboard.is_pressed(hotkey='esc'):
            break
        app(method_used=method,
            session=id_session,
            path_audio=pathAudioTmp,
            path_context=pathContext,
            functions=functions_calls)

