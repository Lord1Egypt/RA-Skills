import json
import time
import hashlib
import requests
from pathlib import Path
from typing import Optional, Tuple

API_TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token"


class TokenManager:
    def __init__(self, app_id: str, app_secret: str):
        self.app_id = app_id
        self.app_secret = app_secret
        self.cache_dir = Path(__file__).parent.parent.parent / ".cache"
        app_id_hash = hashlib.md5(app_id.encode()).hexdigest()[:8]
        self.cache_file = self.cache_dir / f"access_token_{app_id_hash}.json"
        self._token: Optional[str] = None
        self._expires_at: float = 0
    
    def get_token(self, force_refresh: bool = False) -> str:
        now = time.time()
        
        if not force_refresh and self._token and self._expires_at > now + 300:
            return self._token
        
        if not force_refresh and self._load_from_cache():
            return self._token
        
        token, expires_in = self._request_token()
        
        self._token = token
        self._expires_at = now + expires_in
        self._save_to_cache()
        
        return token
    
    def _request_token(self) -> Tuple[str, int]:
        resp = requests.get(
            API_TOKEN_URL,
            params={
                "grant_type": "client_credential",
                "appid": self.app_id,
                "secret": self.app_secret
            },
            timeout=30
        )
        data = resp.json()
        if "access_token" not in data:
            raise WeChatAPIError(f"获取token失败: {data}")
        return data["access_token"], data.get("expires_in", 7200)
    
    def _load_from_cache(self) -> bool:
        if not self.cache_file.exists():
            return False
        try:
            with open(self.cache_file, "r", encoding="utf-8") as f:
                cache = json.load(f)
            if cache.get("expires_at", 0) > time.time() + 300:
                self._token = cache["access_token"]
                self._expires_at = cache["expires_at"]
                return True
        except Exception:
            pass
        return False
    
    def _save_to_cache(self):
        self.cache_dir.mkdir(exist_ok=True)
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump({
                "access_token": self._token,
                "expires_at": self._expires_at
            }, f, ensure_ascii=False)


class WeChatAPIError(Exception):
    pass
