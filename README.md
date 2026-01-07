# Catbox Scraper

An efficient python script for bruteforcing all url(s) and downloading random files from [Catbox](https://catbox.moe), a file-hosting site.

The script takes from file extensions specified inside the main.py, generates random urls and checks to see if they are valid. If they are, it downloads them and stores them in extension-sorted folders.

`https://files.catbox.moe/[a-z0-9]{6}.(extension)` is the format for URL generation.

## Installation and Usage
You will need:
- Python
- Git
```
git clone https://github.com/Shoukshai/catbox-scraper-shouk.git
cd catbox-scraper-shouk
pip install -r requirements.txt
python main.py
```
and the script will handle everything else from there!

Press CTRL+C to stop the script. (Youll have to wait for a bit or force close the terminal)

## Configuration
If you wish to change the extensions the script attempts to check for, simply edit `main.py`'s `FILE_EXTENSIONS` field with the extensions you wish to check for, if you want a list of them: [Click here](https://raw.githubusercontent.com/Shoukshai/catbox-scraper-shouk/refs/heads/main/list_of_extensions.txt)

By default, the script checks for the following: `png, gif, jpg, jpeg, webm, webp, mkv, mov, mp4`

## NOTICE
*I am not responsible for any consequences that come from using this script! Catbox is a file hosting site, and files found on it can be unpredictable. You'll definitely find a LOT of NSFW images as a result of running this; Catbox is used a fair amount by anonymous communities like 4chan.*


