"""
collectors/file.py — File Collector

Collects content from local files (txt, md, json, csv, pdf).
Supports incremental collection by file modification time.
"""

from __future__ import annotations

import json
import logging
import os
import time
from typing import Any

from .base import MemoryCollector, RawMemory, CollectionResult, CollectorStatus

logger = logging.getLogger(__name__)

_SUPPORTED_EXTENSIONS = {".txt", ".md", ".json", ".csv", ".html", ".log"}


class FileConfig:
    """File collector configuration."""
    def __init__(self, paths: list[str] | None = None,
                 extensions: list[str] | None = None,
                 tenant_id: str = "default",
                 reliability_score: float = 0.7,
                 max_file_size: int = 1_000_000,
                 max_files_per_sync: int = 100):
        self.paths = paths or []
        self.extensions = extensions or list(_SUPPORTED_EXTENSIONS)
        self.tenant_id = tenant_id
        self.reliability_score = reliability_score
        self.max_file_size = max_file_size
        self.max_files_per_sync = max_files_per_sync


class FileCollector(MemoryCollector):
    """Collect content from local files."""

    def __init__(self, config: FileConfig | dict | None = None):
        if isinstance(config, FileConfig):
            cfg = config
        else:
            d = config or {}
            cfg = FileConfig(**{k: v for k, v in d.items()
                                if k in FileConfig.__dataclass_fields__})
        super().__init__(config={
            "paths": cfg.paths,
            "extensions": cfg.extensions,
            "tenant_id": cfg.tenant_id,
            "reliability_score": cfg.reliability_score,
            "max_file_size": cfg.max_file_size,
        })
        self._file_config = cfg

    def get_source_id(self) -> str:
        return "file"

    def test_connection(self) -> bool:
        return all(os.path.isdir(p) for p in self._file_config.paths if p)

    async def collect(self, since: float | None = None) -> CollectionResult:
        result = CollectionResult(
            source=self.get_source_id(),
            started_at=time.time(),
            status=CollectorStatus.SYNCING,
        )

        for base_path in self._file_config.paths:
            if not os.path.isdir(base_path):
                continue
            for root, dirs, files in os.walk(base_path):
                for fname in files:
                    ext = os.path.splitext(fname)[1].lower()
                    if ext not in self._file_config.extensions:
                        continue
                    fpath = os.path.join(root, fname)
                    try:
                        mtime = os.path.getmtime(fpath)
                        if since and mtime < since:
                            continue
                        raw = self._read_file(fpath, mtime)
                        if raw:
                            result.items.append(raw)
                            result.collected_count += 1
                            if result.collected_count >= self._file_config.max_files_per_sync:
                                break
                    except Exception as e:
                        result.error_count += 1
                        result.errors.append(f"{fpath}: {e}")
                if result.collected_count >= self._file_config.max_files_per_sync:
                    break

        self.last_sync = time.time()
        self._collect_count += result.collected_count
        result.status = CollectorStatus.IDLE
        result.finished_at = time.time()
        return result

    def _read_file(self, fpath: str, mtime: float) -> RawMemory | None:
        """Read a file and return a RawMemory."""
        fsize = os.path.getsize(fpath)
        if fsize > self._file_config.max_file_size:
            return None

        try:
            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception:
            return None

        if not content or len(content.strip()) < 10:
            return None

        return RawMemory(
            content=content[:10000],  # Cap at 10K chars
            source="file",
            source_id=f"file_{hash(fpath) % 100000}",
            timestamp=mtime,
            metadata={
                "file_path": fpath,
                "file_size": fsize,
                "extension": os.path.splitext(fpath)[1],
                "tenant_id": self._file_config.tenant_id,
            },
        )
