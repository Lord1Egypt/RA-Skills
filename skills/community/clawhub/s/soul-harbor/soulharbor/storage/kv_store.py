"""
KV storage interface
Simple KV storage implementation using local file system
"""

import json
import pickle
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

from ..config import KV_STORE_PATH


class KVStore:
    """Simple key-value store implementation"""
    
    def __init__(self, store_path: Path = KV_STORE_PATH):
        self.store_path = Path(store_path)
        self.store_path.mkdir(parents=True, exist_ok=True)
    
    def _get_file_path(self, key: str) -> Path:
        """Get file path for key"""
        # Use safe file name
        safe_key = key.replace("/", "_").replace("\\", "_")
        return self.store_path / f"{safe_key}.json"
    
    def get(self, key: str) -> Optional[Any]:
        """Get value"""
        file_path = self._get_file_path(key)
        if not file_path.exists():
            return None
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading key {key}: {e}")
            return None
    
    def set(self, key: str, value: Any) -> bool:
        """Set value"""
        file_path = self._get_file_path(key)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(value, f, ensure_ascii=False, indent=2, default=str)
            return True
        except Exception as e:
            print(f"Error writing key {key}: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key"""
        file_path = self._get_file_path(key)
        if file_path.exists():
            try:
                file_path.unlink()
                return True
            except Exception as e:
                print(f"Error deleting key {key}: {e}")
                return False
        return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists"""
        return self._get_file_path(key).exists()
    
    def list_keys(self, prefix: str = "") -> list:
        """List all keys (optional prefix filter)"""
        keys = []
        for file_path in self.store_path.glob("*.json"):
            key = file_path.stem.replace("_", "/")
            if prefix == "" or key.startswith(prefix):
                keys.append(key)
        return keys
