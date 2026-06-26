#!/usr/bin/env python3
import json
import urllib.parse
import urllib.request

from _auth import clear_cached_token, get_token

API_BASE = "https://open-api.chanjing.cc"

PHOTO_RUNNING = {"Ready", "Generating", "Queued"}
PHOTO_SUCCESS = {"Success"}
PHOTO_FAILED = {"Error", "Fail"}

MOTION_RUNNING = {"Ready", "Generating", "Queued"}
MOTION_SUCCESS = {"Success"}
MOTION_FAILED = {"Error", "Fail"}

LORA_RUNNING = {"Queued", "Published", "Generating"}
LORA_SUCCESS = {"Success"}
LORA_FAILED = {"Fail"}


def is_token_invalid(body):
    code = body.get("code")
    msg = str(body.get("msg", ""))
    return code == 10400 or "AccessToken已失效" in msg or "AccessToken verification failed" in msg


def _handle_business_response(body):
    if body.get("code") != 0:
        raise RuntimeError(body.get("msg", body))
    return body.get("data")


def _retry_if_token_invalid(token, do_request):
    body = do_request(token)
    if not is_token_invalid(body):
        return _handle_business_response(body)

    clear_cached_token()
    new_token, err = get_token(force_refresh=True)
    if err:
        raise RuntimeError(err)

    body = do_request(new_token)
    return _handle_business_response(body)


def api_get(token, path, query=None):
    query = query or {}
    suffix = ""
    if query:
        suffix = "?" + urllib.parse.urlencode(query)

    def _do_request(current_token):
        req = urllib.request.Request(
            f"{API_BASE}{path}{suffix}",
            headers={"access_token": current_token},
            method="GET",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))

    return _retry_if_token_invalid(token, _do_request)


def api_post(token, path, payload):
    def _do_request(current_token):
        req = urllib.request.Request(
            f"{API_BASE}{path}",
            data=json.dumps(payload).encode("utf-8"),
            headers={"access_token": current_token, "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))

    return _retry_if_token_invalid(token, _do_request)


def get_photo_task(token, unique_id):
    return api_get(token, "/open/v1/aigc/photo/task", {"unique_id": unique_id})


def list_photo_tasks(token, page=1, page_size=10):
    return api_get(token, "/open/v1/aigc/photo/task/page", {"page": page, "page_size": page_size})


def get_motion_task(token, unique_id):
    return api_get(token, "/open/v1/aigc/motion/task", {"unique_id": unique_id})


def get_lora_task(token, lora_id):
    return api_get(token, "/open/v1/aigc/lora/task", {"lora_id": lora_id})


def first_output_url(data):
    urls = (data or {}).get("output_url") or []
    if isinstance(urls, list) and urls:
        return urls[0]
    return None
