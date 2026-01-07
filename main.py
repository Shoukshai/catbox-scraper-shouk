import os
import sys
import time
import random
import string
import threading
import requests
from concurrent.futures import ThreadPoolExecutor

url = "https://files.catbox.moe/"

FILE_EXTENSIONS = [
    ".png",
    ".gif",
    ".jpg",
    ".jpeg",
    ".webm",
    ".webp",
    ".mkv",
    ".mov",
    ".mp4",
]

THREADS = 32 # Shouldn't go very high or rate limite
UPDATE_RATE = 0.25  # Rate in seconds

urls_checked = 0
hits_found = 0
files_saved = 0
start_time = time.time()

running = True
lock = threading.Lock()

def rdm_str(len_chars: int = 6) -> str:
    charset = string.ascii_lowercase + string.digits
    return "".join(random.choice(charset) for _ in range(len_chars))

def save(folder: str, filename: str, data: bytes) -> bool:
    try:
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, filename)
        with open(path, "wb") as f:
            f.write(data)
        return True
    except:
        return False

def hits_log(url: str) -> None:
    with open("hits.log", "a", encoding="utf-8") as f:
        f.write(url + "\n")

def timer(seconds: int) -> str:
    hours, rem = divmod(seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def dashboard() -> None:
    with lock:
        elapsed = int(time.time() - start_time)
        local_urls_checked = urls_checked
        local_hits_found = hits_found
        local_files_saved = files_saved

    per_sec = local_urls_checked // elapsed if elapsed > 0 else 0

    sys.stdout.write("\033[H")

    print("┌────────────────────────────────────────┐")
    print("│              CATBOX SCRAPER            │")
    print("├────────────────────────────────────────┤")
    print("│                BY DOOT                 │")
    print("│            UPDATED VERSION             │")
    print("└────────────────────────────────────────┘")

    print("┌────────────────────────────────────────┐")
    print("│               MAIN STATS               │")
    print("├────────────────────────────────────────┤")
    print(f"│ TIME ELAPSED : {timer(elapsed):<23} │")
    print(f"│ CHECKS       : {local_urls_checked:<23} │")
    print(f"│ HITS         : {local_hits_found:<23} │")
    print(f"│ SAVED        : {local_files_saved:<23} │")
    print(f"│ PER SECOND   : {per_sec:<23} │")
    print("└────────────────────────────────────────┘")

def worker(session: requests.Session) -> None:
    global urls_checked, hits_found, files_saved, running

    while running:
        for ext in FILE_EXTENSIONS:
            if not running:
                break

            filename = rdm_str() + ext
            full_url = url + filename

            with lock:
                urls_checked += 1

            try:
                response = session.get(full_url, timeout=10)
            except requests.RequestException:
                continue

            if response.status_code == 200:
                hits_log(full_url)

                with lock:
                    hits_found += 1

                folder = ext.lstrip(".")
                success = save(folder, filename, response.content)

                if success:
                    with lock:
                        files_saved += 1

def main() -> None:
    global running

    session = requests.Session()
    session.headers.update({
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 15; SM-S931B Build/AP3A.240905.015.A2; wv) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 "
            "Chrome/127.0.6533.103 Mobile Safari/537.36"
        ),
        "Accept": "*/*",
    })

    os.system("")
    sys.stdout.write("\033[2J")

    last_update = 0

    with ThreadPoolExecutor(max_workers=THREADS) as executor:
        for _ in range(THREADS):
            executor.submit(worker, session)

        try:
            while running:
                now = time.time()
                if now - last_update >= UPDATE_RATE:
                    dashboard()
                    last_update = now
                time.sleep(0.01)
        except KeyboardInterrupt:
            running = False
            time.sleep(0.2)
            sys.stdout.write("\033[?25h")
            print("\nStopped.")

if __name__ == "__main__":
    sys.stdout.write("\033[?25l")
    try:
        main()
    finally:
        sys.stdout.write("\033[?25h")
        sys.stdout.flush()
