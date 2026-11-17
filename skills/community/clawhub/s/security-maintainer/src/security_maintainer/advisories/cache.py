"""
Sistema de caché local determinista con TTL y registro de procedencia.
"""

from __future__ import annotations
import json
import hashlib
import time
from pathlib import Path
from typing import Any, Optional, Dict, Tuple

DEFAULT_CACHE_DIR = Path.home() / ".security-maintainer" / "cache"


class AdvisoryCache:
    """Gestiona el almacenamiento en disco de consultas de vulnerabilidades para evitar peticiones redundantes."""

    def __init__(self, cache_dir: Optional[Path] = None, default_ttl_hours: int = 12):
        self.cache_dir = cache_dir or DEFAULT_CACHE_DIR
        self.default_ttl_seconds = default_ttl_hours * 3600
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _make_key(self, source: str, query: str) -> str:
        h = hashlib.sha256(f"{source}:{query}".encode("utf-8")).hexdigest()
        return f"{source}_{h}.json"

    def get(self, source: str, query: str, ttl_hours: Optional[int] = None) -> Tuple[Optional[Any], bool, float]:
        """
        Retorna (datos, es_valido, antiguedad_horas).
        Si ha expirado pero existe, devuelve datos marcados como es_valido=False para modo degraded/offline.
        """
        filename = self._make_key(source, query)
        filepath = self.cache_dir / filename
        if not filepath.exists():
            return None, False, 0.0

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                record = json.load(f)
            timestamp = record.get("timestamp", 0)
            data = record.get("data")
            age = time.time() - timestamp
            age_hours = age / 3600.0

            ttl_sec = (ttl_hours * 3600) if ttl_hours is not None else self.default_ttl_seconds
            is_valid = age <= ttl_sec
            return data, is_valid, age_hours
        except Exception:
            return None, False, 0.0

    def set(self, source: str, query: str, data: Any) -> None:
        """Guarda los datos con marca de tiempo UTC."""
        filename = self._make_key(source, query)
        filepath = self.cache_dir / filename
        record = {
            "source": source,
            "query": query,
            "timestamp": time.time(),
            "data": data
        }
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(record, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
