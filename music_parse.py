from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import WebDriverException
import time
import csv
import traceback
EC.pre

def get_songs_count(driver):
    """Getting number of songs in this playlist"""
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    last_songs_id = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "d-track__id")))
    number_of_songs = int(last_songs_id[-1].text)
    driver.execute_script("window.scrollTo(0, 0-document.body.scrollHeight);")
    return number_of_songs


def get_my_playlist(driver, songs_count):
    """Getting playlist"""
    my_playlist = []
    try:
        while len(my_playlist) != songs_count:
            song_id = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "d-track__id")))
            title = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "d-track__name")))
            artist = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "d-track__artists")))
            song_duration = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "span.typo-track.deco-typo-secondary")))
            print(len(song_id), len(title), len(artist), len(song_duration))
            for i in range(len(song_id)):
                if len(my_playlist) == int(song_id[i].text)-1:
                    my_playlist.append([artist[i].text, title[i].text, song_duration[i].text])
                    print(song_id[i].text, my_playlist[int(song_id[i].text)-1])
            driver.execute_script("window.scrollBy(0, 5000);")
        return my_playlist
    except Exception:
        print("Ошибка:", traceback.format_exc())


def save_in_csv(path, playlist):
    with open(path, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['song_id,artist,title,duration'])
        for i in range(len(playlist)):
            if playlist[i][0].find("\n") != -1:
                data0 = playlist[i][0][:playlist[i][0].index("\n")]
                writer.writerow([i+1, data0, playlist[i][1], playlist[i][2]])
            else:
                writer.writerow([i+1, playlist[i][0], playlist[i][1], playlist[i][2]])

if __name__ == '__main__':
    try:
        begintime = time.time()
        driver = webdriver.Firefox()
        URL = "https://music.yandex.ru/users/alexandriyskiy21/playlists/3"
        driver.get(URL)
        songs_count = get_songs_count(driver)
        my_playlist = get_my_playlist(driver, songs_count)
        save_in_csv("playlist1.csv", my_playlist)
        print("Прошло "+str(time.time() - begintime)+" секунд")
        driver.close()
    except WebDriverException:
        print("Ошибка:", traceback.format_exc())







