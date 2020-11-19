import flickrapi
import requests
import sqlite3
import numpy as np
import cv2
import sys


def create_db_connection(db_name = "name"):
    try:
        conn = sqlite3.connect('db_name.db')
        cursor = conn.cursor()

    except sqlite3.Error as error:
        print("Error while connecting to sqlite", error)

    return conn


def create_photos_table(conn):
    cur = conn.cursor()
    try:
        cur.execute('''CREATE TABLE photos
                (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                photo BLOB NOT NULL, 
                red_per REAL NOT NULL
                )''')
        conn.commit()
    except sqlite3.Error as error:
        print("Error createing Table photos", error)


def insert_photo_into_photos_table(conn, photo, red_per):
    cur = conn.cursor()
    try:
        cur.execute('''INSERT INTO photos (photo, red_per) VALUES (?, ?)
        ''', (photo, red_per))
        conn.commit()
        cur.close()
    except sqlite3.Error as error:
        print("Error saving photo ", error)


def find_most_red(conn):
    cur = conn.cursor()
    val = cur.execute('SELECT MAX(red_per) FROM photos')
    max_val = val.fetchone()[0]
    val = cur.execute(f'SELECT id, photo, red_per FROM photos WHERE red_per == {max_val}').fetchone()
    cur.close()
    return val


def compute_red_percentage(arr):
    s = np.sum(arr, axis = 0)
    s = np.sum(s, axis = 0)
    return s[0]/np.sum(s)

keyword = "recent"
number = 100

if len(sys.argv) == 3:
    keyword = str(sys.argv[1])
    number = int(sys.argv[2])

if number > 500:
    print("Please provide number not larger than 500")
    sys.exit()

Key = "43b82d2714c4bc830d7d7d61149196ce"
Secret = "acd46467429d4233"

flickr = flickrapi.FlickrAPI(Key, Secret, format='parsed-json')
if keyword == "recent":
    photos = flickr.photos.getRecent(perpage=number)
else:
    photos = flickr.photos.search(tags=keyword, per_page=number)

conn = create_db_connection()
create_photos_table(conn)

for i, photo in enumerate(photos['photos']['photo']):
    print(i)
    server_id = photo['server']
    id = photo['id']
    secret = photo['secret']
    url = f"https://live.staticflickr.com/{server_id}/{id}_{secret}.jpg"
    response = requests.get(url)
    file = open("sample_image.jpg", "wb")
    file.write(response.content)
    file.close()
    np_image = cv2.imread("sample_image.jpg")
    red_per = compute_red_percentage(np_image)
    insert_photo_into_photos_table(conn, response.content, red_per)

res = find_most_red(conn)
conn.close()