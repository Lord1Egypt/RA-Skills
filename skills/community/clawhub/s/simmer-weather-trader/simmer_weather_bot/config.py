import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

SIMMER_API_KEY = os.environ["SIMMER_API_KEY"]
SIMMER_BASE_URL = os.environ.get("SIMMER_BASE_URL", "https://api.simmer.markets")
SIMMER_VENUE = os.environ.get("SIMMER_VENUE", "sim")

NVIDIA_API_KEY = os.environ["NVIDIA_API_KEY"]
FOURCASTNET_URL = "https://climate.api.nvidia.com/v1/nvidia/fourcastnet"
FOURCASTNET_POLL_URL = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/status"
FOURCASTNET_POLL_SECONDS = 5

NOAA_API_BASE = os.environ.get("NOAA_API_BASE", "https://api.weather.gov")
OPEN_METEO_API = os.environ.get("OPEN_METEO_API", "https://api.open-meteo.com/v1/forecast")
WUNDERGROUND_BASE = os.environ.get("WUNDERGROUND_BASE", "https://www.wunderground.com/forecast/us")

TRADE_AMOUNT = float(os.environ.get("TRADE_AMOUNT", "10.0"))
CONFIDENCE_THRESHOLD = int(os.environ.get("CONFIDENCE_THRESHOLD", "100"))

NOAA_USER_AGENT = "SimmerWeatherBot/1.0 (bot@simmermarkets.io)"

HTTP_TIMEOUT = 30.0
PLAYWRIGHT_TIMEOUT = 20000
FOURCASTNET_MAX_POLLS = 40
