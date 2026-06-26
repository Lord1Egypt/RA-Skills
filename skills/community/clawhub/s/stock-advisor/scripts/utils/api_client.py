import requests
from typing import Optional, Any
from .config import API_BASE_URL, API_KEY

class APIClient:
    def __init__(self, base_url: str = API_BASE_URL, api_key: Optional[str] = API_KEY):
        self.base_url = base_url.rstrip("/")
        self.headers = {"X-API-Key": api_key} if api_key else {}

    def get_scan(self, symbol: str) -> dict:
        """Call cloud API for deep stock scan."""
        response = requests.get(f"{self.base_url}/api/scan/{symbol}", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_quote(self, symbol: str) -> dict:
        """Call cloud API for real-time quote."""
        response = requests.get(f"{self.base_url}/api/quote/{symbol}", headers=self.headers)
        response.raise_for_status()
        return response.json()

api_client = APIClient()
