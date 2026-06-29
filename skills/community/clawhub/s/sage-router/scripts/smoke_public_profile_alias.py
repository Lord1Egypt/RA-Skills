#!/usr/bin/env python3
"""Create a disposable generated key and verify public profile aliasing."""
import argparse
import hashlib
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path


def read_env_file(path):
    env = {}
    if not path:
        return env
    for line in Path(path).read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        env[key.strip()] = value.strip().strip("'\"")
    return env


def env_value(env, *names):
    for name in names:
        value = env.get(name) or os.environ.get(name)
        if value:
            return value
    return ""


def supabase_request(supabase_url, service_key, method, path, payload=None, prefer=False):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    headers = {
        "apikey": service_key,
        "Authorization": f"Bearer {service_key}",
        "Content-Type": "application/json",
    }
    if prefer:
        headers["Prefer"] = "return=representation"
    req = urllib.request.Request(supabase_url.rstrip("/") + path, data=data, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as resp:
        body = resp.read().decode("utf-8")
        return json.loads(body) if body else None


def request_json(api_base, raw_key, model, mode):
    if mode == "responses":
        path = "/v1/responses"
        body = {
            "model": model,
            "input": [{"role": "user", "content": "Return only ok."}],
            "max_output_tokens": 8,
            "stream": False,
        }
    else:
        path = "/v1/chat/completions"
        body = {
            "model": model,
            "messages": [{"role": "user", "content": "Return only ok."}],
            "max_tokens": 8,
            "stream": False,
        }
    req = urllib.request.Request(
        f"{api_base.rstrip('/')}{path}",
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {raw_key}",
            "Content-Type": "application/json",
            "User-Agent": "SageRouterEdgeProfileSmoke/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
        response_headers = {key.lower(): value for key, value in resp.headers.items()}
        return {"status": resp.status, "payload": payload, "headers": response_headers}


def request_responses_stream(api_base, raw_key, model):
    req = urllib.request.Request(
        f"{api_base.rstrip('/')}/v1/responses",
        data=json.dumps({
            "model": model,
            "input": [{"role": "user", "content": "Return only streaming ok."}],
            "max_output_tokens": 16,
            "stream": True,
        }).encode("utf-8"),
        method="POST",
        headers={
            "Authorization": f"Bearer {raw_key}",
            "Content-Type": "application/json",
            "User-Agent": "SageRouterEdgeProfileSmoke/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=90) as resp:
        response_headers = {key.lower(): value for key, value in resp.headers.items()}
        events = []
        deltas = []
        done_text = []
        prefix_lines = []
        for raw_line in resp:
            line = raw_line.decode("utf-8", errors="replace").rstrip("\n")
            if line.startswith("event: "):
                events.append(line[len("event: "):])
                continue
            if not line.startswith("data: "):
                continue
            data = line[len("data: "):].strip()
            if not data or data == "[DONE]":
                continue
            try:
                payload = json.loads(data)
            except Exception:
                continue
            for key, target in (("delta", deltas), ("text", done_text)):
                value = payload.get(key)
                if isinstance(value, str) and value:
                    target.append(value)
                    if value.lstrip().startswith("["):
                        prefix_lines.append(value[:160])
        return {
            "status": resp.status,
            "payload": {
                "streamEvents": events,
                "streamText": "".join(deltas),
                "streamDoneText": done_text,
                "streamPrefixLines": prefix_lines,
            },
            "headers": response_headers,
        }


def visible_text_from_payload(payload, mode):
    if mode == "responses-stream":
        return payload.get("streamText") or "".join(payload.get("streamDoneText") or [])
    if mode == "responses":
        return payload.get("output_text") or ""
    choices = payload.get("choices") or []
    if choices and isinstance(choices[0], dict):
        message = choices[0].get("message") or {}
        if isinstance(message, dict):
            return message.get("content") or ""
    return ""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--env-file", default=os.environ.get("SAGE_ROUTER_EDGE_ENV_FILE", ""))
    parser.add_argument("--api-base", default=os.environ.get("SAGEROUTER_API_BASE_URL", "https://api.sagerouter.dev"))
    parser.add_argument("--model", default=os.environ.get("SAGEROUTER_SMOKE_MODEL", "sage-router/frontier"))
    parser.add_argument("--mode", choices=("chat-completions", "responses", "responses-stream"), default="chat-completions")
    args = parser.parse_args()

    env = read_env_file(args.env_file)
    supabase_url = env_value(env, "SAGE_ROUTER_SUPABASE_URL", "SUPABASE_URL").rstrip("/")
    service_key = env_value(env, "SAGE_ROUTER_SUPABASE_SERVICE_ROLE_KEY", "SUPABASE_SERVICE_ROLE_KEY", "SUPABASE_SERVICE_ROLE")
    pepper = env_value(env, "SAGE_ROUTER_API_KEY_HASH_PEPPER", "SAGE_ROUTER_SIGNING_SECRET")
    configured_smoke_key = env_value(env, "SAGEROUTER_SMOKE_API_KEY", "SAGE_ROUTER_CLIENT_API_KEY", "SAGE_ROUTER_API_KEY")
    can_create_disposable_key = bool(supabase_url and service_key and pepper)
    if not (can_create_disposable_key or configured_smoke_key):
        raise SystemExit("missing Supabase generated-key credentials or configured smoke API key")

    now = int(time.time())
    raw_key = f"sk_sage_smoke_{uuid.uuid4().hex}{uuid.uuid4().hex}"
    customer_id = f"edge-smoke-{uuid.uuid4().hex}"
    user_id = f"edge-smoke-user-{uuid.uuid4().hex}"
    key_id = f"edge-smoke-key-{uuid.uuid4().hex}"
    digest = hashlib.sha256((pepper + raw_key).encode("utf-8")).hexdigest()
    result = {"status": None}
    created_disposable_key = False

    try:
        if can_create_disposable_key:
            supabase_request(supabase_url, service_key, "POST", "/rest/v1/sage_router_customers", {
                "id": customer_id,
                "user_id": user_id,
                "email": f"{customer_id}@example.invalid",
                "plan": "pro",
                "status": "active",
                "created_at_epoch": now,
                "updated_at_epoch": now,
            }, prefer=True)
            supabase_request(supabase_url, service_key, "POST", "/rest/v1/sage_router_api_keys", {
                "id": key_id,
                "customer_id": customer_id,
                "user_id": user_id,
                "name": "edge smoke",
                "prefix": raw_key[:18],
                "api_key_hash": digest,
                "status": "active",
                "plan": "pro",
                "created_at_epoch": now,
                "last_used_at_epoch": None,
                "revoked_at_epoch": None,
            }, prefer=True)
            created_disposable_key = True
        else:
            raw_key = configured_smoke_key

        try:
            if args.mode == "responses-stream":
                result = request_responses_stream(args.api_base, raw_key, args.model)
            else:
                result = request_json(args.api_base, raw_key, args.model, args.mode)
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            try:
                payload = json.loads(raw)
            except Exception:
                payload = {"raw": raw[:300]}
            result = {"status": exc.code, "payload": payload, "headers": {key.lower(): value for key, value in exc.headers.items()}}
    finally:
        if created_disposable_key:
            try:
                supabase_request(
                    supabase_url,
                    service_key,
                    "PATCH",
                    f"/rest/v1/sage_router_api_keys?id=eq.{urllib.parse.quote(key_id, safe='')}",
                    {"status": "revoked", "revoked_at_epoch": int(time.time())},
                )
            except Exception:
                pass
            for table, column in (
                ("sage_router_usage_counters", "customer_id"),
                ("sage_router_api_keys", "customer_id"),
                ("sage_router_customers", "id"),
            ):
                try:
                    supabase_request(
                        supabase_url,
                        service_key,
                        "DELETE",
                        f"/rest/v1/{table}?{column}=eq.{urllib.parse.quote(customer_id, safe='')}",
                    )
                except Exception:
                    pass

    payload = result.get("payload") if isinstance(result.get("payload"), dict) else {}
    headers = result.get("headers") if isinstance(result.get("headers"), dict) else {}
    visible_text = visible_text_from_payload(payload, args.mode)
    prefix_lines = payload.get("streamPrefixLines") if args.mode == "responses-stream" else []
    prefix_leak = visible_text.lstrip().startswith("[") or bool(prefix_lines)
    body_model = payload.get("model")
    profile_contract_ok = (
        result.get("status") == 200
        and headers.get("x-sage-router-edge") in {"tailnet-lowest-latency", "cloudflare-origin-selector"}
        and headers.get("x-sage-router-model") == args.model
        and (args.mode == "responses-stream" or body_model == args.model)
        and not prefix_leak
    )
    print(json.dumps({
        "mode": args.mode,
        "status": result.get("status"),
        "bodyModel": body_model,
        "bodyUpstreamModel": payload.get("upstream_model"),
        "visibleText": visible_text[:300],
        "prefixLeak": prefix_leak,
        "streamEvents": payload.get("streamEvents"),
        "streamPrefixLines": prefix_lines,
        "profileContractOk": profile_contract_ok,
        "disposableKey": created_disposable_key,
        "edge": headers.get("x-sage-router-edge"),
        "selectedUpstream": headers.get("x-sage-router-upstream"),
        "headerModel": headers.get("x-sage-router-model"),
        "headerProvider": headers.get("x-sage-router-provider"),
        "headerModelName": headers.get("x-sage-router-model-name"),
        "headerUpstreamModel": headers.get("x-sage-router-upstream-model"),
        "headerUpstreamProvider": headers.get("x-sage-router-upstream-provider"),
        "headerUpstreamModelName": headers.get("x-sage-router-upstream-model-name"),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
