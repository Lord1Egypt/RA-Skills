# /// script
# dependencies = ["requests", "boto3"]
# ///
"""Shared helpers for runpod-media skill scripts."""

import os
import json
import time
import base64
import pathlib
import requests
import mimetypes

# Resolve a key: env var first, then OpenClaw secrets.json
def _from_secrets_json(json_pointer: str) -> str | None:
    """Read a value from ~/.openclaw/secrets.json using a /path/to/key pointer."""
    secrets_path = pathlib.Path.home() / ".openclaw" / "secrets.json"
    if not secrets_path.exists():
        return None
    try:
        data = json.loads(secrets_path.read_text())
        parts = json_pointer.strip("/").split("/")
        for part in parts:
            if not isinstance(data, dict):
                return None
            data = data.get(part)
        return data if isinstance(data, str) else None
    except Exception:
        return None


def init_keys():
    # Priority: env var > OpenClaw secrets.json (~/.openclaw/secrets.json)
    api_key = (
        os.getenv("RUNPOD_API_KEY")
        or _from_secrets_json("/runpod/apiKey")
    )
    if not api_key:
        raise SystemExit(
            "Missing RunPod API key.\n"
            "Add it to ~/.openclaw/secrets.json at /runpod/apiKey, "
            "or set RUNPOD_API_KEY env var."
        )
    # imgbb_key kept for backward compat but no longer used
    imgbb_key = None
    return api_key, imgbb_key


def _r2_config() -> dict:
    """Load R2 config from secrets.json."""
    cfg = _from_secrets_json("/cloudflare/r2/accessKeyId")
    if not cfg:
        # Return full dict
        secrets_path = pathlib.Path.home() / ".openclaw" / "secrets.json"
        data = json.loads(secrets_path.read_text())
        return data.get("cloudflare", {}).get("r2", {})
    return {}


def upload_to_r2(path: str, expiry: int = 60) -> str:
    """Upload a local file to Cloudflare R2 and return a presigned GET URL (default 1 min)."""
    import boto3
    from botocore.config import Config

    secrets_path = pathlib.Path.home() / ".openclaw" / "secrets.json"
    data = json.loads(secrets_path.read_text())
    r2 = data.get("cloudflare", {}).get("r2", {})

    access_key = r2.get("accessKeyId")
    secret_key = r2.get("secretAccessKey")
    endpoint = r2.get("endpoint")
    bucket = r2.get("bucket", "openclaw")

    if not all([access_key, secret_key, endpoint]):
        raise SystemExit("R2 credentials not found in secrets.json under cloudflare.r2")

    client = boto3.client(
        "s3",
        endpoint_url=endpoint,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name="auto",
        config=Config(signature_version="s3v4"),
    )

    file_path = pathlib.Path(path)
    key = f"uploads/{int(time.time())}_{file_path.name}"
    content_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"

    with open(file_path, "rb") as f:
        client.put_object(Bucket=bucket, Key=key, Body=f, ContentType=content_type)

    url = client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expiry,
    )
    print(f"  uploaded to R2: {url[:80]}…")
    return url


def _headers(api_key):
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def runsync(endpoint_id: str, payload: dict, api_key: str, timeout: int = 120) -> dict:
    url = f"https://api.runpod.ai/v2/{endpoint_id}/runsync"
    resp = requests.post(url, json={"input": payload}, headers=_headers(api_key), timeout=timeout)
    resp.raise_for_status()
    data = resp.json()
    if data.get("status") == "FAILED":
        raise RuntimeError(f"Job failed: {data.get('error', data)}")
    return data.get("output", {})


def run_async(endpoint_id: str, payload: dict, api_key: str, timeout: int = 30) -> str:
    url = f"https://api.runpod.ai/v2/{endpoint_id}/run"
    resp = requests.post(url, json={"input": payload}, headers=_headers(api_key), timeout=timeout)
    resp.raise_for_status()
    data = resp.json()
    return data["id"]


def poll_job(endpoint_id: str, job_id: str, api_key: str, max_wait: int = 300, interval: int = 5) -> dict:
    url = f"https://api.runpod.ai/v2/{endpoint_id}/status/{job_id}"
    deadline = time.time() + max_wait
    while time.time() < deadline:
        resp = requests.get(url, headers=_headers(api_key), timeout=30)
        resp.raise_for_status()
        data = resp.json()
        status = data.get("status")
        if status == "COMPLETED":
            return data.get("output", {})
        if status == "FAILED":
            raise RuntimeError(f"Job {job_id} failed: {data.get('error', data)}")
        print(f"  status: {status} — waiting {interval}s…")
        time.sleep(interval)
    raise TimeoutError(f"Job {job_id} did not complete within {max_wait}s")


def ensure_url(path_or_url: str, imgbb_key: str | None = None) -> str:
    """Return a public URL, uploading to R2 (presigned, 1 min) if a local path is given."""
    if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
        return path_or_url
    return upload_to_r2(path_or_url, expiry=60)


def get_media_url(output: dict) -> str | None:
    return (
        output.get("video_url")
        or output.get("image_url")
        or output.get("result")
        or output.get("url")
        or output.get("image")
    )


def output_dir() -> pathlib.Path:
    # Save inside OpenClaw workspace so sandboxed agents can read the files
    d = pathlib.Path.home() / ".openclaw" / "workspace" / "runpod-media"
    d.mkdir(parents=True, exist_ok=True)
    return d


def save_media(url: str, filename: str) -> pathlib.Path:
    dest = output_dir() / filename
    resp = requests.get(url, timeout=120)
    resp.raise_for_status()
    dest.write_bytes(resp.content)
    return dest
