"""Low-level HTTP client for WayinVideo API (stdlib only)."""

import os
import sys
import json
import mimetypes
import urllib.request
import urllib.error

from wayinvideo.constants import (
    SUBMIT_ENDPOINTS,
    UPLOAD_ENDPOINT,
    ALLOWED_VIDEO_MIMETYPES,
    ALLOWED_VIDEO_EXTENSIONS,
    MAX_UPLOAD_SIZE_BYTES,
    API_VERSION,
    USER_AGENT,
)


# ── Internal helpers ─────────────────────────────────────────────────────────

def _get_api_key():
    key = os.environ.get("WAYIN_API_KEY")
    if not key:
        print(
            "Error: WAYIN_API_KEY environment variable is not set.\n"
            "  export WAYIN_API_KEY=<your_key>",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def _headers(content_type="application/json"):
    h = {
        "Authorization": f"Bearer {_get_api_key()}",
        "x-wayinvideo-api-version": API_VERSION,
        "user-agent": USER_AGENT,
    }
    if content_type:
        h["Content-Type"] = content_type
    return h


def _extract_error(exc):
    """Best-effort message extraction from an HTTPError."""
    body = exc.read().decode("utf-8")
    try:
        return json.loads(body).get("message", body)
    except (json.JSONDecodeError, AttributeError):
        return body


# ── Public API ───────────────────────────────────────────────────────────────

def upload_file(file_path):
    """Upload a local video file and return a one-time *identity* token.

    The token can be passed as ``--url`` to ``wayinvideo submit``.

    Supported formats: MP4, AVI, MOV, WEBM.  Max size: 5 GB.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)

    if file_size > MAX_UPLOAD_SIZE_BYTES:
        raise ValueError("File size exceeds the 5 GB limit.")

    content_type, _ = mimetypes.guess_type(file_path)
    if content_type not in ALLOWED_VIDEO_MIMETYPES:
        ext = os.path.splitext(file_name)[1].lower().lstrip(".")
        if ext not in ALLOWED_VIDEO_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {content_type or 'unknown'}. "
                "Supported: MP4, AVI, MOV, WEBM."
            )

    # Step 1 - obtain presigned upload URL + identity
    try:
        req = urllib.request.Request(
            UPLOAD_ENDPOINT,
            data=json.dumps({"name": file_name}).encode("utf-8"),
            headers=_headers(),
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        upload_url = body["data"]["upload_url"]
        identity   = body["data"]["identity"]
    except urllib.error.HTTPError as e:
        raise Exception(f"Upload init failed - {_extract_error(e)}")
    except urllib.error.URLError as e:
        raise Exception(f"Network error during upload init: {e}")

    # Step 2 - PUT file bytes to the presigned URL
    ct = content_type or "application/octet-stream"
    try:
        with open(file_path, "rb") as fp:
            req = urllib.request.Request(
                upload_url, data=fp,
                headers={"Content-Type": ct},
                method="PUT",
            )
            req.add_header("Content-Length", str(file_size))
            with urllib.request.urlopen(req) as resp:
                if resp.getcode() not in (200, 201, 204):
                    raise Exception(f"Upload returned status {resp.getcode()}")
    except urllib.error.HTTPError as e:
        raise Exception(f"File upload failed - HTTP {e.code}")
    except urllib.error.URLError as e:
        raise Exception(f"File upload network error: {e}")

    return identity


def submit_task(task_type, payload):
    """POST a processing task and return the ``id`` (or ``export_task_id``)."""
    url = SUBMIT_ENDPOINTS[task_type]
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers=_headers(),
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if resp.getcode() == 200 and "data" in result:
                data = result["data"]
                return data.get("id") or data.get("export_task_id")
            raise Exception(
                f"API error ({resp.getcode()}): "
                f"{result.get('message', 'unexpected response')}"
            )
    except urllib.error.HTTPError as e:
        raise Exception(f"HTTP {e.code}: {_extract_error(e)}")
    except urllib.error.URLError as e:
        raise Exception(f"Network error: {e}")


def fetch_results(task_type, project_id):
    """GET current results for a task.  Returns the ``data`` dict."""
    if task_type == "export":
        # Export task results endpoint: .../api/v2/clips/export/{taskId}
        url = f"{SUBMIT_ENDPOINTS[task_type]}/{project_id}"
    else:
        # Other tasks use .../results/{projectId}
        url = f"{SUBMIT_ENDPOINTS[task_type]}/results/{project_id}"
    try:
        req = urllib.request.Request(url, headers=_headers(content_type=None))
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if resp.getcode() != 200 or "data" not in result:
                raise Exception(
                    f"API error ({resp.getcode()}): "
                    f"{result.get('message', 'unexpected response')}"
                )
            return result["data"]
    except urllib.error.HTTPError as e:
        raise Exception(f"HTTP {e.code}: {_extract_error(e)}")
    except urllib.error.URLError as e:
        raise Exception(f"Network error: {e}")