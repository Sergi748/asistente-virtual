import os
import wave
import pygame
import pyaudio
import keyboard


def get_audio(path_save, name_audio, chunk=1024, format=pyaudio.paInt16, channels=1, rate=44100):
    p = pyaudio.PyAudio()
    stream = p.open(format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk)

    print('Presiona la tecla esc para detener la grabación...')
    frames = []

    pygame.init()

    try:
        while True:
            if keyboard.is_pressed(hotkey='esc'):
                break

            data = stream.read(chunk)
            frames.append(data)

    except KeyboardInterrupt:
        pass

    print("Grabación detenida")
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(os.path.join(path_save, f'{name_audio}.wav'), 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(format))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()
