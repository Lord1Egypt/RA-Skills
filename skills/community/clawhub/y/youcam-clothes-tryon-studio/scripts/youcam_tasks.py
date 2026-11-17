"""Builds YouCam AI tasks on top of the pure API calls in youcam_api.py.

`run()` drives one feature end to end: it uploads the input file(s) if needed, creates
the processing task, and polls until it finishes (or polling runs out), then returns the
result.
`upload_from_url()` and `poll()` are also available on their own for callers that want to
manage each step individually.
"""

import os
import tempfile
import time
from typing import Any, Optional
from urllib.parse import urlparse

import requests

from constants import (
    TASK_STATUS,
    DEFAULT_MAX_POLLS,
    DEFAULT_POLL_INTERVAL,
    UPLOAD_TIMEOUT,
)
from youcam_api import create_task, get_task, load_contract, upload_file


class UploadBatchError(RuntimeError):
    """Raised when resolving a mixed group of local paths and URLs has any failures."""

    def __init__(self, uploaded: list[dict[str, str]], failed: list[dict[str, str]]):
        self.uploaded = uploaded
        self.failed = failed
        super().__init__(
            f"{len(failed)} of {len(uploaded) + len(failed)} upload(s) failed: "
            + "; ".join(f"{f['source']}: {f['error']}" for f in failed)
        )


def upload_from_url(contract: dict[str, Any], url: str, key: str) -> str:
    """Download a web URL and upload it, returning its file_id.

    Used when a src/ref group mixes local paths and URLs: the upload endpoint only
    registers local file bytes, so a URL has to be fetched client-side first to get a
    file_id that can sit alongside the local files' file_ids in the same list.

    Args:
        contract: The loaded API contract, e.g. from load_contract().
        url: The web URL to download and upload.
        key: The API key to authenticate the request with.

    Returns:
        str: The uploaded file's file_id.
    """
    tmp_path = _download_to_temp(url)
    try:
        return upload_file(contract, tmp_path, key)
    finally:
        os.remove(tmp_path)


def poll(
    contract: dict[str, Any],
    feature: str,
    task_id: str,
    key: str,
    version: Optional[str] = None,
    interval: float = DEFAULT_POLL_INTERVAL,
    max_polls: int = DEFAULT_MAX_POLLS,
) -> dict[str, Any]:
    """Poll a task up to max_polls times, interval seconds apart.

    Running out of polls isn't a failure: the task may just still be processing, so this
    returns normally with whatever status was last observed (typically still "running").
    The caller can decide whether to poll again later with the same task_id.

    Args:
        contract: The feature's loaded API contract, e.g. from load_contract().
        feature: Which YouCam feature this task belongs to, e.g. "skin-analysis".
        task_id: The task to poll, as returned by create_task().
        key: The API key to authenticate the request with.
        version: Which version of the feature to call. Defaults to the standard version.
        interval: How many seconds to wait between checks while the job is processing.
        max_polls: How many times to check on the job before giving up and returning
            whatever status was last seen.

    Returns:
        dict[str, Any]: The task's most recent "data" payload, plus "task_id".
    """
    data = {}
    for _ in range(max_polls):
        data = get_task(contract, feature, task_id, key, version)
        if data.get("task_status") in TASK_STATUS:
            break
        time.sleep(interval)
    return {**data, "task_id": task_id}


def run(
    feature: str,
    src_file: Optional[str] | list[str] = None,
    ref_file: Optional[str] | list[str] = None,
    params: Optional[dict[str, Any]] = None,
    key: Optional[str] = None,
    version: Optional[str] = None,
    interval: float = DEFAULT_POLL_INTERVAL,
    max_polls: int = DEFAULT_MAX_POLLS,
    contract: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Runs one YouCam AI feature on a photo or video and returns the result.

    Args:
        feature: Which YouCam feature to run, e.g. "skin-analysis".
        src_file: The main input photo or video. Give one local file path or web URL,
            or a list of several (some features need multiple photos, e.g. three
            angles of a face). Local paths and web URLs can be mixed in the same list.
            When mixed, every URL is also uploaded (fetched client-side) to get a
            file_id, since the API needs one homogeneous field.
        ref_file: A second input some features need for reference, such as a
            hairstyle photo for a hair transfer or a garment photo for a virtual
            try-on. Follows the same rules as src_file. Not every feature needs this.
        params: Extra options to send along with the request.
        key: The API key to use. Required; the caller (e.g. youcam_core.py's CLI) is
            expected to resolve it from YOUCAM_API_KEY or credentials.json beforehand.
        version: Which version of the feature to call. Defaults to the standard version.
        interval: How many seconds to wait between checks while the job is processing.
        max_polls: How many times to check on the job before giving up and returning
            whatever status was last seen.
        contract: An already-loaded feature contract to reuse instead of loading it again.

    Returns:
        dict[str, Any]: The job's latest result, plus its "task_id".

    Raises:
        ValueError: No API key is available, or no input file/URL/ID was given.
        UploadBatchError: One or more values failed to upload while resolving a mixed
            src_file/ref_file list of local paths and URLs.
    """
    contract = contract or load_contract(feature)
    if not key:
        raise ValueError(
            "missing API key. set the YOUCAM_API_KEY env var, or create credentials.json "
            "(see credentials.example.json for the format)"
        )
    body = dict(params or {})

    src_values = _as_list(src_file)
    if src_values:
        body.update(_resolve_group(contract, key, src_values, "src"))
    elif not any(k in body for k in ("src_file_id", "src_file_url", "src_file_ids", "src_file_urls")):
        raise ValueError("provide src_file, or one of src_file_id/src_file_url/src_file_ids/src_file_urls")

    ref_values = _as_list(ref_file)
    if ref_values:  # needed by features like hair transfer or clothes try-on
        body.update(_resolve_group(contract, key, ref_values, "ref"))

    tid = create_task(contract, feature, body, key, version)
    return poll(contract, feature, tid, key, version, interval, max_polls)


def _download_to_temp(url: str) -> str:
    """Download a URL to a local temp file and return its path. Caller is responsible for removing it."""
    ext = os.path.splitext(urlparse(url).path)[1].lower()
    r = requests.get(url, timeout=UPLOAD_TIMEOUT, stream=True)
    r.raise_for_status()
    fd, tmp_path = tempfile.mkstemp(suffix=ext)
    try:
        with os.fdopen(fd, "wb") as fh:
            for chunk in r.iter_content(chunk_size=1 << 16):
                fh.write(chunk)
    except Exception:
        os.remove(tmp_path)
        raise
    return tmp_path


def _as_list(value: Optional[str] | list[str]) -> list[str]:
    if not value:
        return []
    return [value] if isinstance(value, str) else list(value)


def _is_url(value: str) -> bool:
    return value.startswith(("http://", "https://"))


def _resolve_group(contract: dict[str, Any], key: str, values: list[str], kind: str) -> dict[str, Any]:
    """Resolve one src/ref group into the single body field it maps to."""
    urls = [v for v in values if _is_url(v)]
    paths = [v for v in values if not _is_url(v)]

    if paths:
        uploaded, failed = [], []
        for v in values:
            try:
                fid = upload_from_url(contract, v, key) if _is_url(v) else upload_file(contract, v, key)
                uploaded.append({"source": v, "file_id": fid})
            except Exception as exc:
                failed.append({"source": v, "error": str(exc)})
        if failed:
            raise UploadBatchError(uploaded, failed)
        ids = [u["file_id"] for u in uploaded]
        return {f"{kind}_file_id" if len(ids) == 1 else f"{kind}_file_ids": ids[0] if len(ids) == 1 else ids}
    if urls:
        return {
            f"{kind}_file_url" if len(urls) == 1 else f"{kind}_file_urls": urls[0] if len(urls) == 1 else urls
        }
    return {}
