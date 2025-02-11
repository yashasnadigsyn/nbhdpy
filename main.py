import mpv, os
from rich.panel import Panel
from rich import print as pprint
from parse import get_song_info
import random
import tty
import sys
import termios
import select
import time

def is_data(stream):
    return select.select([stream], [], [], 0) == ([stream], [], [])

orig_settings = termios.tcgetattr(sys.stdin)

try:
    tty.setcbreak(sys.stdin)

    clear  = lambda: os.system('clear')
    clear()
    pprint(Panel.fit("loading..."))
    player = mpv.MPV(ytdl=True, vid=False)
    player.volume = 50

    with open("songs.txt", "r") as f:
        songs_list = [line.strip() for line in f]

    if not songs_list:
        print("Error: songs.txt is empty!")
        sys.exit(1)

    while True:
        song_url = random.choice(songs_list)
        try:
            song_info = get_song_info(song_url)
            clear()
            print_text = f"Title: {song_info['title']} \nDuration: {song_info['duration']} \nViews: {song_info['views']}"
            pprint(Panel.fit(print_text))
        except Exception as e:
            print(f"Error getting song info: {e}")
            continue

        player.play(song_url)

        while True:
            time.sleep(0.1)
            if is_data(sys.stdin):
                x = sys.stdin.read(1)

                if x == 'q':
                        player.stop()
                        sys.exit(0)
                elif x == 'p':
                        player.pause = not player.pause
                elif x == 's':
                        player.stop()
                        clear()
                        pprint(Panel.fit("loading...."))
                        break

            if player.idle_active:
                break

        player.stop()

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
    print("Exiting.")
