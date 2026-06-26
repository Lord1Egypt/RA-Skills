#!/usr/bin/env python3
import json
import urllib.parse
import urllib.request

from _auth import clear_cached_token, get_token

API_BASE = __import__("os").environ.get("CHANJING_API_BASE", "https://open-api.chanjing.cc")

RUNNING_STATUSES = {"Queued", "Ready", "Generating"}
SUCCESS_STATUSES = {"Success"}
FAILED_STATUSES = {"Error", "Fail"}


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
        suffix = "?" + urllib.parse.urlencode(query, doseq=True)

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


def get_task(token, unique_id):
    return api_get(token, "/open/v1/ai_creation/task", {"unique_id": unique_id})


def list_tasks(token, creation_type, page=1, page_size=50, unique_ids=None, is_success=None):
    payload = {
        "unique_ids": unique_ids or [],
        "type": creation_type,
        "page": page,
        "page_size": page_size,
    }
    if is_success is not None:
        payload["is_success"] = bool(is_success)
    return api_post(token, "/open/v1/ai_creation/task/page", payload)


def first_output_url(data):
    urls = (data or {}).get("output_url") or []
    if isinstance(urls, list) and urls:
        return urls[0]
    return None
