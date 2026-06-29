#!/usr/bin/env python3
import calendar
import hashlib
import hmac
import json
import os
import re
import ssl
import threading
import time
import urllib.parse
import urllib.request
from http.client import HTTPConnection, HTTPSConnection
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit


EDGE_PORT = int(os.environ.get("SAGE_ROUTER_EDGE_PORT", "8790"))
UPSTREAMS_RAW = os.environ.get("SAGE_ROUTER_UPSTREAMS", "")
CONTROL_PLANE_UPSTREAM_RAW = os.environ.get("SAGE_ROUTER_CONTROL_PLANE_UPSTREAM", "").strip()
EDGE_TOKEN = os.environ.get("SAGE_ROUTER_EDGE_TOKEN", "")
BACKEND_TOKEN = os.environ.get("SAGE_ROUTER_BACKEND_TOKEN", "local")
CONTROL_PLANE_TOKEN = os.environ.get("SAGE_ROUTER_CONTROL_PLANE_TOKEN", "").strip()
ANALYTICS_TOKEN = os.environ.get("SAGE_ROUTER_ANALYTICS_TOKEN", "").strip()
EDGE_AUTH_MODE = os.environ.get("SAGE_ROUTER_EDGE_AUTH_MODE", "shared-token").strip().lower()
HEALTH_PATH = os.environ.get("SAGE_ROUTER_HEALTH_PATH", "/health")
HEALTH_INTERVAL = float(os.environ.get("SAGE_ROUTER_HEALTH_INTERVAL_SECONDS", os.environ.get("SAGE_ROUTER_HEALTH_INTERVAL", "10").rstrip("s")))
HEALTH_TIMEOUT = float(os.environ.get("SAGE_ROUTER_HEALTH_TIMEOUT_SECONDS", os.environ.get("SAGE_ROUTER_HEALTH_TIMEOUT", "3").rstrip("s")))
REQUEST_TIMEOUT = float(os.environ.get(
    "SAGE_ROUTER_REQUEST_TIMEOUT_SECONDS",
    os.environ.get("SAGE_ROUTER_REQUEST_CONNECT_TIMEOUT_SECONDS", "120"),
))
READ_CHUNK_SIZE = int(os.environ.get("SAGE_ROUTER_EDGE_READ_CHUNK_SIZE", "65536"))
MAX_REJECTED_BODY_DRAIN_BYTES = int(os.environ.get("SAGE_ROUTER_EDGE_MAX_REJECTED_BODY_DRAIN_BYTES", "1048576"))
MAX_MODALITY_LEARN_BODY_BYTES = int(os.environ.get("SAGE_ROUTER_EDGE_MODALITY_LEARN_BODY_BYTES", "2097152"))
OLLAMA_SIBLING_REROUTE_MODELS = {
    item.strip()
    for item in os.environ.get("SAGE_ROUTER_EDGE_OLLAMA_SIBLING_REROUTE_MODELS", "kimi-k2.7-code").split(",")
    if item.strip()
}
RETRY_STATUSES = {401, 429, 502, 503, 504}
MODEL_API_STALE_ROUTE_RETRY_STATUSES = {404, 405}
SUPABASE_URL = (os.environ.get("SAGE_ROUTER_SUPABASE_URL") or os.environ.get("SUPABASE_URL") or "").rstrip("/")
SUPABASE_ANON_KEY = (
    os.environ.get("SAGE_ROUTER_SUPABASE_ANON_KEY")
    or os.environ.get("AOPS_SUPABASE_ANON_KEY")
    or os.environ.get("SUPABASE_ANON_KEY")
    or ""
)
SUPABASE_SERVICE_ROLE_KEY = (
    os.environ.get("SAGE_ROUTER_SUPABASE_SERVICE_ROLE_KEY")
    or os.environ.get("SUPABASE_SERVICE_ROLE")
    or os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    or ""
)
SUPABASE_CUSTOMERS_TABLE = os.environ.get("SAGE_ROUTER_SUPABASE_CUSTOMERS_TABLE", "sage_router_customers")
SUPABASE_API_KEYS_TABLE = os.environ.get("SAGE_ROUTER_SUPABASE_API_KEYS_TABLE", "sage_router_api_keys")
SUPABASE_USAGE_RPC = os.environ.get("SAGE_ROUTER_SUPABASE_USAGE_RPC", "sage_router_increment_usage")
SUPABASE_MODEL_MODALITIES_RPC = os.environ.get("SAGE_ROUTER_SUPABASE_MODEL_MODALITIES_RPC", "sage_router_record_model_modalities")
MODEL_MODALITIES_SHARED_ENABLED = os.environ.get("SAGE_ROUTER_MODEL_MODALITIES_SHARED_ENABLED", "1").strip().lower() not in {"0", "false", "no", "off"}
API_KEY_PREFIX = os.environ.get("SAGE_ROUTER_API_KEY_PREFIX", "sk_sage_")
API_KEY_HASH_PEPPER = os.environ.get("SAGE_ROUTER_API_KEY_HASH_PEPPER") or os.environ.get("SAGE_ROUTER_SIGNING_SECRET") or ""
AUTH_CACHE_TTL_SECONDS = float(os.environ.get("SAGE_ROUTER_EDGE_AUTH_CACHE_SECONDS", "30"))
API_KEY_AUTH_CACHE_TTL_SECONDS = float(os.environ.get("SAGE_ROUTER_EDGE_API_KEY_AUTH_CACHE_SECONDS", "0"))
CORS_ORIGIN = os.environ.get("SAGE_ROUTER_CORS_ORIGIN", "https://app.sagerouter.dev,https://sagerouter.dev,https://www.sagerouter.dev")
CORS_ORIGINS = [origin.strip() for origin in CORS_ORIGIN.split(",") if origin.strip()]
BROWSER_ALLOWED_ORIGINS_RAW = os.environ.get("SAGE_ROUTER_BROWSER_ALLOWED_ORIGINS", "").strip()
ACCOUNT_URL = os.environ.get("SAGE_ROUTER_ACCOUNT_URL", "https://app.sagerouter.dev/account.html")
LOGIN_URL = os.environ.get("SAGE_ROUTER_LOGIN_URL", "https://app.sagerouter.dev/login.html")
PRICING_URL = os.environ.get("SAGE_ROUTER_PRICING_URL", "https://sagerouter.dev/pricing")
BILLING_URL = os.environ.get("SAGE_ROUTER_BILLING_URL", "https://sagerouter.dev/billing")
SUPPORT_URL = os.environ.get("SAGE_ROUTER_SUPPORT_URL", "https://sagerouter.dev/support")
STATUS_URL = os.environ.get("SAGE_ROUTER_STATUS_URL", "https://app.sagerouter.dev/status")
API_BASE_URL = os.environ.get("SAGE_ROUTER_PUBLIC_API_BASE_URL", "https://api.sagerouter.dev")
RATE_LIMIT_ENABLED = os.environ.get("SAGE_ROUTER_EDGE_RATE_LIMIT_ENABLED", "1").strip().lower() not in {"0", "false", "no", "off"}
RATE_LIMIT_WINDOW_SECONDS = int(os.environ.get("SAGE_ROUTER_EDGE_RATE_LIMIT_WINDOW_SECONDS", "60"))
RATE_LIMITS_RAW = os.environ.get(
    "SAGE_ROUTER_EDGE_RATE_LIMITS",
    "trial=30,lite=60,pro=180,max=600,manual=600,paid=180,active=180,default=60",
)
AUTH_ATTEMPT_RATE_LIMIT_PER_WINDOW = int(os.environ.get("SAGE_ROUTER_EDGE_AUTH_ATTEMPT_RATE_LIMIT", "1200"))
TRUST_CLIENT_IP_HEADERS = os.environ.get("SAGE_ROUTER_EDGE_TRUST_CLIENT_IP_HEADERS", "1").strip().lower() not in {"0", "false", "no", "off"}
CLIENT_IP_HEADERS = tuple(
    header.strip()
    for header in os.environ.get("SAGE_ROUTER_EDGE_CLIENT_IP_HEADERS", "CF-Connecting-IP,X-Real-IP,X-Forwarded-For").split(",")
    if header.strip()
)
QUOTA_ENABLED = os.environ.get("SAGE_ROUTER_EDGE_QUOTA_ENABLED", "0").strip().lower() in {"1", "true", "yes", "on"}
MONTHLY_QUOTAS_RAW = os.environ.get(
    "SAGE_ROUTER_EDGE_MONTHLY_QUOTAS",
    "trial=1000,lite=10000,pro=50000,max=200000,paid=50000,active=50000,default=0",
)

PUBLIC_PATHS = {"/edge/health"}
PUBLIC_CONTROL_PLANE_PATHS = {
    "/pricing",
    "/plans",
    "/model-catalog",
    "/features/agent-native",
}
USER_JWT_PREFIXES = (
    "/account",
    "/billing/stripe/checkout",
    "/billing/stripe/portal",
    "/billing/crypto/intent",
    "/billing/crypto/status",
)
GENERATED_API_KEY_PREFIXES = (
    "/v1",
    "/v1beta",
)
OPERATOR_CONTROL_PLANE_PREFIXES = (
    "/analytics",
    "/admin",
    "/setup/model-modalities",
)
PUBLIC_SIGNED_BACKEND_PREFIXES = (
    "/billing/stripe/webhook",
)
DEFAULT_BROWSER_ALLOWED_ORIGIN_HOSTS = {
    "sagerouter.dev",
    "www.sagerouter.dev",
    "app.sagerouter.dev",
    "localhost",
    "127.0.0.1",
}

HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
}
EDGE_OWNED_RESPONSE_HEADERS = {
    "access-control-allow-origin",
    "access-control-allow-methods",
    "access-control-allow-headers",
    "access-control-max-age",
    "access-control-allow-credentials",
}

AUTH_CACHE = {}
AUTH_CACHE_LOCK = threading.Lock()
RATE_LIMIT_BUCKETS = {}
RATE_LIMIT_LOCK = threading.Lock()
MODEL_MODALITY_VALUES = {"text", "image", "audio", "video", "document"}


class Upstream:
    def __init__(self, raw_url):
        raw_url = raw_url.rstrip("/")
        parsed = urlsplit(raw_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError(f"invalid upstream {raw_url!r}: use http:// or https://")
        self.raw_url = raw_url
        self.scheme = parsed.scheme
        self.host = parsed.hostname
        self.port = parsed.port or (443 if parsed.scheme == "https" else 80)
        self.path_prefix = parsed.path.rstrip("/")
        self.healthy = False
        self.latency_ms = None
        self.last_checked = 0.0
        self.last_error = "not checked"
        self.lock = threading.Lock()

    @property
    def hostport(self):
        return f"{self.host}:{self.port}"

    def connection(self, timeout):
        if self.scheme == "https":
            return HTTPSConnection(self.host, self.port, timeout=timeout, context=ssl.create_default_context())
        return HTTPConnection(self.host, self.port, timeout=timeout)

    def target_path(self, request_path):
        if not self.path_prefix:
            return request_path
        if request_path.startswith("/"):
            return f"{self.path_prefix}{request_path}"
        return f"{self.path_prefix}/{request_path}"

    def snapshot(self):
        with self.lock:
            return {
                "url": self.raw_url,
                "healthy": self.healthy,
                "latency_ms": self.latency_ms,
                "last_checked": self.last_checked,
                "last_error": self.last_error,
            }

    def set_health(self, healthy, latency_ms=None, error=""):
        with self.lock:
            self.healthy = healthy
            self.latency_ms = latency_ms
            self.last_checked = time.time()
            self.last_error = error


def parse_upstreams(raw):
    upstreams = []
    for item in raw.replace(" ", ",").split(","):
        item = item.strip()
        if item:
            upstreams.append(Upstream(item))
    if not upstreams:
        raise SystemExit("SAGE_ROUTER_UPSTREAMS is required, for example: http://cyber.tailnet.ts.net:8790,http://umbrel.tailnet.ts.net:8790")
    return upstreams


UPSTREAMS = parse_upstreams(UPSTREAMS_RAW)
CONTROL_PLANE_UPSTREAM = Upstream(CONTROL_PLANE_UPSTREAM_RAW) if CONTROL_PLANE_UPSTREAM_RAW else None


def bearer_token(headers):
    auth = headers.get("Authorization", "") or ""
    return auth[7:].strip() if auth.lower().startswith("bearer ") else ""


def token_matches(token, allowed):
    return bool(token and allowed and hmac.compare_digest(token, allowed))


def api_key_hash(raw_key):
    return hashlib.sha256((API_KEY_HASH_PEPPER + raw_key).encode("utf-8")).hexdigest()


def customer_is_active(customer):
    status = str((customer or {}).get("status") or "").lower()
    plan = str((customer or {}).get("plan") or "").lower()
    return status in {"active", "trialing", "manual", "paid"} and plan not in {"", "free", "inactive"}


def parse_rate_limits(raw):
    limits = {}
    for item in (raw or "").replace(" ", ",").split(","):
        item = item.strip()
        if not item:
            continue
        if "=" in item:
            key, value = item.split("=", 1)
        elif ":" in item:
            key, value = item.split(":", 1)
        else:
            continue
        key = key.strip().lower()
        try:
            limit = int(value.strip())
        except ValueError:
            continue
        if key and limit >= 0:
            limits[key] = limit
    limits.setdefault("default", 60)
    return limits


RATE_LIMITS_BY_PLAN = parse_rate_limits(RATE_LIMITS_RAW)
MONTHLY_QUOTAS_BY_PLAN = parse_rate_limits(MONTHLY_QUOTAS_RAW)


def rate_limit_plan(auth_context):
    plan = str((auth_context or {}).get("plan") or "").strip().lower()
    status = str((auth_context or {}).get("customer_status") or "").strip().lower()
    if plan and plan in RATE_LIMITS_BY_PLAN:
        return plan
    if status and status in RATE_LIMITS_BY_PLAN:
        return status
    return "default"


def plan_limit(auth_context, limits):
    plan = str((auth_context or {}).get("plan") or "").strip().lower()
    status = str((auth_context or {}).get("customer_status") or "").strip().lower()
    if plan and plan in limits:
        return plan, limits[plan]
    if status and status in limits:
        return status, limits[status]
    return "default", limits.get("default", 0)


def rate_limit_identity(auth_context):
    auth_type = str((auth_context or {}).get("type") or "")
    if auth_type in {"edge_token", "public", "public_control_plane", "public_signed_backend", "disabled"}:
        return None
    if auth_type == "generated_key":
        key_id = (auth_context or {}).get("key_id")
        customer_id = (auth_context or {}).get("customer_id")
        user_id = (auth_context or {}).get("user_id")
        return f"api-key:{key_id or customer_id or user_id or 'unknown'}"
    if auth_type == "supabase_user":
        return f"user:{(auth_context or {}).get('user_id') or 'unknown'}"
    return None


def path_rate_segment(path):
    clean_path = urlsplit(path).path
    return clean_path.split("/", 2)[1] if clean_path.startswith("/") else ""


def check_fixed_window_rate_limit(identity, plan, limit, path):
    now = time.time()
    window = int(now // RATE_LIMIT_WINDOW_SECONDS)
    bucket_key = (identity, plan, path_rate_segment(path))
    reset_at = (window + 1) * RATE_LIMIT_WINDOW_SECONDS
    with RATE_LIMIT_LOCK:
        if len(RATE_LIMIT_BUCKETS) > 20000:
            stale_before = window - 2
            for key, value in list(RATE_LIMIT_BUCKETS.items()):
                if value[0] <= stale_before:
                    RATE_LIMIT_BUCKETS.pop(key, None)
        current_window, count = RATE_LIMIT_BUCKETS.get(bucket_key, (window, 0))
        if current_window != window:
            count = 0
            current_window = window
        if limit <= 0 or count >= limit:
            RATE_LIMIT_BUCKETS[bucket_key] = (current_window, count)
            return False, {
                "limit": limit,
                "remaining": 0,
                "reset": int(reset_at),
                "retry_after": max(1, int(reset_at - now)),
            }
        count += 1
        RATE_LIMIT_BUCKETS[bucket_key] = (current_window, count)
        return True, {
            "limit": limit,
            "remaining": max(0, limit - count),
            "reset": int(reset_at),
            "retry_after": max(1, int(reset_at - now)),
        }


def check_rate_limit(auth_context, path):
    if not RATE_LIMIT_ENABLED:
        return True, None
    if RATE_LIMIT_WINDOW_SECONDS <= 0:
        return True, None
    identity = rate_limit_identity(auth_context)
    if not identity:
        return True, None
    plan = rate_limit_plan(auth_context)
    limit = RATE_LIMITS_BY_PLAN.get(plan, RATE_LIMITS_BY_PLAN.get("default", 60))
    return check_fixed_window_rate_limit(identity, plan, limit, path)


def first_client_ip_from_header(value):
    for item in str(value or "").split(","):
        item = item.strip()
        if item:
            return item
    return ""


def client_ip_for_rate_limit(handler):
    if TRUST_CLIENT_IP_HEADERS:
        for header in CLIENT_IP_HEADERS:
            value = handler.headers.get(header)
            ip = first_client_ip_from_header(value)
            if ip:
                return ip
    client_address = getattr(handler, "client_address", None) or ()
    return str(client_address[0] if client_address else "unknown")


def should_rate_limit_auth_attempt(handler):
    if not RATE_LIMIT_ENABLED or RATE_LIMIT_WINDOW_SECONDS <= 0 or AUTH_ATTEMPT_RATE_LIMIT_PER_WINDOW <= 0:
        return False
    if EDGE_AUTH_MODE not in {"supabase", "saas"}:
        return False
    if not is_generated_api_key_path(handler.path):
        return False
    token = bearer_token(handler.headers)
    if token_matches(token, EDGE_TOKEN):
        return False
    return token.startswith(API_KEY_PREFIX)


def check_auth_attempt_rate_limit(handler):
    if not should_rate_limit_auth_attempt(handler):
        return True, None
    identity = f"auth-attempt:{client_ip_for_rate_limit(handler)}"
    return check_fixed_window_rate_limit(
        identity,
        "auth_attempt",
        AUTH_ATTEMPT_RATE_LIMIT_PER_WINDOW,
        handler.path,
    )


def current_usage_period(now=None):
    return time.strftime("%Y-%m", time.gmtime(now or time.time()))


def quota_reset_epoch(period):
    try:
        year, month = [int(part) for part in str(period or "").split("-", 1)]
    except ValueError:
        return None
    if month < 1 or month > 12:
        return None
    if month == 12:
        year += 1
        month = 1
    else:
        month += 1
    return calendar.timegm((year, month, 1, 0, 0, 0, 0, 1, 0))


def should_count_quota(auth_context, path):
    if not QUOTA_ENABLED:
        return False
    if str((auth_context or {}).get("type") or "") != "generated_key":
        return False
    clean_path = urlsplit(path).path
    return clean_path == "/v1" or clean_path.startswith("/v1/")


def quota_headers(state):
    if not state:
        return {}
    headers = {
        "X-Quota-Period": state.get("period", ""),
        "X-Quota-Limit": state.get("quota", ""),
        "X-Quota-Used": state.get("requests", ""),
        "X-Quota-Remaining": state.get("remaining", ""),
        "X-Quota-Reset": state.get("reset_epoch", ""),
    }
    return {key: value for key, value in headers.items() if value != ""}


def check_usage_quota(auth_context, path):
    if not should_count_quota(auth_context, path):
        return True, None
    plan, quota = plan_limit(auth_context, MONTHLY_QUOTAS_BY_PLAN)
    if quota <= 0:
        return True, None
    period = current_usage_period()
    reset_epoch = quota_reset_epoch(period)
    if not supabase_auth_configured(require_service=True):
        return False, {
            "error": "edge_quota_not_configured",
            "plan": plan,
            "quota": quota,
            "remaining": 0,
            "period": period,
            "reset_epoch": reset_epoch,
        }

    payload = {
        "p_customer_id": str(auth_context.get("customer_id") or ""),
        "p_user_id": str(auth_context.get("user_id") or ""),
        "p_plan": str(auth_context.get("plan") or plan),
        "p_period": period,
        "p_increment": 1,
        "p_quota": quota,
    }
    if not payload["p_customer_id"]:
        return False, {
            "error": "edge_quota_missing_customer",
            "plan": plan,
            "quota": quota,
            "remaining": 0,
            "period": payload["p_period"],
            "reset_epoch": reset_epoch,
        }
    try:
        result = supabase_post_json(f"/rest/v1/rpc/{SUPABASE_USAGE_RPC}", payload, timeout=6)
        row = result[0] if isinstance(result, list) and result else result
        if not isinstance(row, dict):
            raise ValueError("usage RPC returned no row")
        state = {
            "customer_id": row.get("customer_id") or payload["p_customer_id"],
            "period": row.get("period") or payload["p_period"],
            "plan": plan,
            "requests": int(row.get("requests") or 0),
            "quota": int(row.get("quota") or quota),
            "remaining": max(0, int(row.get("remaining") or 0)),
            "allowed": bool(row.get("allowed")),
        }
        state["reset_epoch"] = quota_reset_epoch(state["period"])
        return state["allowed"], state
    except Exception as exc:
        print(f"supabase usage quota check failed: {exc}", flush=True)
        return False, {
            "error": "edge_quota_unavailable",
            "plan": plan,
            "quota": quota,
            "remaining": 0,
            "period": payload["p_period"],
            "reset_epoch": reset_epoch,
        }


def supabase_headers(service=False, token=None):
    key = SUPABASE_SERVICE_ROLE_KEY if service else SUPABASE_ANON_KEY
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {token or key}",
        "Accept": "application/json",
    }
    return headers


def supabase_get_json(path, service=False, token=None, timeout=6):
    req = urllib.request.Request(SUPABASE_URL.rstrip("/") + path, headers=supabase_headers(service=service, token=token))
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def supabase_patch_json(path, payload, timeout=4):
    data = json.dumps(payload).encode("utf-8")
    headers = supabase_headers(service=True)
    headers["Content-Type"] = "application/json"
    req = urllib.request.Request(SUPABASE_URL.rstrip("/") + path, data=data, method="PATCH", headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        resp.read(4096)


def supabase_post_json(path, payload, timeout=6):
    data = json.dumps(payload).encode("utf-8")
    headers = supabase_headers(service=True)
    headers["Content-Type"] = "application/json"
    req = urllib.request.Request(SUPABASE_URL.rstrip("/") + path, data=data, method="POST", headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8")
        return json.loads(body) if body else {}


def normalize_model_modalities(modalities):
    return sorted({
        str(modality).strip().lower()
        for modality in (modalities or [])
        if str(modality).strip().lower() in MODEL_MODALITY_VALUES
    })


def request_modalities_from_body(body):
    modalities = {"text"}
    if not body:
        return sorted(modalities)
    try:
        payload = json.loads(body.decode("utf-8") if isinstance(body, (bytes, bytearray)) else str(body))
    except Exception:
        return sorted(modalities)

    def visit(value):
        if isinstance(value, dict):
            lowered_keys = {str(key).lower() for key in value.keys()}
            type_value = str(value.get("type") or "").lower()
            if type_value in {"image_url", "input_image"} or "image_url" in lowered_keys:
                modalities.add("image")
            if type_value in {"input_audio", "audio"} or "audio_url" in lowered_keys or "input_audio" in lowered_keys:
                modalities.add("audio")
            if type_value in {"input_video", "video"} or "video_url" in lowered_keys or "input_video" in lowered_keys:
                modalities.add("video")
            if type_value in {"input_file", "file", "document"} or "file_id" in lowered_keys or "document" in lowered_keys:
                modalities.add("document")
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)
        elif isinstance(value, str):
            lowered = value.lower()
            if lowered.startswith("data:image/"):
                modalities.add("image")
            elif lowered.startswith("data:audio/"):
                modalities.add("audio")
            elif lowered.startswith("data:video/"):
                modalities.add("video")

    visit(payload)
    return sorted(modalities)


def modality_record_from_response(response_headers, status, request_body=None, response_body=None):
    if not (MODEL_MODALITIES_SHARED_ENABLED and 200 <= int(status or 0) < 300 and supabase_auth_configured(require_service=True)):
        return None
    headers = {str(key).lower(): str(value) for key, value in (response_headers or [])}
    provider = (
        headers.get("x-sage-router-upstream-provider", "").strip()
        or headers.get("x-sage-router-provider", "").strip()
    )
    model = (
        headers.get("x-sage-router-upstream-model-name", "").strip()
        or headers.get("x-sage-router-model-name", "").strip()
    )
    if not model:
        model_header = (
            headers.get("x-sage-router-upstream-model", "").strip()
            or headers.get("x-sage-router-model", "").strip()
        )
        if "/" in model_header:
            provider_from_model, model_from_header = model_header.split("/", 1)
            provider = provider or provider_from_model.strip()
            model = model_from_header.strip()
        else:
            model = model_header
    modalities = normalize_model_modalities((headers.get("x-sage-router-modalities", "") or "").split(","))
    if (not provider or not model) and response_body:
        try:
            payload = json.loads(response_body.decode("utf-8") if isinstance(response_body, (bytes, bytearray)) else str(response_body))
            model_header = str(payload.get("model") or "").strip() if isinstance(payload, dict) else ""
            if "/" in model_header:
                provider_from_model, model_from_header = model_header.split("/", 1)
                provider = provider or provider_from_model.strip()
                model = model or model_from_header.strip()
            elif model_header:
                model = model or model_header
        except Exception:
            pass
    if not modalities:
        modalities = request_modalities_from_body(request_body)
    if not (provider and model and modalities):
        return None
    return {"provider": provider, "model": model, "modalities": modalities}


def record_model_modalities(record):
    if not record:
        return

    def _record():
        try:
            supabase_post_json(
                f"/rest/v1/rpc/{SUPABASE_MODEL_MODALITIES_RPC}",
                {
                    "provider_name": record["provider"],
                    "model_name": record["model"],
                    "modalities_in": record["modalities"],
                    "seen_at_epoch_ms": int(time.time() * 1000),
                },
                timeout=6,
            )
        except Exception as exc:
            print(f"supabase model modality edge record failed: {exc}", flush=True)

    threading.Thread(target=_record, daemon=True).start()


def record_model_modalities_from_response_headers(response_headers, status):
    record_model_modalities(modality_record_from_response(response_headers, status))


def should_buffer_response_for_modality(response_headers, status):
    if not (MODEL_MODALITIES_SHARED_ENABLED and 200 <= int(status or 0) < 300):
        return False
    headers = {str(key).lower(): str(value) for key, value in (response_headers or [])}
    if headers.get("x-sage-router-provider") and (headers.get("x-sage-router-model-name") or headers.get("x-sage-router-model")) and headers.get("x-sage-router-modalities"):
        return False
    content_type = headers.get("content-type", "").lower()
    if "application/json" not in content_type:
        return False
    if "content-encoding" in headers:
        return False
    try:
        content_length = int(headers.get("content-length") or "0")
    except ValueError:
        return False
    return 0 < content_length <= MAX_MODALITY_LEARN_BODY_BYTES


def response_is_uncompressed_json(response_headers, status):
    if not (200 <= int(status or 0) < 300):
        return False
    headers = {str(key).lower(): str(value) for key, value in (response_headers or [])}
    if "application/json" not in headers.get("content-type", "").lower():
        return False
    return "content-encoding" not in headers


def response_is_uncompressed_event_stream(response_headers, status):
    if not (200 <= int(status or 0) < 300):
        return False
    headers = {str(key).lower(): str(value) for key, value in (response_headers or [])}
    if "text/event-stream" not in headers.get("content-type", "").lower():
        return False
    return "content-encoding" not in headers


def router_profile_alias_from_body(path, body):
    if not (body and is_generated_api_key_path(path)):
        return ""
    try:
        payload = json.loads(body.decode("utf-8") if isinstance(body, (bytes, bytearray)) else str(body))
    except Exception:
        return ""
    if not isinstance(payload, dict):
        return ""
    model = str(payload.get("model") or "").strip()
    if model.startswith("sage-router/") or model.startswith("smart-router/"):
        return model
    return ""


def model_provider_and_name(model):
    value = str(model or "").strip()
    if "/" in value:
        provider, model_name = value.split("/", 1)
        return provider.strip(), model_name.strip()
    return "", value


MODEL_PREFIX_LABEL_RE = re.compile(r"^\[([A-Za-z0-9_.-]+/[^\]\s]+)\](?=\s|$)\s*")


def strip_leading_model_prefix_labels(text):
    remaining = str(text or "")
    changed = False
    while True:
        match = MODEL_PREFIX_LABEL_RE.match(remaining.lstrip())
        if not match:
            break
        stripped = remaining.lstrip()
        leading_ws = remaining[:len(remaining) - len(stripped)]
        remaining = leading_ws + stripped[match.end():].lstrip()
        changed = True
    return remaining.strip() if changed else remaining


def sanitize_visible_response_payload(payload):
    if not isinstance(payload, dict):
        return payload
    if isinstance(payload.get("output_text"), str):
        payload["output_text"] = strip_leading_model_prefix_labels(payload.get("output_text"))
    for choice in payload.get("choices") or []:
        if not isinstance(choice, dict):
            continue
        for container_key in ("message", "delta"):
            container = choice.get(container_key)
            if isinstance(container, dict) and isinstance(container.get("content"), str):
                container["content"] = strip_leading_model_prefix_labels(container.get("content"))
    for output_item in payload.get("output") or []:
        if not isinstance(output_item, dict):
            continue
        for part in output_item.get("content") or []:
            if isinstance(part, dict) and isinstance(part.get("text"), str):
                part["text"] = strip_leading_model_prefix_labels(part.get("text"))
    for part in payload.get("content") or []:
        if isinstance(part, dict) and isinstance(part.get("text"), str):
            part["text"] = strip_leading_model_prefix_labels(part.get("text"))
    return payload


def sanitize_visible_sse_payload(payload):
    if not isinstance(payload, dict):
        return payload
    sanitize_visible_response_payload(payload)
    for key in ("delta", "text"):
        if isinstance(payload.get(key), str):
            payload[key] = strip_leading_model_prefix_labels(payload.get(key))
    for key in ("part", "item", "response"):
        nested = payload.get(key)
        if isinstance(nested, dict):
            sanitize_visible_sse_payload(nested)
    return payload


def sanitize_router_profile_sse_line(raw_line):
    line = raw_line.decode("utf-8", errors="replace") if isinstance(raw_line, (bytes, bytearray)) else str(raw_line)
    if not line.startswith("data: "):
        return raw_line
    suffix = "\n" if line.endswith("\n") else ""
    data = line[len("data: "):].strip()
    if not data or data == "[DONE]":
        return raw_line
    try:
        payload = json.loads(data)
    except Exception:
        return raw_line
    if not isinstance(payload, dict):
        return raw_line
    payload = sanitize_visible_sse_payload(payload)
    return f"data: {json.dumps(payload, separators=(',', ':'))}{suffix}".encode("utf-8")


def rewrite_router_profile_stream_headers(path, request_body, response_headers):
    alias = router_profile_alias_from_body(path, request_body)
    if not alias:
        return response_headers
    headers = {str(key).lower(): str(value) for key, value in (response_headers or [])}
    upstream_model = (
        headers.get("x-sage-router-upstream-model", "").strip()
        or headers.get("x-sage-router-model", "").strip()
    )
    upstream_provider = headers.get("x-sage-router-upstream-provider", "").strip()
    upstream_model_name = headers.get("x-sage-router-upstream-model-name", "").strip()
    if upstream_model and (not upstream_provider or not upstream_model_name):
        parsed_provider, parsed_model_name = model_provider_and_name(upstream_model)
        upstream_provider = upstream_provider or parsed_provider
        upstream_model_name = upstream_model_name or parsed_model_name
    upstream_provider = upstream_provider or headers.get("x-sage-router-provider", "").strip()
    upstream_model_name = upstream_model_name or headers.get("x-sage-router-model-name", "").strip()

    alias_provider, alias_model_name = model_provider_and_name(alias)
    rewrite_header_names = {
        "content-length",
        "x-sage-router-model",
        "x-sage-router-provider",
        "x-sage-router-model-name",
        "x-sage-router-upstream-model",
        "x-sage-router-upstream-provider",
        "x-sage-router-upstream-model-name",
    }
    replaced_headers = [
        (key, value)
        for key, value in (response_headers or [])
        if str(key).lower() not in rewrite_header_names
    ]
    replaced_headers.extend([
        ("X-Sage-Router-Model", alias),
        ("X-Sage-Router-Provider", alias_provider),
        ("X-Sage-Router-Model-Name", alias_model_name),
    ])
    if upstream_model:
        replaced_headers.append(("X-Sage-Router-Upstream-Model", upstream_model))
    if upstream_provider:
        replaced_headers.append(("X-Sage-Router-Upstream-Provider", upstream_provider))
    if upstream_model_name:
        replaced_headers.append(("X-Sage-Router-Upstream-Model-Name", upstream_model_name))
    return replaced_headers


def rewrite_router_profile_response(path, request_body, response_headers, status, response_body):
    alias = router_profile_alias_from_body(path, request_body)
    if not (alias and response_is_uncompressed_json(response_headers, status) and response_body):
        return response_headers, response_body
    try:
        payload = json.loads(response_body.decode("utf-8") if isinstance(response_body, (bytes, bytearray)) else str(response_body))
    except Exception:
        return response_headers, response_body
    if not isinstance(payload, dict):
        return response_headers, response_body
    payload = sanitize_visible_response_payload(payload)

    headers = {str(key).lower(): str(value) for key, value in (response_headers or [])}
    body_model = str(payload.get("model") or "").strip()
    upstream_model = (
        headers.get("x-sage-router-upstream-model", "").strip()
        or headers.get("x-sage-router-model", "").strip()
        or body_model
    )
    upstream_provider = headers.get("x-sage-router-upstream-provider", "").strip()
    upstream_model_name = headers.get("x-sage-router-upstream-model-name", "").strip()
    if upstream_model and (not upstream_provider or not upstream_model_name):
        parsed_provider, parsed_model_name = model_provider_and_name(upstream_model)
        upstream_provider = upstream_provider or parsed_provider
        upstream_model_name = upstream_model_name or parsed_model_name
    upstream_provider = upstream_provider or headers.get("x-sage-router-provider", "").strip()
    upstream_model_name = upstream_model_name or headers.get("x-sage-router-model-name", "").strip()

    if body_model and body_model != alias and "upstream_model" not in payload:
        payload["upstream_model"] = body_model
    payload["model"] = alias
    transformed_body = json.dumps(payload, separators=(",", ":")).encode("utf-8")

    alias_provider, alias_model_name = model_provider_and_name(alias)
    replaced_headers = []
    rewrite_header_names = {
        "content-length",
        "x-sage-router-model",
        "x-sage-router-provider",
        "x-sage-router-model-name",
        "x-sage-router-upstream-model",
        "x-sage-router-upstream-provider",
        "x-sage-router-upstream-model-name",
    }
    for key, value in (response_headers or []):
        if str(key).lower() not in rewrite_header_names:
            replaced_headers.append((key, value))
    replaced_headers.extend([
        ("X-Sage-Router-Model", alias),
        ("X-Sage-Router-Provider", alias_provider),
        ("X-Sage-Router-Model-Name", alias_model_name),
    ])
    if upstream_model:
        replaced_headers.append(("X-Sage-Router-Upstream-Model", upstream_model))
    if upstream_provider:
        replaced_headers.append(("X-Sage-Router-Upstream-Provider", upstream_provider))
    if upstream_model_name:
        replaced_headers.append(("X-Sage-Router-Upstream-Model-Name", upstream_model_name))
    return replaced_headers, transformed_body


def should_buffer_response_for_edge_transform(path, response_headers, status):
    if not (is_launch_funnel_path(path) and response_is_uncompressed_json(response_headers, status)):
        return False
    headers = {str(key).lower(): str(value) for key, value in (response_headers or [])}
    try:
        content_length = int(headers.get("content-length") or "0")
    except ValueError:
        return False
    return 0 < content_length <= MAX_MODALITY_LEARN_BODY_BYTES


def launch_auth_provider_state_from_marketing(marketing_metrics):
    base = {
        "total": 0,
        "loaded": 0,
        "unavailable": 0,
        "unknown": 0,
        "githubEnabled": 0,
        "githubDisabled": 0,
        "enabledProviders": {"github": 0, "google": 0, "discord": 0, "none": 0, "other": 0},
        "disabledProviders": {"github": 0, "google": 0, "discord": 0, "none": 0, "other": 0},
    }
    source = "unavailable"
    if isinstance(marketing_metrics, dict) and isinstance(marketing_metrics.get("authProviderState"), dict):
        raw = marketing_metrics.get("authProviderState") or {}
        source = "marketing_funnel" if int(raw.get("total") or 0) > 0 else "marketing_funnel_empty"
        for key, value in raw.items():
            if key not in {"enabledProviders", "disabledProviders"}:
                base[key] = value
        if isinstance(raw.get("enabledProviders"), dict):
            base["enabledProviders"].update(raw.get("enabledProviders") or {})
        if isinstance(raw.get("disabledProviders"), dict):
            base["disabledProviders"].update(raw.get("disabledProviders") or {})
    github_available = int(base.get("githubEnabled") or 0) > 0 and int(base.get("githubEnabled") or 0) >= int(base.get("githubDisabled") or 0)
    base.update({
        "source": source,
        "githubAvailable": github_available,
        "recommendedRecoveryAuth": "email_first",
        "operatorGuidance": (
            "Use email/password recovery first; GitHub/OAuth is available only when it is the same signup account."
            if github_available
            else "Use email/password recovery first; do not rely on GitHub/OAuth until provider state is observed healthy."
        ),
    })
    return base


def transform_edge_response_body(path, response_headers, status, body):
    if not (body and should_buffer_response_for_edge_transform(path, response_headers, status)):
        return body
    try:
        payload = json.loads(body.decode("utf-8"))
    except Exception:
        return body
    if not isinstance(payload, dict):
        return body
    if isinstance(payload.get("authProviderState"), dict):
        return body
    marketing_metrics = payload.get("marketingIntent") if isinstance(payload.get("marketingIntent"), dict) else {}
    payload["authProviderState"] = launch_auth_provider_state_from_marketing(marketing_metrics)
    return json.dumps(payload, separators=(",", ":")).encode("utf-8")


def cache_get(key):
    now = time.time()
    with AUTH_CACHE_LOCK:
        item = AUTH_CACHE.get(key)
        if item and item[0] > now:
            return item[1]
        if item:
            AUTH_CACHE.pop(key, None)
    return None


def cache_set(key, value, ttl_seconds=None):
    ttl_seconds = AUTH_CACHE_TTL_SECONDS if ttl_seconds is None else ttl_seconds
    if ttl_seconds <= 0:
        return value
    with AUTH_CACHE_LOCK:
        AUTH_CACHE[key] = (time.time() + ttl_seconds, value)
    return value


def cache_api_key_auth(cache_key, value):
    return cache_set(cache_key, value, API_KEY_AUTH_CACHE_TTL_SECONDS)


def supabase_auth_configured(require_service=False):
    if not (SUPABASE_URL and SUPABASE_ANON_KEY):
        return False
    return bool(SUPABASE_SERVICE_ROLE_KEY) if require_service else True


def verify_supabase_user_jwt(token):
    if not token or not supabase_auth_configured():
        return None
    cache_key = f"user:{hashlib.sha256(token.encode('utf-8')).hexdigest()}"
    cached = cache_get(cache_key)
    if cached is not None:
        return cached
    try:
        user = supabase_get_json("/auth/v1/user", service=False, token=token)
        if isinstance(user, dict) and user.get("id"):
            return cache_set(cache_key, {"type": "supabase_user", "user_id": user.get("id"), "preserve_authorization": True})
    except Exception as exc:
        print(f"supabase user auth failed: {exc}", flush=True)
    return cache_set(cache_key, False)


def verify_supabase_generated_key(token):
    if not token or not token.startswith(API_KEY_PREFIX) or not supabase_auth_configured(require_service=True):
        return None
    digest = api_key_hash(token)
    cache_key = f"api-key:{digest}"
    if API_KEY_AUTH_CACHE_TTL_SECONDS > 0:
        cached = cache_get(cache_key)
        if cached is not None:
            return cached
    try:
        quoted_digest = urllib.parse.quote(digest, safe="")
        key_rows = supabase_get_json(
            f"/rest/v1/{SUPABASE_API_KEYS_TABLE}?select=*&api_key_hash=eq.{quoted_digest}&status=eq.active&limit=1",
            service=True,
        )
        if not key_rows:
            return cache_api_key_auth(cache_key, False)
        key = key_rows[0]
        quoted_customer_id = urllib.parse.quote(str(key.get("customer_id") or ""), safe="")
        customer_rows = supabase_get_json(
            f"/rest/v1/{SUPABASE_CUSTOMERS_TABLE}?select=*&id=eq.{quoted_customer_id}&limit=1",
            service=True,
        )
        customer = customer_rows[0] if customer_rows else None
        if not customer_is_active(customer):
            return cache_api_key_auth(cache_key, False)
        key_id = urllib.parse.quote(str(key.get("id") or ""), safe="")
        if key_id:
            try:
                supabase_patch_json(f"/rest/v1/{SUPABASE_API_KEYS_TABLE}?id=eq.{key_id}", {"last_used_at_epoch": int(time.time())})
            except Exception as exc:
                print(f"supabase last-used update failed: {exc}", flush=True)
        return cache_api_key_auth(cache_key, {
            "type": "generated_key",
            "key_id": key.get("id"),
            "customer_id": customer.get("id"),
            "user_id": customer.get("user_id"),
            "plan": customer.get("plan"),
            "customer_status": customer.get("status"),
            "preserve_authorization": False,
        })
    except Exception as exc:
        print(f"supabase api key auth failed: {exc}", flush=True)
        return cache_api_key_auth(cache_key, False)


def is_user_jwt_path(path):
    clean_path = urlsplit(path).path
    return any(clean_path == prefix or clean_path.startswith(prefix + "/") for prefix in USER_JWT_PREFIXES)


def is_generated_api_key_path(path):
    clean_path = urlsplit(path).path
    return any(clean_path == prefix or clean_path.startswith(prefix + "/") for prefix in GENERATED_API_KEY_PREFIXES)


def should_retry_upstream_status(path, status):
    if status in RETRY_STATUSES:
        return True
    return status in MODEL_API_STALE_ROUTE_RETRY_STATUSES and is_generated_api_key_path(path)


def is_public_control_plane_path(path):
    return urlsplit(path).path in PUBLIC_CONTROL_PLANE_PATHS


def is_model_catalog_control_plane_path(path):
    clean_path = urlsplit(path).path
    return clean_path == "/v1/models" or clean_path.startswith("/v1/models/")


def is_operator_control_plane_path(path):
    clean_path = urlsplit(path).path
    return any(clean_path == prefix or clean_path.startswith(prefix + "/") for prefix in OPERATOR_CONTROL_PLANE_PREFIXES)


def is_operator_analytics_path(path):
    clean_path = urlsplit(path).path
    return clean_path == "/analytics" or clean_path.startswith("/analytics/")


def is_launch_funnel_path(path):
    return urlsplit(path).path == "/analytics/funnel"


def is_public_signed_backend_path(path):
    clean_path = urlsplit(path).path
    return any(clean_path == prefix or clean_path.startswith(prefix + "/") for prefix in PUBLIC_SIGNED_BACKEND_PREFIXES)


def is_public_api_browser_path(path):
    clean_path = urlsplit(path).path or "/"
    return clean_path in {"/", "/dashboard"} or clean_path.startswith("/dashboard/")


def normalize_browser_origin(value):
    value = str(value or "").strip()
    if not value:
        return ""
    parsed = urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return ""
    hostname = parsed.hostname or ""
    if not hostname:
        return ""
    port = parsed.port
    default_port = 443 if parsed.scheme == "https" else 80
    hostport = hostname.lower()
    if port and port != default_port:
        hostport = f"{hostport}:{port}"
    return f"{parsed.scheme}://{hostport}"


def configured_browser_allowed_origins():
    allowed = set()
    for value in (
        CORS_ORIGINS
        + [BROWSER_ALLOWED_ORIGINS_RAW, ACCOUNT_URL, LOGIN_URL, PRICING_URL, STATUS_URL, API_BASE_URL]
    ):
        for item in str(value or "").split(","):
            normalized = normalize_browser_origin(item)
            if normalized and "*" not in normalized:
                allowed.add(normalized)
    return allowed


def edge_cors_state():
    cors_wildcard_allowed = "*" in CORS_ORIGINS
    return {
        "corsWildcardAllowed": cors_wildcard_allowed,
        "corsExplicitOriginRequired": not cors_wildcard_allowed,
        "corsAllowedOriginsCount": len(configured_browser_allowed_origins()),
    }


def browser_origin_allowed(origin):
    normalized = normalize_browser_origin(origin)
    if not normalized:
        return True
    if normalized in configured_browser_allowed_origins():
        return True
    parsed = urlsplit(normalized)
    host = (parsed.hostname or "").lower()
    return host in DEFAULT_BROWSER_ALLOWED_ORIGIN_HOSTS or host.endswith(".sage-router-web.pages.dev")


def is_browser_account_billing_mutation(path, method):
    if str(method or "").upper() != "POST":
        return False
    clean_path = urlsplit(path).path
    if clean_path == "/account/api-keys":
        return True
    if clean_path.startswith("/account/api-keys/") and clean_path.endswith("/revoke"):
        return True
    if clean_path in {
        "/billing/stripe/checkout",
        "/billing/stripe/portal",
        "/billing/crypto/intent",
    }:
        return True
    if clean_path.startswith("/admin/payment-intents/") and clean_path.endswith("/approve"):
        return True
    return clean_path.startswith("/admin/customers/") and (
        clean_path.endswith("/suspend") or clean_path.endswith("/unsuspend")
    )


def drain_rejected_request_body(handler):
    content_length = handler.headers.get("Content-Length")
    if not content_length:
        return
    try:
        remaining = int(content_length)
    except ValueError:
        handler.close_connection = True
        return
    if remaining < 0 or remaining > MAX_REJECTED_BODY_DRAIN_BYTES:
        handler.close_connection = True
        return
    while remaining > 0:
        chunk = handler.rfile.read(min(READ_CHUNK_SIZE, remaining))
        if not chunk:
            handler.close_connection = True
            return
        remaining -= len(chunk)


def should_use_control_plane(path):
    return (
        is_user_jwt_path(path)
        or is_public_control_plane_path(path)
        or is_model_catalog_control_plane_path(path)
        or is_operator_control_plane_path(path)
        or is_public_signed_backend_path(path)
        or is_public_api_browser_path(path)
    )


def outbound_bearer_token(path, auth_context, upstream=None):
    if auth_context.get("preserve_authorization"):
        return None
    if is_model_catalog_control_plane_path(path) and auth_context.get("type") == "generated_key":
        return None
    if (should_use_control_plane(path) or (upstream is not None and upstream is CONTROL_PLANE_UPSTREAM)) and CONTROL_PLANE_TOKEN:
        return CONTROL_PLANE_TOKEN
    return BACKEND_TOKEN


def edge_error_payload(error, path, message=None, **extra):
    payload = {"error": error}
    if message:
        payload["message"] = message
    if is_generated_api_key_path(path):
        payload["accountUrl"] = ACCOUNT_URL
        payload["pricingUrl"] = PRICING_URL
        payload["statusUrl"] = STATUS_URL
        payload["openaiBaseUrl"] = API_BASE_URL.rstrip("/") + "/v1"
        payload["apiKeyPrefix"] = API_KEY_PREFIX
    elif is_user_jwt_path(path):
        payload["loginUrl"] = LOGIN_URL
        payload["accountUrl"] = ACCOUNT_URL
    elif error == "unauthorized" and is_public_api_browser_path(path):
        payload["apiOnly"] = True
        payload["loginUrl"] = LOGIN_URL
        payload["accountUrl"] = ACCOUNT_URL
        payload["statusUrl"] = STATUS_URL
        payload["openaiBaseUrl"] = API_BASE_URL.rstrip("/") + "/v1"
    if extra:
        payload.update({key: value for key, value in extra.items() if value is not None})
    return payload


def append_query(url, **params):
    parsed = urllib.parse.urlsplit(url)
    current = dict(urllib.parse.parse_qsl(parsed.query, keep_blank_values=True))
    current.update({key: value for key, value in params.items() if value not in {None, ""}})
    query = urllib.parse.urlencode(current)
    return urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, query, parsed.fragment))


def quota_recovery_payload(error, path, quota_state, auth_context=None):
    quota_state = quota_state or {}
    auth_context = auth_context or {}
    plan = str(quota_state.get("plan") or auth_context.get("plan") or "").strip().lower()
    reset_epoch = quota_state.get("reset_epoch") or quota_reset_epoch(quota_state.get("period"))
    is_edge_infra_error = str(error or "").startswith("edge_quota_")

    if is_edge_infra_error:
        message = (
            "Sage Router could not verify this account quota right now. "
            "Check the status page or contact support if the issue persists."
        )
    else:
        message = (
            "Monthly Sage Router quota is exhausted for this plan. "
            "Open the account page to upgrade, review billing, or contact support for overflow."
        )

    payload = edge_error_payload(
        error,
        path,
        message,
        plan=plan or None,
        period=quota_state.get("period"),
        quota=quota_state.get("quota"),
        used=quota_state.get("requests"),
        remaining=quota_state.get("remaining"),
        resetEpoch=reset_epoch,
        upgradeUrl=append_query(ACCOUNT_URL, upgrade="quota", plan=plan) if plan and not is_edge_infra_error else None,
        billingUrl=BILLING_URL,
        supportUrl=SUPPORT_URL,
    )
    if not is_edge_infra_error:
        payload["recovery"] = {
            "nextAction": "upgrade_or_contact_support",
            "upgradeUrl": payload.get("upgradeUrl"),
            "billingUrl": BILLING_URL,
            "supportUrl": SUPPORT_URL,
            "statusUrl": STATUS_URL,
        }
    return payload


def edge_error_headers(error, path):
    headers = {}
    if is_generated_api_key_path(path) or is_public_api_browser_path(path):
        headers["Link"] = (
            f'<{ACCOUNT_URL}>; rel="account", '
            f'<{PRICING_URL}>; rel="pricing", '
            f'<{STATUS_URL}>; rel="status"'
        )
    if error == "unauthorized" and is_generated_api_key_path(path):
        headers["WWW-Authenticate"] = (
            'Bearer realm="Sage Router", error="invalid_token", '
            'error_description="Use an active Sage Router API key from app.sagerouter.dev/account.html"'
        )
    return headers


def check_upstream(upstream):
    started = time.perf_counter()
    conn = None
    try:
        conn = upstream.connection(timeout=HEALTH_TIMEOUT)
        headers = {"User-Agent": "sage-router-tailnet-edge/1.0"}
        if BACKEND_TOKEN:
            headers["Authorization"] = f"Bearer {BACKEND_TOKEN}"
        conn.request("GET", upstream.target_path(HEALTH_PATH), headers=headers)
        resp = conn.getresponse()
        resp.read(4096)
        elapsed_ms = round((time.perf_counter() - started) * 1000, 2)
        if 200 <= resp.status < 300:
            upstream.set_health(True, elapsed_ms, "")
        else:
            upstream.set_health(False, elapsed_ms, f"HTTP {resp.status}")
    except Exception as exc:
        upstream.set_health(False, None, str(exc))
    finally:
        if conn:
            conn.close()


def health_loop():
    while True:
        threads = []
        for upstream in UPSTREAMS + ([CONTROL_PLANE_UPSTREAM] if CONTROL_PLANE_UPSTREAM else []):
            thread = threading.Thread(target=check_upstream, args=(upstream,), daemon=True)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join(timeout=HEALTH_TIMEOUT + 1)
        time.sleep(max(1.0, HEALTH_INTERVAL))


def choose_upstream():
    upstreams = healthy_upstreams()
    return upstreams[0] if upstreams else None


def healthy_upstreams():
    snapshots = []
    for upstream in UPSTREAMS:
        snap = upstream.snapshot()
        if snap["healthy"]:
            snapshots.append((snap["latency_ms"] if snap["latency_ms"] is not None else 999999, upstream))
    if snapshots:
        snapshots.sort(key=lambda item: item[0])
        return [upstream for _, upstream in snapshots]
    return []


def control_plane_upstreams():
    if not CONTROL_PLANE_UPSTREAM:
        return None
    snap = CONTROL_PLANE_UPSTREAM.snapshot()
    return [CONTROL_PLANE_UPSTREAM] if snap["healthy"] else []


def generated_api_key_upstreams(path):
    upstreams = healthy_upstreams()
    control_plane = control_plane_upstreams() or []
    if is_generated_api_key_path(path):
        for upstream in control_plane:
            if upstream not in upstreams:
                upstreams.append(upstream)
    return upstreams


def reroute_known_ollama_subscription_body(path, body):
    if not body or not is_generated_api_key_path(path) or not OLLAMA_SIBLING_REROUTE_MODELS:
        return body
    try:
        payload = json.loads(body.decode("utf-8"))
    except Exception:
        return body
    if not isinstance(payload, dict):
        return body
    model = str(payload.get("model") or "").strip()
    if not model.startswith("ollama/"):
        return body
    model_name = model.split("/", 1)[1].strip()
    if model_name not in OLLAMA_SIBLING_REROUTE_MODELS:
        return body
    payload["model"] = f"ollama-2/{model_name}"
    return json.dumps(payload, separators=(",", ":")).encode("utf-8")


def edge_enforcement_state():
    return {
        "rateLimitEnabled": RATE_LIMIT_ENABLED,
        "rateLimitWindowSeconds": RATE_LIMIT_WINDOW_SECONDS,
        "authAttemptRateLimit": AUTH_ATTEMPT_RATE_LIMIT_PER_WINDOW,
        "authAttemptRateLimitEnabled": RATE_LIMIT_ENABLED and RATE_LIMIT_WINDOW_SECONDS > 0 and AUTH_ATTEMPT_RATE_LIMIT_PER_WINDOW > 0,
        "browserOriginGuardEnabled": True,
        "trustClientIpHeaders": TRUST_CLIENT_IP_HEADERS,
        "quotaEnabled": QUOTA_ENABLED,
        "apiKeyAuthCacheSeconds": API_KEY_AUTH_CACHE_TTL_SECONDS,
        "apiKeyPrefix": API_KEY_PREFIX,
        **edge_cors_state(),
    }


def model_modalities_state():
    rpc_name = str(SUPABASE_MODEL_MODALITIES_RPC or "").strip()
    return {
        "sharedEnabled": bool(MODEL_MODALITIES_SHARED_ENABLED and supabase_auth_configured(require_service=True) and rpc_name),
        "supabaseConfigured": bool(SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY),
        "rpcConfigured": bool(rpc_name),
    }


def edge_failover_state():
    return {
        "mode": "lowest-latency-healthy",
        "healthyUpstreamCount": len(healthy_upstreams()),
        "controlPlanePinned": bool(CONTROL_PLANE_UPSTREAM),
        "retryEnabled": True,
        "retryStatuses": sorted(RETRY_STATUSES | MODEL_API_STALE_ROUTE_RETRY_STATUSES),
        "retryHeader": "X-Sage-Router-Retry-Count",
    }


def public_upstream_origin_kind(upstream):
    host = (upstream.host or "").lower()
    raw_url = (upstream.raw_url or "").lower()
    if host.endswith(".ts.net"):
        return "tailnet"
    if "run.app" in host or "cloudfunctions.net" in host or "googleapis.com" in host:
        return "cloud fallback"
    if host.endswith("sagerouter.dev"):
        return "public edge"
    if "localhost" in host or host.startswith("127.") or host.startswith("10.") or host.startswith("192.168."):
        return "private"
    if "tailnet" in raw_url:
        return "tailnet"
    return "custom"


def public_upstream_snapshot(upstream, index, label_prefix="Upstream"):
    snap = upstream.snapshot()
    origin_kind = public_upstream_origin_kind(upstream)
    public_id = "control-plane" if label_prefix == "Control plane" else f"upstream-{index + 1}"
    return {
        "id": public_id,
        "label": f"{label_prefix} {index + 1}" if label_prefix != "Control plane" else "Control plane",
        "originKind": origin_kind,
        "healthy": snap["healthy"],
        "latency_ms": snap["latency_ms"],
        "last_checked": snap["last_checked"],
        "last_error": snap["last_error"],
    }


def public_upstream_id(upstream):
    for index, candidate in enumerate(UPSTREAMS):
        if candidate is upstream:
            return f"upstream-{index + 1}"
    return "upstream-unknown"


def edge_identity_headers(auth_context):
    auth_context = auth_context or {}
    headers = {
        "X-Sage-Router-Edge-Auth-Type": str(auth_context.get("type") or ""),
    }
    for header, key in (
        ("X-Sage-Router-Customer-Id", "customer_id"),
        ("X-Sage-Router-User-Id", "user_id"),
        ("X-Sage-Router-Customer-Plan", "plan"),
        ("X-Sage-Router-Customer-Status", "customer_status"),
    ):
        value = auth_context.get(key)
        if value:
            headers[header] = str(value)
    return headers


class EdgeHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "sage-router-tailnet-edge"

    def log_message(self, fmt, *args):
        print(f"{self.client_address[0]} - {fmt % args}", flush=True)

    def _json(self, status, payload, extra_headers=None):
        body = json.dumps(payload, separators=(",", ":")).encode("utf-8") + b"\n"
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        for key, value in (extra_headers or {}).items():
            self.send_header(key, str(value))
        self._cors_headers()
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _reject_json(self, status, payload, extra_headers=None):
        drain_rejected_request_body(self)
        self.close_connection = True
        headers = dict(extra_headers or {})
        headers.setdefault("Connection", "close")
        self._json(status, payload, headers)

    def _cors_headers(self):
        origin = self.headers.get("Origin") or ""
        if "*" in CORS_ORIGINS:
            self.send_header("Access-Control-Allow-Origin", "*")
        elif origin and origin in CORS_ORIGINS:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.send_header("Access-Control-Allow-Methods", "GET,HEAD,POST,PUT,PATCH,DELETE,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Authorization,Content-Type,Stripe-Signature,X-Requested-With")
        self.send_header("Access-Control-Max-Age", "600")

    def _auth_context(self):
        clean_path = urlsplit(self.path).path
        if clean_path in PUBLIC_PATHS:
            return {"type": "public", "preserve_authorization": True}
        if is_public_control_plane_path(self.path):
            return {"type": "public_control_plane", "preserve_authorization": False}

        token = bearer_token(self.headers)
        if token_matches(token, EDGE_TOKEN):
            return {"type": "edge_token", "preserve_authorization": False}
        if token_matches(token, ANALYTICS_TOKEN) and is_operator_analytics_path(self.path):
            return {"type": "analytics_token", "preserve_authorization": False}

        if is_public_signed_backend_path(self.path):
            return {"type": "public_signed_backend", "preserve_authorization": False}

        if EDGE_AUTH_MODE in {"", "shared-token", "token", "legacy"}:
            if not EDGE_TOKEN:
                return {"type": "disabled", "preserve_authorization": True}
            return None

        if EDGE_AUTH_MODE in {"supabase", "saas"}:
            if is_user_jwt_path(self.path):
                return verify_supabase_user_jwt(token)
            if not is_generated_api_key_path(self.path):
                return None
            return verify_supabase_generated_key(token)

        if EDGE_AUTH_MODE in {"disabled", "off"}:
            return {"type": "disabled", "preserve_authorization": True}

        return None

    def _reject_untrusted_browser_origin(self):
        if not is_browser_account_billing_mutation(self.path, self.command):
            return False
        origin = self.headers.get("Origin") or ""
        if browser_origin_allowed(origin):
            return False
        drain_rejected_request_body(self)
        self.close_connection = True
        self._json(
            403,
            edge_error_payload(
                "origin_not_allowed",
                self.path,
                "Browser-originating account and billing mutations must come from a trusted Sage Router app origin.",
                appBaseUrl=LOGIN_URL.rsplit("/", 1)[0],
            ),
            {
                "Connection": "close",
                "X-Sage-Router-Edge-Auth-Type": "origin_guard",
            },
        )
        return True

    def _edge_health(self):
        upstreams = [public_upstream_snapshot(upstream, index) for index, upstream in enumerate(UPSTREAMS)]
        control_plane = public_upstream_snapshot(CONTROL_PLANE_UPSTREAM, 0, "Control plane") if CONTROL_PLANE_UPSTREAM else None
        fastest = choose_upstream()
        selected_id = None
        if fastest:
            selected_id = public_upstream_id(fastest)
        self._json(200, {
            "status": "ok" if fastest else "degraded",
            "selected": selected_id,
            "selectedUpstreamId": selected_id,
            "upstreams": upstreams,
            "controlPlane": control_plane,
            "authMode": EDGE_AUTH_MODE,
            "enforcement": edge_enforcement_state(),
            "failover": edge_failover_state(),
            "modelModalities": model_modalities_state(),
        }, {
            "X-Sage-Router-Edge": "tailnet-lowest-latency",
            "X-Sage-Router-Selected-Upstream": selected_id or "",
        })

    def _proxy(self):
        if urlsplit(self.path).path == "/edge/health" and self.command in {"GET", "HEAD"}:
            self._edge_health()
            return
        if self.command == "OPTIONS":
            self.send_response(204)
            self._cors_headers()
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        if self._reject_untrusted_browser_origin():
            return
        auth_attempt_allowed, auth_attempt_state = check_auth_attempt_rate_limit(self)
        if not auth_attempt_allowed:
            self._reject_json(429, edge_error_payload("auth_attempt_rate_limited", self.path), {
                **edge_error_headers("rate_limited", self.path),
                "Retry-After": auth_attempt_state["retry_after"],
                "X-RateLimit-Limit": auth_attempt_state["limit"],
                "X-RateLimit-Remaining": auth_attempt_state["remaining"],
                "X-RateLimit-Reset": auth_attempt_state["reset"],
            })
            return
        auth_context = self._auth_context()
        if not auth_context:
            self._reject_json(
                401,
                edge_error_payload(
                    "unauthorized",
                    self.path,
                    "Use an active Sage Router API key for model API routes, or sign in for account routes.",
                ),
                edge_error_headers("unauthorized", self.path),
            )
            return
        if (
            EDGE_AUTH_MODE in {"supabase", "saas"}
            and auth_context.get("type") not in {"edge_token", "public_control_plane", "public_signed_backend"}
            and not supabase_auth_configured(require_service=not is_user_jwt_path(self.path))
        ):
            self._reject_json(
                503,
                edge_error_payload("edge_auth_not_configured", self.path),
                edge_error_headers("edge_auth_not_configured", self.path),
            )
            return
        allowed, rate_state = check_rate_limit(auth_context, self.path)
        if not allowed:
            self._reject_json(429, edge_error_payload("rate_limited", self.path), {
                **edge_error_headers("rate_limited", self.path),
                "Retry-After": rate_state["retry_after"],
                "X-RateLimit-Limit": rate_state["limit"],
                "X-RateLimit-Remaining": rate_state["remaining"],
                "X-RateLimit-Reset": rate_state["reset"],
            })
            return
        quota_allowed, quota_state = check_usage_quota(auth_context, self.path)
        if not quota_allowed:
            status = 503 if quota_state and str(quota_state.get("error") or "").startswith("edge_quota_") else 402
            error = (quota_state or {}).get("error") or "quota_exceeded"
            self._reject_json(
                status,
                quota_recovery_payload(error, self.path, quota_state, auth_context),
                {**edge_error_headers(error, self.path), **quota_headers(quota_state)},
            )
            return

        upstreams = control_plane_upstreams() if should_use_control_plane(self.path) else None
        if upstreams is None:
            upstreams = generated_api_key_upstreams(self.path)
        if not upstreams:
            self._reject_json(
                503,
                edge_error_payload("no healthy sage-router upstreams", self.path),
                edge_error_headers("no healthy sage-router upstreams", self.path),
            )
            return

        body = None
        content_length = self.headers.get("Content-Length")
        if content_length:
            body = self.rfile.read(int(content_length))
        body = reroute_known_ollama_subscription_body(self.path, body)

        base_headers = {}
        for key, value in self.headers.items():
            lower = key.lower()
            if lower in HOP_BY_HOP_HEADERS or lower == "host":
                continue
            if lower == "content-length" and body is not None:
                value = str(len(body))
            base_headers[key] = value

        attempts = []
        for index, upstream in enumerate(upstreams):
            headers = dict(base_headers)
            headers["Host"] = upstream.hostport
            headers["X-Sage-Router-Edge"] = "tailnet-lowest-latency"
            headers["X-Sage-Router-Selected-Upstream"] = upstream.raw_url
            headers.update(edge_identity_headers(auth_context))
            outbound_token = outbound_bearer_token(self.path, auth_context, upstream)
            if outbound_token:
                headers["Authorization"] = f"Bearer {outbound_token}"

            conn = None
            try:
                conn = upstream.connection(timeout=REQUEST_TIMEOUT)
                upstream_method = "GET" if self.command == "HEAD" else self.command
                conn.request(upstream_method, upstream.target_path(self.path), body=body, headers=headers)
                resp = conn.getresponse()
                if should_retry_upstream_status(self.path, resp.status) and index < len(upstreams) - 1:
                    detail = resp.read(4096).decode("utf-8", errors="replace")
                    attempts.append({
                        "upstream": upstream.raw_url,
                        "status": resp.status,
                        "detail": detail[:500],
                    })
                    conn.close()
                    continue

                response_headers = resp.getheaders()
                buffered_response_body = None
                should_buffer_for_router_profile = bool(
                    router_profile_alias_from_body(self.path, body)
                    and response_is_uncompressed_json(response_headers, resp.status)
                )
                if (
                    should_buffer_response_for_modality(response_headers, resp.status)
                    or should_buffer_response_for_edge_transform(self.path, response_headers, resp.status)
                    or should_buffer_for_router_profile
                ):
                    buffered_response_body = resp.read(MAX_MODALITY_LEARN_BODY_BYTES + 1)
                    if len(buffered_response_body) > MAX_MODALITY_LEARN_BODY_BYTES:
                        buffered_response_body = None
                        self.close_connection = True
                        resp.close()
                        raise RuntimeError("response too large for edge response buffer")
                    buffered_response_body = transform_edge_response_body(self.path, response_headers, resp.status, buffered_response_body)
                    response_headers, buffered_response_body = rewrite_router_profile_response(
                        self.path,
                        body,
                        response_headers,
                        resp.status,
                        buffered_response_body,
                    )
                should_sanitize_router_profile_sse = bool(
                    buffered_response_body is None
                    and router_profile_alias_from_body(self.path, body)
                    and response_is_uncompressed_event_stream(response_headers, resp.status)
                )
                if should_sanitize_router_profile_sse:
                    response_headers = rewrite_router_profile_stream_headers(self.path, body, response_headers)
                modality_record = modality_record_from_response(response_headers, resp.status, body, buffered_response_body)

                self.close_connection = True
                self.send_response(resp.status, resp.reason)
                sent_header_names = set()
                for key, value in response_headers:
                    lower_key = key.lower()
                    if lower_key in HOP_BY_HOP_HEADERS or lower_key in EDGE_OWNED_RESPONSE_HEADERS:
                        continue
                    if buffered_response_body is not None and lower_key == "content-length":
                        continue
                    sent_header_names.add(lower_key)
                    self.send_header(key, value)
                if buffered_response_body is not None:
                    self.send_header("Content-Length", str(len(buffered_response_body)))
                    sent_header_names.add("content-length")
                if modality_record:
                    derived_headers = {
                        "X-Sage-Router-Provider": modality_record["provider"],
                        "X-Sage-Router-Model-Name": modality_record["model"],
                        "X-Sage-Router-Model": f'{modality_record["provider"]}/{modality_record["model"]}',
                        "X-Sage-Router-Modalities": ",".join(modality_record["modalities"]),
                    }
                    for key, value in derived_headers.items():
                        if key.lower() not in sent_header_names:
                            self.send_header(key, value)
                self.send_header("X-Sage-Router-Edge", "tailnet-lowest-latency")
                self.send_header("X-Sage-Router-Upstream", public_upstream_id(upstream))
                if attempts:
                    self.send_header("X-Sage-Router-Retry-Count", str(len(attempts)))
                if rate_state:
                    self.send_header("X-RateLimit-Limit", str(rate_state["limit"]))
                    self.send_header("X-RateLimit-Remaining", str(rate_state["remaining"]))
                    self.send_header("X-RateLimit-Reset", str(rate_state["reset"]))
                for key, value in quota_headers(quota_state).items():
                    self.send_header(key, str(value))
                self.send_header("Connection", "close")
                self._cors_headers()
                self.end_headers()
                record_model_modalities(modality_record)
                if self.command == "HEAD":
                    if buffered_response_body is None:
                        resp.read(READ_CHUNK_SIZE)
                    return
                if buffered_response_body is not None:
                    self.wfile.write(buffered_response_body)
                    self.wfile.flush()
                    return
                if should_sanitize_router_profile_sse:
                    while True:
                        line = resp.readline()
                        if not line:
                            break
                        self.wfile.write(sanitize_router_profile_sse_line(line))
                        self.wfile.flush()
                    return
                while True:
                    chunk = resp.read(READ_CHUNK_SIZE)
                    if not chunk:
                        break
                    self.wfile.write(chunk)
                    self.wfile.flush()
                return
            except Exception as exc:
                attempts.append({
                    "upstream": upstream.raw_url,
                    "status": 0,
                    "detail": str(exc)[:500],
                })
            finally:
                if conn:
                    conn.close()

        self._json(502, {"error": "all sage-router upstreams failed", "attempts": attempts})

    def do_GET(self):
        self._proxy()

    def do_HEAD(self):
        self._proxy()

    def do_POST(self):
        self._proxy()

    def do_PUT(self):
        self._proxy()

    def do_PATCH(self):
        self._proxy()

    def do_DELETE(self):
        self._proxy()

    def do_OPTIONS(self):
        self._proxy()


if __name__ == "__main__":
    for upstream in UPSTREAMS + ([CONTROL_PLANE_UPSTREAM] if CONTROL_PLANE_UPSTREAM else []):
        check_upstream(upstream)
    threading.Thread(target=health_loop, daemon=True).start()
    server = ThreadingHTTPServer(("0.0.0.0", EDGE_PORT), EdgeHandler)
    print(f"sage-router-tailnet-edge listening on :{EDGE_PORT} with {len(UPSTREAMS)} upstream(s)", flush=True)
    server.serve_forever()
