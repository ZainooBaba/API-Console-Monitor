import os

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

import sys
import select
from time import sleep, time
import pygame
import requests
from colorama import Fore

HAS_ERROR_INBETWEENS = True

def get_response(url):
    try:
        response = requests.get(url)
        return response.text
    except Exception as e:
        return "Error in response"

def read_url_from_file(filename):
    try:
        with open(filename, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def write_url_to_file(filename, url):
    with open(filename, 'w') as file:
        file.write(url)

def log_change(logfile, message):
    with open(logfile, 'a') as file:
        file.write(f"{message}\n")

def print_api_update(duration, response):
    log_message = f"API took {duration:.2f} seconds to update"
    print(Fore.RED + log_message)
    log_change(log_file, f"{duration:.2f}")
    print(Fore.GREEN + response)

def play_sound(sound_file):
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        sleep(1)

if __name__ == "__main__":

    good_sound_file = "soundFile/good_sound.mp3"
    bad_sound_file = "soundFile/bad_sound.mp3"
    url_file = "api_url.txt"
    log_file = "change_log.txt"
    error_response_file = "Error_Response.txt"

    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
    pygame.mixer.init()

    API_URL = read_url_from_file(url_file)
    if API_URL is None:
        API_URL = "http://localhost:5000/api"

    current_output = None
    last_change_time = time()
    last_check_time = time()

    while True:
        # Check if the user has entered a new URL
        if select.select([sys.stdin], [], [], 0.1)[0]:
            input_line = sys.stdin.readline().strip()
            print(f"URL changed to {input_line}")
            API_URL = input_line
            write_url_to_file(url_file, API_URL)

        # Check if the API has changed
        # if time() - last_check_time > 10:
        if True:
            last_check_time = time()
            response = get_response(API_URL)
            if current_output != response:
                is_compiling = False
                if HAS_ERROR_INBETWEENS:
                    with open("Error_Response.txt", 'r') as file:
                        error_response = file.read()
                        if response.replace('\r\n', '\n') == error_response:
                            # sys.stdout.flush()
                            print(Fore.YELLOW + "API is currently compiling")
                            play_sound(bad_sound_file)
                            is_compiling = True
                if not is_compiling:
                    duration = time() - last_change_time
                    sys.stdout.flush()
                    print_api_update(duration, response)
                    play_sound(good_sound_file)

                current_output = response
                last_change_time = time()

        # sys.stdout.write(f"\rAPI took {time()-last_check_time:.2f} seconds to update")
        # sys.stdout.flush()
        sleep(10)