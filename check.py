import requests, json, os, sys
from urllib.parse import urljoin
from bs4 import BeautifulSoup

URL = "https://cfc.scenecinemas.com/home"
TOKEN = os.environ["TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
FILE = "seen.json"

# GUESS: headers were cut off in the screenshot
html = requests.get(URL, timeout=20, headers={"User-Agent": "Mozilla/5.0"}).text
soup = BeautifulSoup(html, "html.parser")

movies = {}
# GUESS: the selector was cut off after '/movie-'. Check the site's real movie link pattern.
for a in soup.select('a[href*="/movie-"]'):
    name = a.get("title") or a.get_text(strip=True)
    if name:
        movies[a["href"]] = name

print("لقيت", len(movies), "فيلم")  # "Found N movies"
if not movies:
    sys.exit("مفيش أفلام اتقرأت")  # "No movies were read"

# GUESS: the end of this line was cut off
seen = set(json.load(open(FILE))) if os.path.exists(FILE) else None

# On the very first run (seen is None) it only saves the list and sends nothing
if seen is not None:
    for href in movies.keys() - seen:
        requests.get(
            f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            # GUESS: message text was cut off
            params={"chat_id": CHAT_ID,
                    "text": f"New movie: {movies[href]}\n{urljoin(URL, href)}"},
        )

json.dump(sorted((seen or set()) | set(movies.keys())), open(FILE, "w"))
