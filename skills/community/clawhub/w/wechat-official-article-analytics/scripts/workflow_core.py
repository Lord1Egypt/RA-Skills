"""Portable gateway workflows: live prices, durable requests and evidence exports."""
import hashlib
import html
import json
import os
from pathlib import Path
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from datetime import datetime, timezone
from decimal import Decimal
from contextlib import contextmanager

from platform_contract import catalog, failure, identity_headers, price_micros, product_path
from data_safety import public_data

ORIGIN = "https://api.we-media.cn"




def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(",", ":"), default=str).encode()).hexdigest()




def atomic_json(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as out:
        json.dump(public_data(value), out, ensure_ascii=False, indent=2)
        temp = out.name
        out.flush()
        os.fsync(out.fileno())
    os.replace(temp, path)


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))




class APIError(Exception):
    def __init__(self, code, request_id="", status=0, details=None):
        self.code, self.request_id, self.status = str(code), str(request_id), status
        self.details = details or {}
        super().__init__(self.code + (" (requestId=" + self.request_id + ")" if self.request_id else ""))






@contextmanager
def workspace_lock(directory):
    """OS lock releases on crash; no stale PID files or concurrent writers."""
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    with (directory / ".workflow.lock").open("a+b") as handle:
        handle.seek(0)
        if os.name == "nt":
            import msvcrt
            if handle.read(1) == b"":
                handle.write(b"0")
                handle.flush()
            handle.seek(0)
            try:
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError:
                raise ValueError("此工作区已有任务运行，请等待完成") from None
        else:
            import fcntl
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                raise ValueError("此工作区已有任务运行，请等待完成") from None
        try:
            yield
        finally:
            handle.seek(0)
            if os.name == "nt":
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(handle, fcntl.LOCK_UN)






def next_params(data, params):
    """Honor page/cursor contract, including empty pages with hasMore=true."""
    if data.get("hasMore") is False:
        return None
    result = dict(params)
    if data.get("collectionId") and data.get("nextPage") is not None:
        for name in ("offset", "limit", "cursor"):
            result.pop(name, None)
        result.update(collectionId=data["collectionId"], page=data["nextPage"])
    elif data.get("nextCursor", data.get("cursor")) not in (None, "") and data.get("hasMore"):
        result["cursor"] = data.get("nextCursor", data.get("cursor"))
    elif data.get("hasMore") and data.get("nextOffset") is not None and "offset" in params:
        result["offset"] = data["nextOffset"]
    elif data.get("hasMore"):
        raise APIError("PAGINATION_POSITION_MISSING")
    else:
        return None
    if result == params:
        raise APIError("PAGINATION_CURSOR_REPEATED")
    return result










