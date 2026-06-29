#!/usr/bin/env python3
"""Sage Router - Dynamic provider discovery and routing"""
import argparse, base64, datetime, hashlib, hmac, ipaddress, json, logging, math, os, re, secrets, shutil, socket, subprocess, threading, time, urllib.error, urllib.parse, urllib.request, uuid
import concurrent.futures
from dataclasses import dataclass
from enum import Enum, auto
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, List

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger("router")
SAGE_ROUTER_HOME = os.path.expanduser(os.environ.get('SAGE_ROUTER_HOME', '~/.openclaw'))
OPENCLAW_CONFIG = os.environ.get('SAGE_ROUTER_OPENCLAW_CONFIG', os.path.join(SAGE_ROUTER_HOME, 'openclaw.json'))
OPENCLAW_DOTENV = os.environ.get('SAGE_ROUTER_OPENCLAW_DOTENV', os.path.join(SAGE_ROUTER_HOME, '.env'))
APP_PROVIDER_CONFIG = os.environ.get(
    'SAGE_ROUTER_APP_PROVIDER_CONFIG',
    os.path.join(SAGE_ROUTER_HOME, 'openclaw', 'openclaw.json'),
)
APP_CODEX_AUTH_JSON = os.environ.get(
    'SAGE_ROUTER_CODEX_AUTH_JSON',
    os.path.join(SAGE_ROUTER_HOME, '.codex', 'auth.json'),
)
APP_CODEX_AUTH_PROFILE = os.environ.get(
    'SAGE_ROUTER_CODEX_AUTH_PROFILE',
    os.path.join(SAGE_ROUTER_HOME, 'agents', 'main', 'agent', 'auth-profiles.json'),
)
PROVIDER_PROFILES_PATH = os.path.join(os.path.dirname(__file__), 'provider-profiles.json')
ROUTER_PROFILES_PATH = os.path.join(os.path.dirname(__file__), 'router-profiles.json')
APP_MODEL_MODALITIES = os.environ.get(
    'SAGE_ROUTER_MODEL_MODALITIES',
    os.path.join(SAGE_ROUTER_HOME, 'openclaw', 'model-modalities.json'),
)
OPENCLAW_GATEWAY_HELPER = os.path.join(os.path.dirname(__file__), 'openclaw_gateway_agent.mjs')
SELF_PROVIDER_NAMES = {'smart-router', 'sage-router'}
LOCAL_STRICT_PROXY_PROVIDER_NAMES = {'dario', 'openai-codex'}
LOCAL_STRICT_PROXY_API_TYPES = {'openclaw-gateway', 'openai-codex-responses'}
LOCAL_STRICT_DECENTRALIZED_PROVIDER_NAMES = {'darkbloom'}
SHOW_MODEL_PREFIX = os.environ.get('SAGE_ROUTER_SHOW_MODEL_PREFIX', '').strip().lower() in {'1', 'true', 'yes', 'on'}  # Diagnostic-only visible provider/model labels.
FUSION_MODEL_ALIASES = {'fusion', 'sage-router/fusion'}
FUSION_SERVER_TOOL_TYPES = {'sage-router:fusion'}
FUSION_AUTO_TRIGGER_TERMS = (
    'compare',
    'tradeoff',
    'trade-off',
    'for and against',
    'strongest arguments',
    'where do experts disagree',
    'consensus',
    'contradiction',
    'blind spot',
    'risk',
    'risks',
    'audit',
    'review',
    'evaluate',
    'research',
    'recommend',
    'decision',
    'high stakes',
    'high-stakes',
    'multiple perspectives',
    'panel',
)
FUSION_ALLOWED_PLANS = {
    p.strip().lower()
    for p in os.environ.get('SAGE_ROUTER_FUSION_ALLOWED_PLANS', 'pro,max,metered,manual,paid,active').split(',')
    if p.strip()
}
FUSION_PANEL_SIZE = max(2, min(8, int(os.environ.get('SAGE_ROUTER_FUSION_PANEL_SIZE', '3') or '3')))
FUSION_PANEL_TIMEOUT_SECONDS = max(15, int(os.environ.get('SAGE_ROUTER_FUSION_PANEL_TIMEOUT_SECONDS', '90') or '90'))

# Provider name aliases: normalize ollama variants to just "ollama"
_OLLAMA_PROVIDER_ALIASES = {'ollama-cloud', 'ollama-cyber', 'ollama-cyber-fast'}

def display_model_id(provider_name, model):
    """Normalize provider/model for user-facing display.
    
    Collapses ollama variants (ollama-cloud, ollama-cyber, etc.) into 'ollama'
    and strips :cloud/:cloud suffixes that are routing implementation details,
    so the same model always shows the same prefix regardless of which
    ollama endpoint served it.
    """
    display_provider = 'ollama' if provider_name in _OLLAMA_PROVIDER_ALIASES else provider_name
    display_model = str(model or '')
    prefix_candidates = []
    for prefix in [provider_name, display_provider] + (list(_OLLAMA_PROVIDER_ALIASES) if display_provider == 'ollama' else []):
        if prefix and prefix not in prefix_candidates:
            prefix_candidates.append(prefix)
    changed = True
    while changed:
        changed = False
        for prefix in sorted(prefix_candidates, key=len, reverse=True):
            if prefix and display_model.lower().startswith(prefix.lower() + '/'):
                display_model = display_model[len(prefix) + 1:]
                changed = True
                break
    # Strip :cloud and :cloud suffixes — they indicate routing mode, not a different model
    display_model = display_model.removesuffix(':cloud').removesuffix('-cloud')
    return f'{display_provider}/{display_model}'


def load_env_file(path):
    try:
        with open(path) as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith('#') or '=' not in line:
                    continue
                key, value = line.split('=', 1)
                key = key.strip()
                if not key or key in os.environ:
                    continue
                value = value.strip()
                if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
                    value = value[1:-1]
                os.environ[key] = value
    except FileNotFoundError:
        return
    except Exception as e:
        logger.debug(f'Failed to load env file {path}: {e}')


load_env_file(OPENCLAW_DOTENV)
load_env_file(os.path.join(os.path.dirname(__file__), '.env'))

# Backward compat: fall back to SMART_ROUTER_* env vars if SAGE_ROUTER_* not set
import re as _re
_env_compat_done = set()
for _key in list(os.environ):
    if _key.startswith('SMART_ROUTER_') and _key not in os.environ:
        pass  # can't happen, but guard
for _key in list(os.environ):
    if _key.startswith('SMART_ROUTER_'):
        _new_key = _key.replace('SMART_ROUTER_', 'SAGE_ROUTER_', 1)
        if _new_key not in os.environ:
            os.environ[_new_key] = os.environ[_key]
DARIO_PROVIDER_NAME = os.environ.get('SAGE_ROUTER_DARIO_PROVIDER_NAME', 'dario')
DARIO_LOCAL_BASE_URL = os.environ.get('SAGE_ROUTER_DARIO_BASE_URL', 'http://127.0.0.1:3456')
DARIO_LOCAL_API_KEY = os.environ.get('SAGE_ROUTER_DARIO_API_KEY', 'dario')
DARIO_SERVICE_NAME = os.environ.get('SAGE_ROUTER_DARIO_SERVICE', 'dario.service')
DARIO_AUTOSTART = os.environ.get('SAGE_ROUTER_DARIO_AUTOSTART', '1').strip().lower() in {'1', 'true', 'yes', 'on'}
DARIO_PROCESS = None
OPENCLAW_GATEWAY_BASE_URL = os.environ.get('SAGE_ROUTER_OPENCLAW_GATEWAY_URL', 'ws://127.0.0.1:18789')
OPENAI_CODEX_GATEWAY_FALLBACK = os.environ.get('SAGE_ROUTER_OPENAI_CODEX_GATEWAY_FALLBACK', '1').strip().lower() in {'1', 'true', 'yes', 'on'}
OPENAI_CODEX_OAUTH_ENABLED = os.environ.get('SAGE_ROUTER_CODEX_OAUTH_ENABLED', '1').strip().lower() in {'1', 'true', 'yes', 'on'}
OPENAI_CODEX_OAUTH_AUTH_BASE_URL = os.environ.get('SAGE_ROUTER_CODEX_OAUTH_AUTH_BASE_URL', 'https://auth.openai.com').strip().rstrip('/')
OPENAI_CODEX_OAUTH_CLIENT_ID = os.environ.get('SAGE_ROUTER_CODEX_OAUTH_CLIENT_ID', 'app_EMoamEEZ73f0CkXaXp7hrann').strip()
OPENAI_CODEX_OAUTH_ORIGINATOR = os.environ.get('SAGE_ROUTER_CODEX_OAUTH_ORIGINATOR', 'sage-router').strip() or 'sage-router'
OPENAI_CODEX_OAUTH_TIMEOUT_MS = int(os.environ.get('SAGE_ROUTER_CODEX_OAUTH_TIMEOUT_MS', str(15 * 60 * 1000)))
OPENAI_CODEX_OAUTH_DEFAULT_INTERVAL_MS = int(os.environ.get('SAGE_ROUTER_CODEX_OAUTH_INTERVAL_MS', '5000'))
OPENAI_CODEX_OAUTH_MIN_INTERVAL_MS = 1000
OPENAI_CODEX_OAUTH_REFRESH_SKEW_MS = int(os.environ.get('SAGE_ROUTER_CODEX_OAUTH_REFRESH_SKEW_MS', str(5 * 60 * 1000)))
OPENAI_CODEX_OAUTH_HTTP_TIMEOUT_SECONDS = float(os.environ.get('SAGE_ROUTER_CODEX_OAUTH_HTTP_TIMEOUT_SECONDS', '30'))
OPENAI_CODEX_OAUTH_SESSIONS = {}
OPENAI_CODEX_OAUTH_LOCK = threading.Lock()
# Auth-profile-based gateway providers: defined after DEFAULT constants below
DEFAULT_DISABLED_PROVIDERS = {'google', 'google-vertex'}
ENV_DISABLED_PROVIDERS = DEFAULT_DISABLED_PROVIDERS | {
    name.strip() for name in os.environ.get('SAGE_ROUTER_DISABLED_PROVIDERS', '').split(',')
    if name.strip()
}
ENV_DISABLED_MODELS = {
    name.strip() for name in os.environ.get('SAGE_ROUTER_DISABLED_MODELS', '').split(',')
    if name.strip()
}
DISABLED_PROVIDERS = set(ENV_DISABLED_PROVIDERS)
DISABLED_MODELS = set(ENV_DISABLED_MODELS)
OLLAMA_TIMEOUT_SECONDS = int(os.environ.get('SAGE_ROUTER_OLLAMA_TIMEOUT_SECONDS', '120'))
OLLAMA_ALLOW_THINK_FALSE_RETRY = os.environ.get('SAGE_ROUTER_OLLAMA_ALLOW_THINK_FALSE_RETRY', '').strip().lower() in {'1', 'true', 'yes', 'on'}
OPENAI_COMPAT_TIMEOUT_SECONDS = int(os.environ.get('SAGE_ROUTER_OPENAI_TIMEOUT_SECONDS', '35'))
ANTHROPIC_TIMEOUT_SECONDS = int(os.environ.get('SAGE_ROUTER_ANTHROPIC_TIMEOUT_SECONDS', '35'))
GOOGLE_TIMEOUT_SECONDS = int(os.environ.get('SAGE_ROUTER_GOOGLE_TIMEOUT_SECONDS', '35'))
GOOGLE_VERTEX_LOCATION = os.environ.get('SAGE_ROUTER_GOOGLE_VERTEX_LOCATION') or os.environ.get('GOOGLE_CLOUD_LOCATION') or os.environ.get('CLOUD_ML_REGION') or 'us-central1'
GOOGLE_VERTEX_PROJECT = os.environ.get('SAGE_ROUTER_GOOGLE_VERTEX_PROJECT') or os.environ.get('GOOGLE_CLOUD_PROJECT') or os.environ.get('GCP_PROJECT') or ''
GOOGLE_VERTEX_ADC_SCOPE = 'https://www.googleapis.com/auth/cloud-platform'
GOOGLE_VERTEX_TOKEN_CACHE = {'access_token': '', 'expires_at': 0}
OPENCLAW_GATEWAY_TIMEOUT_SECONDS = int(os.environ.get('SAGE_ROUTER_OPENCLAW_TIMEOUT_SECONDS', '90'))
OPENCLAW_GATEWAY_CODE_TIMEOUT_SECONDS = int(os.environ.get('SAGE_ROUTER_OPENCLAW_CODE_TIMEOUT_SECONDS', '45'))
OPENCLAW_GATEWAY_AGENT_ID = os.environ.get('SAGE_ROUTER_OPENCLAW_AGENT_ID', 'main')
AUDIO_STT_PROVIDER = os.environ.get('SAGE_ROUTER_AUDIO_STT_PROVIDER', 'openai').strip() or 'openai'
AUDIO_TTS_PROVIDER = os.environ.get('SAGE_ROUTER_AUDIO_TTS_PROVIDER', 'openai').strip() or 'openai'
AUDIO_PROXY_TIMEOUT_SECONDS = int(os.environ.get('SAGE_ROUTER_AUDIO_PROXY_TIMEOUT_SECONDS', '120'))
REACHABILITY_TIMEOUT_SECONDS = float(os.environ.get('SAGE_ROUTER_REACHABILITY_TIMEOUT_SECONDS', '0.5'))
REACHABILITY_TTL_SECONDS = int(os.environ.get('SAGE_ROUTER_REACHABILITY_TTL_SECONDS', '120'))
OLLAMA_MODEL_REFRESH_TTL_SECONDS = int(os.environ.get('SAGE_ROUTER_OLLAMA_MODEL_REFRESH_TTL_SECONDS', '300'))
HEALTH_SCORE_TTL_SECONDS = int(os.environ.get('SAGE_ROUTER_HEALTH_SCORE_TTL_SECONDS', '60'))
RATE_LIMIT_COOLDOWN_BASE_SECONDS = int(os.environ.get('SAGE_ROUTER_RATE_LIMIT_COOLDOWN_BASE_SECONDS', '120'))
FAILURE_COOLDOWN_BASE_SECONDS = int(os.environ.get('SAGE_ROUTER_FAILURE_COOLDOWN_BASE_SECONDS', '180'))
CONSECUTIVE_FAILURE_COOLDOWN_THRESHOLD = int(os.environ.get('SAGE_ROUTER_CONSECUTIVE_FAILURE_COOLDOWN_THRESHOLD', '2'))
MODEL_MISSING_COOLDOWN_SECONDS = int(os.environ.get('SAGE_ROUTER_MODEL_MISSING_COOLDOWN_SECONDS', '1800'))
EMPTY_OUTPUT_COOLDOWN_SECONDS = int(os.environ.get('SAGE_ROUTER_EMPTY_OUTPUT_COOLDOWN_SECONDS', '600'))
PROVIDER_HEALTH_CACHE = {}
LATENCY_STATS_PATH = os.path.expanduser(os.environ.get('SAGE_ROUTER_LATENCY_STATS_PATH', '~/.cache/sage-router/latency-stats.json'))
ROUTE_EVENTS_PATH = os.path.expanduser(os.environ.get('SAGE_ROUTER_ROUTE_EVENTS_PATH', '~/.cache/sage-router/route-events.jsonl'))
ANALYTICS_TOKEN = os.environ.get('SAGE_ROUTER_ANALYTICS_TOKEN', '').strip()
ANALYTICS_EVENT_LIMIT = int(os.environ.get('SAGE_ROUTER_ANALYTICS_EVENT_LIMIT', '10000'))
FIRESTORE_PROJECT_ID = os.environ.get('SAGE_ROUTER_FIRESTORE_PROJECT_ID') or os.environ.get('GOOGLE_CLOUD_PROJECT') or os.environ.get('GCP_PROJECT')
FIRESTORE_DATABASE = os.environ.get('SAGE_ROUTER_FIRESTORE_DATABASE', '(default)')
FIRESTORE_ROUTE_EVENTS_COLLECTION = os.environ.get('SAGE_ROUTER_FIRESTORE_ROUTE_EVENTS_COLLECTION', 'sage_router_route_events')
FIRESTORE_ENABLED = os.environ.get('SAGE_ROUTER_FIRESTORE_ENABLED', '1').strip().lower() in {'1', 'true', 'yes', 'on'}
SUPABASE_URL = (os.environ.get('SAGE_ROUTER_SUPABASE_URL') or os.environ.get('PUBLIC_SUPABASE_URL') or os.environ.get('SUPABASE_URL') or '').rstrip('/')
SUPABASE_ANON_KEY = os.environ.get('SAGE_ROUTER_SUPABASE_ANON_KEY') or os.environ.get('AOPS_SUPABASE_ANON_KEY') or os.environ.get('SUPABASE_ANON_KEY') or ''
SUPABASE_SERVICE_ROLE_KEY = os.environ.get('SAGE_ROUTER_SUPABASE_SERVICE_ROLE_KEY') or os.environ.get('SUPABASE_SERVICE_ROLE') or os.environ.get('SUPABASE_SERVICE_ROLE_KEY') or ''
SUPABASE_ROUTE_EVENTS_TABLE = os.environ.get('SAGE_ROUTER_SUPABASE_ROUTE_EVENTS_TABLE', 'sage_router_route_events')
SUPABASE_ANALYTICS_SNAPSHOTS_TABLE = os.environ.get('SAGE_ROUTER_SUPABASE_ANALYTICS_SNAPSHOTS_TABLE', 'sage_router_analytics_snapshots')
SUPABASE_CUSTOMERS_TABLE = os.environ.get('SAGE_ROUTER_SUPABASE_CUSTOMERS_TABLE', 'sage_router_customers')
SUPABASE_API_KEYS_TABLE = os.environ.get('SAGE_ROUTER_SUPABASE_API_KEYS_TABLE', 'sage_router_api_keys')
SUPABASE_PAYMENT_INTENTS_TABLE = os.environ.get('SAGE_ROUTER_SUPABASE_PAYMENT_INTENTS_TABLE', 'sage_router_payment_intents')
SUPABASE_USAGE_COUNTERS_TABLE = os.environ.get('SAGE_ROUTER_SUPABASE_USAGE_COUNTERS_TABLE', 'sage_router_usage_counters')
SUPABASE_OPERATOR_AUDIT_TABLE = os.environ.get('SAGE_ROUTER_SUPABASE_OPERATOR_AUDIT_TABLE', 'sage_router_operator_audit_events')
SUPABASE_WAITLIST_TABLE = os.environ.get('SAGE_ROUTER_SUPABASE_WAITLIST_TABLE', 'sage_router_waitlist')
SUPABASE_WAITLIST_FALLBACK_TABLE = os.environ.get('SAGE_ROUTER_SUPABASE_WAITLIST_FALLBACK_TABLE', 'funnel_leads')
SUPABASE_FUNNEL_EVENTS_TABLE = os.environ.get('SAGE_ROUTER_SUPABASE_FUNNEL_EVENTS_TABLE', 'sage_router_funnel_events')
SUPABASE_MODEL_MODALITIES_TABLE = os.environ.get('SAGE_ROUTER_SUPABASE_MODEL_MODALITIES_TABLE', 'sage_router_model_modalities')
SUPABASE_MODEL_MODALITIES_RPC = os.environ.get('SAGE_ROUTER_SUPABASE_MODEL_MODALITIES_RPC', 'sage_router_record_model_modalities')
# Off by default — no remote mirroring of analytics/customers/keys. The
# router should keep its work local; enable only when the operator runs a
# hosted tier that needs the Supabase mirror.
SUPABASE_MIRROR_ENABLED = os.environ.get('SAGE_ROUTER_SUPABASE_MIRROR_ENABLED', '0').strip().lower() in {'1', 'true', 'yes', 'on'}
MODEL_MODALITIES_SHARED_ENABLED = os.environ.get(
    'SAGE_ROUTER_MODEL_MODALITIES_SHARED_ENABLED',
    '1' if SUPABASE_MIRROR_ENABLED else '0',
).strip().lower() in {'1', 'true', 'yes', 'on'}
MODEL_MODALITIES_SHARED_REFRESH_SECONDS = int(os.environ.get('SAGE_ROUTER_MODEL_MODALITIES_SHARED_REFRESH_SECONDS', '60'))
# Off by default — the router does not collect user identities. Enable only
# when running the hosted billing/tenancy tier that requires Supabase Auth.
SUPABASE_AUTH_ENABLED = os.environ.get('SAGE_ROUTER_SUPABASE_AUTH_ENABLED', '0').strip().lower() in {'1', 'true', 'yes', 'on'}
REQUIRE_VERIFIED_EMAIL = os.environ.get('SAGE_ROUTER_REQUIRE_VERIFIED_EMAIL', '1').strip().lower() in {'1', 'true', 'yes', 'on'}
CLIENT_API_KEYS = [
    key.strip()
    for key in (os.environ.get('SAGE_ROUTER_CLIENT_API_KEYS') or os.environ.get('SAGE_ROUTER_CLIENT_API_KEY') or '').split(',')
    if key.strip()
]
CLIENT_AUTH_REQUIRED = os.environ.get('SAGE_ROUTER_CLIENT_AUTH_REQUIRED', '1' if CLIENT_API_KEYS else '0').strip().lower() in {'1', 'true', 'yes', 'on'}
CORS_ORIGIN = os.environ.get('SAGE_ROUTER_CORS_ORIGIN', '*')
CORS_ORIGINS = [o.strip() for o in CORS_ORIGIN.split(',') if o.strip()]
BROWSER_ALLOWED_ORIGINS_RAW = os.environ.get('SAGE_ROUTER_BROWSER_ALLOWED_ORIGINS', '').strip()
ROUTE_AUTH_CONTEXT = threading.local()
CUSTOMER_STORE_PATH = os.path.expanduser(os.environ.get('SAGE_ROUTER_CUSTOMER_STORE_PATH', '~/.cache/sage-router/customers.json'))
API_KEY_PREFIX = os.environ.get('SAGE_ROUTER_API_KEY_PREFIX', 'sk_sage_')
API_KEY_HASH_PEPPER = os.environ.get('SAGE_ROUTER_API_KEY_HASH_PEPPER') or os.environ.get('SAGE_ROUTER_SIGNING_SECRET') or ''
MAX_ACTIVE_API_KEYS_PER_CUSTOMER = int(os.environ.get('SAGE_ROUTER_MAX_ACTIVE_API_KEYS_PER_CUSTOMER', '5'))
ACTIVATION_EMAIL_PROVIDER = os.environ.get('SAGE_ROUTER_ACTIVATION_EMAIL_PROVIDER', 'resend').strip().lower()
ACTIVATION_EMAIL_API_KEY = (
    os.environ.get('SAGE_ROUTER_ACTIVATION_EMAIL_API_KEY')
    or os.environ.get('SAGE_ROUTER_RESEND_API_KEY')
    or os.environ.get('RESEND_API_KEY')
    or ''
)
ACTIVATION_EMAIL_FROM = os.environ.get('SAGE_ROUTER_ACTIVATION_EMAIL_FROM', '').strip()
ACTIVATION_EMAIL_REPLY_TO = os.environ.get('SAGE_ROUTER_ACTIVATION_EMAIL_REPLY_TO', '').strip()
ACTIVATION_EMAIL_MAX_BATCH = max(1, min(int(os.environ.get('SAGE_ROUTER_ACTIVATION_EMAIL_MAX_BATCH', '25') or '25'), 100))
ACTIVATION_EMAIL_REDIRECT_TO = os.environ.get(
    'SAGE_ROUTER_ACTIVATION_EMAIL_REDIRECT_TO',
    'https://app.sagerouter.dev/account?activation=recovery',
).strip()
ACTIVATION_FOLLOWUP_SEND_CONFIRMATION = 'SEND_ACTIVATION_FOLLOWUPS'
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY') or os.environ.get('SAGE_ROUTER_STRIPE_SECRET_KEY') or ''
STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET') or os.environ.get('SAGE_ROUTER_STRIPE_WEBHOOK_SECRET') or ''
STRIPE_PRICE_ID = os.environ.get('SAGE_ROUTER_STRIPE_PRICE_ID') or os.environ.get('STRIPE_PRICE_ID') or ''
STRIPE_PRICE_IDS_RAW = os.environ.get('SAGE_ROUTER_STRIPE_PRICE_IDS', '').strip()
PUBLIC_PLAN_RATE_LIMITS_RAW = os.environ.get(
    'SAGE_ROUTER_EDGE_RATE_LIMITS',
    'trial=30,lite=60,pro=180,max=600,manual=600,paid=180,active=180,default=60',
)
PUBLIC_PLAN_MONTHLY_QUOTAS_RAW = os.environ.get(
    'SAGE_ROUTER_EDGE_MONTHLY_QUOTAS',
    'trial=1000,lite=10000,pro=50000,max=200000,paid=50000,active=50000,default=0',
)
PUBLIC_PLAN_LIMIT_ALIASES = {
    'free': 'default',
    'metered': 'paid',
}
PUBLIC_PLAN_CATALOG = {
    'free': {
        'name': 'Free',
        'price': '$0/month',
        'included': 'local/free providers only when available',
        'features': ['local-first routing', 'manual provider keys', 'basic health and routing debug'],
        'routingProfiles': ['local-first', 'fast-local'],
    },
    'lite': {
        'name': 'Lite',
        'price': '$6/month',
        'quarterly': '$27/quarter',
        'features': ['agent-native routing', 'API keys', 'usage analytics', 'standard fallback chains'],
        'routingProfiles': ['eco', 'balanced', 'agentic'],
    },
    'pro': {
        'name': 'Pro',
        'price': '$30/month',
        'quarterly': '$81/quarter',
        'features': ['frontier routing', 'agentic tool-use preference', 'Fusion multi-model synthesis', 'analytics snapshots', 'subscription failover'],
        'routingProfiles': ['balanced', 'premium', 'frontier', 'agentic', 'fusion'],
    },
    'max': {
        'name': 'Max',
        'price': '$72/month',
        'quarterly': '$216/quarter',
        'features': ['highest quality routing', 'large/frontier model preference', 'priority Fusion budget', 'team/automation use'],
        'routingProfiles': ['premium', 'frontier', 'frontier-large', 'agentic', 'fusion'],
    },
    'metered': {
        'name': 'Metered',
        'price': 'usage-based',
        'minimumPaymentUsd': 0.001,
        'serverMarginPercent': 5,
        'features': ['per-request cost attribution', 'Fusion multi-model synthesis', 'wallet/x402-ready payment intents', 'free-tier fallback policy'],
        'routingProfiles': ['eco', 'balanced', 'premium', 'agentic', 'fusion'],
    },
}
PUBLIC_AGENT_NATIVE_FEATURES = {
    'agenticAutoDetection': {
        'description': 'Detects tool use and multi-step execution language, then prefers models with reliable tool-calling/autonomous task behavior.',
        'signals': ['tools array', 'forced tool_choice', 'build/run/test/fix/debug/deploy/verify/edit/refactor keywords'],
    },
    'toolAwareRouting': {'description': 'Forced tool calls become hard requirements; ordinary tool arrays become soft preference unless the client explicitly requires tools.'},
    'contextAwareRouting': {'description': 'Estimated prompt size and document/vision signals filter or boost capable long-context and multimodal models.'},
    'sessionSafeFallback': {'description': 'Each request builds an ordered fallback chain and retries failed providers without mid-stream handoff.'},
    'costAndPlanTelemetry': {'description': 'Route events include selected model, attempts, elapsed time, customer plan, and auth type for pricing analytics.'},
    'freeTierFallbackPolicy': {'description': 'Eco/local/free profiles can be used for zero or low-balance workflows without blocking agent execution.'},
    'fusionRouting': {'description': 'Paid plans can request sage-router/fusion or the sage-router:fusion server tool for parallel panel responses and judge synthesis on high-stakes research or review prompts.'},
}
PUBLIC_MODEL_CATALOG = {
    'description': 'Public model-family catalog for Sage Router hosted routing. This is discovery metadata only; live /v1/models remains authenticated with generated sk_sage_* customer API keys.',
    'modelApiRequiresGeneratedKey': True,
    'catalogPage': 'https://sagerouter.dev/models',
    'modelApiPath': '/v1/models',
    'recommendedModel': 'sage-router/frontier',
    'families': [
        {
            'id': 'sage-router-profiles',
            'name': 'Sage Router profiles',
            'examples': ['sage-router/auto', 'sage-router/balanced', 'sage-router/frontier', 'sage-router/agentic', 'sage-router/fusion'],
            'access': 'Hosted profile aliases select across authorized providers, local models, and healthy fallback routes. Fusion is Pro/Max gated.',
        },
        {
            'id': 'openai-codex',
            'name': 'OpenAI and Codex-compatible routes',
            'examples': ['gpt-5.5', 'gpt-5.4', 'gpt-5.4-mini'],
            'access': 'Bring an authorized API key or compatible Codex/OpenClaw auth profile.',
        },
        {
            'id': 'anthropic',
            'name': 'Anthropic-compatible routes',
            'examples': ['claude-opus', 'claude-sonnet', 'claude-haiku'],
            'access': 'Bring authorized Anthropic/Dario access; hosted public plans do not pool personal provider accounts.',
        },
        {
            'id': 'gemini',
            'name': 'Google Gemini-compatible routes',
            'examples': ['gemini-3-pro', 'gemini-3-flash', 'gemini-2.5-pro'],
            'access': 'Bring authorized Google API or Vertex credentials.',
        },
        {
            'id': 'ollama',
            'name': 'Ollama local and Ollama Cloud routes',
            'examples': ['llama3.3', 'qwen3-coder', 'gpt-oss:cloud'],
            'access': 'Use customer-controlled local Ollama or authorized Ollama Cloud models discovered through the runtime.',
        },
        {
            'id': 'byok-compatible',
            'name': 'BYOK OpenAI-compatible providers',
            'examples': ['nvidia-nim/nemotron', 'openrouter/free-models', 'darkbloom/custom'],
            'access': 'Bring authorized provider keys for OpenAI-compatible endpoints such as NVIDIA NIM, OpenRouter, private gateways, or other compatible APIs.',
        },
    ],
    'safetyBoundary': 'The public catalog is not a promise of bundled model resale. Provider access must be authorized by the customer or explicitly approved for managed access.',
}
MANAGED_PROVIDER_RESALE_ELIGIBLE_PROVIDER_FAMILIES = (
    'ollama',
    'openai',
    'anthropic',
)
MANAGED_PROVIDER_BYOK_ONLY_PROVIDER_FAMILIES = (
    'openrouter',
    'byok-compatible',
)
MANAGED_PROVIDER_FAMILY_LABELS = {
    'ollama': 'Ollama',
    'openai': 'OpenAI',
    'anthropic': 'Anthropic',
    'openrouter': 'OpenRouter',
    'byok-compatible': 'BYOK-compatible gateways',
}
PUBLIC_LAUNCH_POSITIONING = {
    'targetMrrUsd': 10000,
    'primaryRevenueModel': 'hosted_routing_control_plane',
    'pricingPage': 'https://sagerouter.dev/pricing',
    'comparisonPage': 'https://sagerouter.dev/compare/model-gateways',
    'modelCatalogPage': 'https://sagerouter.dev/models',
    'accountPage': 'https://app.sagerouter.dev/account.html',
    'recommendedMix': {
        'liteCustomers': 100,
        'proCustomers': 200,
        'maxCustomers': 50,
        'monthlyRevenueUsd': 10200,
    },
    'revenuePaths': [
        {
            'label': 'Pro-only',
            'mix': {'proCustomers': 334},
            'monthlyRevenueUsd': 10020,
            'useCase': 'Focused daily developer adoption through Pro activation.',
        },
        {
            'label': 'Max-only',
            'mix': {'maxCustomers': 139},
            'monthlyRevenueUsd': 10008,
            'useCase': 'Founder-led automation, teams, and implementation-review accounts.',
        },
        {
            'label': 'Recommended mixed path',
            'mix': {'liteCustomers': 100, 'proCustomers': 200, 'maxCustomers': 50},
            'monthlyRevenueUsd': 10200,
            'useCase': 'Balanced low-friction signup, daily Pro usage, and Max implementation support.',
        },
        {
            'label': 'Higher-Max mixed path',
            'mix': {'liteCustomers': 50, 'proCustomers': 150, 'maxCustomers': 75},
            'monthlyRevenueUsd': 10200,
            'useCase': 'More founder-led Max conversion with fewer lightweight accounts.',
        },
    ],
    'conversionFunnelTargets': [
        {
            'stage': 'visitor_to_signup',
            'targetRate': 0.05,
            'surface': 'sagerouter.dev, pricing, model gateway comparison',
        },
        {
            'stage': 'signup_to_generated_key',
            'targetRate': 0.60,
            'surface': 'app.sagerouter.dev/account.html',
        },
        {
            'stage': 'generated_key_to_first_routed_request',
            'targetRate': 0.50,
            'surface': 'quickstart and account first request',
        },
        {
            'stage': 'trial_or_free_to_paid',
            'targetRate': 0.15,
            'surface': 'Stripe checkout and plan gating',
        },
        {
            'stage': 'paid_logo_monthly_retention',
            'targetRate': 0.85,
            'surface': 'usage quotas, status, analytics, fallback reliability',
        },
    ],
    'conversionSurfaces': [
        'sagerouter.dev',
        'sagerouter.dev/pricing',
        'sagerouter.dev/models',
        'sagerouter.dev/agent-native',
        'sagerouter.dev/compare/model-gateways',
        'sagerouter.dev/model-routing-calculator',
        'app.sagerouter.dev/account.html',
    ],
    'sells': [
        'hosted account and API-key management',
        'usage quotas and request-per-minute limits',
        'route telemetry and analytics',
        'fallback reliability and Tailnet/private-router resilience',
        'support and private deployment guidance',
    ],
    'complianceBoundary': 'Customer-authorized provider access only; Sage Router does not grant unauthorized model access, pool provider accounts, or bypass provider terms.',
    'managedProviderAccess': {
        'enabled': False,
        'status': 'disabled_pending_provider_terms',
        'description': 'Future managed model-provider access is gated until provider resale terms, billing margin policy, abuse controls, and customer terms are ready.',
        'requiredControls': [
            'provider_resale_terms',
            'margin_policy',
            'positive_unit_economics',
            'provider_terms_acknowledgment',
            'provider_authorization_evidence',
            'authorized_provider_allowlist',
            'provider_cost_metering',
            'per_plan_usage_caps',
            'rate_limits_and_durable_quotas',
            'generated_key_revocation',
            'operator_abuse_review',
            'operator_audit_events',
            'acceptable_use_managed_access_terms',
        ],
        'requiresPositiveUnitEconomics': True,
        'providerTermsAcknowledged': False,
        'configuredProviderFamilies': [],
        'allowedProviderFamilies': [],
        'resaleEligibleProviderFamilies': list(MANAGED_PROVIDER_RESALE_ELIGIBLE_PROVIDER_FAMILIES),
        'byokOnlyProviderFamilies': list(MANAGED_PROVIDER_BYOK_ONLY_PROVIDER_FAMILIES),
        'providerFamilyReadiness': [],
        'oneSubscriptionReadiness': {
            'commercialPreference': 'one-subscription',
            'enabled': False,
            'readyProviderFamilies': [],
            'blockedProviderFamilies': [],
            'byokOnlyProviderFamilies': list(MANAGED_PROVIDER_BYOK_ONLY_PROVIDER_FAMILIES),
        },
        'minimumGrossMarginPercent': 35,
        'costControls': [
            'per_plan_monthly_quotas',
            'request_per_minute_limits',
            'durable_usage_accounting',
            'generated_key_revocation',
            'operator_customer_review',
            'operator_audit_events',
            'authorized_provider_allowlist',
            'provider_resale_terms',
            'managed_access_acceptable_use',
        ],
    },
}
PUBLIC_BASE_URL = (os.environ.get('SAGE_ROUTER_PUBLIC_BASE_URL') or 'https://sagerouter.dev').rstrip('/')
MARKETING_BASE_URL = (os.environ.get('SAGE_ROUTER_MARKETING_BASE_URL') or 'https://sagerouter.dev').rstrip('/')
APP_BASE_URL = (os.environ.get('SAGE_ROUTER_APP_BASE_URL') or os.environ.get('SAGE_ROUTER_PUBLIC_BASE_URL') or 'https://app.sagerouter.dev').rstrip('/')
API_BASE_URL = (os.environ.get('SAGE_ROUTER_API_BASE_URL') or '').rstrip('/')
DEFAULT_BROWSER_ALLOWED_ORIGIN_HOSTS = {
    'sagerouter.dev',
    'www.sagerouter.dev',
    'app.sagerouter.dev',
    'localhost',
    '127.0.0.1',
}
CRYPTO_PAYMENT_ADDRESS = os.environ.get('SAGE_ROUTER_CRYPTO_PAYMENT_ADDRESS', '').strip()
CRYPTO_PAYMENT_ASSET = os.environ.get('SAGE_ROUTER_CRYPTO_PAYMENT_ASSET', 'USDC').strip()
CRYPTO_PAYMENT_NETWORK = os.environ.get('SAGE_ROUTER_CRYPTO_PAYMENT_NETWORK', 'manual').strip()
CRYPTO_PROCESSOR_URL = os.environ.get('SAGE_ROUTER_CRYPTO_PROCESSOR_URL', '').strip()
CRYPTO_PROCESSOR_KEY = os.environ.get('SAGE_ROUTER_CRYPTO_PROCESSOR_KEY', '').strip()
LATENCY_EWMA_ALPHA = float(os.environ.get('SAGE_ROUTER_LATENCY_EWMA_ALPHA', '0.35'))
GENERAL_EMPIRICAL_EXPLORATION_BONUS = float(os.environ.get('SAGE_ROUTER_GENERAL_EXPLORATION_BONUS', '20'))
GENERAL_EMPIRICAL_SUCCESS_EXPLORATION_CAP = float(os.environ.get('SAGE_ROUTER_GENERAL_SUCCESS_EXPLORATION_CAP', '8'))
GENERAL_EMPIRICAL_LATENCY_BONUS_CAP = float(os.environ.get('SAGE_ROUTER_GENERAL_LATENCY_BONUS_CAP', '18'))
GENERAL_EMPIRICAL_LATENCY_PIVOT_MS = float(os.environ.get('SAGE_ROUTER_GENERAL_LATENCY_PIVOT_MS', '2500'))
GENERAL_EMPIRICAL_FAILURE_PENALTY = float(os.environ.get('SAGE_ROUTER_GENERAL_FAILURE_PENALTY', '4'))
DEFAULT_OPENAI_CODEX_MODELS = ['gpt-5.5', 'gpt-5.4', 'gpt-5.4-pro', 'gpt-5.4-mini', 'gpt-5.3-codex', 'gpt-5.3-codex-spark', 'gpt-5.2-codex', 'gpt-5.1-codex-max', 'gpt-5.1-codex-mini', 'gpt-5.1']
DEFAULT_NGC_MODELS = ['nemotron-tts', 'canary-asr', 'nemo-tts', 'nemo-asr', 'nvidia/tts', 'nvidia/asr']
DEFAULT_ANTHROPIC_MODELS = ['claude-opus-4-6', 'claude-opus-4-5', 'claude-opus-4-1', 'claude-opus-4-0', 'claude-sonnet-4-6', 'claude-sonnet-4-5', 'claude-sonnet-4-0', 'claude-haiku-4-5', 'claude-3-7-sonnet-latest', 'claude-3-5-sonnet-latest']
DEFAULT_DARKBLOOM_MODELS = ['mlx-community/gemma-4-26b-a4b-it-8bit', 'qwen3.5-27b-claude-opus-8bit', 'mlx-community/Trinity-Mini-8bit', 'mlx-community/Qwen3.5-122B-A10B-8bit', 'mlx-community/MiniMax-M2.5-8bit']
DEFAULT_CLOUDFLARE_WORKERS_AI_MODELS = ['@cf/meta/llama-3.3-70b-instruct-fp8-fast', '@cf/meta/llama-3.1-8b-instruct', '@cf/deepseek-ai/deepseek-r1-distill-qwen-32b', '@cf/qwen/qwq-32b', '@cf/qwen/qwen2.5-coder-32b-instruct', '@cf/mistral/mistral-small-3.1-24b-instruct']
DEFAULT_OPENAI_MODELS = ['gpt-5.4', 'gpt-5.4-mini', 'gpt-4o', 'gpt-4o-mini']
DEFAULT_OPENROUTER_MODELS = ['openai/gpt-5.4', 'anthropic/claude-sonnet-4.5', 'x-ai/grok-4']
DEFAULT_GOOGLE_MODELS = ['gemini-3-flash-preview', 'gemini-2.5-pro', 'gemini-2.5-flash']
DEFAULT_XAI_MODELS = ['grok-4', 'grok-3', 'grok-3-mini', 'grok-2']
DEFAULT_ZAI_MODELS = ['z1-ultra', 'z1-pro', 'z1-mini']
DEFAULT_GITHUB_COPILOT_MODELS = ['gpt-5.4', 'gpt-5.4-mini', 'claude-sonnet-4-5']


def extract_http_error(exc: Exception) -> str:
    if isinstance(exc, urllib.error.HTTPError):
        try:
            body = exc.read().decode('utf-8', errors='replace').strip()
        except Exception:
            body = ''
        detail = f"HTTP {exc.code} {exc.reason}"
        return f"{detail} | {body[:300]}" if body else detail
    return str(exc)


# Auth-profile-based gateway providers: auto-created when matching profile exists
# Maps auth profile provider name -> (api_type, default_models, default_meta)
GATEWAY_PROVIDER_PROFILES = {
    'openai-codex': ('openai-codex-responses', DEFAULT_OPENAI_CODEX_MODELS, {'reasoning': True, 'contextWindow': 256000, 'maxTokens': 128000, 'input': ['text']}),
    'nvidia-ngc': ('https://api.ngc.nvidia.com', DEFAULT_NGC_MODELS, {'reasoning': False, 'contextWindow': 16384, 'maxTokens': 4096, 'input': ['text', 'audio'], 'output': ['text', 'audio']}),
    'anthropic': ('anthropic-messages', DEFAULT_ANTHROPIC_MODELS, {'reasoning': True, 'contextWindow': 1000000, 'maxTokens': 64000, 'input': ['text']}),
    'openai': ('openai-completions', DEFAULT_OPENAI_MODELS, {'reasoning': False, 'contextWindow': 128000, 'maxTokens': 16384, 'input': ['text']}),
    'xai': ('openai-completions', DEFAULT_XAI_MODELS, {'reasoning': False, 'contextWindow': 128000, 'maxTokens': 16384, 'input': ['text']}),
    'zai': ('openai-completions', DEFAULT_ZAI_MODELS, {'reasoning': True, 'contextWindow': 256000, 'maxTokens': 65536, 'input': ['text']}),
    'darkbloom': ('openai-completions', DEFAULT_DARKBLOOM_MODELS, {'reasoning': False, 'contextWindow': 131072, 'maxTokens': 16384, 'input': ['text']}),
    'github-copilot': ('openclaw-gateway', DEFAULT_GITHUB_COPILOT_MODELS, {'reasoning': True, 'contextWindow': 256000, 'maxTokens': 128000, 'input': ['text']}),
    'cloudflare-workers-ai': ('cloudflare-workers-ai', DEFAULT_CLOUDFLARE_WORKERS_AI_MODELS, {'reasoning': False, 'contextWindow': 32768, 'maxTokens': 4096, 'input': ['text']}),
    'bedrock': ('openclaw-gateway', ['anthropic.claude-sonnet-4-5', 'anthropic.claude-haiku-4-5', 'amazon.nova-pro', 'amazon.nova-lite', 'meta.llama4-405b'], {'reasoning': True, 'contextWindow': 200000, 'maxTokens': 64000, 'input': ['text']}),
    'azure-openai': ('openclaw-gateway', ['gpt-5.4', 'gpt-5.4-mini', 'gpt-4o', 'gpt-4o-mini'], {'reasoning': False, 'contextWindow': 128000, 'maxTokens': 16384, 'input': ['text']}),
}
MAX_PROVIDER_ATTEMPTS = int(os.environ.get('SAGE_ROUTER_MAX_PROVIDER_ATTEMPTS', '8'))
OPENROUTER_FREE_ONLY = os.environ.get('SAGE_ROUTER_OPENROUTER_FREE_ONLY', '0').strip().lower() in {'1', 'true', 'yes', 'on'}
INTENT_CLASSIFIER_ENABLED = os.environ.get('SAGE_ROUTER_INTENT_CLASSIFIER_ENABLED', '0').strip().lower() in {'1', 'true', 'yes', 'on'}
INTENT_CLASSIFIER_PROVIDER = os.environ.get('SAGE_ROUTER_INTENT_CLASSIFIER_PROVIDER', 'ollama')
INTENT_CLASSIFIER_BASE_URL = os.environ.get('SAGE_ROUTER_INTENT_CLASSIFIER_BASE_URL', 'http://127.0.0.1:11434')
INTENT_CLASSIFIER_API_KEY = os.environ.get('SAGE_ROUTER_INTENT_CLASSIFIER_API_KEY', os.environ.get('LLAMACPP_API_KEY', 'local'))
INTENT_CLASSIFIER_MODEL = os.environ.get('SAGE_ROUTER_INTENT_CLASSIFIER_MODEL', 'qwen2.5:0.5b-instruct')
INTENT_CLASSIFIER_TIMEOUT_SECONDS = float(os.environ.get('SAGE_ROUTER_INTENT_CLASSIFIER_TIMEOUT_SECONDS', '3'))
INTENT_CLASSIFIER_MIN_CONFIDENCE = float(os.environ.get('SAGE_ROUTER_INTENT_CLASSIFIER_MIN_CONFIDENCE', '0.65'))
INTENT_CLASSIFIER_MAX_PROMPT_CHARS = int(os.environ.get('SAGE_ROUTER_INTENT_CLASSIFIER_MAX_PROMPT_CHARS', '4000'))
INTENT_CLASSIFIER_ONLY_IF_HEURISTIC_BELOW = int(os.environ.get('SAGE_ROUTER_INTENT_CLASSIFIER_ONLY_IF_HEURISTIC_BELOW', '2'))
# The intent model must never sit on the request path.  Keep routing heuristic-first,
# and let the optional classifier warm a tiny cache for later similar turns only.
INTENT_CLASSIFIER_ASYNC = os.environ.get('SAGE_ROUTER_INTENT_CLASSIFIER_ASYNC', '1').strip().lower() in {'1', 'true', 'yes', 'on'}
INTENT_CLASSIFIER_CACHE_TTL_SECONDS = int(os.environ.get('SAGE_ROUTER_INTENT_CLASSIFIER_CACHE_TTL_SECONDS', '86400'))
INTENT_CLASSIFIER_CACHE_MAX = int(os.environ.get('SAGE_ROUTER_INTENT_CLASSIFIER_CACHE_MAX', '512'))
INTENT_CLASSIFIER_CACHE = {}
INTENT_CLASSIFIER_CACHE_LOCK = threading.Lock()
LATENCY_STATS_LOCK = threading.Lock()
OLLAMA_MODEL_CACHE = {}
OLLAMA_CLOUD_CATALOG_CACHE = {'checked_at': 0, 'models': []}
OLLAMA_CLOUD_CATALOG_TTL_SECONDS = int(os.environ.get('SAGE_ROUTER_OLLAMA_CLOUD_CATALOG_TTL_SECONDS', '21600'))
OLLAMA_CLOUD_CATALOG_URL = os.environ.get('SAGE_ROUTER_OLLAMA_CLOUD_CATALOG_URL', 'https://ollama.com/search?c=cloud')
OLLAMA_CLOUD_CATALOG_MAX_LIBRARIES = int(os.environ.get('SAGE_ROUTER_OLLAMA_CLOUD_CATALOG_MAX_LIBRARIES', '200'))
OLLAMA_CLOUD_CATALOG_MAX_PAGES = int(os.environ.get('SAGE_ROUTER_OLLAMA_CLOUD_CATALOG_MAX_PAGES', '8'))
OLLAMA_CLOUD_CATALOG_ENABLED = os.environ.get('SAGE_ROUTER_OLLAMA_CLOUD_CATALOG_ENABLED', '1').strip().lower() in {'1', 'true', 'yes', 'on'}
LOCAL_OLLAMA_CLOUD_AUTH_BLOCKS = {}
MODEL_HEALTH_CACHE = {}
TEMP_MODEL_BLOCKS = {}
LAST_ROUTE_DEBUG = {
    'updated_at': None,
    'request_id': None,
    'intent': None,
    'complexity': None,
    'thinking': None,
    'routeMode': None,
    'requirements': {},
    'estimatedTokens': 0,
    'json': False,
    'chain': [],
    'scores': [],
    'rejections': [],
    'selected': None,
    'attempts': [],
    'streaming': None,
    'status': None,
    'error': None,
    'totalElapsedMs': None,
}
BACKGROUND_REFRESH_STARTED = False
def canonical_provider_env_key(name: str):
    return (name or '').strip().lower().replace('-', '_')


def load_ollama_manifest_bindings(kind: str):
    prefix = f'SAGE_ROUTER_OLLAMA_MANIFEST_{kind}__'
    bindings = {}
    for key, value in os.environ.items():
        if key.startswith(prefix) and value.strip():
            provider_name = canonical_provider_env_key(key[len(prefix):])
            if provider_name:
                bindings[provider_name] = value.strip()
    return bindings


OLLAMA_MANIFEST_URLS = load_ollama_manifest_bindings('URL')
OLLAMA_MANIFEST_FILES = load_ollama_manifest_bindings('FILE')

INTENT_API_SCORES = {
    'CODE': {'openai-codex-responses': 72, 'ollama': 60, 'openai-completions': 58, 'anthropic-messages': 48, 'google-generative-language': 44, 'google-vertex-ai': 44},
    'ANALYSIS': {'openai-codex-responses': 72, 'ollama': 66, 'anthropic-messages': 58, 'openai-completions': 54, 'google-generative-language': 52, 'google-vertex-ai': 52},
    'CREATIVE': {'openai-codex-responses': 62, 'anthropic-messages': 60, 'google-generative-language': 59, 'google-vertex-ai': 59, 'openai-completions': 55, 'ollama': 50},
    'REALTIME': {'openai-codex-responses': 62, 'google-generative-language': 60, 'google-vertex-ai': 60, 'openai-completions': 60, 'anthropic-messages': 54, 'ollama': 48},
    'GENERAL': {'openai-codex-responses': 64, 'anthropic-messages': 58, 'google-generative-language': 57, 'google-vertex-ai': 57, 'openai-completions': 56, 'ollama': 50},
}

INTENT_MODEL_HINTS = {
    'CODE': ['coder', 'opus', 'sonnet', 'codex', 'gpt-5', 'deepseek', 'qwen', 'kimi', 'glm', 'gptoss'],
    'ANALYSIS': ['opus', 'sonnet', 'gpt-5', 'o3', 'qwen', 'kimi', 'minimax', 'glm'],
    'CREATIVE': ['opus', 'sonnet', 'minimax', 'kimi', 'gpt-5', 'qwen'],
    'REALTIME': ['gpt-4o', 'gpt-5', 'sonnet', 'kimi', 'qwen', 'glm'],
    'GENERAL': ['sonnet', 'gpt-4o', 'gpt-5', 'kimi', 'minimax', 'qwen', 'glm', 'opus'],
}

COMPLEX_MODEL_HINTS = ['opus', 'sonnet', 'gpt-5', 'o3', 'glm-5', 'glm-4.', 'qwen3', 'qwen2.5', 'kimi-k2', 'deepseek-v4']
LIGHTWEIGHT_MODEL_HINTS = ['-mini', 'mini/', ':mini', 'small', 'haiku']
OLLAMA_FAMILY_HINTS = {
    'qwen3.': {'bonus': 9, 'intents': {'CODE', 'ANALYSIS', 'GENERAL'}},
    'kimi': {'bonus': 8, 'intents': {'CODE', 'GENERAL', 'CREATIVE', 'REALTIME'}},
    'kimi-k2': {'bonus': 9, 'intents': {'CODE', 'GENERAL', 'CREATIVE', 'REALTIME', 'ANALYSIS'}},
    'glm-5': {'bonus': 11, 'intents': {'CODE', 'ANALYSIS', 'GENERAL', 'REALTIME'}},
    'minimax-m3': {'bonus': 7, 'intents': {'CREATIVE', 'GENERAL', 'REALTIME'}},
    'minimax-m2.7': {'bonus': 6, 'intents': {'CREATIVE', 'GENERAL', 'REALTIME'}},
    'minimax-m2': {'bonus': 5, 'intents': {'CREATIVE', 'GENERAL'}},
    'deepseek-v4': {'bonus': 10, 'intents': {'CODE', 'ANALYSIS'}},
    'llama': {'bonus': 5, 'intents': {'GENERAL', 'CREATIVE'}},
    'gptoss': {'bonus': 7, 'intents': {'CODE', 'GENERAL', 'ANALYSIS'}},
    'qwen3moe': {'bonus': 8, 'intents': {'CODE', 'GENERAL'}},
    'qwen35moe': {'bonus': 9, 'intents': {'CODE', 'ANALYSIS', 'GENERAL'}},
}


OLLAMA_TOOL_MODEL_HINTS = [
    'qwen3.', 'qwen2.5', 'qwen2', 'kimi-k2', 'minimax-m3', 'minimax-m2', 'glm-5',
    'gpt-oss', 'llama3.1', 'llama3.2', 'llama3.3', 'mistral', 'mixtral', 'nemotron'
]
OLLAMA_NON_TOOL_MODEL_HINTS = ['embed', 'embedding', 'ocr', 'vision', '-vl', ':vl', 'whisper', 'tts']
NVIDIA_TOOL_MODEL_HINTS = [
    'nemotron', 'llama', 'qwen', 'deepseek', 'mistral', 'mixtral', 'gpt-oss', 'glm', 'kimi'
]
NVIDIA_NON_TOOL_MODEL_HINTS = [
    'tts', 'asr', 'canary', 'nemo-tts', 'nemo-asr', 'embed', 'embedding', 'rerank', 'ocr', 'vision', '-vl', ':vl', 'whisper'
]


def is_kimi_model(model: str) -> bool:
    model_l = (model or '').lower()
    return 'kimi' in model_l or 'moonshot' in model_l

ANALYSIS_SIGNAL_TERMS = [
    'analyze', 'analysis', 'evaluate', 'assess', 'compare', 'tradeoff', 'trade-off',
    'why', 'how should', 'how can', 'what should', 'should we', 'can we', 'could we',
    'root cause', 'diagnose', 'strategy', 'recommend', 'recommendation', 'decide',
    'risk', 'failure mode', 'implication', 'forecast', 'predict', 'prioritize',
    'optimize', 'improve', 'smarter', 'heuristic', 'architecture', 'routing',
    'user experience', 'discord-public', 'public channel',
]
ANALYSIS_QUALITY_MODEL_HINTS = [
    'opus', 'sonnet', 'gpt-5.5', 'gpt-5.4', 'gpt-5.3', 'gpt-5', 'o3',
    'gemini-2.5-pro', 'gemini-3-pro', 'qwen3.5', 'qwen3.6', 'qwen3:32b', 'qwen3:30b',
    'kimi-k2', 'minimax-m3', 'minimax-m2.7', 'glm-5', 'deepseek-v4', 'mistral-large-3',
]
WEAK_ANALYSIS_MODEL_HINTS = [
    '-mini', 'mini/', ':mini', 'small', 'haiku', 'flash-lite', 'lite', 'nano', 'tiny',
    '0.5b', '1b', '3b', '7b', '8b', '12b', '14b', '16b',
]

# Known NON-chat families - dynamically extended from /api/tags.
# A family is non-chat if it matches these patterns or is explicitly listed.
NON_CHAT_FAMILY_PATTERNS = ['embed', 'bert', 'clip', 'vl', 'vision', 'ocr', 'asr', 'whisper', 'tts', 'sd', 'rerank']
NON_CHAT_MODEL_HINTS = [
    'embed', 'embedding', 'rerank', 'bge-', 'nomic-embed', 'whisper', 'tts', 'sdxl', 'stable-diffusion',
    'ocr-model', 'asr-model', 'transcribe',
]

# Ollama model families that are NOT text-chat capable.
# Seed list - dynamically extended by background_refresh_detect_families().
NON_CHAT_OLLAMA_FAMILIES = {
    'nomic-bert',   # embedding
    'glmocr',      # OCR vision
    'qwen3vl',     # vision-language
    'llava',       # vision-language
    'clip',        # image embedding
    'bakllava',    # vision-language
    'moondream',   # vision-language
    'minicpm-v',   # vision-language
    'llama-vision',# vision-language
}

class Intent(Enum):
    CODE = auto(); ANALYSIS = auto(); CREATIVE = auto(); REALTIME = auto(); GENERAL = auto()
class Complexity(Enum):
    SIMPLE = auto(); MEDIUM = auto(); COMPLEX = auto()
class ThinkingLevel(Enum):
    LOW = 'low'; MEDIUM = 'medium'; HIGH = 'high'

DEFAULT_THINKING_LEVEL = ThinkingLevel.HIGH

@dataclass
class Provider:
    name: str; api_type: str; base_url: str; api_key: str; models: List[str]; reasoning_models: set[str] | None = None; model_meta: dict[str, dict[str, Any]] | None = None; credentials: list[dict[str, Any]] | None = None; credential_strategy: str = ''


def dedupe_keep_order(items):
    seen = set()
    ordered = []
    for item in items:
        if not item or item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return ordered


def merge_provider(providers, provider):
    existing = providers.get(provider.name)
    if not existing:
        providers[provider.name] = provider
        return
    merged_meta = dict(existing.model_meta or {})
    merged_meta.update(provider.model_meta or {})
    merged_creds = dedupe_credentials((existing.credentials or []) + (provider.credentials or []))
    merged_strategy = provider.credential_strategy or existing.credential_strategy or ''
    providers[provider.name] = Provider(
        provider.name,
        provider.api_type or existing.api_type,
        provider.base_url or existing.base_url,
        provider.api_key or existing.api_key,
        dedupe_keep_order((existing.models or []) + (provider.models or [])),
        set(existing.reasoning_models or set()) | set(provider.reasoning_models or set()),
        merged_meta,
        merged_creds,
        merged_strategy,
    )

def resolve_config_value(value):
    if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
        return os.environ.get(value[2:-1], '')
    return value


# ---------------------------------------------------------------------------
# Multi-credential support: a provider may carry an ordered pool of
# credentials (multiple API keys and/or multiple OAuth subscription paths).
# The pool is failover-ordered: the router tries credentials in order and
# falls over to the next on auth/quota/transient failures. The legacy single
# `apiKey` field is preserved as the first credential for backward compat.
# ---------------------------------------------------------------------------

CRED_FAILOVER_HTTP_CODES = {'401', '402', '403', '404', '408', '409', '418', '425', '429', '500', '502', '503', '504'}
CRED_FAILOVER_TERMS = (
    'unauthorized', 'forbidden', 'rate limit', 'rate_limit', 'ratelimit',
    'quota', 'insufficient_quota', 'billing', 'overloaded', 'capacity',
    'temporarily unavailable', 'timed out', 'timeout', 'connection reset',
    'connection refused', 'auth', 'invalid api key', 'invalid_api_key',
    'expired', 'revoked', 'permission',
)


def normalize_credential(raw):
    """Normalize a raw config credential entry into a canonical dict.

    Accepts either a plain string (treated as an API key) or a dict with
    type/label/key/accessToken/refreshToken/expires/profile fields.
    """
    if raw is None:
        return None
    if isinstance(raw, str):
        raw = raw.strip()
        if not raw:
            return None
        return {'type': 'api_key', 'label': '', 'key': raw}
    if not isinstance(raw, dict):
        return None
    cred = dict(raw)
    ctype = str(cred.get('type') or '').strip().lower() or 'api_key'
    label = str(cred.get('label') or cred.get('name') or '').strip()
    if ctype == 'oauth':
        access = str(cred.get('accessToken') or cred.get('access') or cred.get('token') or '').strip()
        if not access and cred.get('key'):
            access = str(cred.get('key')).strip()
        if not access:
            return None
        return {
            'type': 'oauth',
            'label': label,
            'accessToken': access,
            'refreshToken': str(cred.get('refreshToken') or cred.get('refresh') or '').strip(),
            'expires': int(cred.get('expires') or 0),
            'profile': str(cred.get('profile') or '').strip(),
        }
    # api_key (default)
    key = str(cred.get('key') or cred.get('apiKey') or cred.get('token') or cred.get('value') or '').strip()
    if not key:
        return None
    return {'type': 'api_key', 'label': label, 'key': key}


def dedupe_credentials(creds):
    """Dedupe an ordered credential list by resolved secret value."""
    seen = set()
    out = []
    for raw in creds or []:
        cred = normalize_credential(raw)
        if not cred:
            continue
        sig = cred.get('key') or cred.get('accessToken') or ''
        if sig and sig in seen:
            continue
        if sig:
            seen.add(sig)
        out.append(cred)
    return out


def build_provider_credentials(cfg, legacy_api_key=''):
    """Build the ordered credential pool for a provider config entry.

    Order: explicit `apiKeys` + `oauthPaths` first, then the legacy single
    `apiKey`. Env references (`${VAR}`) are resolved for API keys.
    """
    creds = []
    for raw in (cfg.get('apiKeys') or []):
        cred = normalize_credential(raw)
        if cred:
            creds.append(cred)
    for raw in (cfg.get('oauthPaths') or []):
        cred = normalize_credential(raw)
        if cred:
            cred.setdefault('type', 'oauth')
            if 'type' not in raw and 'accessToken' in raw:
                cred['type'] = 'oauth'
            creds.append(cred)
    if legacy_api_key:
        cred = normalize_credential({'type': 'api_key', 'label': 'default', 'key': legacy_api_key})
        if cred:
            creds.append(cred)
    return dedupe_credentials(creds)


def resolve_credential_key(cred):
    """Return the runtime secret string to send upstream for a credential."""
    if not cred:
        return ''
    if cred.get('type') == 'oauth':
        return str(cred.get('accessToken') or '').strip()
    key = cred.get('key') or ''
    return resolve_config_value(key) if isinstance(key, str) and key.startswith('${') and key.endswith('}') else str(key).strip()


def credential_is_expired(cred, now_ms=None):
    if not cred or cred.get('type') != 'oauth':
        return False
    expires = int(cred.get('expires') or 0)
    if not expires:
        return False
    if now_ms is None:
        now_ms = time.time() * 1000
    return (expires - now_ms) <= 0


def provider_credentials(prov):
    """Return the ordered list of credential dicts for a Provider.

    Falls back to a single-credential pool built from `prov.api_key` when no
    explicit credentials pool is configured (backward compatibility).
    """
    creds = prov.credentials if getattr(prov, 'credentials', None) else None
    if creds:
        return list(creds)
    if prov.api_key:
        return [{'type': 'api_key', 'label': 'default', 'key': prov.api_key}]
    return []


def provider_credential_keys(prov):
    """Ordered list of resolved runtime secret strings for a provider."""
    keys = []
    seen = set()
    for cred in provider_credentials(prov):
        key = resolve_credential_key(cred)
        if key and key not in seen:
            seen.add(key)
            keys.append(key)
    return keys


def is_credential_failover_error(error_text):
    """Decide whether an upstream error should trigger credential failover."""
    text = str(error_text or '').lower()
    if not text:
        return False
    for code in CRED_FAILOVER_HTTP_CODES:
        if f'http {code}' in text:
            return True
    for term in CRED_FAILOVER_TERMS:
        if term in text:
            return True
    return False


def mask_secret(value, visible=4):
    value = str(value or '')
    if not value:
        return ''
    if len(value) <= visible:
        return '•' * len(value)
    return value[:visible] + '•' * (min(len(value) - visible, 16)) + f'…({len(value)})'


def mask_credential(cred):
    cred = dict(cred or {})
    secret = cred.get('key') or cred.get('accessToken') or ''
    cred.pop('key', None)
    cred.pop('accessToken', None)
    cred.pop('refreshToken', None)
    cred['masked'] = mask_secret(secret)
    return cred


# ---------------------------------------------------------------------------
# Credential load balancing. Beyond ordered failover, a provider's credential
# pool can be distributed across keys with one of:
#   - failover   : try pool in order, primary key first (default; backward compat)
#   - round-robin: rotate the starting key per request to spread quota/load
#   - lru        : pick the least-recently-used key first
#   - random     : pick a random order
# Keys that recently failed a failover-classified error enter a short cooldown
# and are deprioritized (tried last) until they recover. The strategy is set
# per-provider via `credentialStrategy` in config or the dashboard.
# ---------------------------------------------------------------------------

CREDENTIAL_STRATEGIES = {'failover', 'round-robin', 'lru', 'random'}
DEFAULT_CREDENTIAL_STRATEGY = (os.environ.get('SAGE_ROUTER_CREDENTIAL_STRATEGY') or 'failover').strip().lower() or 'failover'
CREDENTIAL_COOLDOWN_SECONDS = float(os.environ.get('SAGE_ROUTER_CREDENTIAL_COOLDOWN_SECONDS') or '60')
CREDENTIAL_STATE: dict[tuple, dict] = {}
CREDENTIAL_RR_INDEX: dict[str, int] = {}
CREDENTIAL_STATE_LOCK = threading.Lock()


def _credential_identity(cred, index):
    label = str((cred or {}).get('label') or '').strip()
    return label or f'#{index}'


def provider_credential_strategy(prov):
    raw = str(getattr(prov, 'credential_strategy', '') or '').strip().lower()
    if not raw:
        raw = DEFAULT_CREDENTIAL_STRATEGY
    return raw if raw in CREDENTIAL_STRATEGIES else 'failover'


def _credential_state(provider_name, ident):
    return CREDENTIAL_STATE.setdefault((provider_name, ident), {'lastUsed': 0, 'lastError': 0, 'uses': 0, 'errors': 0})


def mark_credential_used(provider_name, key_or_ident):
    if not key_or_ident:
        return
    with CREDENTIAL_STATE_LOCK:
        st = _credential_state(provider_name, key_or_ident)
        st['lastUsed'] = int(time.time() * 1000)
        st['uses'] = int(st.get('uses', 0)) + 1


def mark_credential_success(provider_name, key_or_ident):
    if not key_or_ident:
        return
    with CREDENTIAL_STATE_LOCK:
        st = _credential_state(provider_name, key_or_ident)
        st['lastError'] = 0
        st['errors'] = 0


def mark_credential_error(provider_name, key_or_ident):
    if not key_or_ident:
        return
    with CREDENTIAL_STATE_LOCK:
        st = _credential_state(provider_name, key_or_ident)
        st['lastError'] = int(time.time() * 1000)
        st['errors'] = int(st.get('errors', 0)) + 1


def select_credential_order(prov):
    """Return the ordered, cooldown-aware list of credential dicts to try."""
    creds = provider_credentials(prov)
    if not creds:
        return []
    strategy = provider_credential_strategy(prov)
    now_ms = time.time() * 1000
    cooldown_ms = CREDENTIAL_COOLDOWN_SECONDS * 1000.0
    enriched = []
    for i, cred in enumerate(creds):
        ident = _credential_identity(cred, i)
        with CREDENTIAL_STATE_LOCK:
            st = dict(CREDENTIAL_STATE.get((prov.name, ident), {'lastUsed': 0, 'lastError': 0, 'uses': 0, 'errors': 0}))
        last_err = st.get('lastError', 0)
        in_cooldown = bool(last_err and (now_ms - last_err) < cooldown_ms)
        enriched.append({'cred': cred, 'ident': ident, 'lastUsed': st.get('lastUsed', 0), 'lastError': last_err, 'uses': st.get('uses', 0), 'errors': st.get('errors', 0), 'in_cooldown': in_cooldown})

    if strategy == 'round-robin':
        with CREDENTIAL_STATE_LOCK:
            start = CREDENTIAL_RR_INDEX.get(prov.name, 0) % max(len(enriched), 1)
            CREDENTIAL_RR_INDEX[prov.name] = (start + 1) % max(len(enriched), 1)
        order = enriched[start:] + enriched[:start]
    elif strategy == 'lru':
        order = sorted(enriched, key=lambda e: (e['lastUsed'] or 0))
    elif strategy == 'random':
        order = list(enriched)
        # Lightweight shuffle without importing random at module top.
        for i in range(len(order) - 1, 0, -1):
            j = int.from_bytes(os.urandom(2), 'big') % (i + 1)
            order[i], order[j] = order[j], order[i]
    else:
        order = enriched  # failover: pool order

    # Deprioritize cooled-down keys; if all are cooling, keep selection order
    # but try the one that errored longest ago first.
    active = [e for e in order if not e['in_cooldown']]
    cooled = sorted([e for e in order if e['in_cooldown']], key=lambda e: e['lastError'] or 0)
    return active + cooled if active else (cooled or order)


def select_credential_keys(prov):
    """Ordered, strategy-aware resolved secret strings to try for a provider."""
    strategy = provider_credential_strategy(prov)
    if strategy == 'failover':
        # Preserve exact legacy behavior: pool order with the (possibly
        # refreshed) primary api_key tried first.
        keys = provider_credential_keys(prov)
        if prov.api_key:
            if prov.api_key in keys:
                keys.remove(prov.api_key)
            keys = [prov.api_key] + keys
        return keys or [prov.api_key]
    order = select_credential_order(prov)
    keys = []
    seen = set()
    for e in order:
        key = resolve_credential_key(e['cred'])
        if key and key not in seen:
            seen.add(key)
            keys.append(key)
    return keys


def select_credential_identities(prov):
    """Ordered identities parallel to select_credential_keys (for state hooks)."""
    strategy = provider_credential_strategy(prov)
    if strategy == 'failover':
        return []  # failover does not use LB state hooks
    order = select_credential_order(prov)
    out = []
    seen = set()
    for e in order:
        key = resolve_credential_key(e['cred'])
        if key and key not in seen:
            seen.add(key)
            out.append(e['ident'])
    return out


def credential_state_snapshot(provider_name, creds):
    """Dashboard-safe per-credential state (no secrets)."""
    now_ms = time.time() * 1000
    cooldown_ms = CREDENTIAL_COOLDOWN_SECONDS * 1000.0
    snap = []
    for i, cred in enumerate(creds):
        ident = _credential_identity(cred, i)
        with CREDENTIAL_STATE_LOCK:
            st = dict(CREDENTIAL_STATE.get((provider_name, ident), {'lastUsed': 0, 'lastError': 0, 'uses': 0, 'errors': 0}))
        last_err = st.get('lastError', 0)
        snap.append({
            'label': ident,
            'uses': st.get('uses', 0),
            'errors': st.get('errors', 0),
            'lastUsedMs': st.get('lastUsed', 0),
            'lastErrorMs': last_err,
            'inCooldown': bool(last_err and (now_ms - last_err) < cooldown_ms),
        })
    return snap


def is_self_provider(name, base_url):
    if name in SELF_PROVIDER_NAMES:
        return True
    parsed = urllib.parse.urlparse(base_url or '')
    return parsed.hostname in {'127.0.0.1', 'localhost'} and parsed.port in {8787, 8788, 8790}


def is_local_dario_endpoint(base_url):
    parsed = urllib.parse.urlparse(base_url or '')
    return parsed.hostname in {'127.0.0.1', 'localhost'} and parsed.port == 3456


def is_lan_or_tailnet_endpoint(base_url):
    """True when the provider endpoint itself is local/LAN/Tailnet.

    Used by route=local-first, which is intentionally local-strict: no
    Internet API endpoints, even if they are otherwise healthy and cheap.
    Allows loopback, RFC1918/private LAN, link-local, IPv6 ULA, and
    Tailscale/CGNAT 100.64.0.0/10 addresses. Bare hostnames and .local/.lan
    names are treated as local network names.
    """
    parsed = urllib.parse.urlparse(base_url or '')
    host = (parsed.hostname or '').strip().lower().rstrip('.')
    if not host:
        return False
    if host in {'localhost'}:
        return True
    if '.' not in host and ':' not in host:
        return True
    if host.endswith(('.local', '.lan', '.home', '.tailnet')):
        return True
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        return False
    tailscale_cgnat = ip.version == 4 and ip in ipaddress.ip_network('100.64.0.0/10')
    return bool(ip.is_loopback or ip.is_private or ip.is_link_local or tailscale_cgnat)


def provider_allowed_in_local_first(provider):
    if provider.name in LOCAL_STRICT_DECENTRALIZED_PROVIDER_NAMES:
        return True
    if provider.name in LOCAL_STRICT_PROXY_PROVIDER_NAMES:
        return False
    if provider.api_type in LOCAL_STRICT_PROXY_API_TYPES:
        return False
    return is_lan_or_tailnet_endpoint(provider.base_url)


def local_first_rejection_reason(provider):
    if provider.name in LOCAL_STRICT_PROXY_PROVIDER_NAMES or provider.api_type in LOCAL_STRICT_PROXY_API_TYPES:
        return 'excluded by local-first (known cloud/SSO proxy provider)'
    return 'excluded by local-first (endpoint is not LAN/Tailnet/local)'


def should_route_anthropic_to_dario(name, api_type, base_url):
    host = (urllib.parse.urlparse(base_url or '').hostname or '').lower()
    if name == DARIO_PROVIDER_NAME or is_local_dario_endpoint(base_url):
        return False
    if name == 'anthropic':
        return True
    return api_type == 'anthropic-messages' and ('anthropic.com' in host or host == 'api.anthropic.com')


def dario_endpoint_ready(timeout=0.5):
    parsed = urllib.parse.urlparse(DARIO_LOCAL_BASE_URL or '')
    host = parsed.hostname or '127.0.0.1'
    port = parsed.port or 3456
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False


def ensure_dario_proxy_ready():
    """Ensure the Dario Anthropic-compatible proxy is reachable.

    On systemd hosts this preserves the old user-service behavior. In Docker or
    other non-systemd runtimes, it can autostart the bundled `dario proxy`
    binary when SAGE_ROUTER_DARIO_AUTOSTART is truthy.
    """
    global DARIO_PROCESS
    if dario_endpoint_ready():
        return True
    try:
        if shutil.which('systemctl'):
            active = subprocess.run(
                ['systemctl', '--user', 'is-active', '--quiet', DARIO_SERVICE_NAME],
                check=False,
                capture_output=True,
                timeout=5,
            )
            if active.returncode == 0 and dario_endpoint_ready(timeout=1.0):
                return True
            if shutil.which('dario'):
                start = subprocess.run(
                    ['systemctl', '--user', 'start', DARIO_SERVICE_NAME],
                    check=False,
                    capture_output=True,
                    timeout=10,
                )
                if start.returncode == 0:
                    for _ in range(20):
                        if dario_endpoint_ready(timeout=0.5):
                            logger.info(f'Started {DARIO_SERVICE_NAME} for Anthropic compatibility')
                            return True
                        time.sleep(0.25)
                else:
                    detail = (start.stderr or start.stdout or b'').decode('utf-8', errors='replace').strip()
                    logger.warning(f'Failed to start {DARIO_SERVICE_NAME}: {detail[:300]}')

        if not DARIO_AUTOSTART:
            logger.warning('Dario autostart disabled and proxy is not reachable')
            return False
        if not shutil.which('dario'):
            logger.warning('Anthropic provider detected but dario is not installed on PATH')
            return False
        if DARIO_PROCESS is not None and DARIO_PROCESS.poll() is None:
            return dario_endpoint_ready(timeout=1.0)
        parsed = urllib.parse.urlparse(DARIO_LOCAL_BASE_URL or '')
        host = parsed.hostname or '127.0.0.1'
        port = str(parsed.port or 3456)
        cmd = ['dario', 'proxy', '--host', host, '--port', port]
        DARIO_PROCESS = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
            start_new_session=True,
        )
        for _ in range(40):
            if dario_endpoint_ready(timeout=0.5):
                logger.info(f'Started bundled Dario proxy at {DARIO_LOCAL_BASE_URL}')
                return True
            if DARIO_PROCESS.poll() is not None:
                break
            time.sleep(0.25)
        logger.warning('Dario proxy autostart did not become reachable')
        return False
    except Exception as e:
        logger.warning(f'Failed to ensure Dario proxy readiness: {e}')
        return False



def openai_chat_completions_url(base_url):
    base = (base_url or '').rstrip('/')
    host = (urllib.parse.urlparse(base).hostname or '').lower()
    if 'githubcopilot.com' in host:
        return base + '/chat/completions'
    if base.endswith('/v1') or base.endswith('/api/v1'):
        return base + '/chat/completions'
    return base + '/v1/chat/completions'


def add_openai_compat_headers(hdrs, provider_name=''):
    if (provider_name or '').strip().lower() == 'github-copilot':
        hdrs.setdefault('User-Agent', 'GitHubCopilotChat/0.35.0')
        hdrs.setdefault('Editor-Version', 'vscode/1.107.0')
        hdrs.setdefault('Editor-Plugin-Version', 'copilot-chat/0.35.0')
        hdrs.setdefault('Copilot-Integration-Id', 'vscode-chat')
    return hdrs

def infer_api_type(name, cfg, base_url):
    api_type = cfg.get('api')
    if api_type:
        if api_type in {'openai', 'openai-compatible'}:
            return 'openai-completions'
        if api_type == 'anthropic':
            return 'anthropic-messages'
        # Normalize google-generative-ai -> google-generative-language (OpenClaw schema enum)
        if api_type in {'google-generative-ai', 'google', 'gemini'}:
            return 'google-generative-language'
        if api_type in {'google-vertex-ai', 'vertex-ai', 'vertex'}:
            return 'google-vertex-ai'
        if api_type in {'cloudflare-workers-ai', 'cloudflare', 'workers-ai'}:
            return 'cloudflare-workers-ai'
        if api_type in {'ollama', 'ollama-cloud'}:
            return 'ollama'
        return api_type
    host = (urllib.parse.urlparse(base_url or '').hostname or '').lower()
    port = urllib.parse.urlparse(base_url or '').port
    name_l = str(name or '').strip().lower()
    if (
        name_l.startswith('ollama') or
        (host in {'ollama', 'localhost', '127.0.0.1', 'host.docker.internal'} and port == 11434) or
        'ollama.com' in host
    ):
        return 'ollama'
    if 'api.cloudflare.com' in host or name in {'cloudflare', 'cloudflare-workers-ai', 'workers-ai'}:
        return 'cloudflare-workers-ai'
    if 'aiplatform.googleapis.com' in host or name_l in {'google-vertex', 'vertex-ai', 'vertex'}:
        return 'google-vertex-ai'
    if 'generativelanguage.googleapis.com' in host or name_l in {'google', 'gemini'}:
        return 'google-generative-language'
    if 'anthropic.com' in host or name_l == 'anthropic':
        return 'anthropic-messages'
    if 'x.ai' in host or name_l == 'xai':
        return 'openai-completions'
    return 'openai-completions'


def discover_anthropic_models():
    """Discover available Anthropic models via the Dario proxy's /v1/models endpoint."""
    try:
        url = DARIO_LOCAL_BASE_URL.rstrip('/') + '/v1/models'
        hdrs = {'x-api-key': DARIO_LOCAL_API_KEY, 'anthropic-version': '2023-06-01'}
        req = urllib.request.Request(url, headers=hdrs)
        with urllib.request.urlopen(req, timeout=10) as resp:
            payload = json.loads(resp.read())
        models = [m.get('id', '') for m in payload.get('data', []) if m.get('id')]
        if models:
            logger.info(f'Discovered {len(models)} Anthropic models via Dario: {models}')
            return models
    except Exception as e:
        logger.debug(f'Dario model discovery failed: {extract_http_error(e)}')
    return None




def cloudflare_workers_ai_base_url(base_url: str) -> str:
    base = (base_url or '').strip().rstrip('/')
    if base:
        return base
    account_id = os.environ.get('SAGE_ROUTER_CLOUDFLARE_ACCOUNT_ID') or os.environ.get('CLOUDFLARE_ACCOUNT_ID') or ''
    if not account_id:
        raise RuntimeError('Cloudflare Workers AI provider needs CLOUDFLARE_ACCOUNT_ID or baseUrl with /accounts/{id}/ai')
    return f'https://api.cloudflare.com/client/v4/accounts/{account_id}/ai'


def cloudflare_workers_ai_run_url(base_url: str, model: str) -> str:
    base = cloudflare_workers_ai_base_url(base_url)
    if '/run/' in base:
        return base
    return base.rstrip('/') + '/run/' + urllib.parse.quote(model, safe='@:/')


def cloudflare_workers_ai_models_url(base_url: str) -> str:
    return cloudflare_workers_ai_base_url(base_url).rstrip('/') + '/models/search'


def discover_cloudflare_workers_ai_models(base_url, api_key=''):
    if not api_key:
        return DEFAULT_CLOUDFLARE_WORKERS_AI_MODELS
    try:
        req = urllib.request.Request(cloudflare_workers_ai_models_url(base_url), headers={'Authorization': f'Bearer {api_key}'})
        with urllib.request.urlopen(req, timeout=OPENAI_COMPAT_TIMEOUT_SECONDS) as resp:
            payload = json.loads(resp.read())
        result = payload.get('result') or []
        models = []
        for entry in result:
            mid = entry.get('id') or entry.get('name') or ''
            task = str(entry.get('task') or entry.get('task_name') or entry.get('type') or '').lower()
            if mid and (not task or any(x in task for x in ('text generation', 'text-generation', 'chat', 'llm'))):
                models.append(mid)
        return dedupe_keep_order(models) or DEFAULT_CLOUDFLARE_WORKERS_AI_MODELS
    except Exception as e:
        logger.warning(f'Cloudflare Workers AI model discovery failed: {extract_http_error(e)}')
        return DEFAULT_CLOUDFLARE_WORKERS_AI_MODELS

def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')


def google_vertex_adc_credentials_path() -> str:
    return os.path.expanduser(
        os.environ.get('SAGE_ROUTER_GOOGLE_APPLICATION_CREDENTIALS')
        or os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        or os.path.join('~', '.config', 'gcloud', 'application_default_credentials.json')
    )


def google_vertex_access_token() -> str:
    now = int(time.time())
    cached = GOOGLE_VERTEX_TOKEN_CACHE
    if cached.get('access_token') and int(cached.get('expires_at') or 0) - now > 120:
        return cached['access_token']
    path = google_vertex_adc_credentials_path()
    with open(path) as f:
        creds = json.load(f)
    if creds.get('type') != 'service_account':
        raise RuntimeError(f'Unsupported ADC credential type for Vertex provider: {creds.get("type") or "missing"}')
    private_key = creds.get('private_key')
    client_email = creds.get('client_email')
    if not private_key or not client_email:
        raise RuntimeError('ADC service account JSON is missing private_key/client_email')
    header = {'alg': 'RS256', 'typ': 'JWT'}
    claims = {
        'iss': client_email,
        'scope': GOOGLE_VERTEX_ADC_SCOPE,
        'aud': 'https://oauth2.googleapis.com/token',
        'iat': now,
        'exp': now + 3600,
    }
    signing_input = (_b64url(json.dumps(header, separators=(',', ':')).encode()) + '.' + _b64url(json.dumps(claims, separators=(',', ':')).encode())).encode()
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding
    key = serialization.load_pem_private_key(private_key.encode(), password=None)
    signature = key.sign(signing_input, padding.PKCS1v15(), hashes.SHA256())
    assertion = signing_input.decode() + '.' + _b64url(signature)
    body = urllib.parse.urlencode({'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer', 'assertion': assertion}).encode()
    req = urllib.request.Request('https://oauth2.googleapis.com/token', data=body, headers={'Content-Type': 'application/x-www-form-urlencoded'})
    with urllib.request.urlopen(req, timeout=GOOGLE_TIMEOUT_SECONDS) as resp:
        payload = json.loads(resp.read())
    token = payload.get('access_token')
    if not token:
        raise RuntimeError('OAuth token response did not include access_token')
    cached['access_token'] = token
    cached['expires_at'] = now + int(payload.get('expires_in') or 3600)
    return token


def google_vertex_base_url(base_url: str) -> str:
    base = (base_url or '').strip().rstrip('/')
    if base:
        return base
    project = GOOGLE_VERTEX_PROJECT
    if not project:
        try:
            with open(google_vertex_adc_credentials_path()) as f:
                project = json.load(f).get('project_id') or ''
        except Exception:
            project = ''
    if not project:
        raise RuntimeError('Vertex provider needs GOOGLE_CLOUD_PROJECT or a service account project_id')
    location = GOOGLE_VERTEX_LOCATION
    return f'https://{location}-aiplatform.googleapis.com/v1/projects/{project}/locations/{location}/publishers/google'


def google_vertex_url(base_url: str, model: str, method: str = 'generateContent') -> str:
    base = google_vertex_base_url(base_url)
    if '/models/' in base:
        return base + f':{method}'
    return base.rstrip('/') + f'/models/{urllib.parse.quote(model, safe="")}:{method}'


def discover_google_vertex_models(base_url):
    configured_defaults = ['gemini-3-flash-preview', 'gemini-2.5-pro', 'gemini-2.5-flash']
    try:
        token = google_vertex_access_token()
        url = google_vertex_base_url(base_url).rstrip('/') + '/models'
        req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
        with urllib.request.urlopen(req, timeout=GOOGLE_TIMEOUT_SECONDS) as resp:
            payload = json.loads(resp.read())
        models = []
        for entry in payload.get('publisherModels', []) or payload.get('models', []):
            name = entry.get('name', '')
            if '/models/' in name:
                name = name.rsplit('/models/', 1)[1]
            if name:
                models.append(name)
        if models:
            logger.info(f'Discovered {len(models)} Vertex AI Gemini models via API')
            return dedupe_keep_order(models)
    except Exception as e:
        logger.warning(f"Vertex AI model discovery {base_url or GOOGLE_VERTEX_PROJECT}: {extract_http_error(e)}")
    return configured_defaults

def discover_google_models(base_url, api_key):
    if not base_url or not api_key:
        return []
    try:
        # Google API requires ?key= query param on /v1beta/models endpoint
        base = base_url.rstrip('/')
        if not base.endswith('/v1beta') and not base.endswith('/v1'):
            base += '/v1beta'
        url = f'{base}/models?key={api_key}'
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=GOOGLE_TIMEOUT_SECONDS) as resp:
            payload = json.loads(resp.read())
        models = []
        for entry in payload.get('models', []):
            methods = entry.get('supportedGenerationMethods') or []
            if 'generateContent' not in methods and 'streamGenerateContent' not in methods:
                continue
            model_name = entry.get('name', '')
            if model_name.startswith('models/'):
                model_name = model_name.split('/', 1)[1]
            if model_name:
                models.append(model_name)
        if models:
            logger.info(f'Discovered {len(models)} Google models via API')
        return dedupe_keep_order(models)
    except Exception as e:
        logger.warning(f"Google model discovery {base_url}: {extract_http_error(e)}")
        return []


def discover_openai_models(base_url, api_key):
    """Discover available OpenAI models via /v1/models endpoint."""
    if not base_url or not api_key:
        return []
    try:
        url = base_url.rstrip('/') + '/v1/models'
        hdrs = {'Authorization': f'Bearer {api_key}'}
        req = urllib.request.Request(url, headers=hdrs)
        with urllib.request.urlopen(req, timeout=OPENAI_COMPAT_TIMEOUT_SECONDS) as resp:
            payload = json.loads(resp.read())
        models = [m.get('id', '') for m in payload.get('data', []) if m.get('id')]
        # Filter to chat completion models only
        chat_models = [m for m in models if any(x in m.lower() for x in ['gpt', 'chat', 'o1', 'o3'])]
        if chat_models:
            logger.info(f'Discovered {len(chat_models)} OpenAI chat models via API')
        return dedupe_keep_order(chat_models)
    except Exception as e:
        logger.debug(f"OpenAI model discovery {base_url}: {extract_http_error(e)}")
        return []



def discover_darkbloom_models(base_url, api_key):
    """Discover Darkbloom models via OpenAI-compatible /v1/models.

    Darkbloom model IDs are mostly MLX community names, so do not apply the
    OpenAI-specific GPT/chat/o-series filter used for api.openai.com.
    """
    if not base_url or not api_key:
        return []
    try:
        root = base_url.rstrip('/')
        url = root + '/v1/models'
        hdrs = {'Authorization': f'Bearer {api_key}'}
        req = urllib.request.Request(url, headers=hdrs)
        with urllib.request.urlopen(req, timeout=OPENAI_COMPAT_TIMEOUT_SECONDS) as resp:
            payload = json.loads(resp.read())
        models = [m.get('id', '') for m in payload.get('data', []) if m.get('id')]
        if models:
            logger.info(f'Discovered {len(models)} Darkbloom models via API')
        return dedupe_keep_order(models)
    except Exception as e:
        logger.debug(f"Darkbloom model discovery {base_url}: {extract_http_error(e)}")
        return []

def discover_openrouter_models(base_url, api_key):
    """Discover OpenRouter models, optionally constrained to :free IDs."""
    if not base_url or not api_key:
        return []
    try:
        root = base_url.rstrip('/')
        if root.endswith('/v1'):
            root = root[:-3]
        url = root.rstrip('/') + '/v1/models'
        hdrs = {'Authorization': f'Bearer {api_key}'}
        req = urllib.request.Request(url, headers=hdrs)
        with urllib.request.urlopen(req, timeout=OPENAI_COMPAT_TIMEOUT_SECONDS) as resp:
            payload = json.loads(resp.read())
        models = [m.get('id', '') for m in payload.get('data', []) if m.get('id')]
        if OPENROUTER_FREE_ONLY:
            models = [m for m in models if str(m).endswith(':free')]
        if models:
            suffix = ' free' if OPENROUTER_FREE_ONLY else ''
            logger.info(f'Discovered {len(models)} OpenRouter{suffix} models via API')
        return dedupe_keep_order(models)
    except Exception as e:
        logger.debug(f"OpenRouter model discovery {base_url}: {extract_http_error(e)}")
        return []


def discover_github_copilot_models(base_url, api_key):
    """Discover available GitHub Copilot models via /v1/models endpoint."""
    if not base_url or not api_key:
        return []
    try:
        url = base_url.rstrip('/') + '/v1/models'
        hdrs = {'Authorization': f'Bearer {api_key}'}
        req = urllib.request.Request(url, headers=hdrs)
        with urllib.request.urlopen(req, timeout=OPENAI_COMPAT_TIMEOUT_SECONDS) as resp:
            payload = json.loads(resp.read())
        models = [m.get('id', '') for m in payload.get('data', []) if m.get('id')]
        if models:
            logger.info(f'Discovered {len(models)} GitHub Copilot models via API')
        return dedupe_keep_order(models)
    except Exception as e:
        logger.debug(f"GitHub Copilot model discovery {base_url}: {extract_http_error(e)}")
        return []


def discover_openclaw_gateway_models(base_url, gateway_token=None):
    """Discover available OpenClaw Gateway models via /v1/models endpoint."""
    if not base_url:
        return []
    try:
        url = base_url.rstrip('/') + '/v1/models'
        req = urllib.request.Request(url)
        # Add auth if token available
        if gateway_token:
            req.add_header('Authorization', f'Bearer {gateway_token}')
        with urllib.request.urlopen(req, timeout=5) as resp:
            payload = json.loads(resp.read())
        models = [m.get('id', '') for m in payload.get('data', []) if m.get('id')]
        if models:
            logger.info(f'Discovered {len(models)} OpenClaw Gateway models via API')
        return dedupe_keep_order(models)
    except Exception as e:
        logger.debug(f"OpenClaw Gateway model discovery {base_url}: {extract_http_error(e)}")
        return []


def discover_xai_models(base_url, api_key):
    """Discover available xAI Grok models via /v1/models endpoint (API-key mode)."""
    if not base_url or not api_key:
        return []
    try:
        url = base_url.rstrip('/') + '/v1/models'
        hdrs = {'Authorization': f'Bearer {api_key}'}
        req = urllib.request.Request(url, headers=hdrs)
        with urllib.request.urlopen(req, timeout=OPENAI_COMPAT_TIMEOUT_SECONDS) as resp:
            payload = json.loads(resp.read())
        models = [m.get('id', '') for m in payload.get('data', []) if m.get('id')]
        if models:
            logger.info(f'Discovered {len(models)} xAI Grok models via API')
        return dedupe_keep_order(models)
    except Exception as e:
        logger.debug(f"xAI model discovery {base_url}: {extract_http_error(e)}")
        return []


def discover_hermes_core_providers():
    """Discover all providers from Hermes Agent core config (~/.hermes/config.yaml and auth.json)."""
    providers = {}
    try:
        config_path = os.path.expanduser("~/.hermes/config.yaml")
        auth_path = os.path.expanduser("~/.hermes/auth.json")
        
        # Read Hermes config
        if os.path.exists(config_path):
            import yaml
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            model_config = config.get('model', {})
            providers['hermes-active'] = {
                'default': model_config.get('default'),
                'provider': model_config.get('provider'),
                'baseUrl': model_config.get('base_url'),
                'source': 'hermes-config'
            }
        
        # Read Hermes auth providers
        if os.path.exists(auth_path):
            with open(auth_path, 'r') as f:
                auth = json.load(f)
            auth_providers = auth.get('providers', {})
            for provider_name, provider_data in auth_providers.items():
                providers[f'hermes-{provider_name}'] = {
                    'authMode': provider_data.get('auth_mode'),
                    'lastRefresh': provider_data.get('last_refresh'),
                    'hasIdToken': bool(provider_data.get('tokens', {}).get('id_token')),
                    'hasAccessToken': bool(provider_data.get('tokens', {}).get('access_token')),
                    'source': 'hermes-auth'
                }
        
        logger.info(f"Discovered {len(providers)} providers from Hermes core")
    except Exception as e:
        logger.debug(f"Hermes core provider discovery failed: {e}")
    return providers


def discover_openclaw_agent_auth_providers():
    """Discover OAuth providers from OpenClaw agent auth-profiles.json."""
    providers = {}
    try:
        # Try main agent first
        auth_path = os.path.expanduser('~/.openclaw/agents/main/agent/auth-profiles.json')
        if not os.path.exists(auth_path):
            # Fallback to checking other agents
            agents_dir = os.path.expanduser('~/.openclaw/agents')
            if os.path.exists(agents_dir):
                for agent in os.listdir(agents_dir):
                    candidate = os.path.join(agents_dir, agent, 'agent', 'auth-profiles.json')
                    if os.path.exists(candidate):
                        auth_path = candidate
                        break
        
        if not os.path.exists(auth_path):
            return providers
        
        with open(auth_path) as f:
            auth = json.load(f)
        
        profiles = auth.get('profiles', {})
        now_ms = time.time() * 1000
        
        for profile_name, profile in profiles.items():
            if profile.get('type') != 'oauth':
                continue
            
            provider_name = profile.get('provider', profile_name.split(':')[0])
            access_token = profile.get('access', '')
            refresh_token = profile.get('refresh', '')
            expires = profile.get('expires', 0)
            
            # Check if expired
            is_valid = expires and (expires - now_ms) > 0
            
            providers[f'openclaw-{profile_name}'] = {
                'provider': provider_name,
                'profile': profile_name,
                'hasAccessToken': bool(access_token),
                'hasRefreshToken': bool(refresh_token),
                'expires': expires,
                'isExpired': not is_valid,
                'source': 'openclaw-agent-auth'
            }
            
            # Also store tokens for gateway to use
            if access_token:
                # Store in a format sage-router can use
                if provider_name not in providers:
                    providers[provider_name] = {
                        'accessToken': access_token,
                        'refreshToken': refresh_token,
                        'expires': expires,
                        'source': 'openclaw-agent-auth',
                        'profile': profile_name
                    }
        
        logger.info(f"Discovered {len(providers)} providers from OpenClaw agent auth")
    except Exception as e:
        logger.debug(f"OpenClaw agent auth discovery failed: {e}")
    
    return providers



def discover_openclaw_cli_providers(timeout_seconds=15):
    """Discover providers using 'openclaw models list --all' CLI with caching."""
    cache_key = 'openclaw_cli_providers'
    cache_ttl = 60  # Cache for 60 seconds
    
    # Check cache
    now = time.time()
    if hasattr(discover_openclaw_cli_providers, '_cache'):
        cached_data, cached_time = discover_openclaw_cli_providers._cache
        if now - cached_time < cache_ttl:
            return cached_data
    
    providers = {}
    try:
        result = subprocess.run(
            ['openclaw', 'models', 'list', '--all'],
            capture_output=True,
            text=True,
            timeout=timeout_seconds
        )
        if result.returncode == 0:
            # Parse the output - assume it's JSON or table format
            output = result.stdout.strip()
            if output.startswith('{'):
                # JSON output
                providers = json.loads(output)
            else:
                # Parse table/text output
                providers = {'raw': output[:5000]}  # Limit size
            logger.info(f"Discovered providers via openclaw CLI")
    except subprocess.TimeoutExpired:
        logger.warning("openclaw CLI timed out - using cached/config data")
    except Exception as e:
        logger.debug(f"openclaw CLI discovery failed: {e}")
    
    # Cache result even if empty (to avoid hammering)
    discover_openclaw_cli_providers._cache = (providers, now)
    return providers


def discover_hermes_cli_providers(timeout_seconds=10):
    """Discover providers using 'hermes' CLI with caching."""
    cache_key = 'hermes_cli_providers'
    cache_ttl = 60  # Cache for 60 seconds
    
    # Check cache
    now = time.time()
    if hasattr(discover_hermes_cli_providers, '_cache'):
        cached_data, cached_time = discover_hermes_cli_providers._cache
        if now - cached_time < cache_ttl:
            return cached_data
    
    providers = {}
    try:
        # Try hermes status --json if available
        result = subprocess.run(
            ['hermes', 'status', '--json'],
            capture_output=True,
            text=True,
            timeout=timeout_seconds
        )
        if result.returncode == 0 and result.stdout.strip():
            try:
                status = json.loads(result.stdout)
                providers['hermes-status'] = status
            except json.JSONDecodeError:
                providers['hermes-status'] = {'raw': result.stdout[:2000]}
        else:
            # Fallback: try hermes model --json
            result2 = subprocess.run(
                ['hermes', 'model', '--json'],
                capture_output=True,
                text=True,
                timeout=timeout_seconds
            )
            if result2.returncode == 0 and result2.stdout.strip():
                try:
                    model_info = json.loads(result2.stdout)
                    providers['hermes-model'] = model_info
                except json.JSONDecodeError:
                    providers['hermes-model'] = {'raw': result2.stdout[:2000]}
        logger.info(f"Discovered providers via Hermes CLI")
    except subprocess.TimeoutExpired:
        logger.warning("Hermes CLI timed out - using cached/config data")
    except Exception as e:
        logger.debug(f"Hermes CLI discovery failed: {e}")
    
    # Cache result even if empty
    discover_hermes_cli_providers._cache = (providers, now)
    return providers


def discover_openclaw_core_providers():
    """Discover all providers and models from OpenClaw core config (~/.openclaw/openclaw.json)."""
    providers = {}
    try:
        config_path = os.path.expanduser("~/.openclaw/openclaw.json")
        if not os.path.exists(config_path):
            return providers
        with open(config_path, 'r') as f:
            config = json.load(f)
        models_config = config.get('models', {})
        providers_config = models_config.get('providers', {})
        for provider_name, provider_cfg in providers_config.items():
            models = []
            raw_models = provider_cfg.get('models', [])
            if isinstance(raw_models, list):
                for m in raw_models:
                    if isinstance(m, dict) and m.get('id'):
                        models.append({
                            'id': m.get('id'),
                            'name': m.get('name', m.get('id')),
                            'reasoning': m.get('reasoning', False),
                            'contextWindow': m.get('contextWindow'),
                            'maxTokens': m.get('maxTokens'),
                            'input': m.get('input', ['text']),
                            'cost': m.get('cost', {})
                        })
            providers[provider_name] = {
                'baseUrl': provider_cfg.get('baseUrl'),
                'api': provider_cfg.get('api', 'openai-completions'),
                'models': models
            }
        logger.info(f"Discovered {len(providers)} providers from OpenClaw core config")
    except Exception as e:
        logger.debug(f"OpenClaw core provider discovery failed: {e}")
    return providers


def fetch_github_providers_manifest(repo_owner, repo_name, path_in_repo="providers.json", timeout_seconds=10):
    """Fetch provider manifest from GitHub repo source code."""
    try:
        url = f"https://raw.githubusercontent.com/{repo_owner}/{repo_name}/main/{path_in_repo}"
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=timeout_seconds) as resp:
            return json.loads(resp.read())
    except Exception as e:
        logger.debug(f"GitHub fetch failed for {repo_owner}/{repo_name}: {e}")
        return None


def discover_openclaw_github_manifests():
    """Discover OpenClaw providers from GitHub source manifests."""
    manifests = {}
    
    # Try to fetch from OpenClaw GitHub repo
    manifest = fetch_github_providers_manifest("openclaw", "openclaw", "providers.json")
    if manifest:
        manifests['openclaw-github'] = manifest
    
    # Fallback: known OpenClaw provider patterns from source analysis
    manifests['openclaw-supported'] = {
        "source": "GitHub source analysis",
        "url": "https://github.com/openclaw/openclaw",
        "providers": [
            {"name": "anthropic", "api": "anthropic-messages", "models": ["claude-opus", "claude-sonnet", "claude-haiku"]},
            {"name": "openai", "api": "openai-completions", "models": ["gpt-5.4", "gpt-4o", "gpt-4o-mini"]},
            {"name": "google", "api": "google-generative-ai", "models": ["gemini-3-pro", "gemini-3-flash", "gemini-2.5-pro", "gemini-2.5-flash"]},
            {"name": "haimaker", "api": "openai-completions", "models": ["qwen3-coder", "llama-3.3-70b"]},
            {"name": "minimax", "api": "openai-completions", "models": ["minimax-m2.5", "minimax-m2.7"]},
            {"name": "moonshot", "api": "openai-completions", "models": ["kimi-k2", "kimi-k2.5", "kimi-k2.6"]},
            {"name": "ollama", "api": "ollama", "models": ["dynamic-local"]},
            {"name": "openrouter", "api": "openai-completions", "models": ["200+ models"]},
            {"name": "xiaomi", "api": "openai-completions", "models": ["mimo-v2-pro"]},
            {"name": "zai", "api": "openai-completions", "models": ["glm-5", "glm-5-turbo", "glm-5.1", "glm-5v-turbo"], "subscriptionPlans": {
                "lite": {"price": "$6/month", "quarterly": "$27/quarter"},
                "pro": {"price": "$30/month", "quarterly": "$81/quarter"},
                "max": {"price": "$72/month", "quarterly": "$216/quarter"}
            }, "apiPricing": {
                "glm-5": {"input": "$1.00/1M", "output": "$3.20/1M"},
                "glm-5-turbo": {"input": "$1.20/1M", "output": "$4.00/1M", "cacheRead": "$0.24/1M"}
            }},
            {"name": "alibaba-qwen", "api": "openai-completions", "models": ["qwen-max", "qwen-plus", "qwen-flash", "qwen-turbo", "qwen2.5-72b", "qwen2.5-coder", "qwen3-vl-flash"], "subscriptionPlans": {
                "codingLite": {"price": "$10/month", "requests": "18,000/month"},
                "codingPro": {"price": "$50/month", "requests": "90,000/month"},
                "freeTier": {"tokens": "1M", "valid": "90 days"}
            }, "apiPricing": {
                "qwen-max": {"input": "$1.60/1M", "output": "$6.40/1M"},
                "qwen-plus": {"input": "$0.40/1M", "output": "$1.20/1M"},
                "qwen-flash": {"input": "$0.022-0.173/1M", "output": "$0.216-1.721/1M"},
                "qwen-turbo": {"input": "$0.05/1M", "output": "$0.20-0.40/1M"}
            }},
            {"name": "bedrock", "api": "openai-completions", "models": ["claude", "nova", "llama"]},
            {"name": "deepseek", "api": "openai-completions", "models": ["deepseek-chat", "deepseek-reasoner"]},
            {"name": "github-copilot", "api": "openai-completions", "models": ["gpt-4o-copilot", "claude-sonnet-copilot"]},
            {"name": "groq", "api": "openai-completions", "models": ["llama", "mixtral"]},
            {"name": "together", "api": "openai-completions", "models": ["various open source"]},
            {"name": "fireworks", "api": "openai-completions", "models": ["various open source"]},
            {"name": "huggingface", "api": "openai-completions", "models": ["inference endpoints"]},
            {"name": "perplexity", "api": "openai-completions", "models": ["sonar"]},
            {"name": "mistral", "api": "openai-completions", "models": ["mistral-large", "mistral-medium"]},
            {"name": "nvidia", "api": "openai-completions", "models": ["nemotron"]},
        ],
        "notes": "OpenClaw supports any OpenAI-compatible endpoint. Dynamic model discovery via /v1/models where available."
    }
    
    return manifests


def discover_hermes_github_manifests():
    """Discover Hermes Agent providers from GitHub source manifests."""
    manifests = {}
    
    # Try to fetch from Hermes GitHub repo
    manifest = fetch_github_providers_manifest("NousResearch", "hermes-agent", "providers.json")
    if manifest:
        manifests['hermes-github'] = manifest
    
    # Fallback: known Hermes provider patterns from source analysis
    manifests['hermes-supported'] = {
        "source": "GitHub source analysis",
        "url": "https://github.com/NousResearch/hermes-agent",
        "providers": [
            {"name": "nous-portal", "api": "openai-completions"},
            {"name": "openrouter", "api": "openai-completions", "models": "200+"},
            {"name": "nvidia-nim", "api": "openai-completions", "models": ["nemotron"]},
            {"name": "xiaomi", "api": "openai-completions", "models": ["mimo-v2-pro"]},
            {"name": "zai", "api": "openai-completions", "models": ["glm-5"]},
            {"name": "kimi", "api": "openai-completions", "models": ["kimi-k2"]},
            {"name": "minimax", "api": "openai-completions", "models": ["minimax-m2"]},
            {"name": "huggingface", "api": "openai-completions"},
            {"name": "openai", "api": "openai-completions"},
            {"name": "anthropic", "api": "anthropic-messages"},
            {"name": "google", "api": "google-generative-ai"},
            {"name": "xai", "api": "openai-completions"},
            {"name": "openclaw-gateway", "api": "openclaw-gateway"},
        ],
        "notes": "Hermes supports any OpenAI-compatible endpoint. Uses hermes model command to switch."
    }
    
    return manifests


def configured_model_id(model):
    if isinstance(model, str):
        return model
    if isinstance(model, dict):
        return model.get('id')
    return None


def fetch_text_url(url, timeout=10):
    req = urllib.request.Request(url, headers={'User-Agent': 'sage-router/ollama-cloud-discovery', 'Accept': 'text/html,application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode('utf-8', errors='replace')


def ollama_cloud_catalog_models(force=False):
    """Discover Ollama Cloud catalog models from ollama.com.

    The public cloud search page is currently server-rendered HTML.  We parse
    library links from /search?c=cloud, then parse each library page for cloud
    tag links such as /library/qwen3.5:cloud or /library/gemma4:31b-cloud.
    """
    if not OLLAMA_CLOUD_CATALOG_ENABLED:
        return []
    now = time.time()
    if not force and OLLAMA_CLOUD_CATALOG_CACHE.get('models') and now - OLLAMA_CLOUD_CATALOG_CACHE.get('checked_at', 0) < OLLAMA_CLOUD_CATALOG_TTL_SECONDS:
        return list(OLLAMA_CLOUD_CATALOG_CACHE.get('models') or [])
    try:
        libraries = []
        parsed_catalog_url = urllib.parse.urlparse(OLLAMA_CLOUD_CATALOG_URL)
        base_query = urllib.parse.parse_qs(parsed_catalog_url.query)
        for page in range(1, max(1, OLLAMA_CLOUD_CATALOG_MAX_PAGES) + 1):
            query = {k: v[:] for k, v in base_query.items()}
            if page > 1:
                query['p'] = [str(page)]
            page_url = urllib.parse.urlunparse(parsed_catalog_url._replace(query=urllib.parse.urlencode(query, doseq=True)))
            search_html = fetch_text_url(page_url, timeout=12)
            before_count = len(libraries)
            for match in _re.finditer(r'href=["\']/library/([a-zA-Z0-9_.-]+)["\']', search_html):
                name = match.group(1).strip()
                if name and name not in libraries:
                    libraries.append(name)
                    if len(libraries) >= max(1, OLLAMA_CLOUD_CATALOG_MAX_LIBRARIES):
                        break
            if len(libraries) >= max(1, OLLAMA_CLOUD_CATALOG_MAX_LIBRARIES):
                break
            # Stop after the first page that contributes no new library links.
            if page > 1 and len(libraries) == before_count:
                break
        libraries = libraries[:max(1, OLLAMA_CLOUD_CATALOG_MAX_LIBRARIES)]
        models = []
        for name in libraries:
            try:
                lib_html = fetch_text_url(f'https://ollama.com/library/{urllib.parse.quote(name)}', timeout=12)
            except Exception as e:
                logger.debug(f'Ollama cloud library fetch failed for {name}: {extract_http_error(e)}')
                models.append(f'{name}:cloud')
                continue
            tags = []
            escaped = _re.escape(name)
            for tag in _re.findall(r'href=["\']/library/' + escaped + r':([^"\']+)["\']', lib_html):
                tag = urllib.parse.unquote(tag).strip()
                if tag and ('cloud' in tag.lower()) and tag not in tags:
                    tags.append(tag)
            if not tags and 'cloud' in lib_html.lower():
                tags = ['cloud']
            for tag in tags:
                models.append(f'{name}:{tag}')
        models = dedupe_keep_order(m for m in models if m and is_cloud_ollama_model(m))
        if models:
            OLLAMA_CLOUD_CATALOG_CACHE.update({'checked_at': now, 'models': models})
            logger.info(f'Discovered {len(models)} Ollama Cloud catalog models')
            return models
    except Exception as e:
        logger.warning(f'Ollama cloud catalog discovery failed: {extract_http_error(e)}')
    return list(OLLAMA_CLOUD_CATALOG_CACHE.get('models') or [])


def ollama_cloud_model_meta(model: str):
    model_l = (model or '').lower()
    meta = {
        'reasoning': any(x in model_l for x in ['deepseek', 'qwen', 'glm', 'nemotron', 'minimax', 'kimi', 'gemini', 'gemma']),
        'contextWindow': 256000,
        'maxTokens': 128000,
        'input': ['text'],
        'servable': True,
        'supportsChat': True,
        'supportsStreaming': True,
        'supportsTools': not any(x in model_l for x in NON_CHAT_MODEL_HINTS),
        'supportsJson': True,
        'manifestReason': 'ollama-cloud-catalog',
    }
    if is_multimodal_model(model) or any(x in model_l for x in ['gemini', 'gemma4', 'qwen3.5', 'kimi-k2.5', 'kimi-k2.6', 'ministral', 'devstral']):
        meta['input'] = ['text', 'image']
        meta['supportsVision'] = True
    return meta


def discover_provider_models(name, cfg, base_url, api_key, api_type):
    raw_models = cfg.get('models', [])
    configured = [mid for mid in (configured_model_id(m) for m in raw_models) if mid] if isinstance(raw_models, list) else []
    # For providers with API discovery, merge configured + discovered
    discovered = []
    if api_type in ('google-generative-language', 'google-generative-ai'):
        discovered = discover_google_models(base_url, api_key)
    elif api_type == 'google-vertex-ai':
        # Vertex AI does not expose a stable publisher-model discovery endpoint in all projects/regions.
        # Prefer configured Gemini model IDs; fall back to a small known-good set when none are configured.
        discovered = [] if configured else discover_google_vertex_models(base_url)
    elif api_type == 'cloudflare-workers-ai':
        discovered = [] if configured else discover_cloudflare_workers_ai_models(base_url, api_key)
    elif api_type == 'openai-completions':
        # Try OpenAI-style discovery for openai, github-copilot, xai, etc.
        if name == 'openrouter' or 'openrouter.ai' in (base_url or '').lower():
            discovered = discover_openrouter_models(base_url, api_key)
            if OPENROUTER_FREE_ONLY:
                configured = [m for m in configured if str(m).endswith(':free')]
        elif name == 'darkbloom' or 'api.darkbloom.dev' in (base_url or '').lower():
            discovered = discover_darkbloom_models(base_url, api_key)
        elif name == 'xai' or 'x.ai' in (base_url or '').lower():
            discovered = discover_xai_models(base_url, api_key)
        else:
            discovered = discover_openai_models(base_url, api_key)
    elif api_type == 'openclaw-gateway':
        # For OpenClaw Gateway, try to discover models
        discovered = discover_openclaw_gateway_models(base_url, api_key)
    elif api_type == 'ollama':
        discovered = ollama_cloud_catalog_models()
    if discovered:
        # Configured models first (stable), then any discovered models not already listed
        return dedupe_keep_order(configured + discovered)
    if configured:
        return dedupe_keep_order(configured)
    return []


def discover_reasoning_models(cfg):
    reasoning_models = set()
    raw_models = cfg.get('models', [])
    for model in raw_models if isinstance(raw_models, list) else []:
        if not isinstance(model, dict):
            continue
        model_id = model.get('id')
        if model_id and model.get('reasoning'):
            reasoning_models.add(model_id)
    return reasoning_models


def discover_model_meta(cfg):
    meta = {}
    raw_models = cfg.get('models', [])
    for model in raw_models if isinstance(raw_models, list) else []:
        if isinstance(model, str):
            meta[model] = {}
            continue
        if not isinstance(model, dict):
            continue
        model_id = model.get('id')
        if not model_id:
            continue
        entry = {
            'reasoning': bool(model.get('reasoning')),
            'contextWindow': model.get('contextWindow'),
            'maxTokens': model.get('maxTokens'),
            'input': model.get('input') or [],
        }
        for key in (
            'preferred', 'resident', 'family', 'families', 'servable', 'manifestReason',
            'supportsChat', 'supportsJson', 'supportsTools', 'supportsStreaming'
        ):
            if key in model:
                entry[key] = model.get(key)
        meta[model_id] = entry
    return meta


def load_router_profile_overlays(existing_providers):
    providers = {}
    try:
        with open(PROVIDER_PROFILES_PATH) as f:
            profiles = json.load(f)
    except FileNotFoundError:
        return providers
    except Exception as e:
        logger.warning(f'Failed to load provider profile overlays: {e}')
        return providers

    requested = [item.strip() for item in os.environ.get('SAGE_ROUTER_PROFILE_OVERLAYS', 'darkbloom').split(',') if item.strip()]
    for name in requested:
        cfg = profiles.get(name)
        if not isinstance(cfg, dict):
            continue
        base_url = resolve_config_value(cfg.get('baseUrl', '') or '')
        api_key = resolve_config_value(cfg.get('apiKey', '') or '')
        api_type = infer_api_type(name, cfg, base_url)
        models = discover_provider_models(name, cfg, base_url, api_key, api_type)
        if not models:
            continue
        reasoning_models = discover_reasoning_models(cfg)
        model_meta = discover_model_meta(cfg)
        providers[name] = Provider(name, api_type, base_url, api_key, models, reasoning_models, model_meta)
        logger.info(f'Loaded router profile overlay provider {name} ({api_type}) with {len(models)} models')
    return providers


def normalize_route_mode(raw):
    value = str(raw or 'balanced').strip().lower()
    aliases = {'deep': 'best', 'thorough': 'best', 'local-strict': 'local-first'}
    value = aliases.get(value, value)
    return value if value in {'fast', 'balanced', 'best', 'local-first', 'realtime'} else 'balanced'


def _content_blocks(payload):
    blocks = []
    if not isinstance(payload, dict):
        return blocks
    for msg in payload.get('messages') or []:
        if isinstance(msg, dict):
            content = msg.get('content')
            if isinstance(content, list):
                blocks.extend([b for b in content if isinstance(b, dict)])
            elif isinstance(content, dict):
                blocks.append(content)
    return blocks


def _payload_text(payload):
    if not isinstance(payload, dict):
        return ''
    return ' '.join(normalize_content((m or {}).get('content', '')) for m in payload.get('messages') or [] if isinstance(m, dict))


def payload_document_signal(payload):
    text = _payload_text(payload).lower()
    blocks = _content_blocks(payload)
    filenames = ' '.join(str(b.get(k, '')) for b in blocks for k in ('filename', 'fileName', 'name', 'path', 'filePath', 'mime_type', 'mimeType', 'media_type', 'mediaType')).lower()
    haystack = f'{text} {filenames}'
    doc_markers = [
        '.pdf', 'application/pdf', '<file ', '<media:', 'media attached', 'external_untrusted_content',
        'document', 'report', 'informe', 'conclusiones', 'findings', 'clinical information',
        'translate', 'summarize', 'extract', 'parse', 'ocr', 'mri', 'rm columna', 'resonancia',
    ]
    return any(marker in haystack for marker in doc_markers) or len(text) > 4000


def payload_vision_signal(payload):
    blocks = _content_blocks(payload)
    for block in blocks:
        if _block_is_image_input(block):
            return True
    # Deep scan catches images nested in Responses `input`, tool calls/results,
    # and other structures that _content_blocks (messages-only) does not reach.
    return payload_has_image_input(payload)


AUDIO_INPUT_BLOCK_TYPES = {'input_audio', 'audio', 'audio_url'}
VIDEO_INPUT_BLOCK_TYPES = {'input_video', 'video', 'video_url'}


def _block_is_audio_input(block):
    if not isinstance(block, dict):
        return False
    btype = str(block.get('type') or '').lower()
    if btype in AUDIO_INPUT_BLOCK_TYPES:
        return True
    mime = str(block.get('mime_type') or block.get('mimeType') or block.get('media_type') or block.get('mediaType') or '').lower()
    if mime.startswith('audio/'):
        return True
    return False


def _block_is_video_input(block):
    if not isinstance(block, dict):
        return False
    btype = str(block.get('type') or '').lower()
    if btype in VIDEO_INPUT_BLOCK_TYPES:
        return True
    mime = str(block.get('mime_type') or block.get('mimeType') or block.get('media_type') or block.get('mediaType') or '').lower()
    if mime.startswith('video/'):
        return True
    return False


def _payload_has_block_type(payload, predicate):
    seen = set()
    def visit(node):
        if id(node) in seen:
            return False
        seen.add(id(node))
        if isinstance(node, dict):
            if predicate(node):
                return True
            for v in node.values():
                if visit(v):
                    return True
        elif isinstance(node, list):
            for item in node:
                if visit(item):
                    return True
        elif isinstance(node, str):
            if node.startswith('data:audio/') and predicate.__name__ == '_block_is_audio_input':
                return True
            if node.startswith('data:video/') and predicate.__name__ == '_block_is_video_input':
                return True
        return False
    try:
        return visit(payload)
    except Exception:
        return False


def payload_audio_signal(payload):
    for block in _content_blocks(payload):
        if _block_is_audio_input(block):
            return True
    return _payload_has_block_type(payload, _block_is_audio_input)


def payload_video_signal(payload):
    for block in _content_blocks(payload):
        if _block_is_video_input(block):
            return True
    return _payload_has_block_type(payload, _block_is_video_input)


def payload_quality_sensitive_signal(payload):
    if not isinstance(payload, dict):
        return False
    needles = ('discord-public', 'public channel', 'group chat', 'telegram', 'whatsapp', 'production', 'external')
    try:
        haystack = json.dumps({k: payload.get(k) for k in ('metadata', 'channel', 'surface', 'source', 'chat_type', 'messages')}, default=str)[:12000].lower()
    except Exception:
        haystack = str(payload)[:12000].lower()
    return any(n in haystack for n in needles)

def normalize_requirements(payload, thinking_level=DEFAULT_THINKING_LEVEL):
    req = payload.get('requirements') if isinstance(payload, dict) else None
    if not isinstance(req, dict):
        req = {}
    # Tool definitions are often attached by OpenClaw even for ordinary chat.
    # For auto tool_choice, keep tools as a soft capability preference rather
    # than a hard requirement so plain chat can still route broadly. If the
    # client explicitly requires tools or forces a concrete tool choice, route
    # only to providers/models that support valid tool calls.
    tool_choice = payload.get('tool_choice')
    forced_tool_choice = bool(tool_choice and tool_choice not in ('auto', 'none'))
    has_tools = forced_tool_choice
    # Check for explicit reasoning requirements. Thinking levels are routing
    # hints; they should not make a forced provider unusable unless the client
    # explicitly requires reasoning-capable models.
    raw_reasoning = payload.get('reasoning')
    explicit_reasoning = bool(payload.get('requiresReasoning') or req.get('reasoning'))
    if isinstance(raw_reasoning, dict):
        effort = str(raw_reasoning.get('effort') or raw_reasoning.get('level') or '').lower()
        explicit_reasoning = explicit_reasoning or effort in {'high', 'max', 'deep'}
    elif isinstance(raw_reasoning, str):
        explicit_reasoning = explicit_reasoning or raw_reasoning.lower() in {'high', 'max', 'deep'}
    elif isinstance(raw_reasoning, bool):
        explicit_reasoning = explicit_reasoning or raw_reasoning
    requires_reasoning = explicit_reasoning
    explicit_streaming = bool(req.get('streaming') or payload.get('requiresStreaming'))
    requested_stream = bool(payload.get('stream'))
    document_signal = bool(req.get('document') or payload.get('requiresDocumentParsing') or payload_document_signal(payload))
    vision_signal = bool(req.get('vision') or payload.get('requiresVision') or payload_vision_signal(payload))
    audio_signal = bool(req.get('audio') or payload.get('requiresAudio') or payload_audio_signal(payload))
    video_signal = bool(req.get('video') or payload.get('requiresVideo') or payload_video_signal(payload))
    normalized = {
        'reasoning': bool(req.get('reasoning') or payload.get('requiresReasoning') or requires_reasoning),
        'json': bool(req.get('json') or payload.get('requiresJson')),
        'tools': bool(req.get('tools') or payload.get('requiresTools') or has_tools),
        'preferTools': bool(payload.get('tools') and not (req.get('tools') or payload.get('requiresTools') or has_tools)),
        'longContext': bool(req.get('longContext') or payload.get('requiresLongContext') or document_signal),
        'document': document_signal,
        'vision': vision_signal,
        'audio': audio_signal,
        'video': video_signal,
        'streaming': bool(explicit_streaming or (requested_stream and not has_tools)),
        'qualitySensitive': bool(req.get('qualitySensitive') or payload.get('requiresQuality') or payload_quality_sensitive_signal(payload)),
        'frontierOrReasoningTools': bool(req.get('frontierOrReasoningTools') or payload.get('requiresFrontierOrReasoningTools')),
        'frontierLargeOnly': bool(req.get('frontierLargeOnly') or payload.get('requiresFrontierLargeOnly')),
        'suppressToolCallContent': bool(req.get('suppressToolCallContent') or payload.get('suppressToolCallContent') or payload.get('suppressIntermediateToolText')),
    }
    # Preserve routing constraints injected by profiles.  Dropping these during
    # normalization lets named profiles such as discord-public accidentally route
    # to denied mini/filler models, which can surface malformed tool-call text.
    for key in ('allowModels', 'denyModels', 'allowProviders', 'denyProviders', 'fallbackProviders'):
        if req.get(key):
            normalized[key] = req.get(key)
    if req.get('minParamsB') is not None:
        normalized['minParamsB'] = req.get('minParamsB')
    agentic_score, agentic_signals = payload_agentic_signal(payload)
    if req.get('agentic') or payload.get('requiresAgentic') or agentic_score >= 2:
        normalized['agentic'] = True
        normalized['agenticScore'] = agentic_score
        normalized['agenticSignals'] = agentic_signals[:8]
        if not normalized.get('tools'):
            normalized['preferTools'] = True
    return normalized


def payload_agentic_signal(payload):
    if not isinstance(payload, dict):
        return 0, []
    signals = []
    if payload.get('tools'):
        signals.append('tools')
    tool_choice = payload.get('tool_choice')
    if tool_choice and tool_choice not in ('auto', 'none'):
        signals.append('forced_tool_choice')
    try:
        text = latest_user_text(normalize_messages(payload.get('messages', []))).lower()
    except Exception:
        text = json.dumps(payload.get('messages') or [], default=str).lower()[:12000]
    keyword_groups = {
        'file_ops': ('read file', 'write file', 'edit', 'patch', 'modify', 'rename', 'move', 'delete'),
        'execution': ('run ', 'test', 'build', 'lint', 'deploy', 'install', 'compile', 'execute'),
        'iteration': ('fix', 'debug', 'verify', 'validate', 'retry', 'regression', 'self-heal'),
        'repo_ops': ('commit', 'branch', 'pull request', 'pr ', 'git ', 'merge', 'refactor'),
        'autonomy': ('go ahead', 'do it', 'implement', 'ship', 'complete', 'end-to-end', 'multi-step'),
    }
    for label, needles in keyword_groups.items():
        if any(n in text for n in needles):
            signals.append(label)
    return len(signals), signals


def stripe_price_ids_by_plan():
    mapping = {}
    for part in STRIPE_PRICE_IDS_RAW.split(','):
        if '=' in part:
            plan, price_id = part.split('=', 1)
            if plan.strip() and price_id.strip():
                mapping[plan.strip().lower()] = price_id.strip()
    if STRIPE_PRICE_ID:
        mapping.setdefault('pro', STRIPE_PRICE_ID)
    return mapping


def normalize_stripe_plan(plan):
    plan = str(plan or '').strip().lower()
    if plan in {'lite', 'pro', 'max'}:
        return plan
    if plan and plan in stripe_price_ids_by_plan():
        return plan
    return ''


def stripe_plan_from_price_id(price_id):
    price_id = str(price_id or '').strip()
    if not price_id:
        return ''
    for plan, configured_price_id in stripe_price_ids_by_plan().items():
        if price_id == configured_price_id:
            return normalize_stripe_plan(plan)
    return ''


def stripe_plan_from_object(obj, fallback_customer_id=None, default='pro'):
    obj = obj if isinstance(obj, dict) else {}
    for collection_name in ('items', 'lines'):
        line_items = (obj.get(collection_name) or {}).get('data') if isinstance(obj.get(collection_name), dict) else []
        if isinstance(line_items, list):
            for item in line_items:
                price = (item or {}).get('price') or {}
                plan = stripe_plan_from_price_id(price.get('id'))
                if plan:
                    return plan
                plan_info = (item or {}).get('plan') or {}
                if isinstance(plan_info, dict):
                    plan = stripe_plan_from_price_id(plan_info.get('id'))
                    if plan:
                        return plan
    if isinstance(obj.get('items'), list):
        for item in obj.get('items') or []:
            price = (item or {}).get('price') or {}
            plan = stripe_plan_from_price_id(price.get('id'))
            if plan:
                return plan
    legacy_plan = obj.get('plan') or {}
    if isinstance(legacy_plan, dict):
        plan = stripe_plan_from_price_id(legacy_plan.get('id'))
        if plan:
            return plan

    metadata = obj.get('metadata') or {}
    plan = normalize_stripe_plan(metadata.get('plan'))
    if plan:
        return plan

    if fallback_customer_id:
        existing = customer_by_id(fallback_customer_id)
        plan = normalize_stripe_plan((existing or {}).get('plan'))
        if plan:
            return plan

    return normalize_stripe_plan(default) or 'pro'


def stripe_checkout_session_entitles_routing(obj):
    obj = obj if isinstance(obj, dict) else {}
    payment_status = str(obj.get('payment_status') or '').strip().lower()
    return payment_status in {'paid', 'no_payment_required'}


def parse_public_plan_limits(raw):
    limits = {}
    for part in str(raw or '').split(','):
        if '=' not in part:
            continue
        plan, value = part.split('=', 1)
        plan = plan.strip().lower()
        try:
            parsed = int(value.strip())
        except ValueError:
            continue
        if plan:
            limits[plan] = parsed
    return limits


def limit_for_public_plan(plan_name, limits, fallback=0):
    plan = str(plan_name or '').strip().lower()
    candidates = [plan]
    alias = PUBLIC_PLAN_LIMIT_ALIASES.get(plan)
    if alias:
        candidates.append(alias)
    candidates.append('default')
    for candidate in candidates:
        if candidate in limits:
            return limits[candidate]
    return fallback


def parse_monthly_price_usd(plan):
    price = str((plan or {}).get('price') or '').strip().lower()
    if not price.startswith('$'):
        return None
    amount = price.split('/', 1)[0].lstrip('$').strip()
    try:
        return float(amount)
    except ValueError:
        return None


def parse_provider_resale_cost_cents_per_thousand_requests():
    raw = (
        os.environ.get('SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS')
        or os.environ.get('SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K')
        or ''
    ).strip()
    if not raw:
        return None
    try:
        parsed = float(raw)
    except ValueError:
        return None
    if parsed <= 0:
        return None
    return parsed


def managed_provider_unit_economics(cost_cents_per_thousand, minimum_gross_margin_percent):
    plans = public_plan_catalog()
    evaluated = []
    cost_configured = cost_cents_per_thousand is not None
    for name, plan in plans.items():
        monthly_requests = int((plan.get('limits') or {}).get('monthlyRequests') or 0)
        monthly_price_usd = parse_monthly_price_usd(plan)
        if not monthly_requests or monthly_price_usd is None or monthly_price_usd <= 0:
            continue
        revenue_cents_per_thousand = (monthly_price_usd * 100.0) / (monthly_requests / 1000.0)
        row = {
            'plan': name,
            'monthlyRequests': monthly_requests,
            'monthlyPriceUsd': monthly_price_usd,
            'revenueCentsPerThousandRequests': round(revenue_cents_per_thousand, 4),
            'minimumGrossMarginPercent': minimum_gross_margin_percent,
            'maximumProviderCostCentsPerThousandRequests': round(
                revenue_cents_per_thousand * max(0, 100 - minimum_gross_margin_percent) / 100.0,
                4,
            ),
        }
        if cost_configured and revenue_cents_per_thousand > 0:
            gross_margin = ((revenue_cents_per_thousand - cost_cents_per_thousand) / revenue_cents_per_thousand) * 100.0
            row['meetsMinimumGrossMargin'] = gross_margin >= minimum_gross_margin_percent
        else:
            row['meetsMinimumGrossMargin'] = False
        evaluated.append(row)
    return {
        'costModel': 'cents_per_thousand_requests',
        'costModelConfigured': cost_configured,
        'costModelEnv': 'SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS',
        'minimumGrossMarginPercent': minimum_gross_margin_percent,
        'evaluatedPlans': evaluated,
        'satisfied': bool(cost_configured and evaluated and all(row.get('meetsMinimumGrossMargin') for row in evaluated)),
    }


def managed_provider_resale_readiness_setup(enabled=False):
    enabled = bool(enabled)
    setup_command = (
        "SAGEROUTER_PROVIDER_RESALE_TERMS_URL='https://sagerouter.dev/provider-resale-terms' \\\n"
        "SAGEROUTER_PROVIDER_RESALE_MARGIN_POLICY_URL='https://sagerouter.dev/margin-policy' \\\n"
        "SAGEROUTER_PROVIDER_RESALE_TERMS_ACKNOWLEDGED='0' \\\n"
        "SAGEROUTER_PROVIDER_RESALE_AUTHORIZATION_REF='PRIVATE_PROVIDER_AUTH_REF' \\\n"
        "SAGEROUTER_PROVIDER_RESALE_ALLOWED_PROVIDERS='ollama,openai,anthropic' \\\n"
        "SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS='REVIEWED_PRIVATE_COST' \\\n"
        "SAGEROUTER_PROVIDER_RESALE_MIN_GROSS_MARGIN_PERCENT='35' \\\n"
        "SAGEROUTER_MANAGED_PROVIDER_RESALE_ENABLE_PUBLIC='0' \\\n"
        "scripts/configure_managed_provider_resale_readiness.sh"
    )
    dry_run_command = (
        "scripts/configure_managed_provider_resale_readiness.sh --check"
    )
    unit_economics_command = (
        "SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS='REVIEWED_PRIVATE_COST' "
        "scripts/configure_managed_provider_resale_readiness.sh --unit-economics"
    )
    enable_command_template = (
        "SAGEROUTER_PROVIDER_RESALE_TERMS_ACKNOWLEDGED='1' \\\n"
        "SAGEROUTER_PROVIDER_RESALE_AUTHORIZATION_REF='PRIVATE_PROVIDER_AUTH_REF' \\\n"
        "SAGEROUTER_MANAGED_PROVIDER_RESALE_ENABLE_PUBLIC='1' \\\n"
        "scripts/configure_managed_provider_resale_readiness.sh"
    )
    return {
        'setupScript': 'scripts/configure_managed_provider_resale_readiness.sh',
        'setupCommand': '' if enabled else setup_command,
        'dryRunCommand': dry_run_command,
        'unitEconomicsCommand': unit_economics_command,
        'enableCommandTemplate': enable_command_template,
        'requiredEnv': [] if enabled else [
            'SAGEROUTER_PROVIDER_RESALE_TERMS_URL',
            'SAGEROUTER_PROVIDER_RESALE_MARGIN_POLICY_URL',
            'SAGEROUTER_PROVIDER_RESALE_TERMS_ACKNOWLEDGED',
            'SAGEROUTER_PROVIDER_RESALE_AUTHORIZATION_REF',
            'SAGEROUTER_PROVIDER_RESALE_ALLOWED_PROVIDERS',
            'SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS',
        ],
        'secretManagerNames': [
            'SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS',
        ],
        'defaultPublicEnable': False,
        'requiresExplicitPublicEnableEnv': 'SAGEROUTER_MANAGED_PROVIDER_RESALE_ENABLE_PUBLIC',
        'operatorAction': (
            'Managed provider access is ready for private beta; keep provider authorization and margin review evidence current.'
            if enabled
            else 'Stage readiness metadata, run the pricing dry-run, and keep public managed resale disabled until provider terms, allowlist, and positive unit economics pass.'
        ),
        'privacy': {
            'containsSecrets': False,
            'containsProviderCredentials': False,
            'containsActualProviderCosts': False,
            'containsGrossMarginPercent': False,
            'containsPrompts': False,
            'containsRawProviderResponses': False,
        },
    }


def current_usage_period(now=None):
    return time.strftime('%Y-%m', time.gmtime(now or time.time()))


def public_plan_catalog():
    plans = json.loads(json.dumps(PUBLIC_PLAN_CATALOG))
    price_ids = stripe_price_ids_by_plan()
    rate_limits = parse_public_plan_limits(PUBLIC_PLAN_RATE_LIMITS_RAW)
    monthly_quotas = parse_public_plan_limits(PUBLIC_PLAN_MONTHLY_QUOTAS_RAW)
    for name, plan in plans.items():
        plan['stripeConfigured'] = bool(price_ids.get(name))
        monthly_requests = limit_for_public_plan(name, monthly_quotas, 0)
        rate_limit_per_minute = limit_for_public_plan(name, rate_limits, 0)
        plan['limits'] = {
            'monthlyRequests': monthly_requests,
            'rateLimitPerMinute': rate_limit_per_minute,
        }
        plan['apiAccess'] = bool(monthly_requests > 0 or name == 'metered')
    return plans


def public_billing_metadata():
    plans = public_plan_catalog()
    stripe_ready_plans = sorted(
        name
        for name, plan in plans.items()
        if plan.get('apiAccess') and plan.get('stripeConfigured')
    )
    api_plan_names = sorted(name for name, plan in plans.items() if plan.get('apiAccess'))
    return {
        'stripe': {
            'configured': bool(STRIPE_SECRET_KEY and stripe_ready_plans),
            'checkoutReady': bool(STRIPE_SECRET_KEY and stripe_ready_plans),
            'billingPortalReady': bool(STRIPE_SECRET_KEY),
            'checkoutPath': '/billing/stripe/checkout',
            'billingPortalPath': '/billing/stripe/portal',
            'configuredPlans': stripe_ready_plans,
            'requiresSignedInUser': True,
            'requiresVerifiedEmail': hosted_email_verification_required(),
        },
        'manualSettlement': {
            'enabled': bool(CRYPTO_PAYMENT_ADDRESS),
            'intentPath': '/billing/crypto/intent',
            'statusPath': '/billing/crypto/status',
            'asset': CRYPTO_PAYMENT_ASSET,
            'network': CRYPTO_PAYMENT_NETWORK,
            'automaticSettlement': bool(CRYPTO_PROCESSOR_URL and CRYPTO_PROCESSOR_KEY),
            'requiresOperatorApproval': True,
        },
        'activation': {
            'activeStatuses': ['active', 'trialing', 'manual', 'paid'],
            'apiPlans': api_plan_names,
            'generatedApiKeyPrefix': API_KEY_PREFIX,
            'maxActiveApiKeysPerCustomer': MAX_ACTIVE_API_KEYS_PER_CUSTOMER,
        },
    }


def public_model_catalog():
    catalog = json.loads(json.dumps(PUBLIC_MODEL_CATALOG))
    catalog['catalogPage'] = f"{MARKETING_BASE_URL}/models"
    catalog['pricingPage'] = f"{MARKETING_BASE_URL}/pricing"
    catalog['accountPage'] = f"{APP_BASE_URL}/account.html"
    catalog['openaiBaseUrl'] = f"{API_BASE_URL or 'https://api.sagerouter.dev'}/v1"
    catalog['apiKeyPrefix'] = API_KEY_PREFIX
    return catalog


def public_launch_metadata():
    api_base_url = API_BASE_URL or 'https://api.sagerouter.dev'
    launch = json.loads(json.dumps(PUBLIC_LAUNCH_POSITIONING))
    managed_provider_access = launch.get('managedProviderAccess') or {}
    managed_provider_resale_enabled = str(os.environ.get('SAGEROUTER_MANAGED_PROVIDER_RESALE_ENABLED', '')).strip().lower() in {'1', 'true', 'yes', 'on'}
    provider_terms_url = os.environ.get('SAGEROUTER_PROVIDER_RESALE_TERMS_URL', '').strip()
    margin_policy_url = os.environ.get('SAGEROUTER_PROVIDER_RESALE_MARGIN_POLICY_URL', '').strip()
    provider_terms_acknowledged = str(os.environ.get('SAGEROUTER_PROVIDER_RESALE_TERMS_ACKNOWLEDGED', '')).strip().lower() in {'1', 'true', 'yes', 'on'}
    provider_authorization_ref = os.environ.get('SAGEROUTER_PROVIDER_RESALE_AUTHORIZATION_REF', '').strip()
    provider_authorization_evidence_ready = bool(provider_authorization_ref)
    configured_provider_families = []
    for item in os.environ.get('SAGEROUTER_PROVIDER_RESALE_ALLOWED_PROVIDERS', '').split(','):
        normalized = item.strip().lower()
        if normalized and normalized not in configured_provider_families:
            configured_provider_families.append(normalized)
    allowed_provider_families = [
        item for item in configured_provider_families
        if item in MANAGED_PROVIDER_RESALE_ELIGIBLE_PROVIDER_FAMILIES
    ]
    byok_only_configured_provider_families = [
        item for item in configured_provider_families
        if item in MANAGED_PROVIDER_BYOK_ONLY_PROVIDER_FAMILIES
    ]
    min_margin = os.environ.get('SAGEROUTER_PROVIDER_RESALE_MIN_GROSS_MARGIN_PERCENT', '').strip()
    if min_margin:
        try:
            managed_provider_access['minimumGrossMarginPercent'] = max(0, int(float(min_margin)))
        except (TypeError, ValueError):
            managed_provider_access['minimumGrossMarginPercent'] = 0
    requires_positive_unit_economics = bool(managed_provider_access.get('requiresPositiveUnitEconomics'))
    margin_ready = int(managed_provider_access.get('minimumGrossMarginPercent') or 0) >= 30
    unit_economics = managed_provider_unit_economics(
        parse_provider_resale_cost_cents_per_thousand_requests(),
        int(managed_provider_access.get('minimumGrossMarginPercent') or 0),
    )
    provider_terms_ready = bool(provider_terms_url and provider_terms_acknowledged)
    provider_allowlist_ready = bool(allowed_provider_families)
    managed_provider_ready = bool(
        provider_terms_ready
        and provider_authorization_evidence_ready
        and provider_allowlist_ready
        and margin_policy_url
        and requires_positive_unit_economics
        and margin_ready
        and unit_economics.get('satisfied')
    )
    missing_controls = []
    if not provider_terms_url:
        missing_controls.append('provider_resale_terms')
    if not provider_terms_acknowledged:
        missing_controls.append('provider_terms_acknowledgment')
    if not provider_authorization_evidence_ready:
        missing_controls.append('provider_authorization_evidence')
    if not provider_allowlist_ready:
        missing_controls.append('authorized_provider_allowlist')
    if not margin_policy_url:
        missing_controls.append('margin_policy')
    if not unit_economics.get('costModelConfigured'):
        missing_controls.append('provider_cost_model')
    if not requires_positive_unit_economics or not unit_economics.get('satisfied'):
        missing_controls.append('positive_unit_economics')
    if not margin_ready:
        missing_controls.append('minimum_gross_margin')
    provider_family_readiness = []
    for family in (
        *MANAGED_PROVIDER_RESALE_ELIGIBLE_PROVIDER_FAMILIES,
        *MANAGED_PROVIDER_BYOK_ONLY_PROVIDER_FAMILIES,
    ):
        resale_eligible = family in MANAGED_PROVIDER_RESALE_ELIGIBLE_PROVIDER_FAMILIES
        configured = family in configured_provider_families
        byok_only = family in MANAGED_PROVIDER_BYOK_ONLY_PROVIDER_FAMILIES
        family_missing_controls = []
        if byok_only:
            status = 'byok_supported_not_managed_resale'
            family_missing_controls.append('provider_resale_authorization')
        elif not configured:
            status = 'not_allowlisted'
            family_missing_controls.append('authorized_provider_allowlist')
        elif managed_provider_ready:
            status = 'ready_for_private_beta'
        else:
            status = 'blocked_global_controls'
            family_missing_controls.extend(missing_controls)
        provider_family_readiness.append({
            'family': family,
            'label': MANAGED_PROVIDER_FAMILY_LABELS.get(family, family),
            'configured': configured,
            'resaleEligible': resale_eligible,
            'byokOnly': byok_only,
            'ready': bool(resale_eligible and configured and managed_provider_ready),
            'status': status,
            'missingControls': sorted(set(family_missing_controls)),
        })
    if managed_provider_resale_enabled:
        managed_provider_access['requested'] = True
        managed_provider_access['readinessSatisfied'] = managed_provider_ready
        if managed_provider_ready:
            managed_provider_access['enabled'] = True
            managed_provider_access['status'] = 'ready_for_private_beta'
        else:
            managed_provider_access['enabled'] = False
            managed_provider_access['status'] = 'requires_readiness_verification'
    else:
        managed_provider_access['requested'] = False
        managed_provider_access['readinessSatisfied'] = False
    managed_provider_access['missingControls'] = missing_controls
    managed_provider_access['providerTermsUrl'] = provider_terms_url
    managed_provider_access['providerTermsAcknowledged'] = provider_terms_acknowledged
    managed_provider_access['providerAuthorizationEvidenceConfigured'] = provider_authorization_evidence_ready
    managed_provider_access['providerAuthorizationEvidenceEnv'] = 'SAGEROUTER_PROVIDER_RESALE_AUTHORIZATION_REF'
    managed_provider_access['configuredProviderFamilies'] = configured_provider_families
    managed_provider_access['allowedProviderFamilies'] = allowed_provider_families
    managed_provider_access['resaleEligibleProviderFamilies'] = list(MANAGED_PROVIDER_RESALE_ELIGIBLE_PROVIDER_FAMILIES)
    managed_provider_access['byokOnlyProviderFamilies'] = list(MANAGED_PROVIDER_BYOK_ONLY_PROVIDER_FAMILIES)
    managed_provider_access['byokOnlyConfiguredProviderFamilies'] = byok_only_configured_provider_families
    managed_provider_access['providerFamilyReadiness'] = provider_family_readiness
    managed_provider_access['oneSubscriptionReadiness'] = {
        'commercialPreference': 'one-subscription',
        'enabled': bool(managed_provider_access.get('enabled')),
        'requested': bool(managed_provider_access.get('requested')),
        'readyProviderFamilies': [
            row['family'] for row in provider_family_readiness
            if row.get('ready')
        ],
        'blockedProviderFamilies': [
            row['family'] for row in provider_family_readiness
            if not row.get('ready')
        ],
        'resaleEligibleProviderFamilies': list(MANAGED_PROVIDER_RESALE_ELIGIBLE_PROVIDER_FAMILIES),
        'byokOnlyProviderFamilies': list(MANAGED_PROVIDER_BYOK_ONLY_PROVIDER_FAMILIES),
        'managedAccessUrl': f"{MARKETING_BASE_URL}/managed-access",
        'safeForPublicDisplay': True,
    }
    managed_provider_access['providerBoundary'] = (
        'OpenRouter and other BYOK-compatible gateways remain supported routing providers, '
        'but they do not satisfy managed provider resale readiness unless separately promoted '
        'into the resale-eligible provider-family allowlist.'
    )
    managed_provider_access['marginPolicyUrl'] = margin_policy_url
    managed_provider_access['unitEconomics'] = unit_economics
    managed_provider_access['acceptableUseUrl'] = f"{MARKETING_BASE_URL}/acceptable-use"
    managed_provider_access['readinessSetup'] = managed_provider_resale_readiness_setup(
        enabled=bool(managed_provider_access.get('enabled'))
    )
    launch['managedProviderAccess'] = managed_provider_access
    launch['pricingPage'] = f"{MARKETING_BASE_URL}/pricing"
    launch['comparisonPage'] = f"{MARKETING_BASE_URL}/compare/model-gateways"
    launch['modelCatalogPage'] = f"{MARKETING_BASE_URL}/models"
    launch['calculatorPage'] = f"{MARKETING_BASE_URL}/model-routing-calculator"
    launch['accountPage'] = f"{APP_BASE_URL}/account.html"
    launch['conversionSurfaces'] = [
        MARKETING_BASE_URL,
        f"{MARKETING_BASE_URL}/pricing",
        f"{MARKETING_BASE_URL}/models",
        f"{MARKETING_BASE_URL}/agent-native",
        f"{MARKETING_BASE_URL}/compare/model-gateways",
        f"{MARKETING_BASE_URL}/model-routing-calculator",
        f"{APP_BASE_URL}/account.html",
    ]
    return {
        'publicBaseUrl': PUBLIC_BASE_URL,
        'marketingBaseUrl': MARKETING_BASE_URL,
        'appBaseUrl': APP_BASE_URL,
        'apiBaseUrl': api_base_url,
        'openaiBaseUrl': f"{api_base_url}/v1",
        'anthropicBaseUrl': api_base_url,
        'accountUrl': f"{APP_BASE_URL}/account.html",
        'loginUrl': f"{APP_BASE_URL}/login.html",
        'checkoutPath': '/billing/stripe/checkout',
        'billingPortalPath': '/billing/stripe/portal',
        'billing': public_billing_metadata(),
        'apiKeyPrefix': API_KEY_PREFIX,
        'maxActiveApiKeysPerCustomer': MAX_ACTIVE_API_KEYS_PER_CUSTOMER,
        'activationEmailReadiness': public_activation_email_readiness(),
        'recommendedModel': 'sage-router/frontier',
        'publicLaunch': launch,
    }


def is_truthy(value):
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    return str(value or '').strip().lower() in {'1', 'true', 'yes', 'on', 'debug', 'route'}


def normalize_debug_mode(payload):
    if not isinstance(payload, dict):
        return False
    debug = payload.get('debug')
    if isinstance(debug, dict):
        if is_truthy(debug.get('route')) or is_truthy(debug.get('routing')):
            return True
    return is_truthy(debug) or is_truthy(payload.get('routeDebug')) or is_truthy(payload.get('debugRoute'))


def estimate_prompt_tokens(messages):
    text = ' '.join((msg.get('content') or '') for msg in messages or [])
    return max(1, int(len(text) / 4))


def model_context_window(provider, model):
    meta = (provider.model_meta or {}).get(model, {})
    return int(meta.get('contextWindow') or 0)


def model_disabled_reason(provider_name, model):
    model_s = str(model or '')
    provider_s = str(provider_name or '')
    if provider_s and model_s:
        block_key = f'{provider_s}/{model_s}'
        blocked = TEMP_MODEL_BLOCKS.get(block_key)
        if blocked:
            if float(blocked.get('until', 0) or 0) <= time.time():
                TEMP_MODEL_BLOCKS.pop(block_key, None)
            else:
                return f"temporarily blocked: {blocked.get('reason') or 'runtime error'}"
    if not DISABLED_MODELS:
        return None
    candidates = {model_s}
    if provider_s:
        candidates.add(f'{provider_s}/{model_s}')
        if provider_s.startswith('nvidia') or provider_s.endswith('-nim') or provider_s == 'nim':
            candidates.add(f'nvidia/{model_s}')
    for disabled in DISABLED_MODELS:
        if disabled in candidates:
            return 'disabled by SAGE_ROUTER_DISABLED_MODELS'
        # Accept provider aliases such as nvidia/openai/gpt-oss-120b for a
        # nvidia-nim provider whose actual model id is openai/gpt-oss-120b.
        if '/' in disabled and disabled.endswith('/' + model_s):
            return 'disabled by SAGE_ROUTER_DISABLED_MODELS'
    return None


def active_temp_model_block(provider_name, model):
    key = f'{provider_name}/{model}'
    blocked = TEMP_MODEL_BLOCKS.get(key)
    if not blocked:
        return None
    if float(blocked.get('until', 0) or 0) <= time.time():
        TEMP_MODEL_BLOCKS.pop(key, None)
        return None
    return blocked


def invalidate_model_health_cache(provider_name, model):
    suffix = f':{provider_name}/{model}'
    for key in list(MODEL_HEALTH_CACHE.keys()):
        if key.endswith(suffix):
            MODEL_HEALTH_CACHE.pop(key, None)



def set_temp_model_block(provider_name, model, seconds, reason):
    if seconds <= 0:
        return
    TEMP_MODEL_BLOCKS[f'{provider_name}/{model}'] = {
        'until': time.time() + seconds,
        'reason': reason,
    }
    invalidate_model_health_cache(provider_name, model)


def set_temp_provider_models_block(provider_name, seconds, reason):
    provider = PROVIDERS.get(provider_name)
    if not provider:
        return
    for model in dedupe_keep_order(provider.models or []):
        set_temp_model_block(provider_name, model, seconds, reason)


def maybe_block_ollama_runtime_error(provider_name, model, error_text):
    provider = PROVIDERS.get(provider_name)
    if not provider or provider.api_type != 'ollama':
        return
    err = str(error_text or '')
    err_l = err.lower()
    if 'http 410' in err_l or ' was retired ' in f' {err_l} ':
        set_temp_model_block(
            provider_name,
            model,
            int(os.environ.get('SAGE_ROUTER_MODEL_RETIRED_COOLDOWN_SECONDS', '86400')),
            err[:180] or 'retired model',
        )
        return
    if 'http 403' in err_l and any(marker in err_l for marker in (
        'payment is past due',
        'requires a subscription',
        'upgrade for access',
    )):
        seconds = int(os.environ.get('SAGE_ROUTER_OLLAMA_SUBSCRIPTION_COOLDOWN_SECONDS', '3600'))
        if 'payment is past due' in err_l:
            set_temp_provider_models_block(provider_name, seconds, err[:180] or 'ollama subscription unavailable')
        else:
            set_temp_model_block(provider_name, model, seconds, err[:180] or 'ollama subscription unavailable')



def clear_temp_model_block(provider_name, model):
    TEMP_MODEL_BLOCKS.pop(f'{provider_name}/{model}', None)
    invalidate_model_health_cache(provider_name, model)


REQUESTED_MODEL_PROVIDER_PREFERENCE = [
    'openai-codex',
    'openai',
    'github-copilot',
    'google-vertex',
    'google',
    DARIO_PROVIDER_NAME,
    'anthropic',
    'xai',
    'mistral',
    'groq',
    'together',
    'fireworks',
    'openrouter',
    'ollama',
    'ollama-cloud',
    'ollama-cyber',
]


def split_provider_model(model_value):
    raw = str(model_value or '').strip()
    if '/' not in raw:
        return None, raw
    provider_name, model = raw.split('/', 1)
    return provider_name.strip() or None, model.strip()


def is_router_profile_model(model):
    name = str(model or '').strip()
    if not name:
        return False
    return name in load_router_profiles() or name in {'auto', 'fusion'}


def requested_model_supported_by_provider(provider_name, model):
    if not provider_name or not model:
        return False
    provider = PROVIDERS.get(provider_name)
    if not provider or provider_name in DISABLED_PROVIDERS:
        return False
    if provider.api_type == 'ollama':
        try:
            fetch_ollama_models(provider)
        except Exception:
            pass
    if active_temp_model_block(provider.name, model):
        return False
    if model not in (provider.models or []):
        return False
    if model_disabled_reason(provider.name, model):
        return False
    if not is_chat_capable_model(provider, model):
        return False
    return True


def requested_model_family_provider_names(model):
    model_l = str(model or '').strip().lower()
    if not model_l:
        return []
    if model_l.startswith(('gpt-', 'o1', 'o3', 'o4')) or 'codex' in model_l:
        return ['openai-codex', 'openai', 'github-copilot', 'azure-openai', 'openrouter']
    if model_l.startswith('claude') or model_l.startswith('anthropic.'):
        return [DARIO_PROVIDER_NAME, 'anthropic', 'bedrock', 'openrouter']
    if model_l.startswith(('gemini-', 'gemma')):
        return ['google-vertex', 'google', 'github-copilot', 'openrouter']
    if model_l.startswith('grok'):
        return ['xai', 'openrouter']
    if model_l.startswith(('mistral', 'codestral', 'ministral')):
        return ['mistral', 'openrouter']
    return []


def requested_model_family_supported_by_provider(provider_name, model):
    if not provider_name or not model:
        return False
    provider = PROVIDERS.get(provider_name)
    if not provider or provider_name in DISABLED_PROVIDERS:
        return False
    if provider.api_type == 'ollama':
        return False
    if provider_name not in requested_model_family_provider_names(model):
        return False
    if active_temp_model_block(provider.name, model):
        return False
    if model_disabled_reason(provider.name, model):
        return False
    if not is_chat_capable_model(provider, model):
        return False
    return provider_endpoint_reachable(provider)


def requested_model_provider_rank(provider_name):
    try:
        return REQUESTED_MODEL_PROVIDER_PREFERENCE.index(provider_name)
    except ValueError:
        return len(REQUESTED_MODEL_PROVIDER_PREFERENCE)


def infer_provider_for_requested_model(model, avoid_provider=None):
    matches = []
    for provider_name, provider in PROVIDERS.items():
        if provider_name == avoid_provider or provider_name in DISABLED_PROVIDERS:
            continue
        if requested_model_supported_by_provider(provider_name, model):
            matches.append(provider_name)
    if not matches:
        for provider_name, provider in PROVIDERS.items():
            if provider_name == avoid_provider or provider_name in DISABLED_PROVIDERS:
                continue
            if requested_model_family_supported_by_provider(provider_name, model):
                matches.append(provider_name)
    if not matches:
        return None
    matches.sort(key=lambda name: (requested_model_provider_rank(name), name))
    return matches[0]


def alternate_ollama_provider_for_stale_request(requested_provider, requested_model):
    """Find a sibling Ollama endpoint when a stale Ollama prefix names the wrong host."""
    candidates = []
    for provider_name, provider in PROVIDERS.items():
        if provider_name == requested_provider or provider_name in DISABLED_PROVIDERS:
            continue
        if provider.api_type != 'ollama':
            continue
        try:
            models = fetch_ollama_models(provider)
        except Exception:
            models = provider.models or []
        if not any(is_chat_capable_model(provider, model) for model in models or []):
            continue
        if not provider_endpoint_reachable(provider):
            continue
        local_rank = 0 if is_local_ollama_provider(provider) else 1
        cloud_rank = 1 if any(is_cloud_ollama_model(model) for model in models or []) else 0
        family_rank = 0 if provider_name.startswith('ollama-') else 1
        candidates.append((local_rank, cloud_rank, family_rank, requested_model_provider_rank(provider_name), provider_name))
    if not candidates:
        return None
    candidates.sort()
    return candidates[0][-1]


def resolve_requested_provider_model(payload):
    requested_provider = str(payload.get('provider') or '').strip() or None
    model_provider, requested_model = split_provider_model(payload.get('model'))
    if requested_provider in SELF_PROVIDER_NAMES:
        requested_provider = None
    if model_provider in SELF_PROVIDER_NAMES:
        nested_provider, nested_model = split_provider_model(requested_model)
        if nested_provider:
            model_provider, requested_model = nested_provider, nested_model
        elif is_router_profile_model(requested_model):
            return None, None
        else:
            model_provider = None
    if model_provider and not requested_provider:
        requested_provider = model_provider
    if not requested_provider and not model_provider and is_router_profile_model(requested_model):
        return None, None
    if not requested_model:
        return requested_provider, requested_model

    if (
        model_provider
        and requested_provider == model_provider
        and requested_provider in {'google', 'google-vertex'}
        and requested_provider in PROVIDERS
        and requested_provider not in DISABLED_PROVIDERS
    ):
        return requested_provider, requested_model

    if (
        requested_provider == 'ollama'
        and is_cloud_ollama_model(requested_model)
        and 'ollama-cloud' in PROVIDERS
        and 'ollama-cloud' not in DISABLED_PROVIDERS
        and requested_model_supported_by_provider('ollama-cloud', requested_model)
    ):
        logger.info(
            "Requested Ollama Cloud model %s will be served by hosted ollama-cloud provider",
            requested_model,
        )
        return 'ollama-cloud', requested_model

    if requested_provider and requested_model_supported_by_provider(requested_provider, requested_model):
        return requested_provider, requested_model

    inferred_provider = infer_provider_for_requested_model(requested_model, avoid_provider=requested_provider)
    if inferred_provider:
        if requested_provider and requested_provider != inferred_provider:
            logger.info(
                "Requested model %s belongs to %s, not stale provider %s; switching provider automatically",
                requested_model,
                inferred_provider,
                requested_provider,
            )
        return inferred_provider, requested_model

    if requested_provider:
        provider = PROVIDERS.get(requested_provider)
        if provider and provider.api_type == 'ollama':
            alternate_provider = alternate_ollama_provider_for_stale_request(requested_provider, requested_model)
            if alternate_provider:
                logger.info(
                    "Requested Ollama-family provider %s does not advertise model %s; using sibling provider %s as the routing hint",
                    requested_provider,
                    requested_model,
                    alternate_provider,
                )
                return alternate_provider, requested_model
            logger.info(
                "Requested Ollama-family provider %s does not advertise model %s; treating provider prefix as a routing hint",
                requested_provider,
                requested_model,
            )
            return None, requested_model

    return requested_provider, requested_model



def model_is_servable(provider, model):
    if model_disabled_reason(provider.name, model):
        return False
    if active_temp_model_block(provider.name, model):
        return False
    if local_ollama_cloud_auth_blocked(provider, model):
        return False
    if provider and provider.api_type != 'ollama':
        return True
    # Hosted Ollama Cloud models are servable through the remote Ollama API even
    # when they are not present in the local /api/tags installed-model list.
    if provider and provider.api_type == 'ollama' and is_cloud_ollama_model(model) and not is_local_ollama_provider(provider):
        return True
    meta = (provider.model_meta or {}).get(model, {})
    return bool(meta.get('servable', True))


def is_chat_capable_model(provider, model):
    model_l = (model or '').lower()
    if any(hint in model_l for hint in ('embed', 'embedding', 'rerank', 'bge-', 'nomic-embed')):
        return False
    if is_nvidia_provider(provider) and any(hint in model_l for hint in NVIDIA_NON_TOOL_MODEL_HINTS):
        return False
    if provider.api_type == 'ollama':
        # 1) Static name-pattern check (fast, catches most cases)
        if any(hint in model_l for hint in NON_CHAT_MODEL_HINTS):
            return False
        # 2) Dynamic family check from discovered metadata
        meta = (provider.model_meta or {}).get(model, {})
        family = (meta.get('family') or '').lower()
        families = [f.lower() for f in (meta.get('families') or []) if f]
        all_families = set(families) | {family} - {''}
        if all_families & NON_CHAT_OLLAMA_FAMILIES:
            return False
    return True


def provider_supports_reasoning(provider, model):
    if provider.api_type in ('openclaw-gateway', 'openai-codex-responses'):
        return True
    if provider.api_type == 'anthropic-messages':
        return model.startswith('claude-') or model.startswith('claude')
    reasoning_models = provider.reasoning_models or set()
    return model in reasoning_models


def is_cloud_ollama_model(model: str):
    model_l = (model or '').strip().lower()
    if ':' not in model_l:
        return False
    tag = model_l.rsplit(':', 1)[1]
    return tag == 'cloud' or tag.endswith('-cloud') or tag.endswith('_cloud')


def is_local_ollama_provider(provider):
    if not provider or provider.api_type != 'ollama':
        return False
    host = (urllib.parse.urlparse(provider.base_url or '').hostname or '').lower()
    return host in {'127.0.0.1', 'localhost', '::1'}


def is_local_cloud_ollama_model(provider, model: str):
    return is_local_ollama_provider(provider) and is_cloud_ollama_model(model)


def local_ollama_cloud_auth_blocked(provider, model: str):
    if not is_local_cloud_ollama_model(provider, model):
        return False
    key = provider.name
    until = float(LOCAL_OLLAMA_CLOUD_AUTH_BLOCKS.get(key, 0) or 0)
    if until <= time.time():
        LOCAL_OLLAMA_CLOUD_AUTH_BLOCKS.pop(key, None)
        return False
    return True


def set_local_ollama_cloud_auth_block(provider_name, seconds=300):
    if not provider_name:
        return
    LOCAL_OLLAMA_CLOUD_AUTH_BLOCKS[provider_name] = time.time() + max(30, int(seconds))
    MODEL_HEALTH_CACHE.clear()


def probe_local_ollama_cloud_auth(provider, model: str):
    if not is_local_cloud_ollama_model(provider, model) or local_ollama_cloud_auth_blocked(provider, model):
        return
    if os.environ.get('SAGE_ROUTER_OLLAMA_CLOUD_AUTH_PREFLIGHT', '1').strip().lower() not in {'1', 'true', 'yes', 'on'}:
        return
    url = provider.base_url.rstrip('/') + '/api/chat'
    payload = {'model': model, 'messages': [{'role': 'user', 'content': 'ping'}], 'stream': False, 'options': {'num_predict': 1}}
    headers = {'Content-Type': 'application/json'}
    if provider.api_key:
        headers['Authorization'] = f'Bearer {provider.api_key}'
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=headers)
        with urllib.request.urlopen(req, timeout=min(8, OLLAMA_TIMEOUT_SECONDS)) as resp:
            resp.read(256)
    except Exception as e:
        err = extract_http_error(e)
        if 'HTTP 401' in err:
            set_local_ollama_cloud_auth_block(provider.name, seconds=int(os.environ.get('SAGE_ROUTER_OLLAMA_CLOUD_AUTH_COOLDOWN_SECONDS', '3600')))
            logger.warning(f'Ollama Cloud auth preflight failed for local provider {provider.name}; suppressing local :cloud routing temporarily')

# Detect if a model supports vision/multimodal based on name patterns
VISION_MODEL_PATTERNS = ['vl', 'vision', 'qwen-vl', 'qwen_vl', 'llava', 'bakllava', 'moondream', 'minicpm-v', 'llama-vision', 'glm-4v', 'gpt-4o', 'gpt-4-turbo', 'claude-3-opus', 'claude-3-sonnet', 'claude-3.5', 'gemini-pro-vision', 'gemini-1.5', 'gpt-5.4', 'gpt-5.5']
OCR_MODEL_PATTERNS = ['ocr', 'paddleocr', 'trocr']

def is_multimodal_model(model: str) -> bool:
    model_l = (model or '').strip().lower()
    # Check exact matches first
    for pattern in VISION_MODEL_PATTERNS:
        pattern_l = pattern.lower()
        if model_l == pattern_l or model_l.startswith(pattern_l + '/') or f'-{pattern_l}' in model_l or f'_{pattern_l}' in model_l:
            return True
    # Check suffix patterns (e.g., model-name-vl)
    if any(model_l.endswith(suffix) for suffix in (':vl', '-vl', '_vl', '-vision', ':vision')):
        return True
    return False


def is_glm_model(model: str) -> bool:
    """True for any GLM-family model (glm-5, glm-5.2, glm-4v, autoglm, glmocr, ...)."""
    return 'glm' in (model or '').lower()


IMAGE_INPUT_BLOCK_TYPES = {'image', 'image_url', 'input_image', 'input_file'}


def _block_is_image_input(block):
    if not isinstance(block, dict):
        return False
    btype = str(block.get('type') or '').lower()
    if btype in IMAGE_INPUT_BLOCK_TYPES:
        # input_file counts only when it carries image mime/data
        if btype == 'input_file':
            mime = str(block.get('mime_type') or block.get('mimeType') or block.get('media_type') or block.get('mediaType') or '').lower()
            return mime.startswith('image/') or bool(block.get('image_url'))
        return True
    mime = str(block.get('mime_type') or block.get('mimeType') or block.get('media_type') or block.get('mediaType') or '').lower()
    if mime.startswith('image/'):
        return True
    # Bare image_url / image fields pointing at image data
    for key in ('image_url', 'image', 'url'):
        val = block.get(key)
        if isinstance(val, dict):
            val = val.get('url') or val.get('image_url')
        if isinstance(val, str) and (val.startswith('data:image/') or '/image' in val.lower()):
            return True
    return False


def payload_has_image_input(payload):
    """Deep scan any payload shape (chat messages, Responses `input`, tool
    messages/results) for image inputs. Catches image tool requests where
    images live inside tool calls or Responses-API item arrays."""
    seen = set()

    def visit(node):
        if id(node) in seen:
            return False
        seen.add(id(node))
        if isinstance(node, dict):
            if _block_is_image_input(node):
                return True
            for v in node.values():
                if visit(v):
                    return True
        elif isinstance(node, list):
            for item in node:
                if visit(item):
                    return True
        elif isinstance(node, str):
            if node.startswith('data:image/'):
                return True
        return False

    try:
        return visit(payload)
    except Exception:
        return False




def looks_like_visible_tool_call(text: str) -> bool:
    """Detect tool-call-shaped text that a non-tool model leaked visibly.

    OpenClaw expects actual OpenAI-compatible tool_calls, not prose/code blocks
    containing `tool_code` or `message(action=...)`. When a provider returns this
    while tools were offered, treat the attempt as failed so routing can fall
    through to a model with real tool-call support instead of posting the leak.
    Keep this intentionally narrow to avoid rejecting legitimate discussion of
    code samples.
    """
    raw = str(text or '').strip()
    if not raw:
        return False
    lowered = raw.lower()
    if 'tool_code' in lowered or '<tool_call' in lowered or '</tool_call>' in lowered:
        return True
    if re.search(r'(?m)^\s*(?:functions\.)?message\s*\(\s*action\s*=', raw):
        return True
    if re.search(r'(?m)^\s*(?:functions\.)?(?:exec|browser|web_fetch|web_search|read|pdf)\s*\(', raw):
        return True
    if re.search(r'(?m)^\s*```(?:tool_code|tool|json)?\s*\n\s*\{\s*["\'](?:tool|name|cmd|path|command)["\']', raw, re.IGNORECASE):
        return True
    if re.search(r'(?m)(?:^|\s)to\s*=\s*(?:exec|read|browser|message|web_search|web_fetch|pdf)\s*\{', raw, re.IGNORECASE):
        return True
    if re.search(r'(?s)\{\s*["\'](?:cmd|command)["\']\s*:\s*["\'][^"\']*(?:cd\s+|/|find\s+|ls\s+|python|bash|git)\b', raw, re.IGNORECASE):
        return True
    if re.search(r'(?s)\{\s*["\']path["\']\s*:\s*["\'](?:/|~|\./|[^"\']*/)[^"\']*["\']\s*\}', raw, re.IGNORECASE):
        return True
    if re.search(r'(?s)\{\s*["\']recipient_name["\']\s*:\s*["\']functions\.[a-z_]+["\']\s*,\s*["\']parameters["\']', raw):
        return True
    return False


def reject_visible_tool_call_leak(payload, text: str, tool_calls) -> str:
    if not (payload or {}).get('tools') or tool_calls:
        return ''
    if looks_like_visible_tool_call(text):
        return 'provider leaked tool call as visible text instead of structured tool_calls'
    return ''

TOOL_CALLS_OMITTED_RE = r'\[\s*tool\s+calls\s*omitted\s*\]'
MODEL_PREFIX_LABEL_RE = r'\[[A-Za-z0-9_.-]+/[^\]\s]+\]'
PARTIAL_MODEL_PREFIX_LABEL_RE = r'\[[A-Za-z0-9_.-]*(?:/[^\]\s]*)?$'


def strip_leading_generic_model_prefix_labels(text: str):
    """Remove leading provider/model labels without requiring route context."""
    remaining = str(text or '')
    changed = False
    while True:
        stripped = remaining.lstrip()
        leading_ws = remaining[:len(remaining) - len(stripped)]
        match = re.match(r'^\[([^\]\n]{1,140})\](?=\s|$)\s*', stripped)
        if not match or not looks_like_model_prefix_label(match.group(1)):
            break
        remaining = leading_ws + stripped[match.end():].lstrip()
        changed = True
    return remaining.strip() if changed else remaining


def strip_model_prefix_tool_placeholder_noise(text: str):
    """Drop replay-only model prefix/tool-placeholder lines without context."""
    remaining = str(text or '')
    if not remaining:
        return ''
    prefix_re = MODEL_PREFIX_LABEL_RE
    prefix_run_re = rf'(?:{prefix_re}\s*)+'
    placeholder_run_re = rf'(?:{prefix_re}\s*)*{TOOL_CALLS_OMITTED_RE}'
    cleaned_lines = []
    changed = False
    for line in remaining.splitlines():
        stripped = line.strip()
        if not stripped:
            cleaned_lines.append(line)
            continue
        labels = re.findall(prefix_re, stripped)
        without_noise = re.sub(prefix_re, '', stripped).strip()
        without_noise = re.sub(TOOL_CALLS_OMITTED_RE, '', without_noise, flags=re.IGNORECASE).strip()
        if labels:
            without_noise = re.sub(PARTIAL_MODEL_PREFIX_LABEL_RE, '', without_noise).strip()
        if not labels and '/' in stripped and stripped.rsplit('/', 1)[1] and re.fullmatch(PARTIAL_MODEL_PREFIX_LABEL_RE, stripped):
            changed = True
            continue
        if labels and not without_noise:
            changed = True
            continue
        if not labels and not without_noise and re.search(TOOL_CALLS_OMITTED_RE, stripped, flags=re.IGNORECASE):
            changed = True
            continue
        cleaned_lines.append(line)
    cleaned = '\n'.join(cleaned_lines).strip() if changed else remaining
    if not cleaned.rstrip().endswith(']'):
        return cleaned
    suffix_noise_re = rf'(?:\s+(?:{placeholder_run_re}|{prefix_run_re}))+\s*$'
    suffix_cleaned = re.sub(suffix_noise_re, '', cleaned, flags=re.IGNORECASE).rstrip()
    if suffix_cleaned != cleaned:
        cleaned = suffix_cleaned
        changed = True
    if changed:
        return re.sub(PARTIAL_MODEL_PREFIX_LABEL_RE, '', cleaned.strip()).rstrip()
    return cleaned


def sanitize_visible_output(text: str):
    """Remove provider-private reasoning/tool scratch from visible text.

    Several upstreams return non-OpenAI fields correctly, but some local or
    OpenAI-compatible models leak reasoning as literal <think>/<thinking> blocks
    or emit tool invocations as prose/code instead of structured tool_calls. The
    router must never pass those scratch channels through to end users.
    """
    raw = text or ''
    if not raw:
        return ''
    cleaned = str(raw)

    # Strip common reasoning/scratchpad blocks. Include aliases used by local
    # reasoning models and OpenAI-compatible gateways.
    for tag in ('think', 'thinking', 'reasoning', 'analysis', 'scratchpad'):
        cleaned = _re.sub(rf'<{tag}\b[^>]*>.*?</{tag}>\s*', '', cleaned, flags=_re.IGNORECASE | _re.DOTALL)
        if f'</{tag}>' in cleaned.lower():
            cleaned = _re.split(rf'</{tag}>', cleaned, flags=_re.IGNORECASE)[-1]
        # Drop any orphan opening tag of a reasoning block (e.g. an unterminated
        # <think>private chain) so private reasoning is never surfaced to users.
        cleaned = _re.sub(rf'<{tag}\b[^>]*>.*\Z', '', cleaned, flags=_re.IGNORECASE | _re.DOTALL)
        cleaned = _re.sub(rf'</?{tag}\b[^>]*>', '', cleaned, flags=_re.IGNORECASE)

    # Strip OpenAI Responses-style <|channel|>...<|message|> tags.  Anything in
    # the 'analysis' / 'commentary' / 'scratchpad' channels is private; the
    # 'final' / 'assistant' channel is the user-visible part.
    channel_block = re.compile(
        r'<\|channel\|>\s*(?:analysis|commentary|scratchpad|thinking|reasoning|internal)\s*<\|message\|>.*?(?=<\|channel\|>|<\|end\|>|\Z)',
        _re.IGNORECASE | _re.DOTALL,
    )
    cleaned = channel_block.sub('', cleaned)
    cleaned = _re.sub(r'<\|channel\|>\s*(?:final|assistant|output)\s*<\|message\|>', '', cleaned, flags=_re.IGNORECASE)
    cleaned = _re.sub(r'<\|/?(channel|message|end)\s*\|>', '', cleaned, flags=_re.IGNORECASE)

    # Strip fenced/labelled tool-call scratch that should have been structured.
    cleaned = _re.sub(r'```\s*(?:tool_code|tool_call|tool|tools)\b.*?```\s*', '', cleaned, flags=_re.IGNORECASE | _re.DOTALL)
    cleaned = _re.sub(r'<tool_call\b[^>]*>.*?</tool_call>\s*', '', cleaned, flags=_re.IGNORECASE | _re.DOTALL)
    cleaned = _re.sub(r'</?tool_call\b[^>]*>', '', cleaned, flags=_re.IGNORECASE)

    # Remove standalone JSON-ish command/tool invocation lines. Keep this narrow
    # and line-oriented so normal explanatory text about tools is preserved.
    cleaned = _re.sub(r'(?m)^\s*(?:to\s*=\s*)?(?:functions\.)?(?:exec|read|browser|message|web_search|web_fetch|pdf)\s*(?:\(|\{).*$\n?', '', cleaned)
    cleaned = _re.sub(r'(?m)^\s*tool_code\s*$\n?', '', cleaned, flags=_re.IGNORECASE)
    cleaned = _re.sub(r'(?m)^\s*\{\s*["\'](?:cmd|command|path|tool|name)["\']\s*:\s*.*\}\s*$\n?', '', cleaned, flags=_re.IGNORECASE)
    cleaned = strip_model_prefix_tool_placeholder_noise(cleaned)
    cleaned = strip_leading_generic_model_prefix_labels(cleaned)

    cleaned = cleaned.strip()
    return cleaned


def is_ocr_model(model: str) -> bool:
    model_l = (model or '').strip().lower()
    for pattern in OCR_MODEL_PATTERNS:
        if pattern in model_l:
            return True
    return False

def normalize_tool_calls(tool_calls):
    normalized = []
    logger.debug(f"normalize_tool_calls input count: {len(tool_calls or [])}")
    for idx, tool_call in enumerate(tool_calls or []):
        if not isinstance(tool_call, dict):
            logger.debug(f"Skipping non-dict tool_call: {tool_call}")
            continue
        function = tool_call.get('function') if isinstance(tool_call.get('function'), dict) else {}
        name = function.get('name') or tool_call.get('name') or f'tool_{idx + 1}'
        arguments = function.get('arguments') if 'arguments' in function else tool_call.get('arguments', {})
        # Ollama expects arguments as an object, not a JSON string
        if isinstance(arguments, str):
            try:
                arguments = json.loads(arguments)
            except Exception as e:
                logger.debug(f"Failed to parse arguments JSON: {e}")
                arguments = {}
        normalized.append({
            'id': tool_call.get('id') or f'call_{uuid.uuid4().hex[:24]}',
            'type': 'function',
            'function': {
                'name': name,
                'arguments': arguments if isinstance(arguments, dict) else {},
            },
        })
        logger.debug(f"Normalized tool call: name={name}, has_arguments={bool(arguments)}")
    logger.debug(f"normalize_tool_calls output count: {len(normalized)}")
    return normalized


def openai_tool_calls(tool_calls):
    """Return OpenAI-compatible tool_calls with function.arguments as JSON strings.

    Internally Sage Router normalizes tool arguments as dicts because Ollama
    expects objects. OpenAI-compatible clients, including OpenClaw tool
    validators, expect function.arguments to be a JSON object string. Returning
    raw arrays/objects can cause empty/invalid tool invocation payloads.
    """
    converted = []
    for tool_call in normalize_tool_calls(tool_calls):
        function = tool_call.get('function') or {}
        arguments = function.get('arguments')
        if isinstance(arguments, str):
            try:
                parsed = json.loads(arguments) if arguments else {}
            except Exception:
                parsed = {}
        else:
            parsed = arguments if isinstance(arguments, dict) else {}
        converted.append({
            'id': tool_call.get('id') or f'call_{uuid.uuid4().hex[:24]}',
            'type': 'function',
            'function': {
                'name': function.get('name') or 'tool',
                'arguments': json.dumps(parsed, separators=(',', ':')),
            },
        })
    return converted


def responses_tool_definition(tool):
    """Convert Chat Completions tool definitions to Responses API tools."""
    if not isinstance(tool, dict):
        return None
    tool_type = tool.get('type')
    if tool_type != 'function':
        return dict(tool)
    function = tool.get('function')
    if isinstance(function, dict):
        converted = {'type': 'function'}
        for key in ('name', 'description', 'parameters', 'strict'):
            if key in function:
                converted[key] = function[key]
        return converted if converted.get('name') else None
    converted = dict(tool)
    return converted if converted.get('name') else None


def responses_tool_definitions(tools):
    converted = []
    for tool in tools or []:
        converted_tool = responses_tool_definition(tool)
        if converted_tool:
            converted.append(converted_tool)
    return converted


def responses_tool_choice(tool_choice):
    if tool_choice in (None, 'auto'):
        return None
    if isinstance(tool_choice, str) and tool_choice in {'none', 'required'}:
        return tool_choice
    if isinstance(tool_choice, dict) and tool_choice.get('type') == 'function':
        fn_name = (tool_choice.get('function') or {}).get('name') or tool_choice.get('name')
        if fn_name:
            return {'type': 'function', 'name': fn_name}
    return tool_choice


def responses_function_call_tool_call(item):
    if not isinstance(item, dict) or item.get('type') != 'function_call':
        return None
    name = item.get('name')
    if not name:
        return None
    arguments = item.get('arguments') or ''
    return {
        'id': item.get('call_id') or item.get('id') or f'call_{uuid.uuid4().hex[:24]}',
        'type': 'function',
        'function': {
            'name': name,
            'arguments': arguments,
        },
    }


def parse_responses_stream(resp):
    full_text = []
    tool_items = {}
    tool_order = []
    event_type = None
    completed_body = None

    def remember_tool_item(item):
        call = responses_function_call_tool_call(item)
        if not call:
            return
        item_id = item.get('id') or item.get('call_id') or call['id']
        if item_id not in tool_order:
            tool_order.append(item_id)
        existing = tool_items.get(item_id) or {}
        # Deep-merge: shallow update would overwrite nested function/arguments
        # and drop bytes already accumulated by response.function_call_arguments.delta.
        existing['id'] = call.get('id', existing.get('id', item_id))
        existing['type'] = call.get('type', existing.get('type', 'function'))
        existing_fn = existing.setdefault('function', {})
        call_fn = call.get('function') or {}
        if call_fn.get('name') and not existing_fn.get('name'):
            existing_fn['name'] = call_fn['name']
        if call_fn.get('arguments'):
            # New event has full arguments — use them, but only if we have
            # nothing accumulated (delta events append below).
            if not existing_fn.get('arguments'):
                existing_fn['arguments'] = call_fn['arguments']
        tool_items[item_id] = existing

    for raw_line in resp:
        line = raw_line.decode().strip() if isinstance(raw_line, bytes) else str(raw_line).strip()
        if line.startswith('event: '):
            event_type = line[6:].strip()
            continue
        if line == 'data: [DONE]':
            break
        if not line.startswith('data: '):
            continue
        try:
            data = json.loads(line[6:])
        except Exception:
            continue
        data_type = data.get('type') or event_type
        if data_type == 'response.output_text.delta':
            full_text.append(data.get('delta', ''))
        elif data_type in {'response.output_item.added', 'response.output_item.done'}:
            remember_tool_item(data.get('item') or {})
        elif data_type == 'response.function_call_arguments.delta':
            item_id = data.get('item_id')
            if not item_id:
                continue
            if item_id not in tool_order:
                tool_order.append(item_id)
            existing = tool_items.setdefault(item_id, {
                'id': data.get('call_id') or item_id,
                'type': 'function',
                'function': {'name': data.get('name') or 'tool', 'arguments': ''},
            })
            existing_function = existing.setdefault('function', {})
            existing_function['arguments'] = (existing_function.get('arguments') or '') + (data.get('delta') or '')
        elif data_type == 'response.function_call_arguments.done':
            item_id = data.get('item_id')
            if not item_id:
                continue
            if item_id not in tool_order:
                tool_order.append(item_id)
            existing = tool_items.setdefault(item_id, {
                'id': data.get('call_id') or item_id,
                'type': 'function',
                'function': {'name': data.get('name') or 'tool', 'arguments': ''},
            })
            existing.setdefault('function', {})['arguments'] = data.get('arguments') or ''
        elif data_type == 'response.completed':
            completed_body = data.get('response') or {}

    if isinstance(completed_body, dict):
        for item in completed_body.get('output') or []:
            remember_tool_item(item)

    tool_calls = [tool_items[item_id] for item_id in tool_order if item_id in tool_items]
    return ''.join(full_text), tool_calls


def responses_content_to_chat_content(content):
    """Convert Responses message content blocks to Chat Completions content."""
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return normalize_content(content)

    chat_parts = []
    text_parts = []
    has_structured_part = False
    for block in content:
        if isinstance(block, str):
            text_parts.append(block)
            chat_parts.append({'type': 'text', 'text': block})
            continue
        if not isinstance(block, dict):
            text = normalize_content(block)
            if text:
                text_parts.append(text)
                chat_parts.append({'type': 'text', 'text': text})
            continue
        block_type = block.get('type')
        if block_type in {'input_text', 'output_text', 'text'}:
            text = block.get('text') or ''
            if text:
                text_parts.append(text)
                chat_parts.append({'type': 'text', 'text': text})
        elif block_type in {'input_image', 'image_url'}:
            image_url = block.get('image_url') or block.get('url')
            if isinstance(image_url, dict):
                image_url = image_url.get('url') or image_url.get('image_url')
            if image_url:
                has_structured_part = True
                chat_parts.append({'type': 'image_url', 'image_url': {'url': image_url}})
        else:
            text = block.get('text') or normalize_content(block)
            if text:
                text_parts.append(text)
                chat_parts.append({'type': 'text', 'text': text})

    if has_structured_part:
        return chat_parts
    return '\n'.join(text_parts)


def responses_input_to_chat_messages(input_value, instructions=None):
    messages = []
    if instructions:
        messages.append({'role': 'system', 'content': normalize_content(instructions)})
    if isinstance(input_value, str):
        messages.append({'role': 'user', 'content': input_value})
        return messages
    if isinstance(input_value, dict):
        input_items = [input_value]
    else:
        input_items = input_value or []

    for item in input_items:
        if isinstance(item, str):
            messages.append({'role': 'user', 'content': item})
            continue
        if not isinstance(item, dict):
            continue
        item_type = item.get('type')
        if item_type == 'function_call_output':
            call_id = item.get('call_id') or item.get('id') or ''
            if not call_id:
                continue
            messages.append({
                'role': 'tool',
                'tool_call_id': call_id,
                'content': normalize_content(item.get('output') or ''),
            })
            continue
        if item_type == 'function_call':
            call_id = item.get('call_id') or item.get('id') or f'call_{uuid.uuid4().hex[:24]}'
            arguments = item.get('arguments') or ''
            if not isinstance(arguments, str):
                arguments = json.dumps(arguments, separators=(',', ':'))
            messages.append({
                'role': 'assistant',
                'content': '',
                'tool_calls': [{
                    'id': call_id,
                    'type': 'function',
                    'function': {'name': item.get('name') or 'tool', 'arguments': arguments},
                }],
            })
            continue
        if item_type and item_type != 'message' and 'role' not in item:
            continue
        role = item.get('role') or 'user'
        if role == 'developer':
            role = 'system'
        content = responses_content_to_chat_content(item.get('content', ''))
        if role == 'assistant' and isinstance(content, str):
            content = strip_assistant_replay_noise(content)
        if content or role == 'tool':
            messages.append({'role': role, 'content': content})

    return messages or [{'role': 'user', 'content': ''}]


def responses_tool_to_chat_tool(tool):
    if not isinstance(tool, dict):
        return None
    if tool.get('type') == 'function' and isinstance(tool.get('function'), dict):
        return tool
    if tool.get('type') == 'function':
        fn = {
            'name': tool.get('name') or 'tool',
            'description': tool.get('description') or '',
            'parameters': tool.get('parameters') or {'type': 'object', 'properties': {}},
        }
        if 'strict' in tool:
            fn['strict'] = tool.get('strict')
        return {'type': 'function', 'function': fn}
    if tool.get('name'):
        return {
            'type': 'function',
            'function': {
                'name': tool.get('name'),
                'description': tool.get('description') or '',
                'parameters': tool.get('parameters') or {'type': 'object', 'properties': {}},
            },
        }
    return None


def responses_tools_to_chat_tools(tools):
    converted = []
    for tool in tools or []:
        converted_tool = responses_tool_to_chat_tool(tool)
        if converted_tool:
            converted.append(converted_tool)
    return converted


def responses_tool_choice_to_chat(tool_choice):
    if tool_choice in (None, 'auto', 'none', 'required'):
        return tool_choice
    if isinstance(tool_choice, dict) and tool_choice.get('type') == 'function':
        name = tool_choice.get('name') or (tool_choice.get('function') or {}).get('name')
        if name:
            return {'type': 'function', 'function': {'name': name}}
    return tool_choice


def responses_payload_to_chat_payload(payload):
    chat_payload = {
        'model': payload.get('model') or 'sage-router/auto',
        'messages': responses_input_to_chat_messages(payload.get('input', []), payload.get('instructions')),
        'stream': False,
    }
    copy_keys = (
        'temperature', 'top_p', 'stop', 'route', 'thinking', 'reasoning',
        'requirements', 'response_format', 'metadata', 'parallel_tool_calls',
        'debug', 'debugMode', 'sageRouterProfile', 'routerProfile', 'profile',
    )
    for key in copy_keys:
        if key in payload:
            chat_payload[key] = payload[key]
    if payload.get('max_output_tokens') is not None:
        chat_payload['max_tokens'] = payload.get('max_output_tokens')
    elif payload.get('max_tokens') is not None:
        chat_payload['max_tokens'] = payload.get('max_tokens')
    tools = responses_tools_to_chat_tools(payload.get('tools'))
    if tools:
        chat_payload['tools'] = tools
    if 'tool_choice' in payload:
        chat_payload['tool_choice'] = responses_tool_choice_to_chat(payload.get('tool_choice'))
    text_format = ((payload.get('text') or {}).get('format') or {})
    if text_format.get('type') in {'json_object', 'json_schema'}:
        chat_payload['response_format'] = text_format
    return chat_payload


def openai_chat_completion_to_responses(result, request_payload, request_id):
    response_id = f"resp_{uuid.uuid4().hex[:24]}"
    created = int(result.get('created') or time.time())
    model = result.get('model') or request_payload.get('model') or 'sage-router/auto'
    choice = (result.get('choices') or [{}])[0] or {}
    message = choice.get('message') or {}
    content = sanitize_visible_output(message.get('content') or '')
    output = []
    output_text = ''
    if content:
        output_text = content
        output.append({
            'id': f"msg_{uuid.uuid4().hex[:24]}",
            'type': 'message',
            'status': 'completed',
            'role': 'assistant',
            'content': [{'type': 'output_text', 'text': content, 'annotations': []}],
        })
    for tool_call in message.get('tool_calls') or []:
        fn = tool_call.get('function') or {}
        arguments = fn.get('arguments') or ''
        if not isinstance(arguments, str):
            arguments = json.dumps(arguments, separators=(',', ':'))
        output.append({
            'id': f"fc_{uuid.uuid4().hex[:24]}",
            'type': 'function_call',
            'status': 'completed',
            'call_id': tool_call.get('id') or f"call_{uuid.uuid4().hex[:24]}",
            'name': fn.get('name') or 'tool',
            'arguments': arguments,
        })

    usage = result.get('usage') or {}
    input_tokens = int(usage.get('prompt_tokens') or usage.get('input_tokens') or 0)
    output_tokens = int(usage.get('completion_tokens') or usage.get('output_tokens') or 0)
    return {
        'id': response_id,
        'object': 'response',
        'created_at': created,
        'status': 'completed',
        'error': None,
        'incomplete_details': None,
        'instructions': request_payload.get('instructions'),
        'max_output_tokens': request_payload.get('max_output_tokens'),
        'model': model,
        'output': output,
        'output_text': output_text,
        'parallel_tool_calls': bool(request_payload.get('parallel_tool_calls', True)),
        'previous_response_id': request_payload.get('previous_response_id'),
        'reasoning': request_payload.get('reasoning'),
        'request_id': request_id,
        'store': bool(request_payload.get('store', False)),
        'temperature': request_payload.get('temperature'),
        'text': request_payload.get('text') or {'format': {'type': 'text'}},
        'tool_choice': request_payload.get('tool_choice', 'auto'),
        'tools': request_payload.get('tools') or [],
        'top_p': request_payload.get('top_p'),
        'truncation': request_payload.get('truncation'),
        'usage': {
            'input_tokens': input_tokens,
            'input_tokens_details': {'cached_tokens': int(usage.get('cached_tokens') or 0)},
            'output_tokens': output_tokens,
            'output_tokens_details': {'reasoning_tokens': int(usage.get('reasoning_tokens') or 0)},
            'total_tokens': int(usage.get('total_tokens') or (input_tokens + output_tokens)),
        },
    }


def sanitize_responses_payload(response):
    if not isinstance(response, dict):
        return response
    sanitized = dict(response)
    if isinstance(sanitized.get('output_text'), str):
        sanitized['output_text'] = sanitize_visible_output(sanitized.get('output_text') or '')
    output = []
    for item in sanitized.get('output') or []:
        if not isinstance(item, dict):
            continue
        updated_item = dict(item)
        if updated_item.get('type') == 'message':
            updated_content = []
            for part in updated_item.get('content') or []:
                if not isinstance(part, dict):
                    updated_content.append(part)
                    continue
                updated_part = dict(part)
                if updated_part.get('type') in {'output_text', 'input_text', 'text'} and isinstance(updated_part.get('text'), str):
                    updated_part['text'] = sanitize_visible_output(updated_part.get('text') or '')
                if updated_part.get('type') in {'output_text', 'input_text', 'text'} and not str(updated_part.get('text') or '').strip():
                    continue
                updated_content.append(updated_part)
            updated_item['content'] = updated_content
            if not updated_content:
                continue
        output.append(updated_item)
    sanitized['output'] = output
    return sanitized


def openai_model_row(model_id, owned_by='sage-router', **metadata):
    row = {
        'id': str(model_id or ''),
        'object': 'model',
        'created': 0,
        'owned_by': str(owned_by or 'sage-router'),
    }
    for key, value in metadata.items():
        if value is not None:
            row[key] = value
    return row


def openai_models_payload():
    rows = []
    seen = set()

    def add(model_id, owned_by='sage-router', **metadata):
        model_id = str(model_id or '').strip()
        if not model_id or model_id in seen:
            return
        seen.add(model_id)
        rows.append(openai_model_row(model_id, owned_by=owned_by, **metadata))

    profiles = load_router_profiles()
    for name, profile in sorted(profiles.items()):
        profile = profile if isinstance(profile, dict) else {}
        add(
            f'sage-router/{name}',
            'sage-router',
            type='router_profile',
            route=profile.get('route'),
            thinking=profile.get('thinking'),
            description=profile.get('description'),
        )
    for name in ('auto', 'fusion'):
        add(f'sage-router/{name}', 'sage-router', type='router_profile')

    for provider_name, provider in sorted(PROVIDERS.items()):
        if provider_name in DISABLED_PROVIDERS:
            continue
        for model in dedupe_keep_order(provider.models or []):
            if model_disabled_reason(provider_name, model):
                continue
            add(
                display_model_id(provider_name, model),
                provider_name,
                type='provider_model',
                provider=provider_name,
            )
    return {'object': 'list', 'data': rows}


def google_models_payload():
    models_data = []
    seen = set()
    for name, prov in PROVIDERS.items():
        if name in DISABLED_PROVIDERS:
            continue
        for m in prov.models:
            if model_disabled_reason(name, m):
                continue
            model_name = f'models/{m}'
            if model_name in seen:
                continue
            seen.add(model_name)
            models_data.append({
                'name': model_name,
                'displayName': m,
                'supportedGenerationMethods': ['generateContent', 'streamGenerateContent'],
            })
    return {'models': models_data}


def write_responses_as_sse(self, response, request_id, extra_headers=None):
    response = sanitize_responses_payload(response)

    def write_event(event_name, data):
        payload = dict(data)
        payload.setdefault('type', event_name)
        self.wfile.write(f"event: {event_name}\ndata: {json.dumps(payload)}\n\n".encode())

    try:
        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.send_header('Cache-Control', 'no-cache')
        self.send_cors_headers()
        for key, value in (extra_headers or {}).items():
            if value:
                self.send_header(key, str(value))
        self.end_headers()
        created = dict(response)
        created['status'] = 'in_progress'
        created['output'] = []
        write_event('response.created', {'response': created})
        for output_index, item in enumerate(response.get('output') or []):
            write_event('response.output_item.added', {'output_index': output_index, 'item': item})
            if item.get('type') == 'message':
                for content_index, part in enumerate(item.get('content') or []):
                    write_event('response.content_part.added', {
                        'item_id': item.get('id'),
                        'output_index': output_index,
                        'content_index': content_index,
                        'part': part,
                    })
                    if part.get('type') == 'output_text' and part.get('text'):
                        write_event('response.output_text.delta', {
                            'item_id': item.get('id'),
                            'output_index': output_index,
                            'content_index': content_index,
                            'delta': part.get('text') or '',
                        })
                        write_event('response.output_text.done', {
                            'item_id': item.get('id'),
                            'output_index': output_index,
                            'content_index': content_index,
                            'text': part.get('text') or '',
                        })
                    write_event('response.content_part.done', {
                        'item_id': item.get('id'),
                        'output_index': output_index,
                        'content_index': content_index,
                        'part': part,
                    })
            elif item.get('type') == 'function_call':
                write_event('response.function_call_arguments.done', {
                    'item_id': item.get('id'),
                    'output_index': output_index,
                    'call_id': item.get('call_id'),
                    'name': item.get('name'),
                    'arguments': item.get('arguments') or '',
                })
            write_event('response.output_item.done', {'output_index': output_index, 'item': item})
        write_event('response.completed', {'response': response})
        self.wfile.write(b'data: [DONE]\n\n')
        self.wfile.flush()
    except (BrokenPipeError, ConnectionResetError):
        logger.warning(f"[{request_id}] Client disconnected during Responses SSE write")


def build_router_metadata(provider_name, model, request_id=''):
    return {
        'provider': provider_name,
        'model': model,
        'request_id': request_id,
    }


# Track which request_ids have already emitted a provider/model prefix,
# so the prefix appears once per unique displayed model. Use display_model_id()
# rather than the raw provider name so aliased backends such as ollama-cloud and
# ollama-cyber do not emit duplicate visible prefixes for the same model.
_PREFIX_SEEN = {}
_PREFIX_SEEN_TTL = 300  # seconds


def _prefix_seen_key(request_id, provider_name, model):
    return (request_id, display_model_id(provider_name, model))


def _expire_prefix_seen(now=None):
    now = now or time.time()
    cutoff = now - _PREFIX_SEEN_TTL
    expired = [key for key, seen_at in _PREFIX_SEEN.items() if seen_at < cutoff]
    for key in expired:
        del _PREFIX_SEEN[key]


def _has_prefix_been_seen(request_id, provider_name, model):
    now = time.time()
    _expire_prefix_seen(now)
    key = _prefix_seen_key(request_id, provider_name, model)
    return key in _PREFIX_SEEN


def _mark_prefix_seen(request_id, provider_name, model):
    _expire_prefix_seen()
    _PREFIX_SEEN[_prefix_seen_key(request_id, provider_name, model)] = time.time()


def text_already_has_model_prefix(text, provider_name, model):
    stripped = (text or '').lstrip()
    display_id = display_model_id(provider_name, model)
    return stripped.startswith(f'[{display_id}]') or stripped.startswith(f'[sage-router {display_id}]')


def looks_like_model_prefix_label(label):
    label = (label or '').strip()
    if label.lower().startswith('sage-router '):
        label = label.split(None, 1)[1].strip()
    if len(label) > 140 or ' ' in label or '/' not in label:
        return False
    return bool(re.match(r'^[A-Za-z0-9_.-]+/[^\]\s]+$', label))


def model_prefix_labels(provider_name, model):
    labels = {
        display_model_id(provider_name, model),
        f'{provider_name}/{model}',
        str(model or ''),
    }
    if '/' in str(model or ''):
        labels.add(str(model or '').split('/', 1)[1])
    return {label for label in labels if label and label != 'None/None'}


def normalize_model_label_part(value):
    value = str(value or '').strip()
    return value.removesuffix(':cloud').removesuffix('-cloud').lower()


def model_prefix_label_matches_context(label, provider_name, model):
    label = (label or '').strip()
    if label.lower().startswith('sage-router '):
        label = label.split(None, 1)[1].strip()
    if not looks_like_model_prefix_label(label):
        return False
    labels = model_prefix_labels(provider_name, model)
    if label in labels:
        return True
    if '/' not in label:
        return False
    label_provider, label_model = label.split('/', 1)
    display_id = display_model_id(provider_name, model)
    display_provider, display_model = display_id.split('/', 1) if '/' in display_id else ('', display_id)
    provider_candidates = {
        str(provider_name or '').strip().lower(),
        str(display_provider or '').strip().lower(),
    }
    if display_provider == 'ollama' or str(provider_name or '').strip().lower().startswith('ollama'):
        provider_candidates.update(p.lower() for p in _OLLAMA_PROVIDER_ALIASES)
        provider_candidates.add('ollama')
    model_candidates = {
        normalize_model_label_part(model),
        normalize_model_label_part(display_model),
    }
    if '/' in str(model or ''):
        model_candidates.add(normalize_model_label_part(str(model).split('/', 1)[1]))
    label_provider_l = label_provider.strip().lower()
    label_model_l = normalize_model_label_part(label_model)
    provider_matches = (
        label_provider_l in provider_candidates
        or any(label_provider_l.startswith(candidate + '-') for candidate in provider_candidates if candidate)
    )
    return provider_matches and label_model_l in model_candidates


def strip_standalone_model_prefix_labels(text, provider_name, model):
    """Remove contextual provider/model labels that appear as standalone text."""
    remaining = text or ''
    if '[' not in remaining or ']' not in remaining:
        return remaining

    def replace(match):
        leading = match.group(1) or ''
        label = match.group(2) or ''
        if model_prefix_label_matches_context(label, provider_name, model):
            return leading
        return match.group(0)

    previous = None
    while previous != remaining:
        previous = remaining
        remaining = re.sub(r'(^|[\s])\[([^\]\n]{1,140})\](?=\s|$)', replace, remaining)
    return remaining


def strip_tool_call_omission_placeholders(text):
    """Remove provider placeholders that only describe hidden tool calls."""
    remaining = text or ''
    if not re.search(TOOL_CALLS_OMITTED_RE, remaining, flags=re.IGNORECASE):
        return remaining
    remaining = re.sub(rf'(^|[\s]){TOOL_CALLS_OMITTED_RE}(?=\s|$)', r'\1', remaining, flags=re.IGNORECASE)
    remaining = re.sub(r'[ \t]{2,}', ' ', remaining)
    remaining = re.sub(r'\n{3,}', '\n\n', remaining)
    return remaining.strip()


def strip_assistant_replay_noise(text):
    """Remove harness replay placeholders before they reach upstream models."""
    remaining = str(text or '')
    if not remaining:
        return ''
    cleaned_lines = []
    for line in remaining.splitlines():
        stripped = line.strip()
        if not stripped:
            cleaned_lines.append(line)
            continue
        if re.search(TOOL_CALLS_OMITTED_RE, stripped, flags=re.IGNORECASE):
            placeholder_labels = re.findall(r'\[([^\]\n]{1,140})\]', stripped)
            if placeholder_labels and placeholder_labels[-1].strip().lower() == 'tool calls omitted' and all(
                label.strip().lower() == 'tool calls omitted' or looks_like_model_prefix_label(label)
                for label in placeholder_labels
            ):
                without_labels = re.sub(r'\[[^\]\n]{1,140}\]\s*', '', stripped).strip()
                if not without_labels:
                    continue
        cleaned_lines.append(line)
    remaining = '\n'.join(cleaned_lines).strip()
    while True:
        stripped = remaining.lstrip()
        leading_ws = remaining[:len(remaining) - len(stripped)]
        match = re.match(r'^\[([^\]\n]{1,140})\]\s*', stripped)
        if not match or not looks_like_model_prefix_label(match.group(1)):
            break
        remaining = leading_ws + stripped[match.end():].lstrip()
    remaining = strip_tool_call_omission_placeholders(remaining)
    return remaining.strip()


def sanitize_replay_messages(messages):
    """Clean assistant-history artifacts while preserving structured tool calls."""
    sanitized = []
    for msg in messages or []:
        if not isinstance(msg, dict):
            continue
        if msg.get('role') != 'assistant':
            sanitized.append(msg)
            continue
        cleaned_content = strip_assistant_replay_noise(normalize_content(msg.get('content', '')))
        tool_calls = normalize_tool_calls(msg.get('tool_calls'))
        if not cleaned_content and not tool_calls:
            continue
        updated = dict(msg)
        updated['content'] = cleaned_content
        if tool_calls:
            updated['tool_calls'] = tool_calls
        sanitized.append(updated)
    return sanitized


def strip_leading_model_prefixes(text, provider_name, model):
    """Remove provider/model labels already emitted by an upstream response."""
    remaining = text or ''
    labels = model_prefix_labels(provider_name, model)
    changed = True
    while changed:
        changed = False
        stripped = remaining.lstrip()
        leading_ws = remaining[:len(remaining) - len(stripped)]
        for label in sorted(labels, key=len, reverse=True):
            prefix = f'[{label}]'
            if stripped.startswith(prefix):
                remaining = leading_ws + stripped[len(prefix):].lstrip()
                changed = True
                break
        if changed:
            continue
        match = re.match(r'^\[([^\]\n]{1,140})\]\s*', stripped)
        if match and looks_like_model_prefix_label(match.group(1)):
            remaining = leading_ws + stripped[match.end():].lstrip()
            changed = True
    remaining = strip_standalone_model_prefix_labels(remaining, provider_name, model)
    return strip_tool_call_omission_placeholders(remaining)


def strip_leading_model_prefixes_for_display(text, display_id):
    display_id = str(display_id or '')
    if '/' in display_id:
        provider_name, model = display_id.split('/', 1)
    else:
        provider_name, model = '', display_id
    return strip_leading_model_prefixes(text, provider_name, model)


def possible_model_prefix_fragment(text, provider_name, model):
    stripped = (text or '').lstrip()
    if not stripped:
        return True
    if not stripped.startswith('['):
        return False
    labels = model_prefix_labels(provider_name, model)
    prefix_candidates = {
        f'[{label}]'
        for label in labels
    } | {
        f'[sage-router {label}]'
        for label in labels
    }
    if any(candidate.startswith(stripped) for candidate in prefix_candidates):
        return True
    closing = stripped.find(']')
    if closing < 0:
        fragment = stripped[1:]
        return len(stripped) <= 160 and '/' in fragment and ' ' not in fragment and '\n' not in stripped
    return looks_like_model_prefix_label(stripped[1:closing])


def possible_tool_call_omission_fragment(text):
    stripped = (text or '').lstrip()
    if not stripped or not stripped.startswith('['):
        return False
    compact = re.sub(r'\s+', ' ', stripped.lower()).strip()
    compact_no_space = re.sub(r'\s+', '', stripped.lower())
    return '[tool calls omitted]'.startswith(compact) or '[toolcallsomitted]'.startswith(compact_no_space)


def sanitize_stream_content_fragment(content, provider_name, model, state=None):
    """Remove leading provider/model labels even when split across SSE chunks."""
    text = sanitize_visible_output(content or '')
    if state is None:
        return strip_leading_model_prefixes(text, provider_name, model)

    combined = str(state.get('prefix_pending') or '') + text
    cleaned = strip_leading_model_prefixes(combined, provider_name, model)
    if cleaned != combined:
        state['prefix_pending'] = ''
        if cleaned:
            if possible_tool_call_omission_fragment(cleaned):
                state['prefix_pending'] = cleaned
                if len(cleaned) <= 200:
                    return ''
            state['prefix_open'] = False
            return cleaned
        return ''

    prefix_still_open = state.get('prefix_open', True)
    possible_late_fragment = (
        not prefix_still_open
        and combined.lstrip().startswith('[')
        and ']' not in combined
    )
    if possible_model_prefix_fragment(combined, provider_name, model) and (prefix_still_open or possible_late_fragment):
        state['prefix_pending'] = combined
        if len(combined) <= 200:
            return ''
    if possible_tool_call_omission_fragment(combined):
        state['prefix_pending'] = combined
        if len(combined) <= 200:
            return ''

    state['prefix_pending'] = ''
    state['prefix_open'] = False
    cleaned = strip_standalone_model_prefix_labels(combined, provider_name, model)
    return strip_tool_call_omission_placeholders(cleaned)


def sanitize_provider_visible_text(text, provider_name, model):
    """Sanitize provider text before it can be wrapped or leak beside tools."""
    return strip_leading_model_prefixes(
        sanitize_visible_output(text or ''),
        provider_name,
        model,
    )


def model_prefix_once(provider_name, model, request_id, text, sage_router_debug=False):
    text = sanitize_provider_visible_text(text, provider_name, model)
    if not text:
        return text
    if text_already_has_model_prefix(text, provider_name, model):
        _mark_prefix_seen(request_id, provider_name, model)
        return text
    if _has_prefix_been_seen(request_id, provider_name, model):
        return text
    _mark_prefix_seen(request_id, provider_name, model)
    display_id = display_model_id(provider_name, model)
    if sage_router_debug:
        return f'[sage-router {display_id}]\n{text}'
    return f'[{display_id}] {text}'


def streaming_debug_prefix(provider_name, model, request_id):
    if _has_prefix_been_seen(request_id, provider_name, model):
        return ''
    _mark_prefix_seen(request_id, provider_name, model)
    return f'[sage-router {display_model_id(provider_name, model)}]\n'


def sanitize_openai_compat_stream_line(raw_line, provider_name, model, state=None):
    """Sanitize visible content in proxied OpenAI-compatible SSE chunks."""
    if not raw_line:
        return raw_line
    if isinstance(raw_line, bytes):
        line = raw_line.decode('utf-8', errors='replace')
        as_bytes = True
    else:
        line = str(raw_line)
        as_bytes = False
    stripped = line.lstrip()
    if not stripped.startswith('data:'):
        return raw_line
    prefix_len = len(line) - len(stripped)
    data = stripped[len('data:'):].strip()
    if not data or data == '[DONE]':
        return raw_line
    try:
        chunk = json.loads(data)
    except Exception:
        return raw_line
    changed = False
    for choice in chunk.get('choices') or []:
        if not isinstance(choice, dict):
            continue
        for container_key in ('delta', 'message'):
            container = choice.get(container_key)
            if not isinstance(container, dict) or 'content' not in container:
                continue
            original = container.get('content') or ''
            cleaned = sanitize_stream_content_fragment(original, provider_name, model, state=state)
            if cleaned != original:
                container['content'] = cleaned
                changed = True
    if not changed:
        return raw_line
    sanitized = f"{line[:prefix_len]}data: {json.dumps(chunk, separators=(',', ':'))}\n"
    return sanitized.encode('utf-8') if as_bytes else sanitized


def maybe_prefix_debug_text(content, metadata, debug_mode=False, allow_prefix=True):
    text = sanitize_provider_visible_text(content, metadata.get('provider'), metadata.get('model'))
    if debug_mode and allow_prefix and text:
        text = model_prefix_once(metadata.get('provider'), metadata.get('model'), metadata.get('request_id'), text, sage_router_debug=True)
    return text


def build_openai_completion(provider_name, model, request_id, content='', tool_calls=None, finish_reason=None, usage=None, debug_mode=False, allow_debug_prefix=True, suppress_tool_call_content=False):
    metadata = build_router_metadata(provider_name, model, request_id)
    normalized_tool_calls = openai_tool_calls(tool_calls)
    if normalized_tool_calls:
        # Never pair visible narration with structured tool calls. Some clients,
        # including Discord delivery surfaces, can expose the text before tool
        # execution, which looks like leaked internal scratch/tool narration.
        content = ''
    # When SHOW_MODEL_PREFIX is on, the [provider/model] prefix provides
    # the model identity. Only add the debug prefix when SHOW_MODEL_PREFIX is off.
    if SHOW_MODEL_PREFIX and not normalized_tool_calls:
        content_text = model_prefix_once(provider_name, model, request_id, content or '')
    else:
        content_text = maybe_prefix_debug_text(content, metadata, debug_mode=debug_mode, allow_prefix=allow_debug_prefix and not normalized_tool_calls)
    message = {'role': 'assistant', 'content': content_text}
    if normalized_tool_calls:
        message['tool_calls'] = normalized_tool_calls
    resolved_finish_reason = finish_reason or ('tool_calls' if normalized_tool_calls else 'stop')
    response = {
        'id': f'chatcmpl-{int(time.time())}',
        'object': 'chat.completion',
        'created': int(time.time()),
        'model': display_model_id(provider_name, model),
        'choices': [{
            'index': 0,
            'message': message,
            'finish_reason': resolved_finish_reason,
        }],
        'usage': usage or {'prompt_tokens': 0, 'completion_tokens': 0},
    }
    if debug_mode:
        response['sage_router'] = metadata
    return response



def openai_completion_has_visible_output(result):
    if not isinstance(result, dict):
        return False
    choices = result.get('choices') or []
    if not choices:
        return False
    message = (choices[0] or {}).get('message') or {}
    content = message.get('content')
    has_text = bool(str(content or '').strip())
    has_tools = bool(message.get('tool_calls'))
    return has_text or has_tools


def is_sage_router_fusion_request(payload):
    if not isinstance(payload, dict):
        return False
    model = str(payload.get('model') or '').strip().lower()
    profile = str(payload.get('profile') or payload.get('routerProfile') or payload.get('sageRouterProfile') or '').strip().lower()
    return model in FUSION_MODEL_ALIASES or profile == 'fusion'


def is_fusion_server_tool(tool):
    return isinstance(tool, dict) and str(tool.get('type') or '').strip().lower() in FUSION_SERVER_TOOL_TYPES


def fusion_server_tools(payload):
    if not isinstance(payload, dict):
        return []
    return [tool for tool in payload.get('tools') or [] if is_fusion_server_tool(tool)]


def tool_choice_targets_fusion(tool_choice):
    if isinstance(tool_choice, str):
        return tool_choice.strip().lower() in FUSION_SERVER_TOOL_TYPES
    if not isinstance(tool_choice, dict):
        return False
    choice_type = str(tool_choice.get('type') or '').strip().lower()
    if choice_type in FUSION_SERVER_TOOL_TYPES:
        return True
    name = str(tool_choice.get('name') or (tool_choice.get('function') or {}).get('name') or '').strip().lower()
    return name in FUSION_SERVER_TOOL_TYPES


def fusion_server_tool_required(payload):
    if not fusion_server_tools(payload):
        return False
    tool_choice = payload.get('tool_choice')
    if isinstance(tool_choice, str) and tool_choice.strip().lower() == 'required':
        return True
    return tool_choice_targets_fusion(tool_choice)


def fusion_prompt_benefits_from_panel(payload):
    requirements = payload.get('requirements') or {}
    if isinstance(requirements, dict) and (
        requirements.get('fusion') or requirements.get('qualitySensitive') or requirements.get('highStakes')
    ):
        return True
    text = fusion_messages_excerpt(payload.get('messages') or [], limit=2400).lower()
    return any(term in text for term in FUSION_AUTO_TRIGGER_TERMS)


def fusion_server_tool_should_invoke(payload):
    if not fusion_server_tools(payload):
        return False
    tool_choice = payload.get('tool_choice')
    if isinstance(tool_choice, str) and tool_choice.strip().lower() == 'none':
        return False
    if fusion_server_tool_required(payload):
        return True
    return fusion_prompt_benefits_from_panel(payload)


def strip_fusion_server_tools_from_payload(payload):
    if not fusion_server_tools(payload):
        return payload
    stripped = dict(payload)
    remaining_tools = [tool for tool in payload.get('tools') or [] if not is_fusion_server_tool(tool)]
    if remaining_tools:
        stripped['tools'] = remaining_tools
    else:
        stripped.pop('tools', None)
    if fusion_server_tool_required(payload) or not remaining_tools:
        stripped.pop('tool_choice', None)
    return stripped


def fusion_payload_from_server_tool(payload):
    fusion_payload = strip_fusion_server_tools_from_payload(payload)
    fusion_payload = dict(fusion_payload)
    fusion_payload['model'] = 'sage-router/fusion'
    fusion_payload.pop('tools', None)
    fusion_payload.pop('tool_choice', None)
    metadata = fusion_payload.get('metadata') if isinstance(fusion_payload.get('metadata'), dict) else {}
    fusion_payload['metadata'] = {**metadata, 'fusionServerTool': True}
    return fusion_payload


def current_route_customer_plan():
    ctx = getattr(ROUTE_AUTH_CONTEXT, 'value', {}) or {}
    return str(ctx.get('customer_plan') or '').strip().lower()


def fusion_plan_allowed():
    ctx = getattr(ROUTE_AUTH_CONTEXT, 'value', {}) or {}
    auth_type = str(ctx.get('auth_type') or '').strip().lower()
    plan = current_route_customer_plan()
    if auth_type == 'generated_key':
        return plan in FUSION_ALLOWED_PLANS
    # Operator/self-hosted tokens are allowed so local deployments can use
    # their own provider credentials without the hosted billing control plane.
    return True


def fusion_messages_excerpt(messages, limit=6000):
    parts = []
    for message in messages or []:
        if not isinstance(message, dict):
            continue
        role = str(message.get('role') or 'user')[:24]
        text = normalize_content(message.get('content', ''))
        if text.strip():
            parts.append(f'{role}: {text.strip()}')
    return '\n'.join(parts)[-limit:]


def fusion_panel_messages(messages):
    return [
        {
            'role': 'system',
            'content': (
                'You are one independent Sage Router Fusion panelist. Answer the user request directly, '
                'with concise reasoning and concrete caveats. Do not mention other panelists or the fusion process.'
            ),
        },
        *normalize_messages(messages or []),
    ]


def fusion_judge_messages(original_messages, panel_rows):
    response_blocks = []
    for index, row in enumerate(panel_rows, start=1):
        text = str(row.get('content') or '').strip()
        if not text:
            continue
        response_blocks.append(
            f'Panel {index} ({row.get("provider")}/{row.get("model")}):\n{text[:5000]}'
        )
    panel_text = '\n\n'.join(response_blocks)
    return [
        {
            'role': 'system',
            'content': (
                'You are Sage Router Fusion. Synthesize the panel into one best final answer. '
                'Use consensus, contradictions, missing coverage, and unique useful details. '
                'Do not expose hidden chain-of-thought. Do not name panel providers unless the user asks.'
            ),
        },
        {
            'role': 'user',
            'content': (
                'Original conversation excerpt:\n'
                f'{fusion_messages_excerpt(original_messages)}\n\n'
                'Panel responses:\n'
                f'{panel_text}\n\n'
                'Write the final answer now.'
            ),
        },
    ]


def call_provider_completion_once(provider_name, model, payload, request_id, thinking, debug_mode=False):
    if provider_name in DISABLED_PROVIDERS or provider_name not in PROVIDERS:
        return False, f'provider unavailable: {provider_name}'
    prov = PROVIDERS[provider_name]
    supports_reasoning = provider_supports_reasoning(prov, model)

    def dispatch(api_key):
        if prov.api_type == 'ollama':
            return call_ollama_completion(prov.base_url, model, payload, api_key, thinking, provider_name=provider_name, debug_mode=debug_mode, request_id=request_id)
        if prov.api_type == 'openclaw-gateway':
            ok_text, text = call_openclaw_gateway(model, payload.get('messages', []), provider_name, thinking, payload.get('response_format', {}).get('type') == 'json_object')
            if not ok_text:
                return False, text
            return True, build_openai_completion(provider_name, model, request_id, text, [], 'stop', {'prompt_tokens': 0, 'completion_tokens': 0}, debug_mode=debug_mode)
        if prov.api_type == 'anthropic-messages':
            return call_anthropic_completion(prov.base_url, model, payload, api_key, thinking, supports_reasoning, debug_mode=debug_mode, request_id=request_id, provider_name=provider_name)
        if prov.api_type == 'google-generative-language':
            return call_google_completion(prov.base_url, model, payload, api_key, thinking, debug_mode=debug_mode, request_id=request_id, provider_name=provider_name)
        if prov.api_type == 'google-vertex-ai':
            return call_google_vertex_completion(prov.base_url, model, payload, thinking, debug_mode=debug_mode, request_id=request_id)
        if prov.api_type == 'cloudflare-workers-ai':
            return call_cloudflare_workers_ai_completion(prov.base_url, model, payload, api_key, thinking, debug_mode=debug_mode, request_id=request_id)
        if prov.api_type == 'openai-codex-responses':
            return call_codex_completion(prov.base_url, model, payload, api_key, provider_name, thinking, supports_reasoning, debug_mode=debug_mode, request_id=request_id)
        return call_openai_compat_completion(prov.base_url, model, payload, api_key, provider_name, thinking, supports_reasoning, debug_mode=debug_mode, request_id=request_id)

    # Provider types whose credential is not a simple bearer/x-api-key token
    # (gateway supplies its own credential; Vertex uses ADC). Skip the
    # multi-credential failover loop for those and dispatch once.
    non_keyed_types = {'openclaw-gateway', 'google-vertex-ai'}
    if prov.api_type in non_keyed_types:
        return dispatch(prov.api_key)

    # Multi-credential selection: order is decided by the provider's
    # credential strategy (failover / round-robin / lru / random). Failover
    # tries pool order with the (possibly refreshed) primary key first; load
    # balancing strategies distribute across keys and deprioritize cooled-down
    # ones. On auth/quota/transient errors we fall over to the next credential.
    strategy = provider_credential_strategy(prov)
    candidate_keys = select_credential_keys(prov)
    identities = select_credential_identities(prov) if strategy != 'failover' else []
    if not candidate_keys:
        candidate_keys = [prov.api_key]
    if len(candidate_keys) <= 1:
        return dispatch(prov.api_key)

    last_err = ''
    for idx, key in enumerate(candidate_keys):
        ident = identities[idx] if idx < len(identities) else ''
        if ident:
            mark_credential_used(provider_name, ident)
        ok, result = dispatch(key)
        if ok:
            if ident:
                mark_credential_success(provider_name, ident)
            if idx > 0:
                logger.info(f"Provider {provider_name} credential #{idx + 1} succeeded after failover (strategy={strategy})")
            return ok, result
        last_err = result if isinstance(result, str) else str(result)
        if not is_credential_failover_error(last_err):
            return ok, result
        if ident:
            mark_credential_error(provider_name, ident)
        logger.warning(f"Provider {provider_name} credential #{idx + 1} failed ({last_err[:120]}); trying next credential (strategy={strategy})")
    return False, last_err


def select_fusion_panel_chain(messages, request_id, thinking, route_mode, requirements, want_json):
    req = dict(requirements or {})
    req.update({'qualitySensitive': True, 'reasoning': True})
    _messages, _intent, _complexity, _tokens, chain = prepare_route(
        messages,
        request_id=f'{request_id}-fusion-select',
        thinking=thinking,
        route_mode=route_mode if route_mode != 'local-first' else 'balanced',
        requirements=req,
        want_json=want_json,
        streaming_mode='fusion-buffered',
    )
    picked = []
    seen = set()
    for provider_name, model in chain:
        key = (provider_name, model)
        if key in seen:
            continue
        seen.add(key)
        picked.append(key)
        if len(picked) >= FUSION_PANEL_SIZE:
            break
    return picked


def run_fusion_panel_candidate(provider_name, model, payload, request_id, thinking, debug_mode=False):
    started = time.time()
    ok = False
    result = None
    error_detail = ''
    try:
        ok, result = call_provider_completion_once(provider_name, model, payload, request_id, thinking, debug_mode=debug_mode)
        if ok and not openai_completion_has_visible_output(result):
            ok = False
            error_detail = 'empty visible content'
        elif not ok:
            error_detail = result
    except Exception as e:
        error_detail = extract_http_error(e)
    elapsed = time.time() - started
    row = {
        'provider': provider_name,
        'model': model,
        'ok': bool(ok),
        'elapsedMs': round(elapsed * 1000.0, 2),
        'detail': '' if ok else str(error_detail or '')[:240],
    }
    if ok:
        choice = (result.get('choices') or [{}])[0] or {}
        message = choice.get('message') or {}
        row['content'] = sanitize_visible_output(message.get('content') or '')
        row['usage'] = result.get('usage') or {}
    return row


def handle_sage_router_fusion(self, payload, request_id, started, return_result=False):
    if not fusion_plan_allowed():
        plan = current_route_customer_plan() or 'free'
        failure = {
            'error': {
                'type': 'billing_error',
                'code': 'fusion_plan_required',
                'message': 'sage-router/fusion is available on Pro, Max, metered, manual, or operator-enabled plans.',
                'plan': plan,
            },
            'request_id': request_id,
        }
        headers = {'X-Sage-Router-Request-Id': request_id, 'X-Sage-Router-Model': 'sage-router/fusion'}
        if return_result:
            return 402, failure, headers
        self.write_json(402, failure, extra_headers=headers)
        return
    if payload.get('tools') or payload.get('tool_choice'):
        failure = {
            'error': {
                'type': 'invalid_request_error',
                'code': 'fusion_tools_unsupported',
                'message': 'sage-router/fusion currently supports plain chat synthesis; send tool calls to sage-router/agentic or sage-router/frontier.',
            },
            'request_id': request_id,
        }
        headers = {'X-Sage-Router-Request-Id': request_id, 'X-Sage-Router-Model': 'sage-router/fusion'}
        if return_result:
            return 400, failure, headers
        self.write_json(400, failure, extra_headers=headers)
        return

    messages = normalize_messages(payload.get('messages', []))
    thinking = normalize_thinking(payload.get('thinking') or payload.get('reasoning') or {'effort': 'high'})
    route_mode = normalize_route_mode(payload.get('route') or 'best')
    requirements = normalize_requirements(payload, thinking)
    want_json = str(payload.get('responseFormat') or '').lower() == 'json' or payload.get('response_format', {}).get('type') == 'json_object'
    debug_mode = normalize_debug_mode(payload)
    panel_chain = select_fusion_panel_chain(messages, request_id, thinking, route_mode, requirements, want_json)
    if not panel_chain:
        failure = {'error': 'Fusion panel has no eligible providers', 'request_id': request_id, 'attempts': []}
        headers = {'X-Sage-Router-Request-Id': request_id, 'X-Sage-Router-Model': 'sage-router/fusion'}
        if return_result:
            return 503, failure, headers
        self.write_json(503, failure, extra_headers=headers)
        return

    panel_payload = dict(payload)
    panel_payload.pop('provider', None)
    panel_payload.pop('tools', None)
    panel_payload.pop('tool_choice', None)
    panel_payload['model'] = 'sage-router/auto'
    panel_payload['messages'] = fusion_panel_messages(messages)
    panel_payload['stream'] = False
    panel_payload['requirements'] = {**requirements, 'qualitySensitive': True, 'reasoning': True}
    panel_rows = []
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=len(panel_chain))
    try:
        futures = [
            executor.submit(run_fusion_panel_candidate, provider_name, model, panel_payload, f'{request_id}-p{index}', thinking, debug_mode)
            for index, (provider_name, model) in enumerate(panel_chain, start=1)
        ]
        done, pending = concurrent.futures.wait(futures, timeout=FUSION_PANEL_TIMEOUT_SECONDS)
        for future in done:
            try:
                panel_rows.append(future.result())
            except Exception as e:
                panel_rows.append({'provider': 'unknown', 'model': 'unknown', 'ok': False, 'elapsedMs': 0, 'detail': extract_http_error(e)[:240]})
        for future in pending:
            future.cancel()
            panel_rows.append({'provider': 'unknown', 'model': 'unknown', 'ok': False, 'elapsedMs': FUSION_PANEL_TIMEOUT_SECONDS * 1000, 'detail': 'fusion panel timeout'})
    finally:
        executor.shutdown(wait=False, cancel_futures=True)

    successful = [row for row in panel_rows if row.get('ok') and str(row.get('content') or '').strip()]
    if not successful:
        total_elapsed = time.time() - started
        safe_attempts = [{k: row.get(k) for k in ('provider', 'model', 'ok', 'elapsedMs', 'detail')} for row in panel_rows[-12:]]
        append_route_event({'request_id': request_id, 'status': 'failed', 'intent': 'FUSION', 'complexity': 'COMPLEX', 'thinking': thinking.value, 'routeMode': 'fusion', 'estimatedTokens': estimate_prompt_tokens(messages), 'json': want_json, 'stream': False, 'requirements': {'fusion': True}, 'selected': None, 'attempts': safe_attempts, 'totalElapsedMs': round(total_elapsed * 1000.0, 2), 'chain': [{'provider': p, 'model': m} for p, m in panel_chain], 'error': 'Fusion panel failed'})
        failure = {'error': 'Fusion panel failed', 'request_id': request_id, 'attempts': safe_attempts}
        headers = {'X-Sage-Router-Request-Id': request_id, 'X-Sage-Router-Model': 'sage-router/fusion'}
        if return_result:
            return 503, failure, headers
        self.write_json(503, failure, extra_headers=headers)
        return

    judge_messages = fusion_judge_messages(messages, successful)
    judge_chain = select_fusion_panel_chain(judge_messages, f'{request_id}-judge', ThinkingLevel.HIGH, 'best', {'qualitySensitive': True, 'reasoning': True}, want_json)
    judge_provider, judge_model = (judge_chain[0] if judge_chain else panel_chain[0])
    judge_payload = {
        'model': 'sage-router/auto',
        'messages': judge_messages,
        'response_format': {'type': 'json_object'} if want_json else {},
        'requirements': {'qualitySensitive': True, 'reasoning': True},
    }
    judge_row = run_fusion_panel_candidate(judge_provider, judge_model, judge_payload, f'{request_id}-judge', ThinkingLevel.HIGH, debug_mode)
    if judge_row.get('ok') and str(judge_row.get('content') or '').strip():
        content = judge_row.get('content') or ''
    else:
        content = successful[0].get('content') or ''

    total_usage = {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}
    for row in [*successful, judge_row]:
        usage = row.get('usage') or {}
        total_usage['prompt_tokens'] += int(usage.get('prompt_tokens') or 0)
        total_usage['completion_tokens'] += int(usage.get('completion_tokens') or 0)
        total_usage['total_tokens'] += int(usage.get('total_tokens') or 0)
    if not total_usage['total_tokens']:
        total_usage.pop('total_tokens', None)
    result = build_openai_completion('sage-router', 'fusion', request_id, content, [], 'stop', total_usage, debug_mode=debug_mode, allow_debug_prefix=False)
    if debug_mode:
        result.setdefault('sage_router', {})['fusion'] = {
            'panelSize': len(panel_chain),
            'successfulPanelists': len(successful),
            'panel': [{k: row.get(k) for k in ('provider', 'model', 'ok', 'elapsedMs', 'detail')} for row in panel_rows],
            'judge': {k: judge_row.get(k) for k in ('provider', 'model', 'ok', 'elapsedMs', 'detail')},
            'access': {'allowedPlans': sorted(FUSION_ALLOWED_PLANS), 'plan': current_route_customer_plan() or 'operator'},
        }
    total_elapsed = time.time() - started
    safe_panel_attempts = [{k: row.get(k) for k in ('provider', 'model', 'ok', 'elapsedMs', 'detail')} for row in panel_rows[-12:]]
    attempts = safe_panel_attempts + [{k: judge_row.get(k) for k in ('provider', 'model', 'ok', 'elapsedMs', 'detail')}]
    LAST_ROUTE_DEBUG.update({'selected': {'provider': 'sage-router', 'model': 'fusion'}, 'attempts': attempts, 'status': 'ok', 'error': None, 'totalElapsedMs': round(total_elapsed * 1000.0, 2), 'routeMode': 'fusion'})
    append_route_event({'request_id': request_id, 'status': 'ok', 'intent': 'FUSION', 'complexity': 'COMPLEX', 'thinking': thinking.value, 'routeMode': 'fusion', 'estimatedTokens': estimate_prompt_tokens(messages), 'json': want_json, 'stream': False, 'requirements': {'fusion': True, 'panelSize': len(panel_chain)}, 'selected': {'provider': 'sage-router', 'model': 'fusion'}, 'attempts': attempts, 'totalElapsedMs': round(total_elapsed * 1000.0, 2), 'chain': [{'provider': p, 'model': m} for p, m in panel_chain]})
    headers = self.routing_headers(result, request_id)
    headers['X-Sage-Router-Fusion'] = '1'
    if return_result:
        return 200, result, headers
    if payload.get('stream'):
        write_openai_completion_as_sse(self, result, request_id)
        return
    self.write_json(200, result, extra_headers=headers)


def build_openai_proxy_payload(payload, model, stream=False, supports_reasoning=False, thinking=DEFAULT_THINKING_LEVEL):
    allowed_keys = [
        'messages', 'tools', 'tool_choice', 'parallel_tool_calls', 'response_format',
        'temperature', 'top_p', 'frequency_penalty', 'presence_penalty',
        'stop', 'n', 'user', 'seed', 'stream_options', 'max_tokens',
        'max_completion_tokens', 'modalities', 'audio', 'metadata'
    ]
    proxied = {'model': model, 'stream': bool(stream)}
    for key in allowed_keys:
        if key in payload:
            proxied[key] = sanitize_replay_messages(payload.get(key)) if key == 'messages' else payload.get(key)
    if supports_reasoning:
        proxied['reasoning'] = payload.get('reasoning') or {'effort': thinking.value}
    return proxied


def openai_messages_to_ollama(messages):
    converted = []
    for msg in sanitize_replay_messages(messages):
        if not isinstance(msg, dict):
            continue
        item = {
            'role': msg.get('role', 'user'),
            'content': normalize_content(msg.get('content', '')),
        }
        tool_calls = normalize_tool_calls(msg.get('tool_calls'))
        if tool_calls:
            item['tool_calls'] = tool_calls
        if msg.get('tool_call_id'):
            item['tool_call_id'] = msg.get('tool_call_id')
        converted.append(item)
    return converted


def ollama_model_supports_native_thinking(model: str) -> bool:
    model_l = (model or '').lower()
    # Ollama exposes native reasoning in a separate message.thinking field for
    # the qwen3.6 family. Keep this conservative so ordinary local models are
    # not sent unsupported think flags.
    return model_l.startswith('qwen3.6') or '/qwen3.6' in model_l or is_kimi_model(model)


def ollama_generation_options(thinking=DEFAULT_THINKING_LEVEL):
    if thinking == ThinkingLevel.LOW:
        return {'num_predict': 1024}
    if thinking == ThinkingLevel.HIGH:
        return {'num_predict': 16384}
    return {'num_predict': 8192}


def build_ollama_payload(model, payload, thinking=DEFAULT_THINKING_LEVEL, stream=False):
    ollama_payload = {
        'model': model,
        'messages': openai_messages_to_ollama(payload.get('messages', [])),
        'stream': bool(stream),
        'options': ollama_generation_options(thinking),
    }
    if ollama_model_supports_native_thinking(model):
        # LOW is operational/exact-output mode. MEDIUM/HIGH allow native Ollama
        # reasoning and give enough generation budget for thinking + final text.
        ollama_payload['think'] = thinking != ThinkingLevel.LOW
        # Use separate thinking budget so reasoning tokens don't consume the
        # content token budget. Models that think can easily spend 10-30K tokens
        # in message.thinking before producing visible content.
        if thinking != ThinkingLevel.LOW:
            opts = dict(ollama_payload.get('options') or {})
            opts['num_predict_thinking'] = 32768
            # Ensure total budget is large enough for both thinking + content
            opts['num_predict'] = max(int(opts.get('num_predict') or 0), 8192)
            # Ollama Cloud models accept larger contexts when explicitly set.
            opts['num_ctx'] = max(int(opts.get('num_ctx') or 0), 65536)
            ollama_payload['options'] = opts
    if payload.get('tools'):
        ollama_payload['tools'] = payload.get('tools')
    return ollama_payload


def openai_tools_to_anthropic(tools):
    converted = []
    for tool in tools or []:
        if not isinstance(tool, dict) or tool.get('type') != 'function':
            continue
        fn = tool.get('function') or {}
        converted.append({
            'name': fn.get('name'),
            'description': fn.get('description', ''),
            'input_schema': fn.get('parameters') or {'type': 'object', 'properties': {}},
        })
    return [tool for tool in converted if tool.get('name')]


def openai_messages_to_anthropic(messages):
    system_text = []
    converted = []
    for msg in sanitize_replay_messages(messages):
        if not isinstance(msg, dict):
            continue
        role = msg.get('role', 'user')
        content = normalize_content(msg.get('content', ''))
        if role == 'system':
            if content:
                system_text.append(content)
            continue
        if role == 'tool':
            block = {'type': 'tool_result', 'tool_use_id': msg.get('tool_call_id') or f'toolu_{uuid.uuid4().hex[:16]}', 'content': content}
            converted.append({'role': 'user', 'content': [block]})
            continue
        blocks = []
        if content:
            blocks.append({'type': 'text', 'text': content})
        for tool_call in normalize_tool_calls(msg.get('tool_calls')):
            raw_arguments = tool_call['function'].get('arguments')
            if isinstance(raw_arguments, dict):
                tool_input = raw_arguments
            else:
                try:
                    tool_input = json.loads(raw_arguments) if raw_arguments else {}
                except Exception:
                    tool_input = {'raw_arguments': raw_arguments}
            blocks.append({'type': 'tool_use', 'id': tool_call['id'], 'name': tool_call['function']['name'], 'input': tool_input})
        converted.append({'role': 'assistant' if role == 'assistant' else 'user', 'content': blocks or [{'type': 'text', 'text': ''}]})
    return '\n'.join(system_text).strip(), converted or [{'role': 'user', 'content': [{'type': 'text', 'text': 'Hello'}]}]


def parse_anthropic_response(body):
    content_blocks = body.get('content', []) or []
    text_parts = []
    tool_calls = []
    for block in content_blocks:
        if not isinstance(block, dict):
            continue
        if block.get('type') == 'text':
            text_parts.append(str(block.get('text', '')))
        elif block.get('type') == 'tool_use':
            tool_calls.append({
                'id': block.get('id') or f'call_{uuid.uuid4().hex[:24]}',
                'type': 'function',
                'function': {
                    'name': block.get('name') or 'tool',
                    'arguments': json.dumps(block.get('input') or {}, separators=(',', ':')),
                },
            })
    return sanitize_visible_output(''.join(text_parts)), normalize_tool_calls(tool_calls), body.get('stop_reason'), {
        'prompt_tokens': ((body.get('usage') or {}).get('input_tokens') or 0),
        'completion_tokens': ((body.get('usage') or {}).get('output_tokens') or 0),
    }


def anthropic_stop_reason_to_openai_finish_reason(stop_reason, has_tool_calls=False):
    reason = str(stop_reason or '').strip().lower()
    if has_tool_calls or reason == 'tool_use':
        return 'tool_calls'
    if reason == 'max_tokens':
        return 'length'
    if reason in ('end_turn', 'stop_sequence', 'stop'):
        return 'stop'
    return reason or 'stop'


def openai_finish_reason_to_anthropic_stop_reason(finish_reason):
    reason = str(finish_reason or '').strip().lower()
    if reason in ('length', 'max_tokens'):
        return 'max_tokens'
    if reason in ('tool_calls', 'function_call', 'tool_use'):
        return 'tool_use'
    if reason == 'stop_sequence':
        return 'stop_sequence'
    return 'end_turn'


def google_finish_reason_to_openai_finish_reason(finish_reason):
    reason = str(finish_reason or '').strip().upper()
    if reason == 'MAX_TOKENS':
        return 'length'
    if reason in ('SAFETY', 'RECITATION', 'BLOCKLIST', 'PROHIBITED_CONTENT', 'SPII'):
        return 'content_filter'
    return 'stop'



def ollama_model_default_tools_support(model: str):
    model_l = (model or '').strip().lower()
    if not model_l or any(hint in model_l for hint in OLLAMA_NON_TOOL_MODEL_HINTS):
        return False
    # Ollama Cloud exposes native tool calling for many hosted chat families.
    # Local Ollama support is model-template dependent, so keep the default
    # conservative unless the model is a known tool-capable family.
    return any(hint in model_l for hint in OLLAMA_TOOL_MODEL_HINTS)


def is_nvidia_provider(provider):
    name_l = (provider.name or '').strip().lower()
    host_l = (urllib.parse.urlparse(provider.base_url or '').hostname or '').lower()
    return any(hint in name_l for hint in ('nvidia', 'nim', 'ngc')) or 'nvidia.com' in host_l


def nvidia_model_default_tools_support(model: str):
    model_l = (model or '').strip().lower()
    if not model_l or any(hint in model_l for hint in NVIDIA_NON_TOOL_MODEL_HINTS):
        return False
    # Observed NVIDIA NIM chat models can leak OpenAI tool schemas as visible
    # assistant text when tools are present, which is especially bad in public
    # Discord channels.  Only allow NIM tool calling when a model is explicitly
    # marked with tools=true in model_meta; the default must be conservative.
    return False

def provider_default_tools_support(provider):
    if provider.api_type == 'anthropic-messages':
        return True
    if provider.api_type == 'ollama':
        return None
    if provider.api_type == 'openai-codex-responses':
        return True
    if provider.api_type == 'openclaw-gateway':
        return True
    if provider.api_type in {'google-generative-language', 'google-vertex-ai'}:
        return True
    if provider.api_type == 'openai-completions' and is_nvidia_provider(provider):
        return None
    if provider.api_type == 'openai-completions' and provider.name in {'openai', 'openai-codex', 'github-copilot'}:
        return True
    return False


def model_capabilities(provider, model):
    meta = (provider.model_meta or {}).get(model, {})
    default_chat = is_chat_capable_model(provider, model)
    default_json = provider.api_type in {'openai-completions', 'openclaw-gateway', 'anthropic-messages', 'google-generative-language', 'google-vertex-ai', 'cloudflare-workers-ai', 'openai-codex-responses'}
    provider_tools_default = provider_default_tools_support(provider)
    if provider_tools_default is None and provider.api_type == 'ollama':
        default_tools = ollama_model_default_tools_support(model)
    elif provider_tools_default is None and is_nvidia_provider(provider):
        default_tools = nvidia_model_default_tools_support(model)
    else:
        default_tools = provider_tools_default
    default_streaming = provider.api_type in {'openai-completions', 'ollama', 'google-generative-language', 'google-vertex-ai', 'openai-codex-responses'}
    return {
        'chat': bool(meta.get('supportsChat', default_chat)),
        'servable': model_is_servable(provider, model),
        'preferred': bool(meta.get('preferred', False)),
        'resident': bool(meta.get('resident', False)),
        'reasoning': provider_supports_reasoning(provider, model),
        'json': bool(meta.get('supportsJson', default_json)),
        'tools': bool(meta.get('supportsTools', default_tools)),
        'streaming': bool(meta.get('supportsStreaming', default_streaming)),
        'vision': bool(meta.get('supportsVision') or ('image' in (meta.get('input') or [])) or is_multimodal_model(model) or ('image' in model_learned_modalities(provider.name, model))),
        'audio': bool(meta.get('supportsAudio') or ('audio' in (meta.get('input') or [])) or ('audio' in model_learned_modalities(provider.name, model))),
        'video': bool(meta.get('supportsVideo') or ('video' in (meta.get('input') or [])) or ('video' in model_learned_modalities(provider.name, model))),
        # Document parsing here means extracted-text document work. Native binary PDF ingestion
        # is still handled by OpenClaw/pdf tooling before it reaches this router.
        'document': bool(meta.get('supportsDocument') or meta.get('supportsFiles') or default_chat),
        'ocr': bool(meta.get('supportsOcr') or is_ocr_model(model)),
        'longContext': model_context_window(provider, model),
        'manifestReason': meta.get('manifestReason'),
    }


def model_meets_requirements(provider, model, requirements, estimated_tokens):
    caps = model_capabilities(provider, model)
    if not caps['servable']:
        return False, 'not servable on host'
    allow_providers = requirements.get('allowProviders') or []
    deny_providers = requirements.get('denyProviders') or []
    allow_models = requirements.get('allowModels') or []
    deny_models = requirements.get('denyModels') or []
    if allow_providers and provider.name not in allow_providers:
        return False, 'provider not allowed by profile'
    if deny_providers and provider.name in deny_providers:
        return False, 'provider denied by profile'
    model_key = f'{provider.name}/{model}'
    if allow_models and not _match_model_patterns(provider.name, model, allow_models):
        return False, 'model not allowed by profile'
    if deny_models and _match_model_patterns(provider.name, model, deny_models):
        return False, 'model denied by profile'
    if requirements.get('frontierLargeOnly') and not model_is_frontier_large(model):
        return False, 'requires frontier large model'
    min_params = requirements.get('minParamsB')
    if min_params is not None:
        try:
            if estimate_model_params_b(model) < float(min_params):
                return False, f'requires >= {min_params}B params'
        except Exception:
            return False, 'invalid minParamsB profile requirement'
    if requirements.get('reasoning') and not caps['reasoning']:
        return False, 'requires reasoning'
    if requirements.get('longContext'):
        ctx = caps['longContext']
        if ctx and ctx < max(64000, estimated_tokens * 2):
            return False, f'context window too small ({ctx})'
    if requirements.get('json') and not caps['json']:
        return False, 'json unsupported'
    if requirements.get('tools') and not caps['tools']:
        return False, 'tools unsupported'
    if requirements.get('frontierOrReasoningTools') and not (model_is_frontier_large(model) or (caps['reasoning'] and caps['tools'])):
        return False, 'requires frontier large model or reasoning+tools'
    if requirements.get('vision'):
        # Route image requests strictly to genuinely image-capable models.
        # Text-only GLM models (glm-5, glm-5.2:cloud, ...) are rejected here
        # because they are not vision-capable; image-capable GLM variants
        # (e.g. glm-4v) pass this check and may serve vision requests.
        if not caps['vision']:
            return False, 'vision unsupported'
    if requirements.get('audio') and not caps.get('audio'):
        return False, 'audio input unsupported'
    if requirements.get('video') and not caps.get('video'):
        return False, 'video input unsupported'
    if requirements.get('document') and not caps['document']:
        return False, 'document parsing unsupported'
    if requirements.get('streaming') and not caps['streaming']:
        return False, 'streaming unsupported'
    return True, None


def comma_list_env(*names):
    for name in names:
        raw = os.environ.get(name, '')
        if raw.strip():
            return [x.strip() for x in raw.split(',') if x.strip()]
    return []


def env_first(*names):
    for name in names:
        value = os.environ.get(name, '')
        if value.strip():
            return value.strip()
    return ''


def atomic_write_json(path, payload, mode=0o600):
    path = os.path.expanduser(path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp_path = f'{path}.tmp-{os.getpid()}-{secrets.token_hex(4)}'
    with open(tmp_path, 'w') as f:
        json.dump(payload, f, indent=2)
        f.write('\n')
    os.chmod(tmp_path, mode)
    os.replace(tmp_path, path)


def parse_json_object(text):
    try:
        parsed = json.loads(text)
        return parsed if isinstance(parsed, dict) else {}
    except Exception:
        return {}


def sanitize_oauth_error_text(value):
    text = str(value or '')
    text = re.sub(r'\x1b\[[\x20-\x3f]*[\x40-\x7e]', '', text)
    text = re.sub(r'[\x00-\x1f\x7f-\x9f]+', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()[:300]


def oauth_headers(content_type):
    return {
        'Content-Type': content_type,
        'User-Agent': f'{OPENAI_CODEX_OAUTH_ORIGINATOR}/sage-router',
        'originator': OPENAI_CODEX_OAUTH_ORIGINATOR,
    }


def post_oauth_request(url, headers, body):
    if isinstance(body, str):
        body = body.encode()
    req = urllib.request.Request(url, data=body, headers=headers, method='POST')
    try:
        with urllib.request.urlopen(req, timeout=OPENAI_CODEX_OAUTH_HTTP_TIMEOUT_SECONDS) as resp:
            return resp.getcode(), resp.read().decode('utf-8', errors='replace')
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', errors='replace')


def parse_positive_ms(value, default_ms):
    try:
        seconds = float(value)
    except (TypeError, ValueError):
        return default_ms
    if not math.isfinite(seconds) or seconds <= 0:
        return default_ms
    return max(OPENAI_CODEX_OAUTH_MIN_INTERVAL_MS, int(seconds * 1000))


def jwt_payload(token):
    if not isinstance(token, str) or token.count('.') < 2:
        return {}
    try:
        payload = token.split('.')[1]
        payload += '=' * (-len(payload) % 4)
        decoded = base64.urlsafe_b64decode(payload.encode())
        data = json.loads(decoded.decode('utf-8'))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def resolve_oauth_expires_at_ms(access_token='', expires_in=None):
    try:
        seconds = float(expires_in)
        if math.isfinite(seconds) and seconds > 0:
            return int(time.time() * 1000 + seconds * 1000)
    except (TypeError, ValueError):
        pass
    exp = jwt_payload(access_token).get('exp')
    try:
        exp_f = float(exp)
        if math.isfinite(exp_f) and exp_f > 0:
            return int(exp_f * 1000)
    except (TypeError, ValueError):
        pass
    return int(time.time() * 1000)


def resolve_oauth_account_id(access_token):
    payload = jwt_payload(access_token)
    for key in ('https://api.openai.com/auth/account_id', 'account_id', 'accountId', 'sub'):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ''


def codex_credentials_from_auth_data(data):
    if not isinstance(data, dict):
        return {}
    profiles = data.get('profiles')
    if isinstance(profiles, dict):
        for prof in profiles.values():
            if not isinstance(prof, dict):
                continue
            prof_provider = prof.get('provider')
            if prof_provider not in {'openai', 'openai-codex'}:
                continue
            if prof_provider == 'openai' and prof.get('type') != 'oauth':
                continue
            access = prof.get('access') or prof.get('access_token') or prof.get('apiKey') or ''
            refresh = prof.get('refresh') or prof.get('refresh_token') or ''
            if access or refresh:
                return {'access': access, 'refresh': refresh, 'expires': prof.get('expires') or prof.get('expires_at')}
    tokens = data.get('tokens')
    if isinstance(tokens, dict):
        access = tokens.get('access_token') or tokens.get('access') or ''
        refresh = tokens.get('refresh_token') or tokens.get('refresh') or ''
        if access or refresh:
            return {'access': access, 'refresh': refresh, 'expires': tokens.get('expires_at') or tokens.get('expires')}
    access = data.get('access_token') or data.get('access') or ''
    refresh = data.get('refresh_token') or data.get('refresh') or ''
    if access or refresh:
        return {'access': access, 'refresh': refresh, 'expires': data.get('expires_at') or data.get('expires')}
    return {}


def codex_auth_needs_refresh(expires):
    if not expires:
        return False
    try:
        expires_f = float(expires)
    except (TypeError, ValueError):
        return False
    if expires_f < 10_000_000_000:
        expires_f *= 1000
    return expires_f <= time.time() * 1000 + OPENAI_CODEX_OAUTH_REFRESH_SKEW_MS


def codex_auth_json_payload(tokens):
    payload = {
        'auth_mode': 'chatgpt',
        'tokens': {
            'access_token': tokens['access'],
            'refresh_token': tokens['refresh'],
            'expires_at': tokens['expires'],
        },
        'last_refresh': int(time.time() * 1000),
    }
    account_id = tokens.get('accountId') or resolve_oauth_account_id(tokens.get('access', ''))
    if account_id:
        payload['tokens']['account_id'] = account_id
    if tokens.get('id_token'):
        payload['tokens']['id_token'] = tokens['id_token']
    return payload


def codex_auth_profile_payload(tokens):
    account_id = tokens.get('accountId') or resolve_oauth_account_id(tokens.get('access', ''))
    profile = {
        'provider': 'openai',
        'type': 'oauth',
        'access': tokens['access'],
        'refresh': tokens['refresh'],
        'expires': tokens['expires'],
    }
    if account_id:
        profile['accountId'] = account_id
    return {'profiles': {'sage-router-codex': profile}}


def save_openai_codex_oauth_tokens(tokens):
    if not tokens.get('access') or not tokens.get('refresh'):
        raise ValueError('codex_tokens_missing')
    atomic_write_json(APP_CODEX_AUTH_JSON, codex_auth_json_payload(tokens))
    atomic_write_json(APP_CODEX_AUTH_PROFILE, codex_auth_profile_payload(tokens))
    reload_configured_providers()
    return {
        'status': 'saved',
        'target': APP_CODEX_AUTH_JSON,
        'codexConfigured': True,
        'configured': sorted(PROVIDERS.keys()),
    }


def refresh_openai_codex_oauth_token(refresh_token):
    body = urllib.parse.urlencode({
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': OPENAI_CODEX_OAUTH_CLIENT_ID,
    })
    status, text = post_oauth_request(
        f'{OPENAI_CODEX_OAUTH_AUTH_BASE_URL}/oauth/token',
        oauth_headers('application/x-www-form-urlencoded'),
        body,
    )
    data = parse_json_object(text)
    if status < 200 or status >= 300:
        error = data.get('error_description') or data.get('error') or text
        raise ValueError(f'codex_token_refresh_failed: {sanitize_oauth_error_text(error)}')
    access = str(data.get('access_token') or '').strip()
    refresh = str(data.get('refresh_token') or refresh_token or '').strip()
    if not access or not refresh:
        raise ValueError('codex_token_refresh_missing_fields')
    return {
        'access': access,
        'refresh': refresh,
        'expires': resolve_oauth_expires_at_ms(access, data.get('expires_in')),
        'accountId': resolve_oauth_account_id(access),
        'id_token': data.get('id_token') if isinstance(data.get('id_token'), str) else '',
    }


def refresh_app_owned_codex_auth_if_needed(path, data):
    path = os.path.expanduser(path)
    app_paths = {os.path.expanduser(APP_CODEX_AUTH_JSON), os.path.expanduser(APP_CODEX_AUTH_PROFILE)}
    if path not in app_paths:
        return data
    creds = codex_credentials_from_auth_data(data)
    refresh = str(creds.get('refresh') or '').strip()
    if not refresh or not codex_auth_needs_refresh(creds.get('expires')):
        return data
    with OPENAI_CODEX_OAUTH_LOCK:
        tokens = refresh_openai_codex_oauth_token(refresh)
        save_openai_codex_oauth_tokens(tokens)
        return codex_auth_json_payload(tokens) if path.endswith('auth.json') else codex_auth_profile_payload(tokens)


def openai_codex_auth_candidate_paths():
    env_paths = comma_list_env(
        'SAGE_ROUTER_OPENAI_CODEX_AUTH_PROFILE_PATHS',
        'OPENAI_CODEX_AUTH_PROFILE_PATHS',
    )
    if not env_paths:
        env_paths = [env_first('SAGE_ROUTER_OPENAI_CODEX_AUTH_PROFILE_PATH', 'OPENAI_CODEX_AUTH_PROFILE_PATH')]
    defaults = [
        APP_CODEX_AUTH_PROFILE,
        os.path.join(SAGE_ROUTER_HOME, 'openclaw', 'agents', 'main', 'agent', 'auth-profiles.json'),
        APP_CODEX_AUTH_JSON,
        os.path.join(SAGE_ROUTER_HOME, 'codex', 'auth.json'),
        os.path.join(SAGE_ROUTER_HOME, 'openai-codex', 'auth.json'),
        '~/.openclaw/agents/main/agent/auth-profiles.json',
        '~/.hermes/auth.json',
    ]
    return dedupe_keep_order([os.path.expanduser(p) for p in env_paths + defaults if p])


def token_not_expired(expires, now_ms):
    if not expires:
        return True
    try:
        expires_f = float(expires)
    except (TypeError, ValueError):
        return True
    if expires_f < 10_000_000_000:
        expires_f *= 1000
    return expires_f > now_ms


def extract_openai_codex_token_from_auth_data(data, provider_name='openai-codex'):
    if not isinstance(data, dict):
        return ''
    now_ms = time.time() * 1000
    profiles = data.get('profiles')
    if isinstance(profiles, dict):
        for prof in profiles.values():
            if not isinstance(prof, dict):
                continue
            prof_provider = prof.get('provider')
            provider_matches = prof_provider == provider_name
            if provider_name == 'openai-codex':
                provider_matches = provider_matches or (prof_provider == 'openai' and prof.get('type') == 'oauth')
            if provider_matches and token_not_expired(prof.get('expires'), now_ms):
                token = prof.get('access') or prof.get('access_token') or prof.get('apiKey') or ''
                if token:
                    return token
    providers = data.get('providers')
    if isinstance(providers, dict):
        for name, prof in providers.items():
            if not isinstance(prof, dict):
                continue
            name_l = str(name).lower()
            if provider_name != 'openai-codex' and provider_name not in name_l:
                continue
            if provider_name == 'openai-codex' and 'codex' not in name_l and 'openai' not in name_l:
                continue
            if token_not_expired(prof.get('expires') or prof.get('expires_at'), now_ms):
                token = prof.get('access') or prof.get('access_token') or prof.get('token') or ''
                if token:
                    return token
    tokens = data.get('tokens')
    if isinstance(tokens, dict):
        token = tokens.get('access_token') or tokens.get('access') or ''
        if token and token_not_expired(tokens.get('expires_at') or tokens.get('expires'), now_ms):
            return token
    token = data.get('access_token') or data.get('access') or ''
    if token and token_not_expired(data.get('expires_at') or data.get('expires'), now_ms):
        return token
    return ''


def model_meta_for_defaults(models, base_meta):
    return {m: dict(base_meta) for m in dedupe_keep_order(models or [])}


def load_openclaw_oauth_credentials(provider_name):
    """Return ordered OAuth credential dicts for a provider from auth-profiles.

    Used to fold existing multi-account OAuth subscription paths (e.g. multiple
    ChatGPT/Codex accounts) into a provider's credential pool so they are
    usable with credential failover and visible in the dashboard.
    """
    auth_path = os.path.expanduser('~/.openclaw/agents/main/agent/auth-profiles.json')
    try:
        with open(auth_path) as af:
            auth = json.load(af)
    except Exception:
        return []
    profiles = auth.get('profiles', {}) if isinstance(auth, dict) else {}
    if not isinstance(profiles, dict):
        return []
    now_ms = time.time() * 1000
    creds = []
    for name, profile in profiles.items():
        if not isinstance(profile, dict) or profile.get('type') != 'oauth':
            continue
        prof_provider = profile.get('provider')
        match = prof_provider == provider_name or (
            provider_name == 'openai-codex' and prof_provider == 'openai'
        )
        if not match:
            continue
        access = profile.get('access') or profile.get('access_token') or ''
        if not access:
            continue
        expires = profile.get('expires')
        if isinstance(expires, (int, float)) and expires <= now_ms:
            # Keep expired OAuth paths in the pool; the refresh layer can
            # renew them and failover covers the gap.
            pass
        label = name
        if '@' in name:
            label = '<email-profile>'
        creds.append({
            'type': 'oauth',
            'label': label or prof_provider,
            'accessToken': access,
            'refreshToken': profile.get('refresh') or profile.get('refresh_token') or '',
            'expires': int(expires or 0),
            'profile': name,
        })
    return dedupe_credentials(creds)


def load_openclaw_auth_access_token(provider_name):
    """Return the current non-expired OpenClaw auth token for a provider.

    For openai-codex, also searches openai OAuth profiles since ChatGPT/Codex
    uses the same OpenAI OAuth token (auth-profiles stores them under provider=openai).
    """
    auth_path = os.path.expanduser('~/.openclaw/agents/main/agent/auth-profiles.json')
    state_path = os.path.expanduser('~/.openclaw/agents/main/agent/auth-state.json')
    if provider_name == 'openai-codex':
        for candidate in openai_codex_auth_candidate_paths():
            try:
                with open(candidate) as cf:
                    data = refresh_app_owned_codex_auth_if_needed(candidate, json.load(cf))
                    token = extract_openai_codex_token_from_auth_data(data, provider_name)
                if token:
                    logger.info(f'Loaded openai-codex OAuth token from configured auth path {candidate}')
                    return token
            except Exception:
                continue
    try:
        with open(auth_path) as af:
            auth = json.load(af)
    except Exception:
        return ''

    profiles = auth.get('profiles', {}) if isinstance(auth, dict) else {}
    if not isinstance(profiles, dict):
        return ''

    state = {}
    try:
        with open(state_path) as sf:
            state = json.load(sf)
    except Exception:
        state = {}

    candidate_names = []
    last_good = (state.get('lastGood') or {}).get(provider_name) if isinstance(state, dict) else None
    if last_good:
        candidate_names.append(last_good)
    ordered = (state.get('order') or {}).get(provider_name, []) if isinstance(state, dict) else []
    if isinstance(ordered, list):
        candidate_names.extend(name for name in ordered if isinstance(name, str))
    candidate_names.extend(
        name for name, profile in profiles.items()
        if isinstance(profile, dict) and profile.get('provider') == provider_name
    )
    # openai-codex shares OAuth tokens with openai (ChatGPT) profiles.
    # auth-profiles.json stores them under provider=openai with type=oauth
    # and fields like chatgptPlanType/accountId that indicate ChatGPT/Codex access.
    if provider_name == 'openai-codex':
        candidate_names.extend(
            name for name, profile in profiles.items()
            if isinstance(profile, dict)
            and profile.get('provider') == 'openai'
            and profile.get('type') == 'oauth'
        )

    now_ms = time.time() * 1000
    for name in dedupe_keep_order(candidate_names):
        profile = profiles.get(name)
        if not isinstance(profile, dict):
            continue
        prof_provider = profile.get('provider')
        if prof_provider != provider_name:
            # For openai-codex, also accept provider=openai OAuth profiles
            if provider_name == 'openai-codex' and prof_provider == 'openai' and profile.get('type') == 'oauth':
                pass
            else:
                continue
        expires = profile.get('expires')
        if isinstance(expires, (int, float)) and expires <= now_ms:
            continue
        token = profile.get('access') or profile.get('access_token') or profile.get('apiKey') or ''
        if token:
            # Avoid logging email-bearing profile names (PII).
            safe_label = '<email-profile>' if '@' in name else name
            logger.info(f'Loaded OpenClaw auth token for {provider_name} from {safe_label}')
            return token
    return ''



def read_openai_codex_oauth_token_from_file():
    """Best-effort local/mounted OAuth token discovery for OpenClaw/Hermes style auth.

    Hosted Cloud Run should prefer SAGE_ROUTER_OPENAI_CODEX_ACCESS_TOKEN from
    Secret Manager. This fallback keeps parity with local OpenClaw/Hermes-style
    auth if an auth profile file is deliberately mounted into the runtime.

    For openai-codex, also searches openai OAuth profiles since ChatGPT/Codex
    uses the same OpenAI OAuth token (auth-profiles stores them under provider=openai).
    """
    openclaw_token = load_openclaw_auth_access_token('openai-codex')
    if openclaw_token:
        return openclaw_token
    for raw_path in openai_codex_auth_candidate_paths():
        path = os.path.expanduser(raw_path)
        try:
            with open(path) as f:
                data = refresh_app_owned_codex_auth_if_needed(path, json.load(f))
        except Exception:
            continue
        token = extract_openai_codex_token_from_auth_data(data, 'openai-codex')
        if token:
            logger.info(f'Loaded openai-codex OAuth token from app-owned auth file {path}')
            return token
    return ''

def load_hosted_secret_providers():
    """Load Cloud Run/hosted provider credentials from environment/Secret Manager.

    This lets Sage Router act as the security and billing boundary: clients pass
    a Sage Router subscription key, while upstream provider tokens stay server-side.
    All values are env-var backed so secrets can be wired through Cloud Run Secret
    Manager without committing provider tokens to config.
    """
    providers = {}

    def add(name, api_type, base_url, api_key, models, meta, reasoning_models=None):
        # openai-codex may ride the openclaw-gateway bridge with an empty
        # router-side key (the gateway supplies its own credential), so
        # let that one case through the early-return.
        if not api_key and not (name == 'openai-codex' and api_type == 'openclaw-gateway'):
            if name not in {'google-vertex'}:
                return
        if name in DISABLED_PROVIDERS:
            logger.info(f'Skipping disabled hosted provider {name}')
            return
        models = dedupe_keep_order(models or [])
        merge_provider(providers, Provider(
            name,
            api_type,
            base_url,
            api_key,
            models,
            set(reasoning_models or [m for m in models if meta.get('reasoning')]),
            model_meta_for_defaults(models, meta),
        ))

    add(
        'openai',
        'openai-completions',
        env_first('SAGE_ROUTER_OPENAI_BASE_URL', 'OPENAI_BASE_URL') or 'https://api.openai.com/v1',
        env_first('SAGE_ROUTER_OPENAI_API_KEY', 'OPENAI_API_KEY'),
        comma_list_env('SAGE_ROUTER_OPENAI_MODELS') or DEFAULT_OPENAI_MODELS,
        {'reasoning': False, 'contextWindow': 128000, 'maxTokens': 16384, 'input': ['text'], 'supportsTools': True, 'supportsJson': True},
    )
    add(
        'openrouter',
        'openai-completions',
        env_first('SAGE_ROUTER_OPENROUTER_BASE_URL', 'OPENROUTER_BASE_URL') or 'https://openrouter.ai/api/v1',
        env_first('SAGE_ROUTER_OPENROUTER_API_KEY', 'OPENROUTER_API_KEY'),
        comma_list_env('SAGE_ROUTER_OPENROUTER_MODELS') or DEFAULT_OPENROUTER_MODELS,
        {'reasoning': True, 'contextWindow': 200000, 'maxTokens': 64000, 'input': ['text'], 'supportsTools': True, 'supportsJson': True},
    )
    add(
        'anthropic',
        'anthropic-messages',
        env_first('SAGE_ROUTER_ANTHROPIC_BASE_URL', 'ANTHROPIC_BASE_URL') or 'https://api.anthropic.com',
        env_first('SAGE_ROUTER_ANTHROPIC_API_KEY', 'ANTHROPIC_API_KEY'),
        comma_list_env('SAGE_ROUTER_ANTHROPIC_MODELS') or DEFAULT_ANTHROPIC_MODELS,
        {'reasoning': True, 'contextWindow': 1000000, 'maxTokens': 64000, 'input': ['text'], 'supportsTools': True, 'supportsJson': True},
    )
    add(
        'google',
        'google-generative-language',
        env_first('SAGE_ROUTER_GOOGLE_BASE_URL', 'GOOGLE_GENERATIVE_LANGUAGE_BASE_URL') or 'https://generativelanguage.googleapis.com/v1beta',
        env_first('SAGE_ROUTER_GOOGLE_API_KEY', 'GOOGLE_API_KEY', 'GEMINI_API_KEY'),
        comma_list_env('SAGE_ROUTER_GOOGLE_MODELS') or DEFAULT_GOOGLE_MODELS,
        {'reasoning': True, 'contextWindow': 1000000, 'maxTokens': 65536, 'input': ['text', 'image'], 'supportsVision': True, 'supportsJson': True},
    )
    if env_first('SAGE_ROUTER_GOOGLE_APPLICATION_CREDENTIALS', 'GOOGLE_APPLICATION_CREDENTIALS', 'SAGE_ROUTER_VERTEX_ENABLED'):
        project = env_first('SAGE_ROUTER_VERTEX_PROJECT_ID', 'GOOGLE_CLOUD_PROJECT', 'GCP_PROJECT')
        location = env_first('SAGE_ROUTER_VERTEX_LOCATION', 'GOOGLE_CLOUD_LOCATION', 'GOOGLE_CLOUD_REGION') or 'us-central1'
        base = env_first('SAGE_ROUTER_VERTEX_BASE_URL')
        if not base and project:
            base = f'https://{location}-aiplatform.googleapis.com/v1/projects/{project}/locations/{location}/publishers/google'
        add(
            'google-vertex',
            'google-vertex-ai',
            base,
            'adc',
            comma_list_env('SAGE_ROUTER_VERTEX_MODELS') or DEFAULT_GOOGLE_MODELS,
            {'reasoning': True, 'contextWindow': 1000000, 'maxTokens': 65536, 'input': ['text', 'image'], 'supportsVision': True, 'supportsJson': True},
        )
    add(
        'xai',
        'openai-completions',
        env_first('SAGE_ROUTER_XAI_BASE_URL', 'XAI_BASE_URL') or 'https://api.x.ai/v1',
        env_first('SAGE_ROUTER_XAI_API_KEY', 'XAI_API_KEY'),
        comma_list_env('SAGE_ROUTER_XAI_MODELS') or DEFAULT_XAI_MODELS,
        {'reasoning': True, 'contextWindow': 128000, 'maxTokens': 16384, 'input': ['text'], 'supportsTools': True, 'supportsJson': True},
    )
    add(
        'zai',
        'openai-completions',
        env_first('SAGE_ROUTER_ZAI_BASE_URL', 'ZAI_BASE_URL') or 'https://api.z.ai/api/paas/v4',
        env_first('SAGE_ROUTER_ZAI_API_KEY', 'ZAI_API_KEY'),
        comma_list_env('SAGE_ROUTER_ZAI_MODELS') or DEFAULT_ZAI_MODELS,
        {'reasoning': True, 'contextWindow': 256000, 'maxTokens': 65536, 'input': ['text'], 'supportsTools': True, 'supportsJson': True},
    )
    add(
        'ollama-cloud',
        'ollama',
        env_first('SAGE_ROUTER_OLLAMA_BASE_URL', 'OLLAMA_HOST') or 'https://ollama.com',
        env_first('SAGE_ROUTER_OLLAMA_API_KEY', 'OLLAMA_API_KEY'),
        comma_list_env('SAGE_ROUTER_OLLAMA_MODELS') or ollama_cloud_catalog_models()[:25],
        {'reasoning': True, 'contextWindow': 256000, 'maxTokens': 128000, 'input': ['text'], 'supportsTools': True, 'supportsJson': True},
    )
    cf_account = env_first('SAGE_ROUTER_CLOUDFLARE_ACCOUNT_ID', 'CLOUDFLARE_ACCOUNT_ID')

    add(
        'nvidia-nim',
        'openai-completions',
        env_first('SAGE_ROUTER_NVIDIA_BASE_URL', 'NVIDIA_BASE_URL') or 'https://integrate.api.nvidia.com/v1',
        env_first('SAGE_ROUTER_NVIDIA_API_KEY', 'NVIDIA_API_KEY', 'NVIDIA_NIM_API_KEY'),
        comma_list_env('SAGE_ROUTER_NVIDIA_MODELS') or DEFAULT_NGC_MODELS,
        {'reasoning': False, 'contextWindow': 16384, 'maxTokens': 4096, 'input': ['text'], 'supportsTools': False, 'supportsJson': True},
    )

    cf_base = env_first('SAGE_ROUTER_CLOUDFLARE_BASE_URL') or (f'https://api.cloudflare.com/client/v4/accounts/{cf_account}/ai' if cf_account else '')
    if cf_base:
        add(
            'cloudflare-workers-ai',
            'cloudflare-workers-ai',
            cf_base,
            env_first('SAGE_ROUTER_CLOUDFLARE_API_TOKEN', 'CLOUDFLARE_API_TOKEN'),
            comma_list_env('SAGE_ROUTER_CLOUDFLARE_MODELS') or DEFAULT_CLOUDFLARE_WORKERS_AI_MODELS,
            {'reasoning': False, 'contextWindow': 32768, 'maxTokens': 4096, 'input': ['text'], 'supportsJson': True},
        )
    codex_models = comma_list_env('SAGE_ROUTER_OPENAI_CODEX_MODELS') or DEFAULT_OPENAI_CODEX_MODELS
    # OpenClaw Codex OAuth: openai-codex is now provider=openai, type=oauth in auth-profiles.
    # Direct calls to chatgpt.com/backend-api/codex with the OAuth token — no gateway needed.
    codex_base_url = env_first('SAGE_ROUTER_OPENAI_CODEX_BASE_URL', 'OPENAI_CODEX_BASE_URL') or 'https://chatgpt.com/backend-api/codex'
    codex_api_key = env_first(
        'SAGE_ROUTER_OPENAI_CODEX_ACCESS_TOKEN',
        'SAGE_ROUTER_OPENAI_CODEX_OAUTH_TOKEN',
        'OPENAI_CODEX_API_KEY',
        'OPENAI_CODEX_ACCESS_TOKEN',
        'OPENAI_CODEX_OAUTH_TOKEN',
        'CODEX_ACCESS_TOKEN',
    ) or read_openai_codex_oauth_token_from_file()
    if codex_api_key:
        # Direct OAuth: send the token as Bearer to chatgpt.com/backend-api/codex.
        add(
            'openai-codex',
            'openai-codex-responses',
            codex_base_url,
            codex_api_key,
            codex_models,
            {'reasoning': True, 'contextWindow': 256000, 'maxTokens': 128000, 'input': ['text'], 'supportsTools': True, 'supportsJson': True},
            reasoning_models=codex_models,
        )
    elif OPENAI_CODEX_GATEWAY_FALLBACK:
        # No OAuth token in this environment. Fall back to the OpenClaw gateway
        # bridge so that the model list still resolves. load_openclaw_providers
        # will overwrite this entry with a real direct-Codex provider as soon
        # as an auth profile is mounted.
        add(
            'openai-codex',
            'openclaw-gateway',
            OPENCLAW_GATEWAY_BASE_URL,
            '',
            codex_models,
            {'reasoning': True, 'contextWindow': 256000, 'maxTokens': 128000, 'input': ['text']},
            reasoning_models=codex_models,
        )
    else:
        logger.info('Skipping openai-codex gateway fallback because SAGE_ROUTER_OPENAI_CODEX_GATEWAY_FALLBACK is off')
    return providers


def merge_harness_discovered_providers(providers):
    harness_discovery_requested = any(
        os.environ.get(key)
        for key in ('SAGE_ROUTER_CONFIG_SOURCE', 'APP_DATA_DIR', 'OPENCLAW_CONFIG', 'HERMES_CONFIG', 'PI_CONFIG', 'CODEX_CONFIG')
    )
    if not harness_discovery_requested:
        return

    try:
        from harness_discovery import load_harness_agnostic_providers
    except Exception as e:
        logger.debug(f'Harness discovery unavailable: {e}')
        return

    try:
        discovered = load_harness_agnostic_providers(
            sage_router_home=SAGE_ROUTER_HOME,
            app_data_dir=os.environ.get('APP_DATA_DIR') or SAGE_ROUTER_HOME,
        )
    except Exception as e:
        logger.debug(f'Harness discovery failed: {e}')
        return

    for name, cfg in discovered.items():
        if name in DISABLED_PROVIDERS:
            logger.info(f'Skipping disabled harness provider {name}')
            continue
        base_url = resolve_config_value(cfg.get('base_url') or cfg.get('baseUrl') or '')
        if is_self_provider(name, base_url):
            continue
        api_key = resolve_config_value(
            cfg.get('api_key') or cfg.get('apiKey') or cfg.get('oauth_access_token') or ''
        )
        router_cfg = {
            'baseUrl': base_url,
            'apiKey': api_key,
            'api': cfg.get('api_type') or cfg.get('api') or '',
            'models': cfg.get('models') or [],
        }
        api_type = infer_api_type(name, router_cfg, base_url)
        models = discover_provider_models(name, router_cfg, base_url, api_key, api_type) or router_cfg['models']
        reasoning_models = discover_reasoning_models(router_cfg)
        model_meta = discover_model_meta(router_cfg)

        if should_route_anthropic_to_dario(name, api_type, base_url):
            ensure_dario_proxy_ready()
            merge_provider(providers, Provider(
                DARIO_PROVIDER_NAME,
                'anthropic-messages',
                DARIO_LOCAL_BASE_URL,
                DARIO_LOCAL_API_KEY,
                dedupe_keep_order(models or DEFAULT_ANTHROPIC_MODELS),
                set(models or DEFAULT_ANTHROPIC_MODELS),
                {m: {'reasoning': True, 'contextWindow': 1000000, 'maxTokens': 64000, 'input': ['text']} for m in dedupe_keep_order(models or DEFAULT_ANTHROPIC_MODELS)},
            ))
            logger.info(f'Normalized harness provider {name} -> {DARIO_PROVIDER_NAME} via local Dario proxy')
            continue

        if name == 'openai-codex' and api_type == 'openai-codex-responses':
            api_key = load_openclaw_auth_access_token('openai-codex') or api_key

        merge_provider(providers, Provider(
            name,
            api_type,
            base_url,
            api_key,
            models,
            reasoning_models,
            model_meta,
        ))
        logger.info(f"Loaded harness provider {name} from {cfg.get('harness', 'unknown')}:{cfg.get('source_path', '')}")


def _load_app_provider_config_safe():
    try:
        if os.path.exists(APP_PROVIDER_CONFIG):
            with open(APP_PROVIDER_CONFIG) as f:
                return json.load(f) or {}
    except Exception:
        pass
    return {}


def _normalize_config_list(value):
    if isinstance(value, list):
        return dedupe_keep_order([str(v).strip() for v in value if str(v).strip()])
    if isinstance(value, str):
        return parse_model_list(value)
    return []


def _apply_dashboard_disabled_sets(config):
    global DISABLED_PROVIDERS, DISABLED_MODELS
    if not isinstance(config, dict):
        config = {}
    disabled_providers = set(_normalize_config_list(config.get('disabledProviders')))
    disabled_models = set(_normalize_config_list(config.get('disabledModels')))
    DISABLED_PROVIDERS = set(ENV_DISABLED_PROVIDERS) | disabled_providers
    DISABLED_MODELS = set(ENV_DISABLED_MODELS) | disabled_models


def _merge_app_provider_config(config):
    """Merge the dashboard-managed provider config (APP_PROVIDER_CONFIG) into
    the loaded OpenClaw config so dashboard-configured providers and their
    multi-credential pools (apiKeys/oauthPaths) are authoritative."""
    try:
        if not APP_PROVIDER_CONFIG or APP_PROVIDER_CONFIG == OPENCLAW_CONFIG:
            return config
        if not os.path.exists(APP_PROVIDER_CONFIG):
            return config
        with open(APP_PROVIDER_CONFIG) as f:
            app_cfg = json.load(f)
    except Exception as e:
        logger.debug(f'APP_PROVIDER_CONFIG merge skipped: {e}')
        _apply_dashboard_disabled_sets({})
        return config
    if not isinstance(app_cfg, dict):
        _apply_dashboard_disabled_sets({})
        return config
    _apply_dashboard_disabled_sets(app_cfg)
    config.setdefault('models', {}).setdefault('providers', {})
    app_providers = (app_cfg.get('models') or {}).get('providers', {}) or {}
    for name, cfg in app_providers.items():
        if isinstance(cfg, dict):
            existing = config['models']['providers'].get(name) or {}
            if isinstance(existing, dict):
                merged = dict(existing)
                merged.update(cfg)
                config['models']['providers'][name] = merged
            else:
                config['models']['providers'][name] = cfg
    return config


def load_openclaw_providers():
    _apply_dashboard_disabled_sets(_load_app_provider_config_safe())
    providers = load_hosted_secret_providers()
    merge_harness_discovered_providers(providers)
    try:
        with open(OPENCLAW_CONFIG) as f:
            config = json.load(f)
        config = _merge_app_provider_config(config)
        for name, cfg in config.get('models', {}).get('providers', {}).items():
            base_url = resolve_config_value(cfg.get('baseUrl', '') or '')
            if is_self_provider(name, base_url):
                continue
            if name in DISABLED_PROVIDERS:
                logger.info(f'Skipping disabled provider {name} during discovery')
                continue
            api_key = resolve_config_value(cfg.get('apiKey', '') or '')
            api_type = infer_api_type(name, cfg, base_url)
            models = discover_provider_models(name, cfg, base_url, api_key, api_type)
            reasoning_models = discover_reasoning_models(cfg)
            model_meta = discover_model_meta(cfg)
            if api_type == 'ollama':
                cloud_models = [m for m in (models or []) if is_cloud_ollama_model(m)]
                if cloud_models:
                    model_meta = {**{m: ollama_cloud_model_meta(m) for m in cloud_models}, **(model_meta or {})}
                    reasoning_models = set(reasoning_models or set()) | {m for m in cloud_models if model_meta.get(m, {}).get('reasoning')}

            if should_route_anthropic_to_dario(name, api_type, base_url):
                ensure_dario_proxy_ready()
                merge_provider(providers, Provider(
                    DARIO_PROVIDER_NAME,
                    'anthropic-messages',
                    DARIO_LOCAL_BASE_URL,
                    DARIO_LOCAL_API_KEY,
                    dedupe_keep_order(models or DEFAULT_ANTHROPIC_MODELS),
                    set(models or DEFAULT_ANTHROPIC_MODELS),
                    {m: {'reasoning': True, 'contextWindow': 1000000, 'maxTokens': 64000, 'input': ['text']} for m in dedupe_keep_order(models or DEFAULT_ANTHROPIC_MODELS)},
                ))
                logger.info(f'Normalized provider {name} -> {DARIO_PROVIDER_NAME} via local Dario proxy')
                continue

            # Prefer OpenClaw's current auth profile over stale OPENAI_CODEX_API_KEY env values.
            if name == 'openai-codex' and api_type == 'openai-codex-responses':
                api_key = load_openclaw_auth_access_token('openai-codex') or api_key

            # Build the ordered multi-credential pool (apiKeys + oauthPaths +
            # legacy single apiKey) and keep `api_key` as the first resolved
            # secret so discovery, streaming, and legacy callers still work.
            cred_pool = build_provider_credentials(cfg, api_key)
            if name == 'openai-codex' and api_type == 'openai-codex-responses':
                # Fold in OAuth subscription paths discovered from auth-profiles
                # so Codex OAuth accounts are usable alongside API keys.
                for cred in list(load_openclaw_oauth_credentials('openai-codex')):
                    cred_pool.append(cred)
                cred_pool = dedupe_credentials(cred_pool)
            if not api_key and cred_pool:
                api_key = resolve_credential_key(cred_pool[0])
            cred_strategy = str(cfg.get('credentialStrategy') or cfg.get('credential_strategy') or '').strip().lower()

            # Add multimodal metadata for GPT-5.4/5.5 which support vision
            multimodal_models = {'gpt-5.5', 'gpt-5.4', 'gpt-5.4-pro', 'gpt-5.4-mini'}
            extra_meta = {m: {'input': ['text', 'image'], 'supportsVision': True} for m in multimodal_models if m in (models or [])}
            if extra_meta:
                model_meta = {**(model_meta or {}), **extra_meta}

            merge_provider(providers, Provider(
                name,
                api_type,
                base_url,
                api_key,
                models,
                reasoning_models,
                model_meta,
                cred_pool,
                cred_strategy,
            ))

        auth_profiles = config.get('auth', {}).get('profiles', {})
        agent_defaults = config.get('agents', {}).get('defaults', {})        
        # Auto-discover gateway-backed providers from auth profiles
        # For each auth profile that matches a known gateway provider, create a provider
        for profile_name, profile in auth_profiles.items():
            if not isinstance(profile, dict):
                continue
            provider_name = profile.get('provider', profile_name.split(':')[0])
            if provider_name in DISABLED_PROVIDERS:
                logger.info(f'Skipping disabled gateway provider {provider_name} during discovery')
                continue
            # Skip if already configured as a regular provider (e.g. ollama, anthropic via Dario)
            if provider_name in providers and provider_name not in GATEWAY_PROVIDER_PROFILES:
                continue
            # Skip ollama - it's always direct, not gateway-backed
            if provider_name == 'ollama':
                continue
            gw_spec = GATEWAY_PROVIDER_PROFILES.get(provider_name)
            if not gw_spec:
                continue
            api_type, default_models, default_meta = gw_spec
            # Don't add if already exists (e.g. anthropic already routed via Dario)
            if provider_name in providers:
                continue
            # Determine models and base URL based on provider type
            gw_models = list(default_models)
            if api_type == 'anthropic-messages':
                # Anthropic - route via Dario
                ensure_dario_proxy_ready()
                gw_models = discover_anthropic_models() or default_models
                merge_provider(providers, Provider(
                    provider_name,
                    'anthropic-messages',
                    DARIO_LOCAL_BASE_URL,
                    DARIO_LOCAL_API_KEY,
                    dedupe_keep_order(gw_models),
                    set(gw_models),
                    {m: dict(default_meta) for m in gw_models},
                ))
                logger.info(f'Auto-created gateway provider {provider_name} (anthropic-messages) with {len(gw_models)} models via Dario')
            elif api_type == 'google-generative-language':
                # Google - direct API if key available, otherwise gateway
                api_key = resolve_config_value(config.get('auth', {}).get('profiles', {}).get(f'{provider_name}:default', {}).get('apiKey', ''))
                if not api_key:
                    # Use gateway as fallback
                    merge_provider(providers, Provider(
                        provider_name,
                        'openclaw-gateway',
                        OPENCLAW_GATEWAY_BASE_URL,
                        '',
                        dedupe_keep_order(gw_models),
                        set(gw_models),
                        {m: dict(default_meta) for m in gw_models},
                    ))
                    logger.info(f'Auto-created gateway provider {provider_name} (google via gateway) with {len(gw_models)} models')
                # If key exists, it would have been loaded as a regular provider
            elif api_type == 'openai-codex-responses':
                # openai-codex: direct responses via chatgpt.com/backend-api/codex with OAuth
                codex_gw_token = load_openclaw_auth_access_token('openai-codex')
                if codex_gw_token:
                    merge_provider(providers, Provider(
                        provider_name,
                        'openai-codex-responses',
                        env_first('SAGE_ROUTER_OPENAI_CODEX_BASE_URL', 'OPENAI_CODEX_BASE_URL') or 'https://chatgpt.com/backend-api/codex',
                        codex_gw_token,
                        dedupe_keep_order(gw_models),
                        set(gw_models),
                        {m: dict(default_meta) for m in gw_models},
                    ))
                    logger.info(f'Auto-created gateway provider {provider_name} (openai-codex-responses) with {len(gw_models)} models')
                elif OPENAI_CODEX_GATEWAY_FALLBACK:
                    # No OAuth token available; fall back to openclaw-gateway bridge
                    merge_provider(providers, Provider(
                        provider_name,
                        'openclaw-gateway',
                        OPENCLAW_GATEWAY_BASE_URL,
                        '',
                        dedupe_keep_order(gw_models),
                        set(gw_models),
                        {m: dict(default_meta) for m in gw_models},
                    ))
                    logger.info(f'Auto-created gateway provider {provider_name} (openclaw-gateway fallback) with {len(gw_models)} models')
                else:
                    logger.info(f'Skipping gateway fallback for {provider_name}; OAuth token not configured')
            else:
                # Other providers (xai, zai, openai) - route via gateway
                merge_provider(providers, Provider(
                    provider_name,
                    'openclaw-gateway',
                    OPENCLAW_GATEWAY_BASE_URL,
                    '',
                    dedupe_keep_order(gw_models),
                    set(gw_models),
                    {m: dict(default_meta) for m in gw_models},
                ))
                logger.info(f'Auto-created gateway provider {provider_name} ({api_type}) with {len(gw_models)} models via gateway')

        for name, provider in load_router_profile_overlays(providers).items():
            merge_provider(providers, provider)

        logger.info(f"Loaded {len(providers)} configured providers: {list(providers.keys())}")
    except Exception as e:
        logger.error(f"Config load failed: {e}")
        providers['ollama'] = Provider('ollama', 'ollama', 'http://127.0.0.1:11434', '', ['qwen3.5:cloud', 'kimi-k2.5:cloud'], set(), {'qwen3.5:cloud': {'reasoning': False, 'contextWindow': 256000, 'maxTokens': 128000, 'input': ['text']}, 'kimi-k2.5:cloud': {'reasoning': False, 'contextWindow': 256000, 'maxTokens': 128000, 'input': ['text']}})
        # Even without a local OpenClaw config (e.g. public Cloud Run demo),
        # explicitly requested profile overlays should still be able to replace
        # the fallback local Ollama provider.
        for name, provider in load_router_profile_overlays(providers).items():
            merge_provider(providers, provider)
    return providers

PROVIDERS = load_openclaw_providers()


def normalize_content(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, str):
                parts.append(block)
            elif isinstance(block, dict):
                block_type = block.get('type')
                if block_type == 'text':
                    parts.append(str(block.get('text', '')))
                elif block_type in {'image', 'image_url', 'input_image'}:
                    parts.append('[image attached]')
                elif block_type in {'document', 'file', 'input_file'}:
                    name = block.get('filename') or block.get('fileName') or block.get('name') or block.get('path') or block.get('filePath') or 'file'
                    mime = block.get('mime_type') or block.get('mimeType') or block.get('media_type') or block.get('mediaType') or ''
                    parts.append(f'[document attached: {name} {mime}]')
                elif 'content' in block:
                    parts.append(normalize_content(block.get('content')))
        return ' '.join(part for part in parts if part).strip()
    if isinstance(content, dict):
        if 'text' in content:
            return str(content.get('text', ''))
        if 'content' in content:
            return normalize_content(content.get('content'))
    return '' if content is None else str(content)


def normalize_messages(messages):
    normalized = []
    for msg in sanitize_replay_messages(messages):
        if not isinstance(msg, dict):
            continue
        normalized.append({
            'role': msg.get('role', 'user'),
            'content': normalize_content(msg.get('content', '')),
        })
    return normalized


def _safe_document_path(path_value):
    path = os.path.abspath(os.path.expanduser(str(path_value or '').strip()))
    allowed_roots = [
        os.path.abspath(os.path.expanduser('~/.openclaw/media/inbound')),
        os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')),
    ]
    if not any(path == root or path.startswith(root + os.sep) for root in allowed_roots):
        return ''
    if not os.path.isfile(path):
        return ''
    return path


def extract_document_paths_from_content(content):
    paths = []
    if isinstance(content, list):
        for block in content:
            if not isinstance(block, dict):
                continue
            for key in ('path', 'filePath', 'filename', 'fileName'):
                candidate = block.get(key)
                safe = _safe_document_path(candidate) if candidate else ''
                if safe:
                    paths.append(safe)
    text = normalize_content(content)
    for match in re.findall(r'(/[^\s\]\)\}<>"\']+\.(?:pdf|txt|md))', text, flags=re.IGNORECASE):
        safe = _safe_document_path(match)
        if safe:
            paths.append(safe)
    return dedupe_keep_order(paths)


def extract_document_text(path, max_chars=30000):
    try:
        lower = path.lower()
        if lower.endswith('.pdf') and shutil.which('pdftotext'):
            proc = subprocess.run(['pdftotext', '-layout', '-nopgbrk', path, '-'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=20)
            if proc.returncode == 0 and proc.stdout.strip():
                return proc.stdout[:max_chars]
            logger.warning(f'pdftotext failed for {path}: {proc.stderr[:180]}')
        if lower.endswith(('.txt', '.md')):
            with open(path, 'r', encoding='utf-8', errors='replace') as f:
                return f.read(max_chars)
    except Exception as e:
        logger.warning(f'document extraction failed for {path}: {e}')
    return ''


def enrich_document_messages(messages, max_chars_per_doc=30000):
    enriched = []
    for msg in messages or []:
        if not isinstance(msg, dict):
            continue
        base = normalize_content(msg.get('content', ''))
        additions = []
        for path in extract_document_paths_from_content(msg.get('content', '')):
            text = extract_document_text(path, max_chars=max_chars_per_doc)
            if text.strip():
                additions.append(f'\n\n[Extracted text from {os.path.basename(path)}]\n{text.strip()}')
            else:
                additions.append(f'\n\n[Document attached but text extraction failed: {os.path.basename(path)}]')
        enriched.append({'role': msg.get('role', 'user'), 'content': (base + ''.join(additions)).strip()})
    return enriched


def load_latency_stats():
    try:
        with open(LATENCY_STATS_PATH) as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
    except FileNotFoundError:
        pass
    except Exception as e:
        logger.warning(f'Latency stats load failed: {e}')
    return {'version': 1, 'intents': {}}


LATENCY_STATS = load_latency_stats()


def save_latency_stats():
    try:
        os.makedirs(os.path.dirname(LATENCY_STATS_PATH), exist_ok=True)
        tmp_path = LATENCY_STATS_PATH + '.tmp'
        with open(tmp_path, 'w') as f:
            json.dump(LATENCY_STATS, f, indent=2, sort_keys=True)
        os.replace(tmp_path, LATENCY_STATS_PATH)
    except Exception as e:
        logger.warning(f'Latency stats save failed: {e}')


def sanitize_route_event(event):
    """Keep analytics useful while explicitly excluding prompt/user content and credentials."""
    allowed = {
        'request_id', 'ts', 'status', 'intent', 'complexity', 'thinking', 'routeMode',
        'estimatedTokens', 'json', 'stream', 'requirements', 'selected', 'attempts',
        'totalElapsedMs', 'chain', 'error', 'customer_id', 'customer_plan', 'auth_type'
    }
    clean = {k: v for k, v in dict(event or {}).items() if k in allowed}
    clean.setdefault('ts', int(time.time()))
    return clean


def route_auth_metadata_from_context(ctx):
    ctx = ctx or {}
    customer = ctx.get('customer') or {}
    meta = {'auth_type': ctx.get('type') or 'unknown'}
    if customer.get('id'):
        meta['customer_id'] = customer.get('id')
    elif ctx.get('customer_id'):
        meta['customer_id'] = ctx.get('customer_id')
    if customer.get('plan'):
        meta['customer_plan'] = customer.get('plan')
    elif ctx.get('customer_plan'):
        meta['customer_plan'] = ctx.get('customer_plan')
    return meta


def set_route_auth_context(ctx):
    ROUTE_AUTH_CONTEXT.value = route_auth_metadata_from_context(ctx)


def clear_route_auth_context():
    ROUTE_AUTH_CONTEXT.value = {}


def append_route_event(event):
    """Persist one structured routing event locally, then mirror durable telemetry async."""
    try:
        os.makedirs(os.path.dirname(ROUTE_EVENTS_PATH), exist_ok=True)
        event = dict(event or {})
        for key, value in (getattr(ROUTE_AUTH_CONTEXT, 'value', {}) or {}).items():
            event.setdefault(key, value)
        event = sanitize_route_event(event)
        with open(ROUTE_EVENTS_PATH, 'a') as f:
            f.write(json.dumps(event, sort_keys=True, separators=(',', ':')) + '\n')
    except Exception as e:
        logger.debug(f'Route event append failed: {e}')
        event = sanitize_route_event(event)
    mirror_route_event_async(event)


def read_recent_route_events(limit=None):
    """Read recent structured route events without retaining prompts or message bodies."""
    limit = int(limit or ANALYTICS_EVENT_LIMIT)
    events = []
    try:
        with open(ROUTE_EVENTS_PATH) as f:
            lines = f.readlines()[-limit:]
        for line in lines:
            try:
                event = json.loads(line)
                if isinstance(event, dict):
                    events.append(sanitize_route_event(event))
            except Exception:
                continue
    except FileNotFoundError:
        pass
    except Exception as e:
        logger.debug(f'Route events read failed: {e}')
    return events


def metadata_access_token():
    try:
        req = urllib.request.Request(
            'http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token',
            headers={'Metadata-Flavor': 'Google'},
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            payload = json.loads(resp.read().decode('utf-8'))
        return payload.get('access_token') or ''
    except Exception as e:
        logger.debug(f'GCP metadata token unavailable: {e}')
        return ''


def firestore_value(value):
    if value is None:
        return {'nullValue': None}
    if isinstance(value, bool):
        return {'booleanValue': value}
    if isinstance(value, int) and not isinstance(value, bool):
        return {'integerValue': str(value)}
    if isinstance(value, float):
        return {'doubleValue': value}
    if isinstance(value, list):
        return {'arrayValue': {'values': [firestore_value(v) for v in value]}}
    if isinstance(value, dict):
        return {'mapValue': {'fields': {str(k): firestore_value(v) for k, v in value.items()}}}
    return {'stringValue': str(value)}


def firestore_plain(value):
    if not isinstance(value, dict):
        return None
    if 'stringValue' in value:
        return value.get('stringValue')
    if 'integerValue' in value:
        try:
            return int(value.get('integerValue'))
        except Exception:
            return value.get('integerValue')
    if 'doubleValue' in value:
        return float(value.get('doubleValue'))
    if 'booleanValue' in value:
        return bool(value.get('booleanValue'))
    if 'nullValue' in value:
        return None
    if 'arrayValue' in value:
        return [firestore_plain(v) for v in (value.get('arrayValue') or {}).get('values', [])]
    if 'mapValue' in value:
        return {k: firestore_plain(v) for k, v in ((value.get('mapValue') or {}).get('fields') or {}).items()}
    return None


def write_firestore_route_event(event):
    if not (FIRESTORE_ENABLED and FIRESTORE_PROJECT_ID):
        return False
    token = metadata_access_token()
    if not token:
        return False
    event = sanitize_route_event(event)
    doc_id = urllib.parse.quote(str(event.get('request_id') or uuid.uuid4().hex), safe='')
    database = urllib.parse.quote(FIRESTORE_DATABASE, safe='')
    coll = urllib.parse.quote(FIRESTORE_ROUTE_EVENTS_COLLECTION, safe='')
    url = f'https://firestore.googleapis.com/v1/projects/{FIRESTORE_PROJECT_ID}/databases/{database}/documents/{coll}/{doc_id}'
    body = json.dumps({'fields': {k: firestore_value(v) for k, v in event.items()}}).encode('utf-8')
    req = urllib.request.Request(url, data=body, method='PATCH', headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    })
    with urllib.request.urlopen(req, timeout=8) as resp:
        resp.read(256)
    return True


def read_firestore_route_events(window_seconds=7 * 24 * 3600, limit=None):
    if not (FIRESTORE_ENABLED and FIRESTORE_PROJECT_ID):
        return []
    token = metadata_access_token()
    if not token:
        return []
    limit = int(limit or ANALYTICS_EVENT_LIMIT)
    since = int(time.time()) - int(window_seconds or 0) if window_seconds else 0
    database = urllib.parse.quote(FIRESTORE_DATABASE, safe='')
    url = f'https://firestore.googleapis.com/v1/projects/{FIRESTORE_PROJECT_ID}/databases/{database}/documents:runQuery'
    query = {
        'structuredQuery': {
            'from': [{'collectionId': FIRESTORE_ROUTE_EVENTS_COLLECTION}],
            'where': {'fieldFilter': {'field': {'fieldPath': 'ts'}, 'op': 'GREATER_THAN_OR_EQUAL', 'value': {'integerValue': str(since)}}},
            'orderBy': [{'field': {'fieldPath': 'ts'}, 'direction': 'DESCENDING'}],
            'limit': limit,
        }
    }
    req = urllib.request.Request(url, data=json.dumps(query).encode('utf-8'), headers={
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            payload = json.loads(resp.read().decode('utf-8'))
        events = []
        for row in payload if isinstance(payload, list) else []:
            fields = ((row.get('document') or {}).get('fields') or {})
            event = {k: firestore_plain(v) for k, v in fields.items()}
            if event:
                events.append(sanitize_route_event(event))
        return list(reversed(events))
    except Exception as e:
        logger.debug(f'Firestore analytics read failed: {extract_http_error(e)}')
        return []


def supabase_request(path, method='GET', body=None, service=False, extra_headers=None, timeout=8):
    key = SUPABASE_SERVICE_ROLE_KEY if service else SUPABASE_ANON_KEY
    if not (SUPABASE_URL and key):
        return None
    headers = {'apikey': key, 'Authorization': f'Bearer {key}'}
    if body is not None:
        headers['Content-Type'] = 'application/json'
        headers['Prefer'] = 'resolution=merge-duplicates,return=minimal'
    if extra_headers:
        headers.update(extra_headers)
    data = json.dumps(body).encode('utf-8') if body is not None else None
    req = urllib.request.Request(SUPABASE_URL.rstrip('/') + path, data=data, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
    if not raw:
        return None
    try:
        return json.loads(raw.decode('utf-8'))
    except Exception:
        return raw.decode('utf-8', errors='replace')


def write_supabase_route_event(event):
    if not (SUPABASE_MIRROR_ENABLED and SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY):
        return False
    event = sanitize_route_event(event)
    selected = event.get('selected') or {}
    row = {
        'request_id': str(event.get('request_id') or uuid.uuid4().hex),
        'event_ts': int(event.get('ts') or time.time()),
        'status': event.get('status'),
        'intent': event.get('intent'),
        'complexity': event.get('complexity'),
        'thinking': event.get('thinking'),
        'route_mode': event.get('routeMode'),
        'estimated_tokens': event.get('estimatedTokens'),
        'selected_provider': selected.get('provider'),
        'selected_model': selected.get('model'),
        'total_elapsed_ms': event.get('totalElapsedMs'),
        'attempt_count': len(event.get('attempts') or []),
        'event': event,
    }
    supabase_request(f'/rest/v1/{SUPABASE_ROUTE_EVENTS_TABLE}', method='POST', body=row, service=True)
    return True


def write_supabase_analytics_snapshot(snapshot):
    if not (SUPABASE_MIRROR_ENABLED and SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY):
        return False
    row = {
        'snapshot_id': f"{int(snapshot.get('generatedAt') or time.time())}-{int(snapshot.get('windowSeconds') or 0)}",
        'generated_at_epoch': int(snapshot.get('generatedAt') or time.time()),
        'window_seconds': int(snapshot.get('windowSeconds') or 0),
        'events_analyzed': int(snapshot.get('eventsAnalyzed') or 0),
        'snapshot': snapshot,
    }
    supabase_request(f'/rest/v1/{SUPABASE_ANALYTICS_SNAPSHOTS_TABLE}', method='POST', body=row, service=True)
    return True


def read_supabase_route_events(window_seconds=7 * 24 * 3600, limit=None):
    if not (SUPABASE_MIRROR_ENABLED and SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY):
        return []
    since = int(time.time()) - int(window_seconds or 0) if window_seconds else 0
    limit = int(limit or ANALYTICS_EVENT_LIMIT)
    path = f'/rest/v1/{SUPABASE_ROUTE_EVENTS_TABLE}?select=event&event_ts=gte.{since}&order=event_ts.desc&limit={limit}'
    try:
        rows = supabase_request(path, service=True, timeout=10) or []
        events = [sanitize_route_event((r or {}).get('event') or {}) for r in rows if isinstance(r, dict)]
        return list(reversed([e for e in events if e]))
    except Exception as e:
        logger.debug(f'Supabase analytics read failed: {extract_http_error(e)}')
        return []


def parse_epoch_value(value):
    if value is None or value == '':
        return None
    if isinstance(value, (int, float)):
        return int(value)
    text = str(value).strip()
    if not text:
        return None
    try:
        return int(float(text))
    except Exception:
        pass
    try:
        normalized = text.replace('Z', '+00:00')
        return int(datetime.datetime.fromisoformat(normalized).timestamp())
    except Exception:
        return None


def row_epoch(row, *keys):
    for key in keys:
        value = parse_epoch_value((row or {}).get(key))
        if value is not None:
            return value
    return None


def in_epoch_window(epoch, since, now):
    if epoch is None:
        return False
    return int(epoch) >= int(since) and int(epoch) <= int(now)


def percent_rate(numerator, denominator):
    if not denominator:
        return None
    return round(float(numerator) / float(denominator), 4)


LAUNCH_CONVERSION_TARGETS = {
    'signupToGeneratedKey': {
        'label': 'Signup to generated key',
        'targetRate': 0.60,
        'action': 'Tighten account onboarding, generated-key copy, and first setup CTA.',
    },
    'generatedKeyToFirstRequest': {
        'label': 'Generated key to first routed request',
        'targetRate': 0.50,
        'action': 'Improve quickstart examples, browser first-request testing, and 401/402/429/503 guidance.',
    },
    'setupCopyToFirstRequest': {
        'label': 'Setup copy to first routed request',
        'targetRate': 0.35,
        'action': 'Tighten copied setup snippets, Codex/OpenAI client examples, and first-request diagnostics.',
    },
    'signupToPaidConversion': {
        'label': 'Signup to paid conversion',
        'targetRate': 0.15,
        'action': 'Reduce checkout friction and strengthen Lite/Pro/Max upgrade prompts.',
    },
    'paidRecentUsage': {
        'label': 'Paid customer recent usage',
        'targetRate': 0.85,
        'action': 'Use reliability/status, analytics value, and quota alerts to retain paid accounts.',
    },
}


LAUNCH_CONVERSION_ACTIONS = {
    'signupToGeneratedKey': {
        'owner': 'Activation',
        'surface': 'account',
        'ctaPath': '/account.html',
        'action': 'Audit the signed-in account path from verified email to generated key, then simplify copy and key creation CTAs.',
        'successMetric': 'Raise signup-to-generated-key conversion to at least 60%.',
    },
    'generatedKeyToFirstRequest': {
        'owner': 'Activation',
        'surface': 'quickstart',
        'ctaPath': '/quickstart',
        'action': 'Test the generated-key quickstart, Codex config, and browser first-request check against the public edge.',
        'successMetric': 'Raise generated-key-to-first-request conversion to at least 50%.',
    },
    'setupCopyToFirstRequest': {
        'owner': 'Activation',
        'surface': 'setup snippets',
        'ctaPath': '/docs/codex',
        'action': 'Tighten copied Codex/OpenAI snippets and route copy events into the first-request troubleshooting flow.',
        'successMetric': 'Raise setup-copy-to-first-request activation to at least 35%.',
    },
    'signupToPaidConversion': {
        'owner': 'Revenue',
        'surface': 'pricing',
        'ctaPath': '/pricing',
        'action': 'Move active signups toward Lite/Pro/Max checkout with plan-specific proof and manual fallback when Stripe is unavailable.',
        'successMetric': 'Raise signup-to-paid conversion to at least 15%.',
    },
    'paidRecentUsage': {
        'owner': 'Retention',
        'surface': 'account analytics',
        'ctaPath': '/analytics.html',
        'action': 'Review idle paid accounts for quota, 503, first-request, and value-proof issues before churn shows up.',
        'successMetric': 'Keep at least 85% of paid customers using the router recently.',
    },
    'mrrTargetAttainment': {
        'owner': 'Revenue',
        'surface': 'plan mix',
        'ctaPath': '/launch-plan',
        'action': 'Work the largest Pro/Max plan gaps with founder-led outreach, gateway migration proof, and managed-access qualification.',
        'successMetric': 'Close the remaining gap to $10k MRR.',
    },
    'checkoutReadinessFriction': {
        'owner': 'Billing',
        'surface': 'checkout',
        'ctaPath': '/billing.html',
        'action': 'Fix checkout, billing-portal, or manual-settlement friction before buying more traffic.',
        'successMetric': 'Drive billing-friction rate to 0%.',
    },
}


CHECKOUT_INTENT_EVENTS = {
    'account_checkout_clicked',
    'account_checkout_failed',
    'account_checkout_unavailable',
    'account_billing_portal_failed',
    'account_crypto_intent_failed',
    'account_usage_upgrade_clicked',
    'calculator_checkout_clicked',
    'calculator_checkout_unavailable',
    'launch_plan_checkout_clicked',
    'gateway_compare_checkout_clicked',
    'pricing_checkout_clicked',
}
CHECKOUT_UNAVAILABLE_EVENTS = {
    'account_checkout_failed',
    'account_checkout_unavailable',
    'account_billing_portal_failed',
    'account_crypto_intent_failed',
    'calculator_checkout_unavailable',
}
SETUP_SNIPPET_COPY_EVENTS = {
    'quickstart_snippet_copied',
    'codex_docs_snippet_copied',
    'account_snippet_copied',
    'content_article_snippet_copied',
}
OPERATOR_FOLLOWUP_COPY_EVENTS = {
    'operator_no_key_followup_copied',
    'operator_no_key_followup_batch_copied',
    'operator_no_key_followup_csv_copied',
    'operator_no_key_followup_mailto_opened',
}
OPERATOR_FOLLOWUP_SEND_DRY_RUN_EVENTS = {
    'operator_no_key_followup_send_dry_run',
}
OPERATOR_FOLLOWUP_SEND_EVENTS = {
    'operator_no_key_followup_sent',
}
OPERATOR_FOLLOWUP_SEND_FAILURE_EVENTS = {
    'operator_no_key_followup_send_failed',
}
KEY_FIRST_REDIRECT_EVENTS = {
    'account_checkout_key_first_redirected',
    'account_intent_create_key_clicked',
    'calculator_key_activation_clicked',
    'codex_docs_key_activation_clicked',
    'content_article_key_activation_clicked',
    'fusion_key_activation_clicked',
    'gateway_compare_key_activation_clicked',
    'landing_key_first_direct_clicked',
    'landing_setup_next_clicked',
    'launch_plan_key_activation_clicked',
    'login_key_recovery_account_setup_clicked',
    'model_catalog_key_activation_clicked',
    'pricing_key_activation_clicked',
}
KEY_RECOVERY_VIEW_EVENTS = {
    'account_key_recovery_email_field_auto',
    'account_key_recovery_signed_in_prompt_shown',
    'account_key_recovery_viewed',
    'content_article_key_recovery_clicked',
    'pricing_key_recovery_clicked',
    'login_key_recovery_landed',
    'login_key_recovery_clicked',
    'login_key_recovery_same_account_prompted',
    'login_key_recovery_session_redirected',
    'billing_account_clicked',
    'landing_key_recovery_clicked',
    'model_catalog_key_recovery_clicked',
    'status_key_recovery_clicked',
    'support_key_recovery_clicked',
}
KEY_CREATE_ATTEMPT_EVENTS = {
    'account_api_key_create_clicked',
    'account_intent_create_key_clicked',
}
KEY_CREATE_SUCCESS_EVENTS = {
    'account_api_key_created',
    'account_key_recovery_key_created',
}
KEY_CREATE_FAILURE_EVENTS = {
    'account_api_key_create_failed',
}


def launch_checkout_friction(marketing_metrics):
    events = (marketing_metrics or {}).get('events') if isinstance(marketing_metrics, dict) else {}
    if not isinstance(events, dict):
        events = {}
    total_intent = 0
    unavailable = 0
    unavailable_by_event = {}
    for event, count in events.items():
        try:
            value = int(count or 0)
        except (TypeError, ValueError):
            value = 0
        if value <= 0:
            continue
        if event in CHECKOUT_INTENT_EVENTS:
            total_intent += value
        if event in CHECKOUT_UNAVAILABLE_EVENTS:
            unavailable += value
            unavailable_by_event[event] = unavailable_by_event.get(event, 0) + value
    return {
        'totalCheckoutIntent': total_intent,
        'unavailableEvents': unavailable,
        'unavailableByEvent': unavailable_by_event,
        'unavailableRate': percent_rate(unavailable, total_intent),
        'targetUnavailableRate': 0.0,
        'action': 'Fix Stripe checkout readiness or route demand into manual activation before buying more checkout traffic.',
    }


def launch_conversion_action(row):
    metric = str((row or {}).get('metric') or '')
    spec = LAUNCH_CONVERSION_ACTIONS.get(metric, {})
    status = str((row or {}).get('status') or '')
    if status == 'on_track':
        priority = 'monitor'
    elif status == 'below_target':
        priority = 'fix_now'
    else:
        priority = 'collect_data'
    return {
        'metric': metric,
        'label': (row or {}).get('label') or metric,
        'status': status,
        'priority': priority,
        'owner': spec.get('owner') or 'Operator',
        'surface': spec.get('surface') or 'launch funnel',
        'ctaPath': spec.get('ctaPath') or '/launch-plan',
        'actualRate': (row or {}).get('actualRate'),
        'targetRate': (row or {}).get('targetRate'),
        'gap': (row or {}).get('gap'),
        'action': spec.get('action') or (row or {}).get('action') or '',
        'successMetric': spec.get('successMetric') or 'Move this conversion metric back on target.',
    }


def launch_conversion_snapshot(rates, mrr, checkout_friction=None):
    targets = {}
    bottlenecks = []
    for metric, spec in LAUNCH_CONVERSION_TARGETS.items():
        target_rate = float(spec.get('targetRate') or 0)
        actual_rate = rates.get(metric)
        gap = None if actual_rate is None else round(max(0.0, target_rate - float(actual_rate)), 4)
        row = {
            'metric': metric,
            'label': spec.get('label') or metric,
            'actualRate': actual_rate,
            'targetRate': target_rate,
            'gap': gap,
            'status': 'not_enough_data' if actual_rate is None else ('on_track' if gap <= 0 else 'below_target'),
            'action': spec.get('action') or '',
        }
        targets[metric] = row
        if row['status'] != 'on_track':
            bottlenecks.append(row)

    mrr_target = float((mrr or {}).get('targetMrrUsd') or 0)
    mrr_current = float((mrr or {}).get('estimatedCurrentMrrUsd') or 0)
    mrr_gap = max(0.0, mrr_target - mrr_current) if mrr_target > 0 else None
    mrr_row = {
        'metric': 'mrrTargetAttainment',
        'label': '$10k MRR attainment',
        'actualRate': (mrr or {}).get('targetAttainment'),
        'targetRate': 1.0 if mrr_target > 0 else None,
        'gap': None if mrr_gap is None else round(mrr_gap, 2),
        'status': 'not_configured' if mrr_target <= 0 else ('on_track' if mrr_gap <= 0 else 'below_target'),
        'action': 'Close the remaining plan-mix gap with Pro/Max conversion and founder-led Max sales.',
    }
    targets[mrr_row['metric']] = mrr_row
    if mrr_row['status'] != 'on_track':
        bottlenecks.append(mrr_row)

    if isinstance(checkout_friction, dict):
        total_checkout_intent = int(checkout_friction.get('totalCheckoutIntent') or 0)
        unavailable_events = int(checkout_friction.get('unavailableEvents') or 0)
        unavailable_rate = checkout_friction.get('unavailableRate')
        checkout_row = {
            'metric': 'checkoutReadinessFriction',
            'label': 'Checkout readiness friction',
            'actualRate': unavailable_rate,
            'targetRate': 0.0,
            'gap': unavailable_rate,
            'status': 'not_enough_data' if total_checkout_intent <= 0 else ('on_track' if unavailable_events <= 0 else 'below_target'),
            'action': checkout_friction.get('action') or 'Fix checkout readiness before scaling paid acquisition.',
        }
        targets[checkout_row['metric']] = checkout_row
        if checkout_row['status'] != 'on_track':
            bottlenecks.append(checkout_row)

    bottlenecks.sort(key=lambda row: (0 if row.get('status') == 'below_target' else 1, row.get('gap') is None, -(float(row.get('gap') or 0))))
    conversion_actions = [launch_conversion_action(row) for row in bottlenecks]
    return {'targets': targets, 'bottlenecks': bottlenecks[:5], 'conversionActions': conversion_actions[:7]}


def launch_no_key_execution_checklist(recommended_segments, outreach_not_worked):
    segments = list(recommended_segments or [])
    if not segments:
        segments = ['all']
    labels = {
        'verified': 'Open/email verified drafts first',
        'unverified': 'Open/email unverified drafts second',
        'missing_auth_user': 'Review missing-auth-user signups',
        'missing_user_id': 'Review missing-user-id signups',
        'unavailable': 'Review verification-unavailable signups',
        'not_required': 'Open/email no-verification-required drafts',
        'all': 'Open/email all no-key drafts',
    }
    checklist = []
    for index, segment in enumerate(segments, start=1):
        checklist.append({
            'step': index,
            'segment': segment,
            'action': labels.get(segment) or f'Open/email {segment} drafts',
            'successMetric': 'Recovery link opened or signup creates a generated key.',
        })
    checklist.append({
        'step': len(checklist) + 1,
        'segment': 'worked',
        'action': 'Mark the worked segment only after real outreach is sent or copied into the outbound channel.',
        'successMetric': 'operatorFollowUpCopies increases before keyRecoveryViews and generated-key customers.',
    })
    if outreach_not_worked:
        checklist.append({
            'step': len(checklist) + 1,
            'segment': 'measure',
            'action': 'Refresh the funnel and watch keyRecoveryViews, then customersWithGeneratedApiKeys.',
            'successMetric': 'signupToGeneratedKey moves above zero.',
        })
    return checklist


ACTIVATION_REVIEW_ONLY_SEGMENTS = {'missing_auth_user', 'missing_user_id', 'unavailable'}


def launch_activation_delivery_counts(activation_follow_ups=None, counts=None, total=None):
    activation_follow_ups = activation_follow_ups or {}
    if counts is None:
        counts = activation_follow_ups.get('countsByEmailVerification') if isinstance(activation_follow_ups, dict) else {}
    counts = counts if isinstance(counts, dict) else {}
    if total is None:
        total = activation_follow_ups.get('total') if isinstance(activation_follow_ups, dict) else 0
    total = int(total or 0)
    sendable_queued = 0
    review_only_queued = 0
    known_queued = 0
    sendable_segments = []
    review_only_segments = []
    for segment, raw_count in counts.items():
        count = int(raw_count or 0)
        if count <= 0:
            continue
        known_queued += count
        if segment in ACTIVATION_REVIEW_ONLY_SEGMENTS:
            review_only_queued += count
            review_only_segments.append(segment)
        else:
            sendable_queued += count
            sendable_segments.append(segment)
    return {
        'sendableQueued': sendable_queued,
        'reviewOnlyQueued': review_only_queued,
        'unknownQueued': max(0, total - known_queued),
        'sendableSegments': sendable_segments,
        'reviewOnlySegments': review_only_segments,
    }


def marketing_event_result_count(metadata):
    try:
        value = int(float((metadata or {}).get('resultCount') or 1))
    except (TypeError, ValueError):
        value = 1
    return max(1, min(value, 10000))


def launch_next_best_action(stages, rates, mrr, activation_follow_ups, conversion_actions=None):
    """Return one privacy-safe operator action tied to the current launch bottleneck."""
    stages = stages or {}
    rates = rates or {}
    activation_follow_ups = activation_follow_ups or {}
    conversion_actions = conversion_actions or []
    no_key_total = int(activation_follow_ups.get('total') or 0)
    no_key_new = int(activation_follow_ups.get('windowedNewSignups') or 0)
    operator_follow_up_copies = int(activation_follow_ups.get('operatorFollowUpCopies') or 0)
    operator_follow_up_worked = int(activation_follow_ups.get('operatorFollowUpWorked') or 0)
    operator_follow_up_send_dry_runs = int(activation_follow_ups.get('operatorFollowUpSendDryRuns') or 0)
    operator_follow_up_sends = int(activation_follow_ups.get('operatorFollowUpSends') or 0)
    operator_follow_up_send_failures = int(activation_follow_ups.get('operatorFollowUpSendFailures') or 0)
    operator_follow_up_send_dry_run_recipients = int(activation_follow_ups.get('operatorFollowUpSendDryRunRecipients') or 0)
    operator_follow_up_sent_recipients = int(activation_follow_ups.get('operatorFollowUpSentRecipients') or 0)
    operator_follow_up_send_failure_recipients = int(activation_follow_ups.get('operatorFollowUpSendFailureRecipients') or 0)
    key_first_redirects = int(activation_follow_ups.get('keyFirstRedirects') or 0)
    key_recovery_views = int(activation_follow_ups.get('keyRecoveryViews') or 0)
    signups = int(stages.get('signups') or 0)
    generated_keys = int(stages.get('customersWithGeneratedApiKeys') or stages.get('generatedApiKeys') or 0)
    first_requests = int(stages.get('customersWithFirstRoutedRequest') or stages.get('firstRoutedRequest') or 0)
    paid_customers = int(stages.get('paidCustomers') or 0)
    signup_to_key_rate = rates.get('signupToGeneratedKey')
    signup_to_key_below_target = signup_to_key_rate is None or float(signup_to_key_rate or 0) < float(LAUNCH_CONVERSION_TARGETS['signupToGeneratedKey']['targetRate'])
    if no_key_total > 0 and signup_to_key_below_target:
        outreach_not_worked = operator_follow_up_worked <= 0
        verification_counts = activation_follow_ups.get('countsByEmailVerification') if isinstance(activation_follow_ups, dict) else {}
        delivery_counts = launch_activation_delivery_counts(activation_follow_ups, verification_counts, no_key_total)
        recommended_segments = [
            segment for segment in ('verified', 'unverified', 'missing_auth_user', 'missing_user_id', 'unavailable', 'not_required')
            if int((verification_counts or {}).get(segment) or 0) > 0
        ]
        no_key_anchor = 'no-key-followups:segments' if len(recommended_segments) > 1 else 'no-key-followups'
        execution_checklist = launch_no_key_execution_checklist(recommended_segments, outreach_not_worked)
        return {
            'metric': 'signupToGeneratedKey',
            'priority': 'fix_now',
            'owner': 'Activation',
            'surface': 'launch funnel' if outreach_not_worked else 'account',
            'ctaPath': (
                f'{APP_BASE_URL.rstrip("/")}/launch-funnel.html#{no_key_anchor}'
                if outreach_not_worked
                else activation_follow_ups.get('primaryCtaUrl') or launch_activation_follow_up_url(activation_follow_ups.get('suggestedPlan') or 'pro')
            ),
            'action': (
                'Open the operator no-key signup queue, send the sendable verified/unverified drafts, review auth-repair segments separately, then mark the worked segment through the launch funnel telemetry.'
                if outreach_not_worked
                else activation_follow_ups.get('recommendedOperatorAction') or 'Send the generated-key-first recovery link to no-key signups.'
            ),
            'executionChecklist': execution_checklist,
            'successMetric': activation_follow_ups.get('successMetric') or 'Move no-key signups into generated-key accounts, then first routed request.',
            'evidence': {
                'signups': signups,
                'generatedKeyCustomers': generated_keys,
                'noKeyFollowUpsQueued': no_key_total,
                'sendableQueued': delivery_counts.get('sendableQueued', 0),
                'reviewOnlyQueued': delivery_counts.get('reviewOnlyQueued', 0),
                'unknownQueued': delivery_counts.get('unknownQueued', 0),
                'sendableSegments': delivery_counts.get('sendableSegments') or [],
                'reviewOnlySegments': delivery_counts.get('reviewOnlySegments') or [],
                'windowedNoKeySignups': no_key_new,
                'operatorFollowUpCopies': operator_follow_up_copies,
                'operatorFollowUpWorked': operator_follow_up_worked,
                'operatorFollowUpWorkedByKind': activation_follow_ups.get('operatorFollowUpWorkedByKind') or {},
                'operatorFollowUpSendDryRuns': operator_follow_up_send_dry_runs,
                'operatorFollowUpSendDryRunsByKind': activation_follow_ups.get('operatorFollowUpSendDryRunsByKind') or {},
                'operatorFollowUpSendDryRunRecipients': operator_follow_up_send_dry_run_recipients,
                'operatorFollowUpSends': operator_follow_up_sends,
                'operatorFollowUpSendsByKind': activation_follow_ups.get('operatorFollowUpSendsByKind') or {},
                'operatorFollowUpSentRecipients': operator_follow_up_sent_recipients,
                'operatorFollowUpSendFailures': operator_follow_up_send_failures,
                'operatorFollowUpSendFailuresByKind': activation_follow_ups.get('operatorFollowUpSendFailuresByKind') or {},
                'operatorFollowUpSendFailureRecipients': operator_follow_up_send_failure_recipients,
                'keyFirstRedirects': key_first_redirects,
                'keyFirstRedirectsByState': activation_follow_ups.get('keyFirstRedirectsByState') or {},
                'keyRecoveryViews': key_recovery_views,
                'keyRecoveryViewsByState': activation_follow_ups.get('keyRecoveryViewsByState') or {},
                'keyCreateAttempts': int(activation_follow_ups.get('keyCreateAttempts') or 0),
                'keyCreateAttemptsByState': activation_follow_ups.get('keyCreateAttemptsByState') or {},
                'keyCreateSuccesses': int(activation_follow_ups.get('keyCreateSuccesses') or 0),
                'keyCreateSuccessesByState': activation_follow_ups.get('keyCreateSuccessesByState') or {},
                'keyCreateFailures': int(activation_follow_ups.get('keyCreateFailures') or 0),
                'keyCreateFailuresByState': activation_follow_ups.get('keyCreateFailuresByState') or {},
                'emailVerification': verification_counts or {},
                'recommendedSegments': recommended_segments,
                'signupToGeneratedKey': signup_to_key_rate,
            },
            'privacy': activation_follow_ups.get('privacy') or {
                'containsEmails': False,
                'containsCustomerIds': False,
                'containsApiKeys': False,
                'containsProviderCredentials': False,
            },
        }
    if generated_keys > 0 and first_requests <= 0:
        return {
            'metric': 'generatedKeyToFirstRequest',
            'priority': 'fix_now',
            'owner': 'Activation',
            'surface': 'quickstart',
            'ctaPath': '/quickstart',
            'action': 'Use the browser Responses API probe and copyable Codex/OpenAI snippets to get a first routed request.',
            'successMetric': 'Move generated-key accounts into first routed request.',
            'evidence': {
                'generatedKeyCustomers': generated_keys,
                'firstRoutedRequestCustomers': first_requests,
                'generatedKeyToFirstRequest': rates.get('generatedKeyToFirstRequest'),
            },
        }
    if paid_customers <= 0:
        first_conversion = conversion_actions[0] if conversion_actions else {}
        return {
            'metric': first_conversion.get('metric') or 'mrrTargetAttainment',
            'priority': first_conversion.get('priority') or 'fix_now',
            'owner': first_conversion.get('owner') or 'Revenue',
            'surface': first_conversion.get('surface') or 'plan mix',
            'ctaPath': first_conversion.get('ctaPath') or '/launch-plan',
            'action': first_conversion.get('action') or 'Convert the first active generated-key users into paid Lite, Pro, or Max customers.',
            'successMetric': first_conversion.get('successMetric') or 'Create the first paid Sage Router customer.',
            'evidence': {
                'paidCustomers': paid_customers,
                'estimatedCurrentMrrUsd': (mrr or {}).get('estimatedCurrentMrrUsd'),
                'targetMrrUsd': (mrr or {}).get('targetMrrUsd'),
            },
        }
    return conversion_actions[0] if conversion_actions else {
        'metric': 'monitorLaunchFunnel',
        'priority': 'monitor',
        'owner': 'Operator',
        'surface': 'launch funnel',
        'ctaPath': '/launch-funnel.html',
        'action': 'Monitor activation, first request, checkout, and retention rates against the $10k MRR plan.',
        'successMetric': 'Keep each launch funnel stage on target.',
    }


def launch_operator_execution_packet(next_best_action, activation_follow_ups):
    """Return a no-secret action packet for operator dashboards and agents."""
    next_best_action = next_best_action or {}
    activation_follow_ups = activation_follow_ups or {}
    total = int(activation_follow_ups.get('total') or 0)
    plan = normalize_stripe_plan(activation_follow_ups.get('suggestedPlan') or 'pro') or 'pro'
    urls = activation_follow_ups.get('primaryCtaUrls') if isinstance(activation_follow_ups.get('primaryCtaUrls'), dict) else {}
    if not urls:
        urls = launch_activation_follow_up_urls(plan)
    password_url = urls.get('passwordFallback') or activation_follow_ups.get('primaryCtaUrl') or launch_activation_follow_up_url(plan, auth=False)
    github_url = urls.get('githubOAuth') or launch_activation_follow_up_url(plan, auth='github')
    counts = activation_follow_ups.get('countsByEmailVerification') if isinstance(activation_follow_ups.get('countsByEmailVerification'), dict) else {}
    evidence = next_best_action.get('evidence') if isinstance(next_best_action.get('evidence'), dict) else {}
    email_readiness = activation_follow_ups.get('emailReadiness') if isinstance(activation_follow_ups.get('emailReadiness'), dict) else activation_email_readiness()
    recommended_segments = [
        segment for segment in (evidence.get('recommendedSegments') or [])
        if isinstance(segment, str) and segment
    ]
    if not recommended_segments:
        recommended_segments = [
            segment for segment in ('verified', 'unverified', 'missing_auth_user', 'missing_user_id', 'unavailable', 'not_required')
            if int((counts or {}).get(segment) or 0) > 0
        ]
    if not recommended_segments and total > 0:
        recommended_segments = ['all']

    segment_labels = {
        'verified': 'verified signups',
        'unverified': 'unverified signups',
        'missing_auth_user': 'missing auth-user signups',
        'missing_user_id': 'missing user-id signups',
        'unavailable': 'verification-unavailable signups',
        'not_required': 'verification-not-required signups',
        'all': 'all no-key signups',
    }
    segment_actions = []
    sendable_queued = 0
    review_only_queued = 0
    for segment in recommended_segments:
        count = total if segment == 'all' else int((counts or {}).get(segment) or 0)
        if count <= 0:
            continue
        review_only = segment in ACTIVATION_REVIEW_ONLY_SEGMENTS
        if review_only:
            review_only_queued += count
        else:
            sendable_queued += count
        segment_actions.append({
            'segment': segment,
            'label': segment_labels.get(segment, segment),
            'count': count,
            'deliveryMode': 'review' if review_only else 'send',
            'sendable': not review_only,
            'reviewReason': 'Needs auth-user repair before recovery email can be sent.' if review_only else '',
            'copyKind': f'{segment}_aggregate_draft_copied',
            'workedKind': f'{segment}_marked_worked' if segment in {'verified', 'unverified'} else 'marked_worked',
            'sendOrder': len(segment_actions) + 1,
        })
        if not review_only:
            segment_commands = (email_readiness.get('segmentCommandTemplates') or {}).get(segment) or {}
            segment_actions[-1]['dryRunCommand'] = segment_commands.get('dryRunCommand') or activation_followup_send_command(segment=segment, dry_run=True)
            segment_actions[-1]['sendCommand'] = segment_commands.get('sendCommand') or activation_followup_send_command(segment=segment, dry_run=False)
    send_telemetry = {
        'dryRunActions': int(activation_follow_ups.get('operatorFollowUpSendDryRuns') or 0),
        'dryRunRecipients': int(activation_follow_ups.get('operatorFollowUpSendDryRunRecipients') or 0),
        'sendActions': int(activation_follow_ups.get('operatorFollowUpSends') or 0),
        'sentRecipients': int(activation_follow_ups.get('operatorFollowUpSentRecipients') or 0),
        'failedActions': int(activation_follow_ups.get('operatorFollowUpSendFailures') or 0),
        'failedRecipients': int(activation_follow_ups.get('operatorFollowUpSendFailureRecipients') or 0),
        'dryRunByKind': activation_follow_ups.get('operatorFollowUpSendDryRunsByKind') or {},
        'sentByKind': activation_follow_ups.get('operatorFollowUpSendsByKind') or {},
        'failedByKind': activation_follow_ups.get('operatorFollowUpSendFailuresByKind') or {},
    }
    send_telemetry['dryRunVerified'] = send_telemetry['dryRunRecipients'] >= max(1, sendable_queued) if sendable_queued > 0 else False
    send_telemetry['sendApprovalRequired'] = sendable_queued > 0 and send_telemetry['sentRecipients'] < sendable_queued
    send_telemetry['nextSendSegment'] = next((row.get('segment') for row in segment_actions if row.get('sendable')), 'all' if sendable_queued > 0 else '')

    draft_subject = 'Finish your Sage Router setup key'
    draft_body = (
        'You already started Sage Router. The next step is to create your generated sk_sage setup key before checkout or routing setup.\n\n'
        f'Use the same email/password path first: {password_url}\n'
        f'If you signed in with GitHub, use this path instead: {github_url}\n\n'
        'No provider key, prompt text, OAuth token, generated API key, or checkout is needed before the setup key exists.'
    )
    return {
        'kind': 'signup_to_key_recovery' if total > 0 else 'none',
        'title': 'Signup-to-key recovery packet',
        'priority': next_best_action.get('priority') or ('fix_now' if total > 0 else 'monitor'),
        'owner': next_best_action.get('owner') or 'Activation',
        'surface': next_best_action.get('surface') or 'launch funnel',
        'metric': next_best_action.get('metric') or 'signupToGeneratedKey',
        'recommendedAction': (
            next_best_action.get('action')
            or activation_follow_ups.get('recommendedOperatorAction')
            or 'Send the generated-key-first recovery link to no-key signups.'
        ),
        'ctaPath': (
            next_best_action.get('ctaPath')
            or activation_follow_ups.get('primaryCtaUrl')
            or password_url
        ),
        'successMetric': (
            next_best_action.get('successMetric')
            or activation_follow_ups.get('successMetric')
            or 'Move no-key signups into generated-key accounts, then first routed request.'
        ),
        'executionChecklist': next_best_action.get('executionChecklist') or launch_no_key_execution_checklist(recommended_segments, True),
        'totalQueued': total,
        'sendableQueued': sendable_queued,
        'reviewOnlyQueued': review_only_queued,
        'windowedNewSignups': int(activation_follow_ups.get('windowedNewSignups') or 0),
        'sendTelemetry': send_telemetry,
        'segmentCounts': counts or {},
        'segmentActions': segment_actions,
        'primaryCtaKind': activation_follow_ups.get('primaryCtaKind') or 'same_email_password',
        'recommendedCtaOrder': activation_follow_ups.get('recommendedCtaOrder') or ['passwordFallback', 'githubOAuth'],
        'recoveryUrls': {
            'passwordFallback': password_url,
            'githubOAuth': github_url,
        },
        'draft': {
            'subject': draft_subject,
            'body': draft_body,
        },
        'telemetry': {
            'copyEvents': sorted(OPERATOR_FOLLOWUP_COPY_EVENTS),
            'workedKindPattern': '<segment>_marked_worked',
            'recoveryViewEvents': sorted(KEY_RECOVERY_VIEW_EVENTS),
            'keyCreateAttemptEvents': sorted(KEY_CREATE_ATTEMPT_EVENTS),
            'keyCreateSuccessEvents': sorted(KEY_CREATE_SUCCESS_EVENTS),
            'successMetric': next_best_action.get('successMetric') or activation_follow_ups.get('successMetric') or 'Move no-key signups into generated-key accounts, then first routed request.',
        },
        'emailReadiness': email_readiness,
        'instructions': [
            (
                'Dry-run verified; wait for explicit operator approval before real send.'
                if send_telemetry.get('dryRunVerified') and send_telemetry.get('sendApprovalRequired')
                else 'Dry-run the activation sender before real outreach.'
            ),
            'Send or copy the draft to sendable signup segments only after approval.',
            'Review auth-repair segments separately before expecting recovery email delivery.',
            email_readiness.get('operatorAction') or 'Use the dashboard send controls after dry-run verification.',
            'Mark the segment worked only after real outreach is sent or copied into the outbound channel.',
            'Refresh the funnel and watch keyRecoveryViews, keyCreateAttempts, and customersWithGeneratedApiKeys.',
        ],
        'privacy': {
            'containsEmails': False,
            'containsCustomerIds': False,
            'containsApiKeys': False,
            'containsProviderCredentials': False,
            'containsPrompts': False,
            'containsOAuthTokens': False,
            'aggregateOnly': True,
        },
    }


def public_plan_monthly_price_usd(plan_name):
    plan = PUBLIC_PLAN_CATALOG.get(str(plan_name or '').strip().lower()) or {}
    price = str(plan.get('price') or '')
    match = re.search(r'\$([0-9]+(?:\.[0-9]+)?)/month', price)
    if not match:
        return 0
    value = float(match.group(1))
    return int(value) if value.is_integer() else value


def manual_payment_amount_for_plan(plan_name):
    plan_name = normalize_stripe_plan(plan_name)
    if not plan_name:
        return ''
    amount = public_plan_monthly_price_usd(plan_name)
    return str(amount) if amount else ''


def launch_revenue_action(plan, customer_gap, mrr_gap):
    plan_name = str(plan or '').strip().lower()
    if plan_name == 'max':
        return 'Book founder-led Max demos for automation/team users and attach private deployment support.'
    if plan_name == 'pro':
        return 'Convert active generated-key users into Pro with frontier profile, analytics, and fallback proof.'
    if plan_name == 'lite':
        return 'Use low-friction Lite checkout from pricing, calculator, and quickstart entry points.'
    return f'Close {int(customer_gap or 0)} paid customer gap worth ${int(mrr_gap or 0):,}/month.'


def launch_mrr_snapshot(customers):
    target = int(PUBLIC_LAUNCH_POSITIONING.get('targetMrrUsd') or 0)
    recommended = PUBLIC_LAUNCH_POSITIONING.get('recommendedMix') or {}
    paid_by_plan = {}
    for customer in customers:
        if not customer_is_active(customer):
            continue
        plan = str(customer.get('plan') or 'free').strip().lower() or 'free'
        paid_by_plan[plan] = paid_by_plan.get(plan, 0) + 1

    by_plan = {}
    revenue_actions = []
    current_mrr = 0
    for plan in sorted(set(paid_by_plan) | {'lite', 'pro', 'max'}):
        customers_on_plan = int(paid_by_plan.get(plan, 0))
        monthly_price = public_plan_monthly_price_usd(plan)
        plan_mrr = customers_on_plan * monthly_price
        current_mrr += plan_mrr
        target_customers = int(recommended.get(f'{plan}Customers') or 0)
        customer_gap = max(0, target_customers - customers_on_plan)
        target_mrr = target_customers * monthly_price
        mrr_gap = max(0, target_mrr - plan_mrr)
        by_plan[plan] = {
            'paidCustomers': customers_on_plan,
            'monthlyPriceUsd': monthly_price,
            'estimatedMrrUsd': plan_mrr,
            'targetCustomers': target_customers,
            'remainingToTarget': customer_gap,
            'targetMrrUsd': target_mrr,
            'remainingMrrToTargetUsd': mrr_gap,
            'targetAttainment': percent_rate(customers_on_plan, target_customers),
        }
        if customer_gap > 0 and target_mrr > 0:
            revenue_actions.append({
                'plan': plan,
                'label': f'Close {plan.title()} plan gap',
                'currentCustomers': customers_on_plan,
                'targetCustomers': target_customers,
                'customerGap': customer_gap,
                'monthlyPriceUsd': monthly_price,
                'estimatedMrrUsd': plan_mrr,
                'targetMrrUsd': target_mrr,
                'remainingMrrToTargetUsd': mrr_gap,
                'action': launch_revenue_action(plan, customer_gap, mrr_gap),
            })

    revenue_actions.sort(key=lambda row: (
        -int(row.get('remainingMrrToTargetUsd') or 0),
        -int(row.get('monthlyPriceUsd') or 0),
        str(row.get('plan') or ''),
    ))

    return {
        'targetMrrUsd': target,
        'estimatedCurrentMrrUsd': current_mrr,
        'targetAttainment': percent_rate(current_mrr, target),
        'recommendedMixMonthlyRevenueUsd': recommended.get('monthlyRevenueUsd'),
        'paidCustomersByPlan': paid_by_plan,
        'byPlan': by_plan,
        'planRevenueActions': revenue_actions,
        'assumptions': {
            'source': 'public_plan_catalog',
            'managedProviderAccessIncluded': bool((PUBLIC_LAUNCH_POSITIONING.get('managedProviderAccess') or {}).get('enabled')),
        },
    }


def read_launch_customer_rows(limit=10000):
    try:
        if customer_store_uses_supabase():
            return supabase_select(
                SUPABASE_CUSTOMERS_TABLE,
                'select=id,user_id,plan,status,created_at_epoch,updated_at_epoch,stripe_customer_id,stripe_subscription_id'
                f'&limit={int(limit)}',
                timeout=8,
            )
        return [
            {
                'id': row.get('id'),
                'user_id': row.get('user_id'),
                'plan': row.get('plan'),
                'status': row.get('status'),
                'created_at_epoch': row.get('created_at_epoch'),
                'updated_at_epoch': row.get('updated_at_epoch'),
                'stripe_customer_id': row.get('stripe_customer_id'),
                'stripe_subscription_id': row.get('stripe_subscription_id'),
            }
            for row in (local_customer_store().get('customers') or [])
            if isinstance(row, dict)
        ]
    except Exception as e:
        logger.debug(f'Launch funnel customer read failed: {extract_http_error(e)}')
        return []


def read_launch_auth_user_rows(limit=1000):
    """Read privacy-safe Supabase Auth signup rows for launch funnel counts."""
    if not (SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY):
        return None
    try:
        url = SUPABASE_URL.rstrip('/') + f'/auth/v1/admin/users?page=1&per_page={int(limit)}'
        req = urllib.request.Request(url, headers={
            'apikey': SUPABASE_SERVICE_ROLE_KEY,
            'Authorization': f'Bearer {SUPABASE_SERVICE_ROLE_KEY}',
        })
        with urllib.request.urlopen(req, timeout=8) as resp:
            payload = json.loads(resp.read().decode('utf-8'))
        users = payload.get('users') if isinstance(payload, dict) else None
        if not isinstance(users, list):
            return None
        rows = []
        for user in users:
            if not isinstance(user, dict) or not user.get('id'):
                continue
            rows.append({
                'id': str(user.get('id')),
                'email': user.get('email') or ((user.get('user_metadata') or {}).get('email')),
                'created_at': user.get('created_at'),
                'email_confirmed': bool(user.get('email_confirmed_at') or user.get('confirmed_at')),
            })
        return rows
    except Exception as e:
        logger.debug(f'Launch funnel auth user read failed: {extract_http_error(e)}')
        return None


def auth_user_rows_by_id(auth_users):
    return {
        str(row.get('id')): row
        for row in (auth_users or [])
        if isinstance(row, dict) and row.get('id')
    }


def auth_verification_state_for_customer(customer, auth_users=None):
    required = hosted_email_verification_required()
    if not required:
        return {'required': False, 'verified': True, 'source': 'not_required'}
    user_id = str((customer or {}).get('user_id') or '').strip()
    if not user_id:
        return {'required': True, 'verified': False, 'source': 'missing_user_id'}
    rows = auth_users if isinstance(auth_users, list) else read_launch_auth_user_rows()
    if not isinstance(rows, list):
        return {'required': True, 'verified': False, 'source': 'unavailable'}
    row = auth_user_rows_by_id(rows).get(user_id)
    if not row:
        return {'required': True, 'verified': False, 'source': 'missing_auth_user'}
    return {
        'required': True,
        'verified': bool(row.get('email_confirmed')),
        'source': 'supabase_auth_admin',
    }


def auth_verification_bucket(state):
    state = state or {}
    if not state.get('required'):
        return 'not_required'
    source = str(state.get('source') or '')
    if source in {'unavailable', 'missing_user_id', 'missing_auth_user'}:
        return source
    return 'verified' if state.get('verified') else 'unverified'


def read_launch_api_key_rows(limit=10000):
    try:
        if customer_store_uses_supabase():
            return supabase_select(
                SUPABASE_API_KEYS_TABLE,
                'select=id,customer_id,status,created_at_epoch,last_used_at_epoch'
                f'&limit={int(limit)}',
                timeout=8,
            )
        return [
            {
                'id': row.get('id'),
                'customer_id': row.get('customer_id'),
                'status': row.get('status'),
                'created_at_epoch': row.get('created_at_epoch'),
                'last_used_at_epoch': row.get('last_used_at_epoch'),
            }
            for row in (local_customer_store().get('api_keys') or [])
            if isinstance(row, dict)
        ]
    except Exception as e:
        logger.debug(f'Launch funnel API key read failed: {extract_http_error(e)}')
        return []


MANAGED_ACCESS_TARGET_PROVIDER_BUCKETS = (
    'mixed-frontier',
    'ollama',
    'openai',
    'anthropic',
    'byok-compatible',
)
MANAGED_ACCESS_COMMERCIAL_PREFERENCE_BUCKETS = (
    'one-subscription',
    'byok-plus-routing',
    'private-contract',
)
MANAGED_ACCESS_SUPPORT_NEED_BUCKETS = (
    'implementation-support',
    'private-deployment',
    'migration-help',
    'managed-provider-review',
)
MANAGED_ACCESS_TARGET_LAUNCH_WINDOW_BUCKETS = (
    'this-week',
    'this-month',
    'this-quarter',
    'exploring',
)
MANAGED_ACCESS_INTENT_BUCKETS = (
    'max-implementation',
    'private-deployment',
    'gateway-migration',
    'one-subscription',
    'ollama',
    'openai',
    'anthropic',
)
MARKETING_SOURCE_SURFACE_BUCKETS = (
    'article',
    'self-hosted',
    'pricing',
    'model-routing-calculator',
    'quickstart',
    'codex-docs',
    'fusion',
    'compare-gateways',
    'agent-native',
    'integrations',
    'managed-access',
    'launch-plan',
    'model-catalog',
    'account',
    'login',
    'billing',
    'status',
    'support',
    'landing',
)
MARKETING_ATTRIBUTION_CHANNEL_BUCKETS = (
    'direct',
    'github',
    'google',
    'model-gateway',
    'x',
    'discord',
    'reddit',
    'newsletter',
    'docs',
    'sagerouter',
)
MARKETING_MODEL_CATALOG_FAMILY_BUCKETS = (
    'sage-router-profiles',
    'openai-codex',
    'anthropic',
    'gemini',
    'ollama',
    'byok-compatible',
    'all',
    'other',
)
MARKETING_MODEL_CATALOG_QUERY_BUCKETS = (
    'sage-router-profiles',
    'openai-codex',
    'anthropic',
    'gemini',
    'ollama',
    'byok-compatible',
    'empty',
    'other',
)


def waitlist_metadata(row):
    metadata = row.get('metadata') if isinstance(row, dict) else None
    if isinstance(metadata, str):
        try:
            metadata = json.loads(metadata)
        except Exception:
            metadata = {}
    if not isinstance(metadata, dict):
        metadata = {}
    return metadata


def waitlist_interest_bucket(row):
    metadata = waitlist_metadata(row)
    interest = str(metadata.get('interest') or 'general').strip().lower()
    if interest == 'managed-access':
        return 'managedAccess'
    if interest and interest != 'general':
        return 'other'
    return 'general'


def waitlist_metadata_bucket(metadata, allowed, *keys):
    for key in keys:
        value = str(metadata.get(key) or '').strip().lower()
        if value in allowed:
            return value
    return 'unknown'


def marketing_event_metadata(row):
    metadata = row.get('metadata') if isinstance(row, dict) else None
    if isinstance(metadata, str):
        try:
            metadata = json.loads(metadata)
        except Exception:
            metadata = {}
    if not isinstance(metadata, dict):
        metadata = {}
    # Strip PII before aggregation/action generation.
    metadata = {k: v for k, v in metadata.items() if k not in {'email', 'userEmail', 'user_email', 'customerEmail', 'customer_email', 'buyerEmail', 'buyer_email'}}
    return metadata


def marketing_event_is_smoke(row, metadata=None):
    if not isinstance(row, dict):
        return False
    metadata = metadata if isinstance(metadata, dict) else marketing_event_metadata(row)
    values = [
        metadata.get('smoke'),
        metadata.get('test'),
        metadata.get('button'),
        metadata.get('state'),
    ]
    source_page = str(row.get('source_page') or row.get('sourcePage') or '').lower()
    if 'smoke=1' in source_page:
        return True
    return any(str(value or '').strip().lower() in {'true', '1', 'yes', 'smoke', 'test'} for value in values)


MARKETING_BOT_USER_AGENT_FRAGMENTS = (
    'bot',
    'crawler',
    'spider',
    'ahrefs',
    'semrush',
    'mj12bot',
    'dotbot',
    'bingpreview',
    'slurp',
    'duckduckbot',
    'baiduspider',
    'yandex',
    'facebookexternalhit',
    'twitterbot',
    'linkedinbot',
    'discordbot',
    'telegrambot',
    'whatsapp',
    'curl/',
    'wget/',
    'python-requests',
    'go-http-client',
    'headless',
    'lighthouse',
    'pagespeed',
    'chrome-lighthouse',
)

MARKETING_SUSPICIOUS_BROWSER_FRAGMENTS = (
    'chrome/79.0.3945.79',
)


def marketing_event_user_agent(metadata):
    return str(
        (metadata or {}).get('user_agent')
        or (metadata or {}).get('userAgent')
        or (metadata or {}).get('ua')
        or ''
    ).strip().lower()


def marketing_event_minute(row):
    created_at = str((row or {}).get('created_at') or (row or {}).get('createdAt') or '').strip()
    if len(created_at) >= 16:
        return created_at[:16]
    return ''


def marketing_event_source_path(row, metadata=None):
    metadata = metadata if isinstance(metadata, dict) else marketing_event_metadata(row)
    raw = str(
        (row or {}).get('source_page')
        or (row or {}).get('sourcePage')
        or metadata.get('sourcePage')
        or metadata.get('source_page')
        or metadata.get('page')
        or ''
    ).strip()
    if not raw:
        return ''
    try:
        parsed = urllib.parse.urlparse(raw)
        return parsed.path or raw.split('?', 1)[0] or '/'
    except Exception:
        return raw.split('?', 1)[0] or '/'


def marketing_event_is_known_bot(row, metadata=None):
    metadata = metadata if isinstance(metadata, dict) else marketing_event_metadata(row)
    ua = marketing_event_user_agent(metadata)
    if not ua:
        return False
    return any(fragment in ua for fragment in MARKETING_BOT_USER_AGENT_FRAGMENTS) or any(
        fragment in ua for fragment in MARKETING_SUSPICIOUS_BROWSER_FRAGMENTS
    )


def marketing_synthetic_sweep_keys(rows, metadata_available=True):
    buckets = {}
    for row in rows or []:
        if not isinstance(row, dict):
            continue
        metadata = marketing_event_metadata(row) if metadata_available else {}
        ua = marketing_event_user_agent(metadata)
        minute = marketing_event_minute(row)
        if not ua or not minute:
            continue
        key = (minute, ua)
        bucket = buckets.setdefault(key, {'events': 0, 'paths': set()})
        bucket['events'] += 1
        path = marketing_event_source_path(row, metadata)
        if path:
            bucket['paths'].add(path)
    return {
        key
        for key, bucket in buckets.items()
        if bucket['events'] >= 15 or (bucket['events'] >= 8 and len(bucket['paths']) >= 4)
    }


def marketing_event_is_synthetic(row, metadata=None, sweep_keys=None):
    metadata = metadata if isinstance(metadata, dict) else marketing_event_metadata(row)
    if marketing_event_is_known_bot(row, metadata):
        return True
    if sweep_keys and (marketing_event_minute(row), marketing_event_user_agent(metadata)) in sweep_keys:
        return True
    return False


def marketing_source_surface_bucket(metadata):
    source = str(metadata.get('sourceSurface') or metadata.get('source') or '').strip().lower()
    if source in MARKETING_SOURCE_SURFACE_BUCKETS:
        return source
    if source:
        return 'other'
    return 'unknown'


def marketing_channel_bucket(metadata):
    utm_source = str(metadata.get('utmSource') or metadata.get('utm_source') or '').strip().lower()
    referrer_host = str(metadata.get('referrerHost') or '').strip().lower()
    referer = str(metadata.get('referer') or '').strip().lower()
    candidates = [utm_source, referrer_host, referer]
    if not any(candidates):
        return 'direct'
    haystack = ' '.join(value for value in candidates if value)
    if 'github' in haystack:
        return 'github'
    if 'openrouter' in haystack or 'model-gateway' in haystack or 'modelgateway' in haystack:
        return 'model-gateway'
    if 'discord' in haystack:
        return 'discord'
    if 'reddit' in haystack:
        return 'reddit'
    if 'newsletter' in haystack or 'email' in haystack:
        return 'newsletter'
    if 'google' in haystack:
        return 'google'
    if 'twitter' in haystack or 'x.com' in haystack:
        return 'x'
    if 'docs' in haystack:
        return 'docs'
    if 'sagerouter.dev' in haystack or 'app.sagerouter.dev' in haystack:
        return 'sagerouter'
    return 'other'


def marketing_model_catalog_bucket(metadata, allowed, *keys):
    for key in keys:
        value = str(metadata.get(key) or '').strip().lower()
        if not value:
            continue
        return value if value in allowed else 'other'
    return 'unknown'


def new_model_catalog_demand_metrics():
    return {
        'modelFamily': {bucket: 0 for bucket in (*MARKETING_MODEL_CATALOG_FAMILY_BUCKETS, 'unknown')},
        'queryBucket': {bucket: 0 for bucket in (*MARKETING_MODEL_CATALOG_QUERY_BUCKETS, 'unknown')},
    }


def marketing_event_is_model_catalog(event, metadata):
    return str(event or '').startswith('model_catalog_') or str(metadata.get('source') or '').strip().lower() == 'model-catalog'


def launch_acquisition_action(kind, bucket):
    normalized = str(bucket or '').strip().lower()
    if kind == 'sourceSurface':
        actions = {
            'pricing': 'Tighten pricing CTAs, checkout plan defaults, and proof around hosted key activation.',
            'article': 'Turn long-form local-first routing readers into quickstart, Codex setup, and gateway comparison CTAs.',
            'self-hosted': 'Turn self-hosted router evaluators into local quickstart, GitHub install, and hosted key activation CTAs.',
            'model-routing-calculator': 'Turn calculator interest into generated-key-first Pro/Max activation and implementation calls.',
            'model-catalog': 'Turn catalog demand into hosted key activation, route-profile proof, and model availability copy.',
            'quickstart': 'Use copyable quickstart snippets to convert generated-key users into first routed requests.',
            'fusion': 'Convert Fusion page demand into Pro/Max checkout, gateway migration proof, and first high-stakes synthesis requests.',
            'compare-gateways': 'Route gateway comparison traffic into the migration guide, model catalog, and hosted checkout.',
            'agent-native': 'Turn agent-native routing traffic into Pro key activation, Codex setup, and first agent request proof.',
            'integrations': 'Turn integration setup traffic into hosted key activation, quickstart copies, and first routed requests.',
            'managed-access': 'Turn managed-access beta demand into authorization review, margin validation, and Max/BYOK activation.',
            'launch-plan': 'Turn launch-plan readers into Pro checkout, calculator qualification, or managed-access beta conversations.',
            'landing': 'Keep the homepage focused on account creation, pricing, model catalog, and migration CTAs.',
            'account': 'Reduce signed-in friction from plan selection to generated key and first routed request.',
            'login': 'Improve login/signup handoff copy and OAuth/email fallback paths.',
            'billing': 'Use billing recovery traffic to unblock checkout, portal, manual activation, and quota issues.',
        }
        return actions.get(normalized, 'Review this source surface for the next highest-friction CTA.')
    actions = {
        'model-gateway': 'Publish gateway migration proof and comparison CTAs for users already shopping hosted routers.',
        'github': 'Convert GitHub traffic with README, issue-template, and docs links into quickstart and pricing paths.',
        'google': 'Improve search landing pages around OpenAI-compatible routing, model fallback, and hosted API keys.',
        'discord': 'Use Discord/community traffic for founder-led activation help and first-request debugging.',
        'reddit': 'Package comparison, migration, and reliability proof for Reddit-style evaluation threads.',
        'newsletter': 'Turn newsletter traffic into pricing/calculator/account CTAs with a single launch offer.',
        'docs': 'Add checkout and account next steps to docs pages that already educate qualified traffic.',
        'direct': 'Clarify the direct landing path from homepage to plan, generated key, and first routed request.',
        'sagerouter': 'Cross-link internal Sage Router pages toward the current lowest-performing activation step.',
    }
    return actions.get(normalized, 'Review this channel for acquisition copy, CTA placement, and checkout friction.')


DEFAULT_LAUNCH_ACQUISITION_ACTIONS = (
    {
        'kind': 'attributionChannel',
        'bucket': 'model-gateway',
        'action': 'Seed gateway comparison traffic with migration proof, model catalog links, and hosted checkout CTAs.',
    },
    {
        'kind': 'attributionChannel',
        'bucket': 'github',
        'action': 'Use README, release notes, and issue templates to route qualified builders into quickstart and pricing.',
    },
    {
        'kind': 'sourceSurface',
        'bucket': 'pricing',
        'action': 'Test the Lite/Pro/Max checkout path from pricing before buying broader acquisition.',
    },
    {
        'kind': 'sourceSurface',
        'bucket': 'model-routing-calculator',
        'action': 'Drive early prospects to the calculator so Pro/Max fit and savings claims are captured before signup.',
    },
    {
        'kind': 'sourceSurface',
        'bucket': 'model-catalog',
        'action': 'Seed model catalog traffic with hosted key activation, frontier profile proof, and gateway migration CTAs.',
    },
    {
        'kind': 'sourceSurface',
        'bucket': 'quickstart',
        'action': 'Use copyable quickstart snippets to convert generated-key users into first routed requests.',
    },
    {
        'kind': 'sourceSurface',
        'bucket': 'codex-docs',
        'action': 'Turn Codex setup demand into hosted key activation and copy-to-first-request proof.',
    },
    {
        'kind': 'sourceSurface',
        'bucket': 'fusion',
        'action': 'Drive Fusion evaluators into Pro/Max checkout and migration snippets.',
    },
    {
        'kind': 'sourceSurface',
        'bucket': 'agent-native',
        'action': 'Turn agent-native routing readers into Pro key activation, Codex setup, and first agent request proof.',
    },
    {
        'kind': 'sourceSurface',
        'bucket': 'integrations',
        'action': 'Turn integration setup readers into hosted key activation, quickstart copies, and first routed requests.',
    },
    {
        'kind': 'sourceSurface',
        'bucket': 'managed-access',
        'action': 'Seed managed-access beta conversations while keeping public resale disabled until authorization and margin controls pass.',
    },
    {
        'kind': 'sourceSurface',
        'bucket': 'launch-plan',
        'action': 'Use the launch plan as the founder-led sales artifact for $10k MRR outreach and managed-access beta calls.',
    },
)


def launch_acquisition_actions(marketing_metrics):
    if not isinstance(marketing_metrics, dict):
        return []
    rows = []
    specs = (
        ('sourceSurface', marketing_metrics.get('sourceSurfaces') or {}),
        ('attributionChannel', marketing_metrics.get('attributionChannels') or {}),
    )
    for kind, counts in specs:
        if not isinstance(counts, dict):
            continue
        for bucket, count in counts.items():
            try:
                clicks = int(count or 0)
            except (TypeError, ValueError):
                clicks = 0
            if clicks <= 0 or bucket in {'unknown', 'other'}:
                continue
            rows.append({
                'kind': kind,
                'bucket': str(bucket),
                'clicks': clicks,
                'priority': 'scale_existing_signal',
                'action': launch_acquisition_action(kind, bucket),
            })
    rows.sort(key=lambda row: (-int(row.get('clicks') or 0), str(row.get('kind') or ''), str(row.get('bucket') or '')))
    if not rows:
        return [
            {
                'kind': row['kind'],
                'bucket': row['bucket'],
                'clicks': 0,
                'priority': 'seed_launch_channel',
                'action': row['action'],
            }
            for row in DEFAULT_LAUNCH_ACQUISITION_ACTIONS
        ]
    return rows[:16]


def new_auth_provider_state_metrics():
    provider_buckets = {'github': 0, 'google': 0, 'discord': 0, 'none': 0, 'other': 0}
    return {
        'total': 0,
        'loaded': 0,
        'unavailable': 0,
        'unknown': 0,
        'githubEnabled': 0,
        'githubDisabled': 0,
        'enabledProviders': dict(provider_buckets),
        'disabledProviders': dict(provider_buckets),
    }


def metadata_bool(value):
    if isinstance(value, bool):
        return value
    normalized = str(value or '').strip().lower()
    if normalized in {'1', 'true', 'yes', 'on', 'enabled'}:
        return True
    if normalized in {'0', 'false', 'no', 'off', 'disabled'}:
        return False
    return None


def provider_state_list(value):
    if isinstance(value, (list, tuple, set)):
        parts = value
    else:
        parts = str(value or '').split(',')
    providers = []
    for part in parts:
        provider = str(part or '').strip().lower()
        if not provider:
            continue
        providers.append(provider if provider in {'github', 'google', 'discord', 'none'} else 'other')
    return providers or ['none']


def update_auth_provider_state_metrics(metrics, metadata):
    state = str(metadata.get('state') or '').strip().lower()
    auth_state = metrics['authProviderState']
    auth_state['total'] += 1
    if state in {'loaded', 'unavailable'}:
        auth_state[state] += 1
    else:
        auth_state['unknown'] += 1

    github_enabled = metadata_bool(metadata.get('githubEnabled'))
    if github_enabled is True:
        auth_state['githubEnabled'] += 1
    elif github_enabled is False:
        auth_state['githubDisabled'] += 1

    for provider in provider_state_list(metadata.get('enabledProviders')):
        auth_state['enabledProviders'][provider] = auth_state['enabledProviders'].get(provider, 0) + 1
    for provider in provider_state_list(metadata.get('disabledProviders')):
        auth_state['disabledProviders'][provider] = auth_state['disabledProviders'].get(provider, 0) + 1


def launch_auth_provider_state(marketing_metrics):
    base = new_auth_provider_state_metrics()
    source = 'unavailable'
    if isinstance(marketing_metrics, dict) and isinstance(marketing_metrics.get('authProviderState'), dict):
        raw = marketing_metrics.get('authProviderState') or {}
        source = 'marketing_funnel' if int(raw.get('total') or 0) > 0 else 'marketing_funnel_empty'
        base = {
            **base,
            **{k: v for k, v in raw.items() if k not in {'enabledProviders', 'disabledProviders'}},
            'enabledProviders': {
                **base['enabledProviders'],
                **(raw.get('enabledProviders') if isinstance(raw.get('enabledProviders'), dict) else {}),
            },
            'disabledProviders': {
                **base['disabledProviders'],
                **(raw.get('disabledProviders') if isinstance(raw.get('disabledProviders'), dict) else {}),
            },
        }
    github_available = int(base.get('githubEnabled') or 0) > 0 and int(base.get('githubEnabled') or 0) >= int(base.get('githubDisabled') or 0)
    return {
        **base,
        'source': source,
        'githubAvailable': github_available,
        'recommendedRecoveryAuth': 'email_first',
        'operatorGuidance': (
            'Use email/password recovery first; GitHub/OAuth is available only when it is the same signup account.'
            if github_available
            else 'Use email/password recovery first; do not rely on GitHub/OAuth until provider state is observed healthy.'
        ),
    }


def new_managed_access_demand_metrics():
    return {
        'targetProviderFamily': {bucket: 0 for bucket in (*MANAGED_ACCESS_TARGET_PROVIDER_BUCKETS, 'unknown')},
        'commercialPreference': {bucket: 0 for bucket in (*MANAGED_ACCESS_COMMERCIAL_PREFERENCE_BUCKETS, 'unknown')},
        'supportNeed': {bucket: 0 for bucket in (*MANAGED_ACCESS_SUPPORT_NEED_BUCKETS, 'unknown')},
        'targetLaunchWindow': {bucket: 0 for bucket in (*MANAGED_ACCESS_TARGET_LAUNCH_WINDOW_BUCKETS, 'unknown')},
        'intent': {bucket: 0 for bucket in (*MANAGED_ACCESS_INTENT_BUCKETS, 'unknown')},
    }


def read_launch_waitlist_counts(since, limit=10000):
    if not (SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY):
        return None, 'supabase_not_configured'
    since_iso = datetime.datetime.fromtimestamp(int(since), datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
    quoted_since = urllib.parse.quote(since_iso, safe=':-TZ')
    tables = [SUPABASE_WAITLIST_TABLE, SUPABASE_WAITLIST_FALLBACK_TABLE]
    metrics = {
        'total': 0,
        'interest': {
            'general': 0,
            'managedAccess': 0,
            'other': 0,
            'unknown': 0,
        },
        'managedAccessDemand': new_managed_access_demand_metrics(),
    }
    tables_read = 0
    for table in [t for t in tables if t]:
        try:
            try:
                rows = supabase_select(
                    table,
                    f'select=created_at,metadata&created_at=gte.{quoted_since}&limit={int(limit)}',
                    timeout=6,
                )
                metadata_available = True
            except Exception as e:
                logger.debug(f'Launch funnel waitlist metadata read failed for {table}: {extract_http_error(e)}')
                rows = supabase_select(
                    table,
                    f'select=created_at&created_at=gte.{quoted_since}&limit={int(limit)}',
                    timeout=6,
                )
                metadata_available = False
            rows = rows or []
            metrics['total'] += len(rows)
            tables_read += 1
            for row in rows:
                bucket = waitlist_interest_bucket(row) if metadata_available else 'unknown'
                metrics['interest'][bucket] = metrics['interest'].get(bucket, 0) + 1
                if bucket == 'managedAccess':
                    metadata = waitlist_metadata(row)
                    target_provider = waitlist_metadata_bucket(
                        metadata,
                        MANAGED_ACCESS_TARGET_PROVIDER_BUCKETS,
                        'target_provider_family',
                        'targetProviderFamily',
                    )
                    commercial_preference = waitlist_metadata_bucket(
                        metadata,
                        MANAGED_ACCESS_COMMERCIAL_PREFERENCE_BUCKETS,
                        'commercial_preference',
                        'commercialPreference',
                    )
                    support_need = waitlist_metadata_bucket(
                        metadata,
                        MANAGED_ACCESS_SUPPORT_NEED_BUCKETS,
                        'support_need',
                        'supportNeed',
                    )
                    target_launch_window = waitlist_metadata_bucket(
                        metadata,
                        MANAGED_ACCESS_TARGET_LAUNCH_WINDOW_BUCKETS,
                        'target_launch_window',
                        'targetLaunchWindow',
                    )
                    intent = waitlist_metadata_bucket(
                        metadata,
                        MANAGED_ACCESS_INTENT_BUCKETS,
                        'intent',
                    )
                    metrics['managedAccessDemand']['targetProviderFamily'][target_provider] += 1
                    metrics['managedAccessDemand']['commercialPreference'][commercial_preference] += 1
                    metrics['managedAccessDemand']['supportNeed'][support_need] += 1
                    metrics['managedAccessDemand']['targetLaunchWindow'][target_launch_window] += 1
                    metrics['managedAccessDemand']['intent'][intent] += 1
        except Exception as e:
            logger.debug(f'Launch funnel waitlist read failed for {table}: {extract_http_error(e)}')
    if tables_read == 0:
        return None, 'waitlist_tables_unavailable'
    return metrics, None


def read_launch_waitlist_count(since, limit=10000):
    metrics, error = read_launch_waitlist_counts(since, limit)
    if metrics is None:
        return None, error
    return metrics.get('total', 0), error


def read_launch_marketing_funnel_counts(since, limit=10000):
    if not (SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY):
        return None, 'supabase_not_configured'
    since_iso = datetime.datetime.fromtimestamp(int(since), datetime.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')
    quoted_since = urllib.parse.quote(since_iso, safe=':-TZ')
    metrics = {
        'total': 0,
        'events': {},
        'plans': {},
        'sourceSurfaces': {bucket: 0 for bucket in (*MARKETING_SOURCE_SURFACE_BUCKETS, 'other', 'unknown')},
        'attributionChannels': {bucket: 0 for bucket in (*MARKETING_ATTRIBUTION_CHANNEL_BUCKETS, 'other', 'unknown')},
        'modelCatalogDemand': new_model_catalog_demand_metrics(),
        'authProviderState': new_auth_provider_state_metrics(),
        'setupSnippetCopies': 0,
        'setupSnippetCopiesBySnippet': {},
        'operatorFollowUpCopies': 0,
        'operatorFollowUpCopiesByKind': {},
        'operatorFollowUpWorked': 0,
        'operatorFollowUpWorkedByKind': {},
        'operatorFollowUpSendDryRuns': 0,
        'operatorFollowUpSendDryRunsByKind': {},
        'operatorFollowUpSendDryRunRecipients': 0,
        'operatorFollowUpSends': 0,
        'operatorFollowUpSendsByKind': {},
        'operatorFollowUpSentRecipients': 0,
        'operatorFollowUpSendFailures': 0,
        'operatorFollowUpSendFailuresByKind': {},
        'operatorFollowUpSendFailureRecipients': 0,
        'keyFirstRedirects': 0,
        'keyFirstRedirectsByState': {},
        'keyRecoveryViews': 0,
        'keyRecoveryViewsByState': {},
        'keyCreateAttempts': 0,
        'keyCreateAttemptsByState': {},
        'keyCreateSuccesses': 0,
        'keyCreateSuccessesByState': {},
        'keyCreateFailures': 0,
        'keyCreateFailuresByState': {},
        'filteredSyntheticEvents': 0,
    }
    try:
        try:
            rows = supabase_select(
                SUPABASE_FUNNEL_EVENTS_TABLE,
                f'select=event,plan,created_at,source_page,metadata&created_at=gte.{quoted_since}&limit={int(limit)}',
                timeout=6,
            ) or []
            metadata_available = True
        except Exception as e:
            logger.debug(f'Launch funnel marketing event metadata read failed: {extract_http_error(e)}')
            rows = supabase_select(
                SUPABASE_FUNNEL_EVENTS_TABLE,
                f'select=event,plan,created_at,source_page&created_at=gte.{quoted_since}&limit={int(limit)}',
                timeout=6,
            ) or []
            metadata_available = False
    except Exception as e:
        logger.debug(f'Launch funnel marketing event read failed: {extract_http_error(e)}')
        return None, 'marketing_funnel_events_unavailable'

    synthetic_sweep_keys = marketing_synthetic_sweep_keys(rows, metadata_available)
    for row in rows:
        if not isinstance(row, dict):
            continue
        event = str(row.get('event') or 'unknown').strip() or 'unknown'
        plan = str(row.get('plan') or '').strip().lower()
        metadata = marketing_event_metadata(row) if metadata_available else {}
        if marketing_event_is_smoke(row, metadata):
            continue
        if marketing_event_is_synthetic(row, metadata, synthetic_sweep_keys):
            metrics['filteredSyntheticEvents'] += 1
            continue
        metrics['total'] += 1
        metrics['events'][event] = metrics['events'].get(event, 0) + 1
        if plan:
            metrics['plans'][plan] = metrics['plans'].get(plan, 0) + 1
        if metadata_available:
            source_surface = marketing_source_surface_bucket(metadata)
            attribution_channel = marketing_channel_bucket(metadata)
        else:
            source_surface = 'unknown'
            attribution_channel = 'unknown'
        metrics['sourceSurfaces'][source_surface] = metrics['sourceSurfaces'].get(source_surface, 0) + 1
        metrics['attributionChannels'][attribution_channel] = metrics['attributionChannels'].get(attribution_channel, 0) + 1
        if marketing_event_is_model_catalog(event, metadata):
            family = marketing_model_catalog_bucket(
                metadata,
                MARKETING_MODEL_CATALOG_FAMILY_BUCKETS,
                'modelFamily',
                'model_family',
            )
            query_bucket = marketing_model_catalog_bucket(
                metadata,
                MARKETING_MODEL_CATALOG_QUERY_BUCKETS,
                'queryBucket',
                'query_bucket',
            )
            metrics['modelCatalogDemand']['modelFamily'][family] = metrics['modelCatalogDemand']['modelFamily'].get(family, 0) + 1
            metrics['modelCatalogDemand']['queryBucket'][query_bucket] = metrics['modelCatalogDemand']['queryBucket'].get(query_bucket, 0) + 1
        if event == 'auth_provider_state_checked':
            update_auth_provider_state_metrics(metrics, metadata)
        if event in SETUP_SNIPPET_COPY_EVENTS:
            metrics['setupSnippetCopies'] += 1
            snippet = str(metadata.get('snippet') or 'unknown').strip().lower()[:80] or 'unknown'
            metrics['setupSnippetCopiesBySnippet'][snippet] = metrics['setupSnippetCopiesBySnippet'].get(snippet, 0) + 1
        if event in OPERATOR_FOLLOWUP_COPY_EVENTS:
            metrics['operatorFollowUpCopies'] += 1
            kind = str(metadata.get('state') or event).strip().lower()[:80] or event
            metrics['operatorFollowUpCopiesByKind'][kind] = metrics['operatorFollowUpCopiesByKind'].get(kind, 0) + 1
            if kind == 'marked_worked' or kind.endswith('_marked_worked'):
                metrics['operatorFollowUpWorked'] += 1
                metrics['operatorFollowUpWorkedByKind'][kind] = metrics['operatorFollowUpWorkedByKind'].get(kind, 0) + 1
        if event in OPERATOR_FOLLOWUP_SEND_DRY_RUN_EVENTS:
            metrics['operatorFollowUpSendDryRuns'] += 1
            metrics['operatorFollowUpSendDryRunRecipients'] += marketing_event_result_count(metadata)
            kind = str(metadata.get('state') or event).strip().lower()[:80] or event
            metrics['operatorFollowUpSendDryRunsByKind'][kind] = metrics['operatorFollowUpSendDryRunsByKind'].get(kind, 0) + 1
        if event in OPERATOR_FOLLOWUP_SEND_EVENTS:
            metrics['operatorFollowUpSends'] += 1
            metrics['operatorFollowUpSentRecipients'] += marketing_event_result_count(metadata)
            kind = str(metadata.get('state') or event).strip().lower()[:80] or event
            metrics['operatorFollowUpSendsByKind'][kind] = metrics['operatorFollowUpSendsByKind'].get(kind, 0) + 1
        if event in OPERATOR_FOLLOWUP_SEND_FAILURE_EVENTS:
            metrics['operatorFollowUpSendFailures'] += 1
            metrics['operatorFollowUpSendFailureRecipients'] += marketing_event_result_count(metadata)
            kind = str(metadata.get('state') or event).strip().lower()[:80] or event
            metrics['operatorFollowUpSendFailuresByKind'][kind] = metrics['operatorFollowUpSendFailuresByKind'].get(kind, 0) + 1
        if event in KEY_FIRST_REDIRECT_EVENTS:
            metrics['keyFirstRedirects'] += 1
            state = str(metadata.get('state') or event).strip().lower()[:80] or event
            metrics['keyFirstRedirectsByState'][state] = metrics['keyFirstRedirectsByState'].get(state, 0) + 1
        if event in KEY_RECOVERY_VIEW_EVENTS:
            metrics['keyRecoveryViews'] += 1
            state = str(metadata.get('state') or 'unknown').strip().lower()[:80] or 'unknown'
            metrics['keyRecoveryViewsByState'][state] = metrics['keyRecoveryViewsByState'].get(state, 0) + 1
        if event in KEY_CREATE_ATTEMPT_EVENTS:
            metrics['keyCreateAttempts'] += 1
            state = str(metadata.get('state') or event).strip().lower()[:80] or event
            metrics['keyCreateAttemptsByState'][state] = metrics['keyCreateAttemptsByState'].get(state, 0) + 1
        if event in KEY_CREATE_SUCCESS_EVENTS:
            metrics['keyCreateSuccesses'] += 1
            state = str(metadata.get('state') or event).strip().lower()[:80] or event
            metrics['keyCreateSuccessesByState'][state] = metrics['keyCreateSuccessesByState'].get(state, 0) + 1
        if event in KEY_CREATE_FAILURE_EVENTS:
            metrics['keyCreateFailures'] += 1
            state = str(metadata.get('state') or event).strip().lower()[:80] or event
            metrics['keyCreateFailuresByState'][state] = metrics['keyCreateFailuresByState'].get(state, 0) + 1
    return metrics, None


def route_events_for_window(window_seconds, event_limit=None):
    now = int(time.time())
    since = now - int(window_seconds or 0) if window_seconds else 0
    durable_events = read_firestore_route_events(window_seconds, event_limit)
    source = 'firestore' if durable_events else 'local'
    if not durable_events:
        durable_events = read_supabase_route_events(window_seconds, event_limit)
        source = 'supabase' if durable_events else 'local'
    events = durable_events or [e for e in read_recent_route_events(event_limit) if int(e.get('ts', 0) or 0) >= since]
    return source, events


def build_launch_funnel_snapshot(window_seconds=30 * 24 * 3600, event_limit=None):
    """Summarize hosted launch conversion without returning PII, prompts, or secrets."""
    now = int(time.time())
    since = now - int(window_seconds or 0) if window_seconds else 0
    customers = [normalize_customer(row) for row in read_launch_customer_rows() if isinstance(row, dict)]
    auth_user_rows = read_launch_auth_user_rows()
    auth_users_available = isinstance(auth_user_rows, list)
    auth_users = [row for row in (auth_user_rows or []) if isinstance(row, dict)]
    api_keys = [row for row in read_launch_api_key_rows() if isinstance(row, dict)]
    event_source, route_events = route_events_for_window(window_seconds, event_limit)
    waitlist_metrics, waitlist_error = read_launch_waitlist_counts(since)
    marketing_metrics, marketing_error = read_launch_marketing_funnel_counts(since)
    acquisition_actions = launch_acquisition_actions(marketing_metrics)
    if isinstance(marketing_metrics, dict):
        for key, default in {
            'keyCreateAttempts': 0,
            'keyCreateAttemptsByState': {},
            'keyCreateSuccesses': 0,
            'keyCreateSuccessesByState': {},
            'keyCreateFailures': 0,
            'keyCreateFailuresByState': {},
        }.items():
            marketing_metrics.setdefault(key, default)
        marketing_metrics = {
            **marketing_metrics,
            'acquisitionActions': acquisition_actions,
            'checkoutFriction': launch_checkout_friction(marketing_metrics),
        }
    waitlist_count = waitlist_metrics.get('total', 0) if isinstance(waitlist_metrics, dict) else None
    waitlist_interest = waitlist_metrics.get('interest') if isinstance(waitlist_metrics, dict) else None
    managed_access_demand = waitlist_metrics.get('managedAccessDemand') if isinstance(waitlist_metrics, dict) else None
    managed_access_interest = waitlist_interest.get('managedAccess', 0) if isinstance(waitlist_interest, dict) else None
    marketing_intent_events = marketing_metrics.get('total', 0) if isinstance(marketing_metrics, dict) else None
    setup_snippet_copies = marketing_metrics.get('setupSnippetCopies', 0) if isinstance(marketing_metrics, dict) else None

    customer_ids = {str(c.get('id')) for c in customers if c and c.get('id')}
    customer_user_ids = {str(c.get('user_id')) for c in customers if c and c.get('user_id')}
    customer_signup_ids = {
        str(c.get('id'))
        for c in customers
        if c and c.get('id') and in_epoch_window(row_epoch(c, 'created_at_epoch', 'created_at'), since, now)
    }
    customer_signup_user_ids = {
        str(c.get('user_id'))
        for c in customers
        if c and c.get('user_id') and in_epoch_window(row_epoch(c, 'created_at_epoch', 'created_at'), since, now)
    }
    auth_signup_ids = {
        str(row.get('id'))
        for row in auth_users
        if row.get('id') and in_epoch_window(row_epoch(row, 'created_at'), since, now)
    }
    auth_confirmed_signup_ids = {
        str(row.get('id'))
        for row in auth_users
        if row.get('id') and row.get('email_confirmed') and in_epoch_window(row_epoch(row, 'created_at'), since, now)
    }
    auth_signup_count = len(auth_signup_ids) if auth_users_available else None
    customer_signup_count = len(customer_signup_ids)
    signups_count = max(auth_signup_count or 0, customer_signup_count) if auth_users_available else customer_signup_count
    auth_signups_without_customer_rows = len(auth_signup_ids - customer_user_ids) if auth_users_available else 0
    customer_signups_without_auth_rows = len(customer_signup_user_ids - auth_signup_ids) if auth_users_available else 0
    active_key_customer_ids = {
        str(k.get('customer_id'))
        for k in api_keys
        if k.get('customer_id') and str(k.get('status') or 'active').lower() == 'active'
    }
    generated_key_customer_ids = {
        str(k.get('customer_id'))
        for k in api_keys
        if k.get('customer_id') and in_epoch_window(row_epoch(k, 'created_at_epoch', 'created_at'), since, now)
    }
    first_request_customer_ids = {
        str(e.get('customer_id'))
        for e in route_events
        if e.get('customer_id') and in_epoch_window(row_epoch(e, 'ts', 'event_ts'), since, now)
    }
    first_request_customer_ids.update(
        str(k.get('customer_id'))
        for k in api_keys
        if k.get('customer_id') and in_epoch_window(row_epoch(k, 'last_used_at_epoch'), since, now)
    )
    paid_customer_ids = {
        str(c.get('id'))
        for c in customers
        if c and c.get('id') and customer_is_active(c)
    }
    paid_conversion_ids = {
        str(c.get('id'))
        for c in customers
        if c and c.get('id') and customer_is_active(c) and in_epoch_window(row_epoch(c, 'updated_at_epoch', 'created_at_epoch', 'created_at'), since, now)
    }
    retained_paid_ids = paid_customer_ids & first_request_customer_ids

    stages = {
        'marketingIntentEvents': marketing_intent_events,
        'waitlistLeads': waitlist_count,
        'managedAccessBetaInterest': managed_access_interest,
        'signups': signups_count,
        'customersWithActiveApiKeys': len(active_key_customer_ids & customer_ids),
        'customersWithGeneratedApiKeys': len(generated_key_customer_ids & customer_ids),
        'setupSnippetCopies': setup_snippet_copies,
        'customersWithFirstRoutedRequest': len(first_request_customer_ids & customer_ids),
        'paidConversions': len(paid_conversion_ids),
        'paidCustomers': len(paid_customer_ids),
        'retainedPaidCustomers': len(retained_paid_ids),
    }
    signup_hydration = {
        'authSignups': len(auth_signup_ids) if auth_users_available else None,
        'confirmedAuthSignups': len(auth_confirmed_signup_ids) if auth_users_available else None,
        'customerRowsCreated': customer_signup_count,
        'effectiveSignups': signups_count,
        'customerSignupsWithoutAuthRows': customer_signups_without_auth_rows if auth_users_available else None,
        'authSignupsWithoutCustomerRows': auth_signups_without_customer_rows if auth_users_available else None,
        'source': 'supabase_auth_admin' if auth_users_available else ('unavailable' if SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY else 'not_configured'),
    }
    notes = []
    if auth_signups_without_customer_rows:
        notes.append(f'auth_signups_without_customer_rows:{auth_signups_without_customer_rows}')
    if customer_signups_without_auth_rows:
        notes.append(f'customer_signups_without_auth_rows:{customer_signups_without_auth_rows}')
    if waitlist_error:
        notes.append(f'waitlist_count_unavailable:{waitlist_error}')
    if marketing_error:
        notes.append(f'marketing_funnel_unavailable:{marketing_error}')
    if not (SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY):
        notes.append('customer/key funnel read is local-only because Supabase service credentials are not configured')
    rates = {
        'waitlistToSignup': percent_rate(stages['signups'], stages['waitlistLeads']) if stages['waitlistLeads'] is not None else None,
        'managedAccessShareOfWaitlist': percent_rate(stages['managedAccessBetaInterest'], stages['waitlistLeads']) if stages['waitlistLeads'] is not None else None,
        'signupToGeneratedKey': percent_rate(stages['customersWithGeneratedApiKeys'], stages['signups']),
        'generatedKeyToFirstRequest': percent_rate(stages['customersWithFirstRoutedRequest'], stages['customersWithGeneratedApiKeys']),
        'setupCopyToFirstRequest': percent_rate(stages['customersWithFirstRoutedRequest'], stages['setupSnippetCopies']),
        'signupToPaidConversion': percent_rate(stages['paidConversions'], stages['signups']),
        'paidRecentUsage': percent_rate(stages['retainedPaidCustomers'], stages['paidCustomers']),
    }
    mrr = launch_mrr_snapshot(customers)
    checkout_friction = marketing_metrics.get('checkoutFriction') if isinstance(marketing_metrics, dict) else None
    conversion = launch_conversion_snapshot(rates, mrr, checkout_friction)
    activation_follow_ups = launch_activation_follow_ups(
        customers,
        api_keys,
        since=since,
        now=now,
        auth_users=auth_users if auth_users_available else None,
    )
    if isinstance(marketing_metrics, dict):
        activation_follow_ups = {
            **activation_follow_ups,
            'operatorFollowUpCopies': int(marketing_metrics.get('operatorFollowUpCopies') or 0),
            'operatorFollowUpCopiesByKind': marketing_metrics.get('operatorFollowUpCopiesByKind') or {},
            'operatorFollowUpWorked': int(marketing_metrics.get('operatorFollowUpWorked') or 0),
            'operatorFollowUpWorkedByKind': marketing_metrics.get('operatorFollowUpWorkedByKind') or {},
            'operatorFollowUpSendDryRuns': int(marketing_metrics.get('operatorFollowUpSendDryRuns') or 0),
            'operatorFollowUpSendDryRunsByKind': marketing_metrics.get('operatorFollowUpSendDryRunsByKind') or {},
            'operatorFollowUpSendDryRunRecipients': int(marketing_metrics.get('operatorFollowUpSendDryRunRecipients') or 0),
            'operatorFollowUpSends': int(marketing_metrics.get('operatorFollowUpSends') or 0),
            'operatorFollowUpSendsByKind': marketing_metrics.get('operatorFollowUpSendsByKind') or {},
            'operatorFollowUpSentRecipients': int(marketing_metrics.get('operatorFollowUpSentRecipients') or 0),
            'operatorFollowUpSendFailures': int(marketing_metrics.get('operatorFollowUpSendFailures') or 0),
            'operatorFollowUpSendFailuresByKind': marketing_metrics.get('operatorFollowUpSendFailuresByKind') or {},
            'operatorFollowUpSendFailureRecipients': int(marketing_metrics.get('operatorFollowUpSendFailureRecipients') or 0),
            'keyFirstRedirects': int(marketing_metrics.get('keyFirstRedirects') or 0),
            'keyFirstRedirectsByState': marketing_metrics.get('keyFirstRedirectsByState') or {},
            'keyRecoveryViews': int(marketing_metrics.get('keyRecoveryViews') or 0),
            'keyRecoveryViewsByState': marketing_metrics.get('keyRecoveryViewsByState') or {},
            'keyCreateAttempts': int(marketing_metrics.get('keyCreateAttempts') or 0),
            'keyCreateAttemptsByState': marketing_metrics.get('keyCreateAttemptsByState') or {},
            'keyCreateSuccesses': int(marketing_metrics.get('keyCreateSuccesses') or 0),
            'keyCreateSuccessesByState': marketing_metrics.get('keyCreateSuccessesByState') or {},
            'keyCreateFailures': int(marketing_metrics.get('keyCreateFailures') or 0),
            'keyCreateFailuresByState': marketing_metrics.get('keyCreateFailuresByState') or {},
        }
    activation_follow_ups['emailReadiness'] = activation_email_readiness()
    auth_provider_state = launch_auth_provider_state(marketing_metrics)
    next_best_action = launch_next_best_action(
        stages,
        rates,
        mrr,
        activation_follow_ups,
        conversion.get('conversionActions') if isinstance(conversion, dict) else [],
    )
    operator_execution_packet = launch_operator_execution_packet(next_best_action, activation_follow_ups)
    pricing_metadata = {
        **public_launch_metadata(),
        'plans': public_plan_catalog(),
        'agentNativeFeatures': PUBLIC_AGENT_NATIVE_FEATURES,
    }

    return {
        'version': 1,
        'generatedAt': now,
        'windowSeconds': int(window_seconds or 0),
        'source': {
            'customers': 'supabase' if customer_store_uses_supabase() else 'local',
            'apiKeys': 'supabase' if customer_store_uses_supabase() else 'local',
            'authUsers': 'supabase' if auth_users_available else ('unavailable' if SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY else 'not_configured'),
            'routeEvents': event_source,
            'waitlist': 'supabase' if waitlist_count is not None else 'unavailable',
            'marketingFunnel': 'supabase' if marketing_intent_events is not None else 'unavailable',
        },
        'privacy': {
            'containsEmails': False,
            'promptsStored': False,
            'messageBodiesStored': False,
            'containsProviderCredentials': False,
            'containsApiKeys': False,
        },
        'marketingIntent': marketing_metrics,
        'authProviderState': auth_provider_state,
        'acquisitionActions': acquisition_actions,
        'activationFollowUps': activation_follow_ups,
        'nextBestAction': next_best_action,
        'operatorExecutionPacket': operator_execution_packet,
        'pricing': pricing_metadata,
        'stages': stages,
        'signupHydration': signup_hydration,
        'waitlistInterest': waitlist_interest,
        'managedAccessDemand': managed_access_demand,
        'mrr': mrr,
        'rates': rates,
        **conversion,
        'notes': notes,
    }


def mirror_route_event_async(event):
    def worker():
        try:
            write_firestore_route_event(event)
        except Exception as e:
            logger.debug(f'Firestore route event mirror failed: {extract_http_error(e)}')
        try:
            write_supabase_route_event(event)
        except Exception as e:
            logger.debug(f'Supabase route event mirror failed: {extract_http_error(e)}')
    threading.Thread(target=worker, daemon=True).start()


def mirror_analytics_snapshot_async(snapshot):
    def worker():
        try:
            write_supabase_analytics_snapshot(snapshot)
        except Exception as e:
            logger.debug(f'Supabase analytics snapshot mirror failed: {extract_http_error(e)}')
    threading.Thread(target=worker, daemon=True).start()


def percentile(values, pct):
    if not values:
        return None
    values = sorted(float(v) for v in values)
    if len(values) == 1:
        return round(values[0], 2)
    pos = (len(values) - 1) * pct
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return round(values[int(pos)], 2)
    return round(values[lo] + (values[hi] - values[lo]) * (pos - lo), 2)


ANALYTICS_MODEL_PREFIXES = {
    'anthropic', 'claude', 'openai', 'google', 'gemini', 'vertex', 'openrouter',
    'ollama', 'ollama-cloud', 'nvidia', 'nvidia-nim', 'cloudflare', 'workers-ai',
    'xai', 'grok', 'zai', 'darkbloom', 'github', 'copilot', 'codex', 'models',
}


def analytics_model_id(provider, model):
    """Return a stable display/grouping key for analytics model rows.

    Providers often expose chain-like IDs such as
    ``openrouter/anthropic/claude-...`` while another route records
    ``anthropic/claude-...``.  For the analytics UI these are the same
    underlying model, so strip transport/provider namespace segments and group
    repeated models together.  Provider-level rows still preserve provider
    reliability separately.
    """
    parts = [p.strip() for p in str(model or '').split('/') if p.strip()]
    if not parts:
        return 'unknown'
    provider_names = {str(provider or '').strip().lower()}
    provider_names.update(str(name).strip().lower() for name in (PROVIDERS.keys() if isinstance(PROVIDERS, dict) else []))
    while len(parts) > 1:
        head = parts[0].lower()
        if head in ANALYTICS_MODEL_PREFIXES or head in provider_names:
            parts.pop(0)
            continue
        break
    return '/'.join(parts) or str(model or 'unknown')


def provider_model_id(provider, model):
    return f'{provider or "unknown"}/{model or "unknown"}'


def build_analytics_snapshot(window_seconds=7 * 24 * 3600, event_limit=None, customer_id=None):
    """Build provider/model performance analytics for the paid observability layer."""
    now = int(time.time())
    since = now - int(window_seconds or 0) if window_seconds else 0
    durable_events = read_firestore_route_events(window_seconds, event_limit)
    source = 'firestore' if durable_events else 'local'
    if not durable_events:
        durable_events = read_supabase_route_events(window_seconds, event_limit)
        source = 'supabase' if durable_events else 'local'
    events = durable_events or [e for e in read_recent_route_events(event_limit) if int(e.get('ts', 0) or 0) >= since]
    if customer_id:
        events = [e for e in events if str(e.get('customer_id') or '') == str(customer_id)]
    provider_rows = {}
    model_rows = {}
    intent_rows = {}

    def row_for(table, key):
        row = table.setdefault(key, {
            'requests': 0,
            'successes': 0,
            'failures': 0,
            'attempts': 0,
            'attemptFailures': 0,
            'latencies': [],
            'lastSeenAt': 0,
            'providers': set(),
            'providerModels': set(),
        })
        return row

    for event in events:
        event = sanitize_route_event(event)
        status_ok = event.get('status') == 'ok'
        selected = event.get('selected') or {}
        attempts = event.get('attempts') or []
        intent = str(event.get('intent') or 'UNKNOWN')
        total_ms = event.get('totalElapsedMs')
        intent_row = row_for(intent_rows, intent)
        intent_row['requests'] += 1
        intent_row['successes' if status_ok else 'failures'] += 1
        if isinstance(total_ms, (int, float)):
            intent_row['latencies'].append(float(total_ms))
        intent_row['lastSeenAt'] = max(intent_row['lastSeenAt'], int(event.get('ts', 0) or 0))

        if selected:
            provider = selected.get('provider') or 'unknown'
            model = selected.get('model') or 'unknown'
            for table, key in ((provider_rows, provider), (model_rows, analytics_model_id(provider, model))):
                row = row_for(table, key)
                if table is model_rows:
                    row['providers'].add(provider)
                    row['providerModels'].add(provider_model_id(provider, model))
                row['requests'] += 1
                row['successes' if status_ok else 'failures'] += 1
                if isinstance(total_ms, (int, float)):
                    row['latencies'].append(float(total_ms))
                row['lastSeenAt'] = max(row['lastSeenAt'], int(event.get('ts', 0) or 0))

        for attempt in attempts:
            provider = attempt.get('provider') or 'unknown'
            model = attempt.get('model') or 'unknown'
            ok = bool(attempt.get('ok'))
            elapsed = attempt.get('elapsedMs')
            for table, key in ((provider_rows, provider), (model_rows, analytics_model_id(provider, model))):
                row = row_for(table, key)
                if table is model_rows:
                    row['providers'].add(provider)
                    row['providerModels'].add(provider_model_id(provider, model))
                row['attempts'] += 1
                if not ok:
                    row['attemptFailures'] += 1
                if isinstance(elapsed, (int, float)):
                    row['latencies'].append(float(elapsed))

    for intent, providers in (LATENCY_STATS.get('intents') or {}).items():
        for provider, models in (providers or {}).items():
            for model, stat in (models or {}).items():
                for table, row_key in ((provider_rows, provider), (model_rows, analytics_model_id(provider, model))):
                    row = row_for(table, row_key)
                    if table is model_rows:
                        row['providers'].add(provider)
                        row['providerModels'].add(provider_model_id(provider, model))
                    successes = int(stat.get('successes', 0) or 0)
                    failures = int(stat.get('failures', 0) or 0)
                    if row['requests'] == 0:
                        row['successes'] += successes
                        row['failures'] += failures
                        row['requests'] += successes + failures
                    ewma = stat.get('latency_ewma_ms')
                    if isinstance(ewma, (int, float)):
                        row['latencies'].append(float(ewma))
                    row['lastSeenAt'] = max(row['lastSeenAt'], int(stat.get('updated_at', 0) or 0))

    def finalize(table, include_model_fields=False):
        out = []
        for key, row in table.items():
            requests = int(row['requests'])
            successes = int(row['successes'])
            failures = int(row['failures'])
            attempts = int(row['attempts'])
            attempt_failures = int(row['attemptFailures'])
            lats = row.pop('latencies', [])
            success_rate = (successes / requests) if requests else None
            attempt_failure_rate = (attempt_failures / attempts) if attempts else None
            item = {
                'id': key,
                'requests': requests,
                'successes': successes,
                'failures': failures,
                'successRate': round(success_rate, 4) if success_rate is not None else None,
                'attempts': attempts,
                'attemptFailureRate': round(attempt_failure_rate, 4) if attempt_failure_rate is not None else None,
                'p50Ms': percentile(lats, 0.50),
                'p95Ms': percentile(lats, 0.95),
                'avgMs': round(sum(lats) / len(lats), 2) if lats else None,
                'lastSeenAt': row.get('lastSeenAt') or None,
            }
            if include_model_fields:
                item['providers'] = sorted(row.get('providers') or [])
                item['providerModels'] = sorted(row.get('providerModels') or [])
            out.append(item)
        return sorted(out, key=lambda x: (-(x.get('successRate') or 0), x.get('p50Ms') or 999999, -x.get('requests', 0)))

    models = finalize(model_rows, include_model_fields=True)
    providers = finalize(provider_rows)
    intents = finalize(intent_rows)
    best_fast = [m for m in models if m.get('successRate') is not None and m.get('p50Ms') is not None][:10]
    most_reliable = sorted(models, key=lambda x: (-(x.get('successRate') or 0), -(x.get('requests') or 0), x.get('p95Ms') or 999999))[:10]
    degraded = sorted([m for m in models if (m.get('attemptFailureRate') or 0) > 0 or (m.get('successRate') is not None and m.get('successRate') < 0.95)], key=lambda x: (-(x.get('attemptFailureRate') or 0), x.get('successRate') or 0))[:10]

    snapshot = {
        'version': 2,
        'generatedAt': now,
        'windowSeconds': int(window_seconds or 0),
        'eventsAnalyzed': len(events),
        'source': source,
        'scope': {'customer_id': str(customer_id)} if customer_id else {'customer_id': None},
        'privacy': {
            'promptsStored': False,
            'messageBodiesStored': False,
            'containsProviderCredentials': False,
        },
        'providers': providers,
        'models': models,
        'intents': intents,
        'recommendations': {
            'fastestModels': best_fast,
            'mostReliableModels': most_reliable,
            'degradedModels': degraded,
        },
    }
    mirror_analytics_snapshot_async(snapshot)
    return snapshot


def supabase_user_for_bearer(token):
    if not (SUPABASE_AUTH_ENABLED and SUPABASE_URL and SUPABASE_ANON_KEY and token):
        return None
    try:
        req = urllib.request.Request(SUPABASE_URL.rstrip('/') + '/auth/v1/user', headers={
            'apikey': SUPABASE_ANON_KEY,
            'Authorization': f'Bearer {token}',
        })
        with urllib.request.urlopen(req, timeout=6) as resp:
            user = json.loads(resp.read().decode('utf-8'))
        return user if isinstance(user, dict) and user.get('id') else None
    except Exception as e:
        logger.debug(f'Supabase auth validation failed: {extract_http_error(e)}')
        return None


def bearer_token(handler):
    auth = handler.headers.get('Authorization') or ''
    return auth[7:].strip() if auth.lower().startswith('bearer ') else ''


def now_epoch():
    return int(time.time())


def local_customer_store():
    try:
        with open(CUSTOMER_STORE_PATH) as f:
            data = json.load(f)
        if isinstance(data, dict):
            data.setdefault('customers', [])
            data.setdefault('api_keys', [])
            data.setdefault('payment_intents', [])
            data.setdefault('operator_audit_events', [])
            return data
    except FileNotFoundError:
        pass
    except Exception as e:
        logger.debug(f'Local customer store read failed: {e}')
    return {'customers': [], 'api_keys': [], 'payment_intents': [], 'operator_audit_events': []}


def write_local_customer_store(data):
    os.makedirs(os.path.dirname(CUSTOMER_STORE_PATH), exist_ok=True)
    tmp = CUSTOMER_STORE_PATH + '.tmp'
    with open(tmp, 'w') as f:
        json.dump(data, f, indent=2, sort_keys=True)
    os.replace(tmp, CUSTOMER_STORE_PATH)


def customer_store_uses_supabase():
    return bool(SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY)


def supabase_select(table, query, timeout=8):
    return supabase_request(f'/rest/v1/{table}?{query}', service=True, timeout=timeout) or []


def supabase_insert(table, row, timeout=8):
    return supabase_request(
        f'/rest/v1/{table}',
        method='POST',
        body=row,
        service=True,
        extra_headers={'Prefer': 'return=representation'},
        timeout=timeout,
    ) or []


def supabase_patch(table, row_id, updates, timeout=8):
    quoted = urllib.parse.quote(str(row_id), safe='')
    return supabase_request(
        f'/rest/v1/{table}?id=eq.{quoted}',
        method='PATCH',
        body=updates,
        service=True,
        extra_headers={'Prefer': 'return=representation'},
        timeout=timeout,
    ) or []


def normalize_customer(row):
    if not isinstance(row, dict):
        return None
    row = dict(row)
    row.setdefault('plan', 'free')
    row.setdefault('status', 'inactive')
    row.setdefault('created_at_epoch', now_epoch())
    row.setdefault('updated_at_epoch', row.get('created_at_epoch') or now_epoch())
    return row


def public_customer(row):
    row = normalize_customer(row) or {}
    return {
        'id': row.get('id'),
        'user_id': row.get('user_id'),
        'email': row.get('email'),
        'plan': row.get('plan') or 'free',
        'status': row.get('status') or 'inactive',
        'stripe_customer_id': row.get('stripe_customer_id') or '',
        'stripe_subscription_id': row.get('stripe_subscription_id') or '',
        'created_at_epoch': row.get('created_at_epoch'),
        'updated_at_epoch': row.get('updated_at_epoch'),
    }


def account_usage_for_customer(customer):
    customer = normalize_customer(customer) or {}
    plan = str(customer.get('plan') or 'free').lower()
    rate_limits = parse_public_plan_limits(PUBLIC_PLAN_RATE_LIMITS_RAW)
    monthly_quotas = parse_public_plan_limits(PUBLIC_PLAN_MONTHLY_QUOTAS_RAW)
    period = current_usage_period()
    quota = limit_for_public_plan(plan, monthly_quotas, 0)
    rate_limit = limit_for_public_plan(plan, rate_limits, 0)
    requests = 0
    updated_at = None
    if customer_store_uses_supabase() and customer.get('id'):
        try:
            customer_id = urllib.parse.quote(str(customer.get('id')), safe='')
            quoted_period = urllib.parse.quote(period, safe='')
            rows = supabase_select(
                SUPABASE_USAGE_COUNTERS_TABLE,
                f'select=*&customer_id=eq.{customer_id}&period=eq.{quoted_period}&limit=1',
                timeout=5,
            )
            if rows:
                requests = max(0, int(rows[0].get('requests') or 0))
                updated_at = rows[0].get('updated_at_epoch')
        except Exception as e:
            logger.warning(f'Customer usage lookup failed: {extract_http_error(e)}')
    remaining = max(quota - requests, 0) if quota > 0 else None
    return {
        'customer_id': customer.get('id') or '',
        'period': period,
        'plan': plan,
        'status': customer.get('status') or 'inactive',
        'requests': requests,
        'quota': quota,
        'remaining': remaining,
        'unlimited': quota <= 0,
        'rateLimitPerMinute': rate_limit,
        'routing_enabled': customer_is_active(customer),
        'updated_at_epoch': updated_at,
    }


def customer_is_active(customer):
    status = str((customer or {}).get('status') or '').lower()
    plan = str((customer or {}).get('plan') or '').lower()
    return status in {'active', 'trialing', 'manual', 'paid'} and plan not in {'', 'free', 'inactive'}


def customer_for_user(user, create=True):
    if not user or not user.get('id'):
        return None
    # Router does not collect user identities unless the operator has
    # explicitly enabled the hosted billing tier.
    if not (SUPABASE_AUTH_ENABLED or os.environ.get('SAGE_ROUTER_BILLING_ENABLED', '0').strip().lower() in {'1', 'true', 'yes', 'on'}):
        return None
    user_id = str(user.get('id'))
    email = user.get('email') or ((user.get('user_metadata') or {}).get('email'))
    if customer_store_uses_supabase():
        quoted = urllib.parse.quote(user_id, safe='')
        rows = supabase_select(SUPABASE_CUSTOMERS_TABLE, f'select=*&user_id=eq.{quoted}&limit=1')
        if rows:
            return normalize_customer(rows[0])
        if not create:
            return None
        row = {
            'id': uuid.uuid4().hex,
            'user_id': user_id,
            'email': email,
            'plan': 'free',
            'status': 'inactive',
            'created_at_epoch': now_epoch(),
            'updated_at_epoch': now_epoch(),
        }
        rows = supabase_insert(SUPABASE_CUSTOMERS_TABLE, row)
        return normalize_customer(rows[0] if rows else row)

    data = local_customer_store()
    for row in data.get('customers', []):
        if row.get('user_id') == user_id:
            return normalize_customer(row)
    if not create:
        return None
    row = {
        'id': uuid.uuid4().hex,
        'user_id': user_id,
        'email': email,
        'plan': 'free',
        'status': 'inactive',
        'created_at_epoch': now_epoch(),
        'updated_at_epoch': now_epoch(),
    }
    data['customers'].append(row)
    write_local_customer_store(data)
    return normalize_customer(row)


def api_key_hash(raw_key):
    material = (API_KEY_HASH_PEPPER + raw_key).encode('utf-8')
    return hashlib.sha256(material).hexdigest()


def generate_api_key():
    return API_KEY_PREFIX + secrets.token_urlsafe(32)


def key_prefix(raw_key):
    return raw_key[:16]


def public_api_key(row, customer=None):
    customer = normalize_customer(customer) if customer else None
    effective_plan = (customer or {}).get('plan') or row.get('plan') or ''
    customer_status = (customer or {}).get('status') or ''
    return {
        'id': row.get('id'),
        'name': row.get('name') or '',
        'prefix': row.get('prefix') or '',
        'status': row.get('status') or 'active',
        'plan': effective_plan,
        'key_plan': row.get('plan') or '',
        'customer_status': customer_status,
        'routing_enabled': bool(customer_is_active(customer)),
        'created_at_epoch': row.get('created_at_epoch'),
        'last_used_at_epoch': row.get('last_used_at_epoch'),
        'revoked_at_epoch': row.get('revoked_at_epoch'),
    }


def api_keys_for_customer(customer_id):
    if customer_store_uses_supabase():
        quoted = urllib.parse.quote(str(customer_id), safe='')
        return supabase_select(SUPABASE_API_KEYS_TABLE, f'select=*&customer_id=eq.{quoted}&order=created_at_epoch.desc')
    data = local_customer_store()
    return [r for r in data.get('api_keys', []) if r.get('customer_id') == customer_id]


def active_api_key_count_for_customer(customer_id):
    return sum(1 for row in api_keys_for_customer(customer_id) if (row.get('status') or 'active') == 'active')


def account_activation_for_customer(customer, usage=None, api_keys=None):
    customer = normalize_customer(customer) or {}
    usage = usage or account_usage_for_customer(customer)
    if api_keys is None:
        api_keys = api_keys_for_customer(customer.get('id')) if customer.get('id') else []
    active_keys = [row for row in (api_keys or []) if (row.get('status') or 'active') == 'active']
    routing_enabled = bool(usage.get('routing_enabled'))
    requests = max(0, int(usage.get('requests') or 0))
    quota = max(0, int(usage.get('quota') or 0))
    quota_used_percent = None
    if quota > 0:
        quota_used_percent = min(100, max(0, round((requests / quota) * 100, 2)))
    if not active_keys:
        next_action = 'create_key'
    elif not routing_enabled:
        next_action = 'choose_plan'
    elif requests <= 0:
        next_action = 'send_first_request'
    elif quota_used_percent is not None and quota_used_percent >= 90:
        next_action = 'upgrade_before_quota'
    elif quota_used_percent is not None and quota_used_percent >= 75:
        next_action = 'watch_quota'
    else:
        next_action = 'monitor_usage'
    return {
        'plan': usage.get('plan') or customer.get('plan') or 'free',
        'status': usage.get('status') or customer.get('status') or 'inactive',
        'routingEnabled': routing_enabled,
        'keyCount': len(api_keys or []),
        'activeKeyCount': len(active_keys),
        'requestCount': requests,
        'firstRequestComplete': requests > 0,
        'quota': quota,
        'quotaUsedPercent': quota_used_percent,
        'nextAction': next_action,
    }


def launch_activation_follow_up_url(plan='pro', auth='github'):
    plan = normalize_stripe_plan(plan) or 'pro'
    params = {
        'start': 'create_key',
        'plan': plan,
        'utm_source': 'operator',
        'utm_medium': 'launch_funnel',
        'utm_campaign': 'signup_to_key_recovery',
    }
    path = 'account.html'
    if auth is False:
        path = 'login.html'
        params['auth'] = 'email'
    else:
        auth_value = str(auth or 'github').strip().lower()
        if auth_value in {'password', 'email', 'email_password', 'password_fallback', 'fallback', 'none'}:
            path = 'login.html'
            params['auth'] = 'email'
        else:
            params['auth'] = auth_value
    query = urllib.parse.urlencode(params)
    return f'{APP_BASE_URL.rstrip("/")}/{path}?{query}'


def launch_activation_follow_up_urls(plan='pro'):
    plan = normalize_stripe_plan(plan) or 'pro'
    return {
        'githubOAuth': launch_activation_follow_up_url(plan, auth='github'),
        'passwordFallback': launch_activation_follow_up_url(plan, auth=False),
    }


def operator_customer_follow_up(customer, activation=None, email_verification=None):
    customer = normalize_customer(customer) or {}
    activation = activation or account_activation_for_customer(customer)
    plan = normalize_stripe_plan(customer.get('plan') or activation.get('plan') or 'pro') or 'pro'
    urls = launch_activation_follow_up_urls(plan)
    verification_bucket = auth_verification_bucket(email_verification or auth_verification_state_for_customer(customer))
    return {
        'nextAction': activation.get('nextAction') or 'create_key',
        'suggestedPlan': plan,
        'primaryCtaKind': 'same_email_password',
        'primaryCtaUrl': urls['passwordFallback'],
        'passwordFallback': urls['passwordFallback'],
        'githubOAuth': urls['githubOAuth'],
        'recommendedCtaOrder': ['passwordFallback', 'githubOAuth'],
        'emailVerificationSegment': verification_bucket,
        'utmCampaign': 'signup_to_key_recovery',
        'privacy': {
            'containsEmails': False,
            'containsCustomerIds': False,
            'containsApiKeys': False,
            'containsProviderCredentials': False,
        },
    }


def operator_activation_contact_subject(segment):
    return (
        'Verify email, then finish your Sage Router setup key'
        if str(segment or '').lower() == 'unverified'
        else 'Finish your Sage Router setup key'
    )


def operator_activation_contact_body(plan, urls, segment):
    plan = normalize_stripe_plan(plan) or 'pro'
    segment = str(segment or 'all').lower()
    password_url = (urls or {}).get('passwordFallback') or launch_activation_follow_up_url(plan, auth=False)
    github_url = (urls or {}).get('githubOAuth') or launch_activation_follow_up_url(plan, auth='github')
    intro = (
        'You already started Sage Router setup, but email verification and the hosted API key step are not complete yet.'
        if segment == 'unverified'
        else 'You already started Sage Router setup, but the hosted API key step is not complete yet.'
    )
    next_step = (
        'Next step: use the same email you signed up with, verify it if prompted, then create the generated sk_sage setup key before checkout or routing setup:'
        if segment == 'unverified'
        else 'Next step: use the same email you signed up with, then create the generated sk_sage setup key before checkout or routing setup:'
    )
    return '\n'.join([
        intro,
        '',
        next_step,
        password_url,
        '',
        'Use GitHub/OAuth only if it is the same account you used before:',
        github_url,
        '',
        f'Suggested path: {plan.upper()} activation -> generated key -> /v1/models verification -> first Responses API request.',
        '',
        'Boundary: do not send prompts, provider credentials, OAuth tokens, generated API keys, private keys, cookies, or raw provider responses.',
    ])


def operator_activation_contact_csv(contacts):
    rows = [[
        'email',
        'segment',
        'plan',
        'next_action',
        'same_email_recovery_url',
        'github_oauth_url',
        'subject',
    ]]
    for contact in contacts or []:
        rows.append([
            contact.get('email') or '',
            contact.get('emailVerificationSegment') or '',
            contact.get('suggestedPlan') or '',
            contact.get('nextAction') or '',
            contact.get('passwordFallback') or '',
            contact.get('githubOAuth') or '',
            contact.get('subject') or '',
        ])

    def cell(value):
        text = str(value if value is not None else '').replace('"', '""')
        return f'"{text}"' if re.search(r'[",\n\r]', text) else text

    return '\n'.join(','.join(cell(value) for value in row) for row in rows)


def operator_activation_contact_export(customers):
    contacts = []
    segments = {}
    plan_counts = {}
    for customer in customers or []:
        customer = normalize_customer(customer)
        if not customer or str(customer.get('status') or '').lower() == 'suspended':
            continue
        email = str(customer.get('email') or '').strip()
        if not email:
            continue
        keys = api_keys_for_customer(customer.get('id')) if customer.get('id') else []
        usage = account_usage_for_customer(customer)
        activation = account_activation_for_customer(customer, usage=usage, api_keys=keys)
        if activation.get('nextAction') != 'create_key' or int(activation.get('activeKeyCount') or 0) > 0:
            continue
        email_verification = auth_verification_state_for_customer(customer)
        follow_up = operator_customer_follow_up(customer, activation=activation, email_verification=email_verification)
        segment = follow_up.get('emailVerificationSegment') or auth_verification_bucket(email_verification)
        plan = follow_up.get('suggestedPlan') or 'pro'
        subject = operator_activation_contact_subject(segment)
        urls = {
            'passwordFallback': follow_up.get('passwordFallback') or follow_up.get('primaryCtaUrl'),
            'githubOAuth': follow_up.get('githubOAuth'),
        }
        contacts.append({
            'sendOrder': len(contacts) + 1,
            'email': email,
            'emailVerificationSegment': segment,
            'emailVerified': bool(email_verification.get('verified')),
            'suggestedPlan': plan,
            'nextAction': activation.get('nextAction') or 'create_key',
            'subject': subject,
            'body': operator_activation_contact_body(plan, urls, segment),
            'passwordFallback': urls['passwordFallback'],
            'githubOAuth': urls['githubOAuth'],
        })
        segments[segment] = segments.get(segment, 0) + 1
        plan_counts[plan] = plan_counts.get(plan, 0) + 1
    contacts.sort(key=lambda row: (str(row.get('emailVerificationSegment') or ''), row.get('email') or ''))
    for idx, contact in enumerate(contacts, start=1):
        contact['sendOrder'] = idx
    return {
        'kind': 'activation_contact_export',
        'contacts': contacts,
        'count': len(contacts),
        'segments': segments,
        'plans': plan_counts,
        'csv': operator_activation_contact_csv(contacts),
        'privacy': {
            'operatorOnly': True,
            'explicitContactExport': True,
            'containsEmails': True,
            'containsCustomerIds': False,
            'containsRawApiKeys': False,
            'containsApiKeys': False,
            'containsApiKeyHashes': False,
            'containsProviderCredentials': False,
            'containsPrompts': False,
            'containsRawProviderResponses': False,
        },
        'telemetry': {
            'copyEvents': ['operator_no_key_contact_export_copied'],
            'workedEvents': ['operator_no_key_contact_export_marked_worked'],
            'recoveryViewEvents': ['account_key_recovery_viewed'],
            'keyCreateAttemptEvents': ['account_api_key_create_clicked'],
            'keyCreateSuccessEvents': ['account_key_recovery_key_created'],
        },
    }


def activation_email_configured():
    if ACTIVATION_EMAIL_PROVIDER == 'resend':
        return bool(ACTIVATION_EMAIL_API_KEY and ACTIVATION_EMAIL_FROM)
    if ACTIVATION_EMAIL_PROVIDER == 'supabase-recovery':
        return bool(SUPABASE_URL and SUPABASE_ANON_KEY and ACTIVATION_EMAIL_REDIRECT_TO)
    return False


def activation_email_provider_label():
    if ACTIVATION_EMAIL_PROVIDER == 'supabase-recovery':
        return 'supabase-recovery'
    return ACTIVATION_EMAIL_PROVIDER or 'resend'


def activation_followup_send_command(segment='all', dry_run=True, limit=None):
    segment = re.sub(r'[^a-z0-9_.-]+', '_', str(segment or 'all').strip().lower()) or 'all'
    max_limit = max(1, min(int(limit or ACTIVATION_EMAIL_MAX_BATCH), ACTIVATION_EMAIL_MAX_BATCH))
    payload = {
        'status': 'inactive',
        'segment': segment,
        'limit': max_limit,
        'dryRun': bool(dry_run),
    }
    if not dry_run:
        payload['sendConfirmation'] = ACTIVATION_FOLLOWUP_SEND_CONFIRMATION
    command = (
        'curl -fsS -X POST https://api.sagerouter.dev/admin/customers/send-activation-followups \\\n'
        '  -H "Authorization: Bearer ${SAGE_ROUTER_API_KEY}" \\\n'
        '  -H "Origin: https://app.sagerouter.dev" \\\n'
        '  -H "Content-Type: application/json" \\\n'
        f"  --data '{json.dumps(payload, separators=(',', ':'))}'"
    )
    if dry_run:
        command += " \\\n  | jq '{configured,dryRun,queued,sent,failed,segments,plans}'"
    return command


def activation_email_readiness():
    configured = activation_email_configured()
    provider = activation_email_provider_label()
    setup_command = ''
    if not configured:
        if provider == 'supabase-recovery':
            setup_command = (
                "SAGE_ROUTER_ACTIVATION_EMAIL_PROVIDER='supabase-recovery' \\\n"
                "SAGE_ROUTER_ACTIVATION_EMAIL_REDIRECT_TO='https://app.sagerouter.dev/account?activation=recovery' \\\n"
                "scripts/configure_activation_email_sender.sh"
            )
        else:
            setup_command = (
                "SAGE_ROUTER_ACTIVATION_EMAIL_FROM='Sage Router <activation@sagerouter.dev>' \\\n"
                "SAGE_ROUTER_RESEND_API_KEY='re_...' \\\n"
                "SAGE_ROUTER_ACTIVATION_EMAIL_REPLY_TO='support@sagerouter.dev' \\\n"
                "scripts/configure_activation_email_sender.sh"
            )
    dry_run_command = activation_followup_send_command(segment='all', dry_run=True)
    send_command_template = activation_followup_send_command(segment='all', dry_run=False)
    segment_command_templates = {
        segment: {
            'dryRunCommand': activation_followup_send_command(segment=segment, dry_run=True),
            'sendCommand': activation_followup_send_command(segment=segment, dry_run=False),
        }
        for segment in ('verified', 'unverified')
    }
    segment_command_templates['all'] = {
        'dryRunCommand': dry_run_command,
        'sendCommand': send_command_template,
    }
    return {
        'provider': provider,
        'configured': configured,
        'sendEndpoint': '/admin/customers/send-activation-followups',
        'dryRunSupported': True,
        'sendConfirmation': ACTIVATION_FOLLOWUP_SEND_CONFIRMATION,
        'dryRunCommand': dry_run_command,
        'sendCommandTemplate': send_command_template,
        'segmentCommandTemplates': segment_command_templates,
        'sendsEmailWhenConfigured': configured,
        'fromConfigured': bool(ACTIVATION_EMAIL_FROM),
        'apiKeyConfigured': bool(ACTIVATION_EMAIL_API_KEY) if provider == 'resend' else bool(SUPABASE_ANON_KEY),
        'replyToConfigured': bool(ACTIVATION_EMAIL_REPLY_TO),
        'supabaseConfigured': bool(SUPABASE_URL and SUPABASE_ANON_KEY),
        'recoveryRedirectConfigured': bool(ACTIVATION_EMAIL_REDIRECT_TO),
        'maxBatch': ACTIVATION_EMAIL_MAX_BATCH,
        'requiredEnv': [] if configured else (
            [
                'SAGE_ROUTER_SUPABASE_URL',
                'SAGE_ROUTER_SUPABASE_ANON_KEY',
                'SAGE_ROUTER_ACTIVATION_EMAIL_PROVIDER=supabase-recovery',
            ]
            if provider == 'supabase-recovery' else [
                'SAGE_ROUTER_ACTIVATION_EMAIL_FROM',
                'SAGE_ROUTER_RESEND_API_KEY or SAGE_ROUTER_ACTIVATION_EMAIL_API_KEY',
            ]
        ),
        'secretManagerNames': [] if configured else (
            ['SAGE_ROUTER_SUPABASE_ANON_KEY']
            if provider == 'supabase-recovery' else [
                'SAGE_ROUTER_ACTIVATION_EMAIL_FROM',
                'SAGE_ROUTER_RESEND_API_KEY',
                'SAGE_ROUTER_ACTIVATION_EMAIL_REPLY_TO',
            ]
        ),
        'setupCommand': setup_command,
        'setupScript': 'scripts/configure_activation_email_sender.sh',
        'operatorAction': (
            'Use Send from the operator dashboard after dry-run verification.'
            if configured
            else 'Configure the activation email sender or use the mailto/copy fallback for signup-to-key recovery.'
        ),
        'privacy': {
            'containsSecrets': False,
            'containsApiKeyValues': False,
            'containsProviderCredentials': False,
            'containsEmails': False,
        },
    }


def public_activation_email_readiness():
    readiness = activation_email_readiness()
    setup_script = readiness.get('setupScript') or 'scripts/configure_activation_email_sender.sh'
    return {
        'provider': readiness.get('provider') or 'resend',
        'configured': bool(readiness.get('configured')),
        'sendsEmailWhenConfigured': bool(readiness.get('sendsEmailWhenConfigured')),
        'dryRunSupported': bool(readiness.get('dryRunSupported')),
        'fromConfigured': bool(readiness.get('fromConfigured')),
        'apiKeyConfigured': bool(readiness.get('apiKeyConfigured')),
        'replyToConfigured': bool(readiness.get('replyToConfigured')),
        'supabaseConfigured': bool(readiness.get('supabaseConfigured')),
        'recoveryRedirectConfigured': bool(readiness.get('recoveryRedirectConfigured')),
        'maxBatch': readiness.get('maxBatch'),
        'sendConfirmationRequired': True,
        'sendConfirmation': readiness.get('sendConfirmation') or ACTIVATION_FOLLOWUP_SEND_CONFIRMATION,
        'requiredEnv': readiness.get('requiredEnv') or [],
        'secretManagerNames': readiness.get('secretManagerNames') or [],
        'setupScript': setup_script,
        'setupCheckCommand': f'{setup_script} --check',
        'operatorAction': readiness.get('operatorAction') or '',
        'fallback': 'copy_mailto_operator_packet',
        'privacy': {
            'containsSecrets': False,
            'containsApiKeyValues': False,
            'containsProviderCredentials': False,
            'containsEmails': False,
            'containsAdminCommands': False,
        },
    }


def send_activation_email(contact):
    if ACTIVATION_EMAIL_PROVIDER == 'supabase-recovery':
        if not activation_email_configured():
            raise RuntimeError('activation_email_not_configured')
        email = str(contact.get('email') or '').strip()
        if not email:
            raise RuntimeError('activation_email_missing_recipient')
        query = ''
        if ACTIVATION_EMAIL_REDIRECT_TO:
            query = '?redirect_to=' + urllib.parse.quote(ACTIVATION_EMAIL_REDIRECT_TO, safe='')
        req = urllib.request.Request(
            SUPABASE_URL.rstrip('/') + '/auth/v1/recover' + query,
            data=json.dumps({'email': email}).encode('utf-8'),
            headers={
                'apikey': SUPABASE_ANON_KEY,
                'Authorization': f'Bearer {SUPABASE_ANON_KEY}',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'User-Agent': 'sage-router-activation-followup/1.0',
            },
            method='POST',
        )
        with urllib.request.urlopen(req, timeout=12) as resp:
            raw = resp.read().decode('utf-8')
            try:
                body = json.loads(raw) if raw else {}
            except Exception:
                body = {}
            return {
                'status': resp.status,
                'provider': 'supabase-recovery',
                'id': body.get('id') or body.get('message_id'),
            }
    if ACTIVATION_EMAIL_PROVIDER != 'resend':
        raise RuntimeError('activation_email_provider_unsupported')
    if not activation_email_configured():
        raise RuntimeError('activation_email_not_configured')
    payload = {
        'from': ACTIVATION_EMAIL_FROM,
        'to': [contact.get('email') or ''],
        'subject': contact.get('subject') or operator_activation_contact_subject(contact.get('emailVerificationSegment')),
        'text': contact.get('body') or '',
    }
    if ACTIVATION_EMAIL_REPLY_TO:
        payload['reply_to'] = [ACTIVATION_EMAIL_REPLY_TO]
    idempotency_source = json.dumps(
        {
            'to': contact.get('email') or '',
            'subject': payload.get('subject') or '',
            'text': payload.get('text') or '',
        },
        sort_keys=True,
        separators=(',', ':'),
    )
    idempotency_key = 'sage-router-activation-' + hashlib.sha256(idempotency_source.encode('utf-8')).hexdigest()
    req = urllib.request.Request(
        'https://api.resend.com/emails',
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {ACTIVATION_EMAIL_API_KEY}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Idempotency-Key': idempotency_key,
            'User-Agent': 'sage-router-activation-followup/1.0',
        },
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=12) as resp:
        raw = resp.read().decode('utf-8')
        try:
            body = json.loads(raw) if raw else {}
        except Exception:
            body = {}
        return {
            'status': resp.status,
            'provider': 'resend',
            'id': body.get('id'),
        }


def operator_activation_followup_send(customers, segment='', limit=25, dry_run=False):
    export = operator_activation_contact_export(customers)
    requested_segment = str(segment or '').strip().lower()
    max_limit = max(1, min(int(limit or ACTIVATION_EMAIL_MAX_BATCH), ACTIVATION_EMAIL_MAX_BATCH))
    contacts = export.get('contacts') or []
    if requested_segment and requested_segment not in {'all', '*'}:
        contacts = [
            contact for contact in contacts
            if str(contact.get('emailVerificationSegment') or '').strip().lower() == requested_segment
        ]
    contacts = contacts[:max_limit]
    configured = activation_email_configured()
    result = {
        'kind': 'activation_followup_send',
        'provider': ACTIVATION_EMAIL_PROVIDER or 'resend',
        'configured': configured,
        'dryRun': bool(dry_run),
        'requestedSegment': requested_segment or 'all',
        'limit': max_limit,
        'queued': len(contacts),
        'sent': 0,
        'failed': 0,
        'results': [],
        'segments': {},
        'plans': {},
        'privacy': {
            'operatorOnly': True,
            'containsEmails': True,
            'containsCustomerIds': False,
            'containsRawApiKeys': False,
            'containsApiKeys': False,
            'containsApiKeyHashes': False,
            'containsProviderCredentials': False,
            'containsPrompts': False,
            'containsRawProviderResponses': False,
            'sendsEmailWhenConfigured': configured and not dry_run,
        },
    }
    for contact in contacts:
        segment_name = contact.get('emailVerificationSegment') or 'unknown'
        plan = contact.get('suggestedPlan') or 'pro'
        result['segments'][segment_name] = result['segments'].get(segment_name, 0) + 1
        result['plans'][plan] = result['plans'].get(plan, 0) + 1
        row = {
            'sendOrder': contact.get('sendOrder'),
            'email': contact.get('email'),
            'segment': segment_name,
            'emailVerificationSegment': segment_name,
            'suggestedPlan': plan,
            'subject': contact.get('subject'),
        }
        if dry_run:
            row['status'] = 'dry_run'
            result['results'].append(row)
            continue
        if not configured:
            row['status'] = 'not_configured'
            result['failed'] += 1
            result['results'].append(row)
            continue
        try:
            sent = send_activation_email(contact)
            row.update({'status': 'sent', 'providerMessageId': sent.get('id')})
            result['sent'] += 1
        except Exception as e:
            logger.warning(f'Activation follow-up send failed: {extract_http_error(e)}')
            row.update({'status': 'failed', 'error': 'activation_email_send_failed'})
            result['failed'] += 1
        result['results'].append(row)
    if not configured and not dry_run:
        result['error'] = 'activation_email_not_configured'
        result['requiredEnv'] = [
            'SAGE_ROUTER_ACTIVATION_EMAIL_FROM',
            'SAGE_ROUTER_RESEND_API_KEY or SAGE_ROUTER_ACTIVATION_EMAIL_API_KEY',
        ]
    return result


def launch_activation_follow_ups(customers, api_keys, since=0, now=None, auth_users=None):
    """Return privacy-safe aggregate follow-ups for signups blocked before key creation."""
    now = int(now or now_epoch())
    keys_by_customer = {}
    for row in api_keys or []:
        customer_id = str((row or {}).get('customer_id') or '')
        if customer_id:
            keys_by_customer.setdefault(customer_id, []).append(row)

    counts_by_status = {}
    counts_by_plan = {}
    counts_by_email_verification = {}
    total = 0
    windowed_new_signups = 0
    oldest_created_at = None
    newest_created_at = None
    for customer in customers or []:
        customer = normalize_customer(customer)
        if not customer or str(customer.get('status') or '').lower() == 'suspended':
            continue
        customer_id = str(customer.get('id') or '')
        activation = account_activation_for_customer(
            customer,
            api_keys=keys_by_customer.get(customer_id, []),
        )
        if activation.get('nextAction') != 'create_key' or int(activation.get('activeKeyCount') or 0) > 0:
            continue
        total += 1
        status = str(customer.get('status') or activation.get('status') or 'inactive').lower() or 'unknown'
        plan = str(customer.get('plan') or activation.get('plan') or 'free').lower() or 'free'
        suggested_plan = plan if plan in {'lite', 'pro', 'max'} else 'pro'
        verification_bucket = auth_verification_bucket(auth_verification_state_for_customer(customer, auth_users=auth_users))
        counts_by_status[status] = counts_by_status.get(status, 0) + 1
        counts_by_plan[suggested_plan] = counts_by_plan.get(suggested_plan, 0) + 1
        counts_by_email_verification[verification_bucket] = counts_by_email_verification.get(verification_bucket, 0) + 1
        created_at = row_epoch(customer, 'created_at_epoch', 'created_at')
        if in_epoch_window(created_at, since, now):
            windowed_new_signups += 1
        if created_at:
            oldest_created_at = created_at if oldest_created_at is None else min(oldest_created_at, created_at)
            newest_created_at = created_at if newest_created_at is None else max(newest_created_at, created_at)

    primary_plan = 'pro'
    if counts_by_plan:
        primary_plan = sorted(counts_by_plan.items(), key=lambda item: (-item[1], item[0]))[0][0]
    delivery_counts = launch_activation_delivery_counts(
        counts=counts_by_email_verification,
        total=total,
    )
    return {
        'total': total,
        **delivery_counts,
        'windowedNewSignups': windowed_new_signups,
        'nextAction': 'create_key',
        'suggestedPlan': primary_plan,
        'countsBySuggestedPlan': counts_by_plan,
        'countsByStatus': counts_by_status,
        'countsByEmailVerification': counts_by_email_verification,
        'oldestCreatedAtEpoch': oldest_created_at,
        'newestCreatedAtEpoch': newest_created_at,
        'primaryCtaUrl': launch_activation_follow_up_url(primary_plan, auth=False),
        'primaryCtaKind': 'same_email_password',
        'recommendedCtaOrder': ['passwordFallback', 'githubOAuth'],
        'primaryCtaUrls': launch_activation_follow_up_urls(primary_plan),
        'recommendedOperatorAction': 'Send the no-secret generated-key-first follow-up before asking for checkout or routing setup.',
        'successMetric': 'Move no-key signups into generated-key accounts, then first routed request.',
        'privacy': {
            'containsEmails': False,
            'containsCustomerIds': False,
            'containsApiKeys': False,
            'containsProviderCredentials': False,
        },
    }


def operator_customer_review(customer, usage=None, api_keys=None):
    customer = normalize_customer(customer) or {}
    usage = usage or account_usage_for_customer(customer)
    if api_keys is None:
        api_keys = api_keys_for_customer(customer.get('id')) if customer.get('id') else []
    activation = account_activation_for_customer(customer, usage=usage, api_keys=api_keys)
    status = str(customer.get('status') or activation.get('status') or 'inactive').lower()
    plan = str(customer.get('plan') or activation.get('plan') or 'free').lower()
    requests = max(0, int(activation.get('requestCount') or usage.get('requests') or 0))
    quota = max(0, int(activation.get('quota') or usage.get('quota') or 0))
    quota_used_percent = activation.get('quotaUsedPercent')
    if quota_used_percent is None and quota > 0:
        quota_used_percent = min(100, max(0, round((requests / quota) * 100, 2)))
    active_key_count = max(0, int(activation.get('activeKeyCount') or 0))
    key_count = max(0, int(activation.get('keyCount') or len(api_keys or []) or 0))
    routing_enabled = bool(activation.get('routingEnabled'))
    now = now_epoch()

    def flag(code, severity, label):
        return {'code': code, 'severity': severity, 'label': label}

    flags = []
    if status == 'suspended':
        flags.append(flag('suspended', 'bad', 'Suspended'))
    elif status in {'past_due', 'unpaid'}:
        flags.append(flag('payment_review', 'warn', 'Payment review'))
    elif status in {'canceled', 'blocked'}:
        flags.append(flag('inactive_billing', 'warn', 'Inactive billing'))

    if not routing_enabled:
        flags.append(flag('routing_blocked', 'bad' if status == 'suspended' else 'warn', 'Routing blocked'))

    if active_key_count <= 0 and routing_enabled:
        flags.append(flag('no_active_api_key', 'warn', 'No active API key'))
    elif active_key_count <= 0 and plan in {'free', 'inactive', ''}:
        flags.append(flag('new_signup', 'info', 'New signup'))

    if active_key_count > 0 and not routing_enabled:
        flags.append(flag('keys_blocked', 'warn', 'Keys blocked'))

    if active_key_count > 0 and requests <= 0 and routing_enabled:
        flags.append(flag('no_first_request', 'warn', 'No first request'))

    if MAX_ACTIVE_API_KEYS_PER_CUSTOMER > 0 and active_key_count >= MAX_ACTIVE_API_KEYS_PER_CUSTOMER:
        flags.append(flag('active_key_limit', 'warn', 'At active-key limit'))

    if quota > 0 and quota_used_percent is not None:
        if quota_used_percent >= 100:
            flags.append(flag('quota_exhausted', 'bad', 'Quota exhausted'))
        elif quota_used_percent >= 90:
            flags.append(flag('quota_high', 'warn', 'Quota above 90%'))
        elif quota_used_percent >= 75:
            flags.append(flag('quota_watch', 'info', 'Quota above 75%'))

    last_usage = usage.get('updated_at_epoch')
    try:
        last_usage = int(last_usage or 0)
    except Exception:
        last_usage = 0
    if routing_enabled and requests > 0 and last_usage > 0 and now - last_usage > 14 * 24 * 3600:
        flags.append(flag('paid_idle', 'info', 'Paid but idle'))

    if not flags:
        flags.append(flag('healthy', 'good', 'No review flags'))

    severity_order = {'bad': 3, 'warn': 2, 'info': 1, 'good': 0}
    severity = max((row.get('severity') for row in flags), key=lambda value: severity_order.get(value, 0))
    return {
        'severity': severity,
        'flags': flags,
        'flagCodes': [row['code'] for row in flags],
        'activeKeyLimit': MAX_ACTIVE_API_KEYS_PER_CUSTOMER,
        'keyCount': key_count,
        'activeKeyCount': active_key_count,
        'quotaUsedPercent': quota_used_percent,
    }


def create_api_key_for_customer(customer, name='Default'):
    max_active = MAX_ACTIVE_API_KEYS_PER_CUSTOMER
    if max_active > 0 and active_api_key_count_for_customer(customer.get('id')) >= max_active:
        raise ValueError(f'active_api_key_limit_reached:{max_active}')
    raw_key = generate_api_key()
    row = {
        'id': uuid.uuid4().hex,
        'customer_id': customer.get('id'),
        'user_id': customer.get('user_id'),
        'name': (name or 'Default')[:80],
        'prefix': key_prefix(raw_key),
        'api_key_hash': api_key_hash(raw_key),
        'status': 'active',
        'plan': customer.get('plan') or 'free',
        'created_at_epoch': now_epoch(),
        'last_used_at_epoch': None,
        'revoked_at_epoch': None,
    }
    if customer_store_uses_supabase():
        rows = supabase_insert(SUPABASE_API_KEYS_TABLE, row)
        row = rows[0] if rows else row
    else:
        data = local_customer_store()
        data['api_keys'].append(row)
        write_local_customer_store(data)
    return raw_key, row


def revoke_api_key_for_customer(customer_id, key_id):
    if customer_store_uses_supabase():
        rows = supabase_select(
            SUPABASE_API_KEYS_TABLE,
            f'select=*&id=eq.{urllib.parse.quote(str(key_id), safe="")}&customer_id=eq.{urllib.parse.quote(str(customer_id), safe="")}&limit=1',
        )
        if not rows:
            return None
        updated = supabase_patch(SUPABASE_API_KEYS_TABLE, key_id, {
            'status': 'revoked',
            'revoked_at_epoch': now_epoch(),
        })
        return updated[0] if updated else {**rows[0], 'status': 'revoked', 'revoked_at_epoch': now_epoch()}
    data = local_customer_store()
    found = None
    for row in data.get('api_keys', []):
        if row.get('id') == key_id and row.get('customer_id') == customer_id:
            row['status'] = 'revoked'
            row['revoked_at_epoch'] = now_epoch()
            found = row
            break
    if found:
        write_local_customer_store(data)
    return found


def revoke_active_api_keys_for_customer(customer_id):
    revoked = []
    for row in api_keys_for_customer(customer_id):
        if str(row.get('status') or 'active').lower() != 'active':
            continue
        updated = revoke_api_key_for_customer(customer_id, row.get('id'))
        if updated:
            revoked.append(updated)
    return revoked


def suspend_customer_for_operator(customer_id, reason_code='operator_review'):
    customer = customer_by_id(customer_id)
    if not customer:
        return None, [], None
    status_before = str(customer.get('status') or '')
    revoked = revoke_active_api_keys_for_customer(customer_id)
    updated = update_customer(customer_id, {'status': 'suspended'})
    current = updated or customer_by_id(customer_id)
    audit_event = record_operator_audit_event(
        'customer.suspend',
        customer_id,
        status_before=status_before,
        status_after='suspended',
        revoked_api_keys_count=len(revoked),
        reason_code=reason_code,
    )
    return current, revoked, audit_event


def unsuspend_customer_for_operator(customer_id, desired_status='inactive', reason_code='operator_review'):
    customer = customer_by_id(customer_id)
    if not customer:
        return None, None
    status_before = str(customer.get('status') or '')
    status = str(desired_status or 'inactive').strip().lower()
    allowed = {'inactive', 'active', 'trialing', 'manual', 'paid', 'past_due'}
    if status not in allowed:
        raise ValueError('invalid_customer_status')
    updated = update_customer(customer_id, {'status': status})
    current = updated or customer_by_id(customer_id)
    audit_event = record_operator_audit_event(
        'customer.unsuspend',
        customer_id,
        status_before=status_before,
        status_after=status,
        revoked_api_keys_count=0,
        reason_code=reason_code,
    )
    return current, audit_event


def billing_status_for_customer(customer_id, desired_status):
    existing = customer_by_id(customer_id)
    if str((existing or {}).get('status') or '').lower() == 'suspended':
        return 'suspended'
    return desired_status


def mark_api_key_used(key_id):
    try:
        if customer_store_uses_supabase():
            supabase_patch(SUPABASE_API_KEYS_TABLE, key_id, {'last_used_at_epoch': now_epoch()}, timeout=4)
        else:
            data = local_customer_store()
            for row in data.get('api_keys', []):
                if row.get('id') == key_id:
                    row['last_used_at_epoch'] = now_epoch()
                    break
            write_local_customer_store(data)
    except Exception as e:
        logger.debug(f'API key last-used update failed: {extract_http_error(e)}')


def verify_generated_api_key(raw_key):
    if not raw_key or not raw_key.startswith(API_KEY_PREFIX):
        return None
    digest = api_key_hash(raw_key)
    rows = []
    if customer_store_uses_supabase():
        rows = supabase_select(SUPABASE_API_KEYS_TABLE, f'select=*&api_key_hash=eq.{urllib.parse.quote(digest, safe="")}&limit=1')
    else:
        rows = [r for r in local_customer_store().get('api_keys', []) if hmac.compare_digest(str(r.get('api_key_hash') or ''), digest)]
    if not rows:
        return None
    key = rows[0]
    if str(key.get('status') or '').lower() != 'active':
        return None
    customer = customer_by_id(key.get('customer_id'))
    if not customer_is_active(customer):
        return None
    mark_api_key_used(key.get('id'))
    return {'type': 'generated_key', 'key': key, 'customer': customer}


def customer_by_id(customer_id):
    if not customer_id:
        return None
    if customer_store_uses_supabase():
        rows = supabase_select(SUPABASE_CUSTOMERS_TABLE, f'select=*&id=eq.{urllib.parse.quote(str(customer_id), safe="")}&limit=1')
        return normalize_customer(rows[0]) if rows else None
    for row in local_customer_store().get('customers', []):
        if row.get('id') == customer_id:
            return normalize_customer(row)
    return None


def customer_by_stripe_customer_id(stripe_customer_id):
    if not stripe_customer_id:
        return None
    if customer_store_uses_supabase():
        rows = supabase_select(SUPABASE_CUSTOMERS_TABLE, f'select=*&stripe_customer_id=eq.{urllib.parse.quote(str(stripe_customer_id), safe="")}&limit=1')
        return normalize_customer(rows[0]) if rows else None
    for row in local_customer_store().get('customers', []):
        if row.get('stripe_customer_id') == stripe_customer_id:
            return normalize_customer(row)
    return None


def resolve_stripe_webhook_customer_id(obj):
    obj = obj if isinstance(obj, dict) else {}
    metadata = obj.get('metadata') or {}
    metadata_customer_id = str(metadata.get('customer_id') or obj.get('client_reference_id') or '').strip()
    stripe_customer_id = str(obj.get('customer') or '').strip()
    customer_from_stripe = customer_by_stripe_customer_id(stripe_customer_id) if stripe_customer_id else None

    if customer_from_stripe:
        resolved_id = str(customer_from_stripe.get('id') or '')
        if metadata_customer_id and metadata_customer_id != resolved_id:
            raise ValueError('stripe_customer_mismatch')
        return resolved_id

    if metadata_customer_id:
        customer = customer_by_id(metadata_customer_id)
        if not customer:
            raise ValueError('stripe_customer_not_found')
        existing_stripe_customer_id = str(customer.get('stripe_customer_id') or '').strip()
        if stripe_customer_id and existing_stripe_customer_id and existing_stripe_customer_id != stripe_customer_id:
            raise ValueError('stripe_customer_mismatch')
        return metadata_customer_id

    return ''


def update_customer(customer_id, updates):
    updates = dict(updates or {})
    updates['updated_at_epoch'] = now_epoch()
    if customer_store_uses_supabase():
        rows = supabase_patch(SUPABASE_CUSTOMERS_TABLE, customer_id, updates)
        return normalize_customer(rows[0]) if rows else customer_by_id(customer_id)
    data = local_customer_store()
    found = None
    for row in data.get('customers', []):
        if row.get('id') == customer_id:
            row.update(updates)
            found = row
            break
    if found:
        write_local_customer_store(data)
    return normalize_customer(found)


OPERATOR_AUDIT_REASON_CODES = {
    'operator_review',
    'abuse_review',
    'chargeback',
    'security',
    'provider_risk',
    'billing_review',
    'customer_request',
    'other',
}
OPERATOR_AUDIT_ACTIONS = {'customer.suspend', 'customer.unsuspend', 'payment_intent.approve', 'api_key.revoke'}


def operator_audit_reason(value):
    reason = str(value or 'operator_review').strip().lower().replace('-', '_')
    return reason if reason in OPERATOR_AUDIT_REASON_CODES else 'operator_review'


def public_operator_audit_event(row):
    row = row if isinstance(row, dict) else {}
    metadata = row.get('metadata') if isinstance(row.get('metadata'), dict) else {}

    def int_or_zero(value):
        try:
            return max(0, int(value or 0))
        except Exception:
            return 0

    return {
        'id': row.get('id') or '',
        'customer_id': row.get('customer_id') or '',
        'actor': row.get('actor') or 'operator',
        'action': row.get('action') if row.get('action') in OPERATOR_AUDIT_ACTIONS else 'customer.suspend',
        'reason_code': operator_audit_reason(row.get('reason_code') or metadata.get('reason_code')),
        'status_before': row.get('status_before') or metadata.get('status_before') or '',
        'status_after': row.get('status_after') or metadata.get('status_after') or '',
        'revoked_api_keys_count': int_or_zero(row.get('revoked_api_keys_count') or metadata.get('revoked_api_keys_count')),
        'created_at_epoch': int_or_zero(row.get('created_at_epoch')),
    }


def record_operator_audit_event(action, customer_id, status_before='', status_after='', revoked_api_keys_count=0, reason_code='operator_review', actor='operator'):
    if action not in OPERATOR_AUDIT_ACTIONS or not customer_id:
        return None
    row = {
        'id': uuid.uuid4().hex,
        'customer_id': str(customer_id),
        'actor': 'customer' if str(actor or '').lower() == 'customer' else 'operator',
        'action': action,
        'reason_code': operator_audit_reason(reason_code),
        'status_before': str(status_before or ''),
        'status_after': str(status_after or ''),
        'revoked_api_keys_count': max(0, int(revoked_api_keys_count or 0)),
        'created_at_epoch': now_epoch(),
    }
    if customer_store_uses_supabase():
        try:
            rows = supabase_insert(SUPABASE_OPERATOR_AUDIT_TABLE, row, timeout=5)
            return public_operator_audit_event(rows[0] if rows else row)
        except Exception as e:
            logger.warning(f'Operator audit Supabase write failed: {extract_http_error(e)}')
            return public_operator_audit_event(row)
    data = local_customer_store()
    data['operator_audit_events'].append(row)
    write_local_customer_store(data)
    return public_operator_audit_event(row)


def operator_audit_events_for_customer(customer_id, limit=20):
    try:
        limit = int(limit or 20)
    except Exception:
        limit = 20
    limit = max(1, min(limit, 50))
    if not customer_id:
        return []
    rows = []
    if customer_store_uses_supabase():
        try:
            quoted = urllib.parse.quote(str(customer_id), safe='')
            rows = supabase_select(
                SUPABASE_OPERATOR_AUDIT_TABLE,
                f'select=*&customer_id=eq.{quoted}&order=created_at_epoch.desc&limit={limit}',
                timeout=5,
            )
        except Exception as e:
            logger.warning(f'Operator audit Supabase lookup failed: {extract_http_error(e)}')
            rows = []
    else:
        rows = [
            row for row in local_customer_store().get('operator_audit_events', [])
            if row.get('customer_id') == customer_id
        ]
        rows.sort(key=lambda row: int(row.get('created_at_epoch') or 0), reverse=True)
        rows = rows[:limit]
    return [public_operator_audit_event(row) for row in rows]


def bounded_payment_text(value, limit=160):
    return re.sub(r'\s+', ' ', str(value or '')).strip()[:max(1, int(limit or 160))]


def public_payment_intent(row):
    row = row if isinstance(row, dict) else {}
    metadata = row.get('metadata') if isinstance(row.get('metadata'), dict) else {}
    public_metadata = {}
    for key in (
        'settlement',
        'automatic_settlement',
        'plan',
        'amount_source',
        'approved_at_epoch',
        'settlement_reference',
    ):
        if key in metadata:
            public_metadata[key] = metadata.get(key)
    return {
        'id': row.get('id') or '',
        'kind': row.get('kind') or '',
        'customer_id': row.get('customer_id') or '',
        'user_id': row.get('user_id') or '',
        'status': row.get('status') or '',
        'asset': row.get('asset') or '',
        'network': row.get('network') or '',
        'amount': row.get('amount') or '',
        'address': row.get('address') or '',
        'metadata': public_metadata,
        'created_at_epoch': row.get('created_at_epoch'),
        'updated_at_epoch': row.get('updated_at_epoch'),
    }


def customer_matches_operator_query(customer, query):
    query = str(query or '').strip().lower()
    if not query:
        return True
    fields = [
        customer.get('id'),
        customer.get('user_id'),
        customer.get('email'),
        customer.get('stripe_customer_id'),
        customer.get('stripe_subscription_id'),
    ]
    return any(query in str(value or '').lower() for value in fields)


def operator_customer_rows(query='', status='', limit=50):
    try:
        limit = int(limit or 50)
    except Exception:
        limit = 50
    limit = max(1, min(limit, 100))
    status = str(status or '').strip().lower()
    select = 'select=id,user_id,email,plan,status,stripe_customer_id,stripe_subscription_id,created_at_epoch,updated_at_epoch'
    try:
        if customer_store_uses_supabase():
            fetch_limit = 1000 if query or status else limit
            rows = supabase_select(
                SUPABASE_CUSTOMERS_TABLE,
                f'{select}&order=updated_at_epoch.desc&limit={fetch_limit}',
                timeout=8,
            )
        else:
            rows = list(local_customer_store().get('customers') or [])
    except Exception as e:
        logger.debug(f'Operator customer lookup failed: {extract_http_error(e)}')
        rows = []
    out = []
    for row in rows:
        customer = normalize_customer(row)
        if not customer:
            continue
        if status and str(customer.get('status') or '').lower() != status:
            continue
        if not customer_matches_operator_query(customer, query):
            continue
        out.append(customer)
        if len(out) >= limit:
            break
    return out


def operator_customer_summary(customer, include_audit=True):
    customer = normalize_customer(customer) or {}
    keys = api_keys_for_customer(customer.get('id')) if customer.get('id') else []
    usage = account_usage_for_customer(customer)
    activation = account_activation_for_customer(customer, usage=usage, api_keys=keys)
    email_verification = auth_verification_state_for_customer(customer)
    audit_events = operator_audit_events_for_customer(customer.get('id'), limit=20) if include_audit and customer.get('id') else []
    follow_up = operator_customer_follow_up(customer, activation=activation, email_verification=email_verification)
    return {
        'customer': public_customer(customer),
        'usage': usage,
        'activation': activation,
        'followUp': follow_up,
        'emailVerification': email_verification,
        'review': operator_customer_review(customer, usage=usage, api_keys=keys),
        'api_keys': [public_api_key(row, customer) for row in keys],
        'auditEvents': audit_events if include_audit else [],
        'latestAuditEvent': audit_events[0] if audit_events else None,
    }


def operator_customer_listing_summary(customers):
    summaries = list(customers or [])
    status_counts = {}
    next_actions = {}
    email_verification = {'verified': 0, 'unverified': 0, 'unknown': 0}
    no_key_create_key = 0
    has_emails = False
    for summary in summaries:
        customer = summary.get('customer') or {}
        activation = summary.get('activation') or {}
        verification = summary.get('emailVerification') or {}
        status = str(customer.get('status') or activation.get('status') or 'unknown').strip().lower() or 'unknown'
        next_action = str(activation.get('nextAction') or 'unknown').strip().lower() or 'unknown'
        status_counts[status] = status_counts.get(status, 0) + 1
        next_actions[next_action] = next_actions.get(next_action, 0) + 1
        if customer.get('email'):
            has_emails = True
        if verification.get('verified') is True:
            email_verification['verified'] += 1
        elif verification.get('verified') is False:
            email_verification['unverified'] += 1
        else:
            email_verification['unknown'] += 1
        if int(activation.get('activeKeyCount') or 0) <= 0 and next_action == 'create_key':
            no_key_create_key += 1
    return {
        'returned': len(summaries),
        'statusCounts': status_counts,
        'nextActions': next_actions,
        'emailVerification': email_verification,
        'noKeyCreateKey': no_key_create_key,
        'hasEmails': has_emails,
    }


def token_matches_any(token, allowed_tokens):
    if not token:
        return False
    return any(hmac.compare_digest(token, allowed) for allowed in allowed_tokens if allowed)


def safe_trusted_header(handler, name, limit=160):
    value = str((getattr(handler, 'headers', {}) or {}).get(name) or '').strip()
    if not value or '\r' in value or '\n' in value:
        return ''
    return value[:max(1, int(limit or 160))]


def trusted_edge_generated_key_context(handler):
    edge_auth_type = safe_trusted_header(handler, 'X-Sage-Router-Edge-Auth-Type', 64).lower()
    if edge_auth_type != 'generated_key':
        return None
    customer_id = safe_trusted_header(handler, 'X-Sage-Router-Customer-Id', 128)
    if not customer_id:
        return None
    plan = safe_trusted_header(handler, 'X-Sage-Router-Customer-Plan', 64)
    customer_status = safe_trusted_header(handler, 'X-Sage-Router-Customer-Status', 64)
    user_id = safe_trusted_header(handler, 'X-Sage-Router-User-Id', 128)
    customer = customer_by_id(customer_id) or {'id': customer_id}
    if plan and not customer.get('plan'):
        customer = {**customer, 'plan': plan}
    if customer_status and not customer.get('status'):
        customer = {**customer, 'status': customer_status}
    if user_id and not customer.get('user_id'):
        customer = {**customer, 'user_id': user_id}
    return {
        'type': 'generated_key',
        'customer': customer,
        'customer_id': customer_id,
        'customer_plan': customer.get('plan') or plan,
        'edge_authenticated': True,
    }


def analytics_authorized(handler):
    bearer = bearer_token(handler)
    if ANALYTICS_TOKEN and hmac.compare_digest(bearer, ANALYTICS_TOKEN):
        return True
    if token_matches_any(bearer, CLIENT_API_KEYS):
        return True
    return not ANALYTICS_TOKEN and not SUPABASE_AUTH_ENABLED


def client_auth_context(handler):
    if not CLIENT_AUTH_REQUIRED:
        return {'type': 'disabled'}
    bearer = bearer_token(handler)
    if token_matches_any(bearer, CLIENT_API_KEYS):
        edge_context = trusted_edge_generated_key_context(handler)
        if edge_context:
            return edge_context
        return {'type': 'legacy_key'}
    generated = verify_generated_api_key(bearer)
    if generated:
        return generated
    return None


def client_request_authorized(handler):
    return bool(client_auth_context(handler))


def model_api_auth_error_payload():
    api_base_url = API_BASE_URL or 'https://api.sagerouter.dev'
    return {
        'error': 'unauthorized',
        'message': 'Use an active Sage Router API key from the hosted account page.',
        'accountUrl': f"{APP_BASE_URL}/account.html",
        'pricingUrl': f"{MARKETING_BASE_URL}/pricing",
        'statusUrl': f"{APP_BASE_URL}/status",
        'openaiBaseUrl': f"{api_base_url.rstrip('/')}/v1",
        'apiKeyPrefix': API_KEY_PREFIX,
    }


def model_api_auth_error_headers():
    account_url = f"{APP_BASE_URL}/account.html"
    pricing_url = f"{MARKETING_BASE_URL}/pricing"
    status_url = f"{APP_BASE_URL}/status"
    return {
        'WWW-Authenticate': (
            'Bearer realm="Sage Router", error="invalid_token", '
            'error_description="Use an active Sage Router API key from app.sagerouter.dev/account.html"'
        ),
        'Link': f'<{account_url}>; rel="account", <{pricing_url}>; rel="pricing", <{status_url}>; rel="status"',
    }


def normalize_browser_origin(value):
    if not value:
        return ''
    try:
        parsed = urllib.parse.urlparse(str(value).strip())
    except Exception:
        return ''
    if parsed.scheme.lower() not in {'http', 'https'} or not parsed.netloc:
        return ''
    return f'{parsed.scheme.lower()}://{parsed.netloc.lower()}'


def configured_browser_allowed_origins():
    origins = set()
    for raw in (PUBLIC_BASE_URL, MARKETING_BASE_URL, APP_BASE_URL, API_BASE_URL):
        origin = normalize_browser_origin(raw)
        if origin:
            origins.add(origin)
    for raw in BROWSER_ALLOWED_ORIGINS_RAW.split(','):
        origin = normalize_browser_origin(raw)
        if origin:
            origins.add(origin)
    for raw in CORS_ORIGINS:
        if raw == '*':
            continue
        origin = normalize_browser_origin(raw)
        if origin:
            origins.add(origin)
    return origins


def browser_origin_allowed(origin):
    origin = normalize_browser_origin(origin)
    if not origin:
        return True
    if origin in configured_browser_allowed_origins():
        return True
    try:
        hostname = urllib.parse.urlparse(origin).hostname or ''
    except Exception:
        return False
    if hostname in DEFAULT_BROWSER_ALLOWED_ORIGIN_HOSTS:
        return True
    return hostname.endswith('.sage-router-web.pages.dev')


def require_trusted_browser_origin(handler):
    origin = normalize_browser_origin(handler.headers.get('Origin') or '')
    if browser_origin_allowed(origin):
        return True
    handler.write_json(403, {
        'error': 'origin_not_allowed',
        'message': 'Browser-originating account and billing mutations must come from a trusted Sage Router app origin.',
        'appBaseUrl': APP_BASE_URL,
    })
    return False


def operator_request_authorized(handler):
    if not CLIENT_AUTH_REQUIRED:
        return True
    bearer = bearer_token(handler)
    if ANALYTICS_TOKEN and hmac.compare_digest(bearer, ANALYTICS_TOKEN):
        return True
    return token_matches_any(bearer, CLIENT_API_KEYS)


def require_operator_request(handler):
    if operator_request_authorized(handler):
        return True
    handler.write_json(401, {'error': 'unauthorized'})
    return False


def read_json_body(handler):
    length = int(handler.headers.get('Content-Length', 0) or 0)
    raw = handler.rfile.read(length) if length else b'{}'
    try:
        return json.loads(raw or b'{}')
    except Exception:
        return {}


def parse_model_list(value):
    if isinstance(value, list):
        return dedupe_keep_order([str(v).strip() for v in value if str(v).strip()])
    if isinstance(value, str):
        parts = re.split(r'[\n,]+', value)
        return dedupe_keep_order([p.strip() for p in parts if p.strip()])
    return []


def normalize_dashboard_api_type(api_type):
    api_type = str(api_type or '').strip()
    api_aliases = {
        'openai': 'openai-completions',
        'openai-compatible': 'openai-completions',
        'anthropic': 'anthropic-messages',
        'google': 'google-generative-language',
        'gemini': 'google-generative-language',
        'codex': 'openai-codex-responses',
        'ollama-cloud': 'ollama',
    }
    return api_aliases.get(api_type, api_type)


def default_base_url_for_api(api_type):
    api_type = normalize_dashboard_api_type(api_type)
    return {
        'ollama': 'https://ollama.com',
        'openai-completions': 'https://api.openai.com/v1',
        'anthropic-messages': 'https://api.anthropic.com',
        'google-generative-language': 'https://generativelanguage.googleapis.com/v1beta',
        'openai-codex-responses': 'https://chatgpt.com/backend-api/codex',
        'cloudflare-workers-ai': '',
    }.get(api_type, '')


def setup_state_payload():
    return {
        'status': 'ok',
        'paths': {
            'providerConfig': APP_PROVIDER_CONFIG,
            'codexAuthJson': APP_CODEX_AUTH_JSON,
            'codexAuthProfile': APP_CODEX_AUTH_PROFILE,
        },
        'providers': sorted(PROVIDERS.keys()),
        'disabled': sorted(DISABLED_PROVIDERS),
        'codexConfigured': bool(read_openai_codex_oauth_token_from_file()),
        'codexOAuthAvailable': OPENAI_CODEX_OAUTH_ENABLED,
        'clientAuthRequired': CLIENT_AUTH_REQUIRED,
        'port': int(os.environ.get('PORT') or os.environ.get('APP_PORT') or 8790),
        'credentials': list_setup_credentials(),
    }


def reload_configured_providers():
    global PROVIDERS
    PROVIDERS = load_openclaw_providers()
    MODEL_HEALTH_CACHE.clear()
    PROVIDER_HEALTH_CACHE.clear()
    return PROVIDERS


def save_setup_provider(payload):
    provider_name = str(payload.get('name') or '').strip().lower()
    if not provider_name:
        provider_name = str(payload.get('provider') or payload.get('kind') or '').strip().lower()
    provider_name = re.sub(r'[^a-z0-9_.-]+', '-', provider_name).strip('-')
    if not provider_name:
        raise ValueError('provider_name_required')
    if provider_name in SELF_PROVIDER_NAMES:
        raise ValueError('self_provider_not_allowed')

    api_type = normalize_dashboard_api_type(payload.get('api') or payload.get('apiType') or payload.get('kind')) or infer_api_type(provider_name, {}, '')
    base_url = str(payload.get('baseUrl') or payload.get('base_url') or default_base_url_for_api(api_type)).strip()
    api_key = str(payload.get('apiKey') or payload.get('api_key') or payload.get('token') or '').strip()
    models = parse_model_list(payload.get('models'))

    try:
        with open(APP_PROVIDER_CONFIG) as f:
            config = json.load(f)
    except Exception:
        config = {}
    if not isinstance(config, dict):
        config = {}
    config.setdefault('models', {}).setdefault('providers', {})
    provider_cfg = {
        'baseUrl': base_url,
        'api': api_type,
        'models': models,
    }
    if api_key:
        provider_cfg['apiKey'] = api_key
    config['models']['providers'][provider_name] = provider_cfg
    atomic_write_json(APP_PROVIDER_CONFIG, config)
    reload_configured_providers()
    return {
        'status': 'saved',
        'provider': provider_name,
        'api': api_type,
        'models': len(models),
        'configured': sorted(PROVIDERS.keys()),
    }


def save_codex_setup_auth(payload):
    auth_json = payload.get('authJson') or payload.get('auth_json')
    auth_profile_json = payload.get('authProfileJson') or payload.get('auth_profile_json')
    access_token = str(payload.get('accessToken') or payload.get('access_token') or payload.get('token') or '').strip()

    if isinstance(auth_json, str) and auth_json.strip():
        auth_json = json.loads(auth_json)
    if isinstance(auth_profile_json, str) and auth_profile_json.strip():
        auth_profile_json = json.loads(auth_profile_json)

    if isinstance(auth_json, dict):
        if not extract_openai_codex_token_from_auth_data(auth_json, 'openai-codex'):
            raise ValueError('codex_access_token_not_found')
        atomic_write_json(APP_CODEX_AUTH_JSON, auth_json)
        target = APP_CODEX_AUTH_JSON
    elif isinstance(auth_profile_json, dict):
        if not extract_openai_codex_token_from_auth_data(auth_profile_json, 'openai-codex'):
            raise ValueError('codex_access_token_not_found')
        atomic_write_json(APP_CODEX_AUTH_PROFILE, auth_profile_json)
        target = APP_CODEX_AUTH_PROFILE
    elif access_token:
        profile = {
            'profiles': {
                'sage-router-codex': {
                    'provider': 'openai-codex',
                    'type': 'oauth',
                    'access': access_token,
                    'expires': 0,
                }
            }
        }
        atomic_write_json(APP_CODEX_AUTH_PROFILE, profile)
        target = APP_CODEX_AUTH_PROFILE
    else:
        raise ValueError('codex_auth_required')

    reload_configured_providers()
    return {
        'status': 'saved',
        'target': target,
        'codexConfigured': bool(read_openai_codex_oauth_token_from_file()),
        'configured': sorted(PROVIDERS.keys()),
    }


def _save_app_provider_config(config):
    atomic_write_json(APP_PROVIDER_CONFIG, config)


def _set_list_membership(config, key, value, enabled):
    items = _normalize_config_list(config.get(key))
    if enabled:
        items = [item for item in items if item != value]
    elif value not in items:
        items.append(value)
    config[key] = items
    return items


def set_setup_provider_enabled(payload):
    provider_name = str(payload.get('provider') or payload.get('name') or '').strip().lower()
    provider_name = re.sub(r'[^a-z0-9_.-]+', '-', provider_name).strip('-')
    if not provider_name:
        raise ValueError('provider_name_required')
    if provider_name in SELF_PROVIDER_NAMES:
        raise ValueError('self_provider_not_allowed')
    enabled = bool(payload.get('enabled'))
    config = _load_app_provider_config_safe()
    if not isinstance(config, dict):
        config = {}
    disabled = _set_list_membership(config, 'disabledProviders', provider_name, enabled)
    _save_app_provider_config(config)
    reload_configured_providers()
    return {
        'status': 'saved',
        'provider': provider_name,
        'enabled': provider_name not in DISABLED_PROVIDERS,
        'disabledProviders': disabled,
        'envDisabled': provider_name in ENV_DISABLED_PROVIDERS,
        'configured': sorted(PROVIDERS.keys()),
    }


def set_setup_model_enabled(payload):
    model = str(payload.get('model') or '').strip()
    provider_name = str(payload.get('provider') or '').strip().lower()
    provider_name = re.sub(r'[^a-z0-9_.-]+', '-', provider_name).strip('-')
    if not model:
        raise ValueError('model_required')
    disabled_key = f'{provider_name}/{model}' if provider_name else model
    enabled = bool(payload.get('enabled'))
    config = _load_app_provider_config_safe()
    if not isinstance(config, dict):
        config = {}
    disabled = _set_list_membership(config, 'disabledModels', disabled_key, enabled)
    _save_app_provider_config(config)
    _apply_dashboard_disabled_sets(config)
    MODEL_HEALTH_CACHE.clear()
    return {
        'status': 'saved',
        'provider': provider_name,
        'model': model,
        'enabled': not bool(model_disabled_reason(provider_name, model)),
        'disabledModels': disabled,
        'envDisabled': disabled_key in ENV_DISABLED_MODELS or model in ENV_DISABLED_MODELS,
    }


def _app_provider_credentials(cfg):
    """Return the raw (unmasked) credential entries stored for a provider cfg."""
    creds = []
    for raw in (cfg.get('apiKeys') or []):
        c = normalize_credential(raw)
        if c:
            creds.append({'slot': 'apiKeys', **c})
    for raw in (cfg.get('oauthPaths') or []):
        c = normalize_credential(raw)
        if c:
            creds.append({'slot': 'oauthPaths', **c})
    legacy = cfg.get('apiKey') or cfg.get('api_key')
    if legacy:
        c = normalize_credential({'type': 'api_key', 'label': 'default', 'key': legacy})
        if c:
            creds.append({'slot': 'apiKey', **c})
    return dedupe_credentials(creds)


def list_setup_credentials():
    """Return a masked, dashboard-safe summary of every provider's credentials."""
    config = _load_app_provider_config_safe()
    providers_cfg = (config.get('models') or {}).get('providers', {}) or {}
    summary = []
    for name in sorted(set(providers_cfg.keys()) | set(PROVIDERS.keys())):
        cfg = providers_cfg.get(name) or {}
        provider = PROVIDERS.get(name)
        if not cfg and provider:
            cfg = {
                'api': provider.api_type,
                'baseUrl': provider.base_url,
            }
        creds = _app_provider_credentials(cfg)
        if provider and provider.credentials:
            creds = dedupe_credentials(creds + list(provider.credentials or []))
        raw_creds = [(c.get('key') or c.get('accessToken') or '') for c in creds]
        strategy = str(cfg.get('credentialStrategy') or cfg.get('credential_strategy') or '').strip().lower() or DEFAULT_CREDENTIAL_STRATEGY
        if strategy not in CREDENTIAL_STRATEGIES:
            strategy = 'failover'
        api_type = normalize_dashboard_api_type(cfg.get('api') or infer_api_type(name, cfg, cfg.get('baseUrl', '')))
        masked = []
        snap = credential_state_snapshot(name, creds)
        for i, c in enumerate(creds):
            mc = mask_credential(c)
            st = snap[i] if i < len(snap) else {}
            mc['state'] = st
            masked.append(mc)
        summary.append({
            'provider': name,
            'api': api_type,
            'baseUrl': cfg.get('baseUrl') or default_base_url_for_api(api_type),
            'strategy': strategy,
            'strategies': sorted(CREDENTIAL_STRATEGIES),
            'credentials': masked,
        })
    return summary


def set_setup_credential_strategy(payload):
    """Set the credential load-balancing strategy for a provider."""
    provider_name = str(payload.get('provider') or payload.get('name') or '').strip().lower()
    provider_name = re.sub(r'[^a-z0-9_.-]+', '-', provider_name).strip('-')
    if not provider_name:
        raise ValueError('provider_name_required')
    strategy = str(payload.get('strategy') or '').strip().lower()
    if strategy not in CREDENTIAL_STRATEGIES:
        raise ValueError(f'invalid_strategy (one of {sorted(CREDENTIAL_STRATEGIES)})')
    config = _load_app_provider_config_safe()
    config.setdefault('models', {}).setdefault('providers', {})
    providers_cfg = config['models']['providers']
    cfg = providers_cfg.get(provider_name)
    if not isinstance(cfg, dict):
        raise ValueError('provider_not_found')
    cfg['credentialStrategy'] = strategy
    providers_cfg[provider_name] = cfg
    _save_app_provider_config(config)
    # Reset round-robin index so a strategy change starts fresh.
    with CREDENTIAL_STATE_LOCK:
        CREDENTIAL_RR_INDEX.pop(provider_name, None)
    reload_configured_providers()
    return {
        'status': 'saved',
        'provider': provider_name,
        'strategy': strategy,
        'configured': sorted(PROVIDERS.keys()),
    }


def save_setup_credential(payload):
    """Add an API key or OAuth subscription path to a provider's credential pool.

    Creates the provider entry if it does not yet exist. Never overwrites
    existing credentials — the new credential is appended to the pool.
    """
    provider_name = str(payload.get('provider') or payload.get('name') or '').strip().lower()
    provider_name = re.sub(r'[^a-z0-9_.-]+', '-', provider_name).strip('-')
    if not provider_name:
        raise ValueError('provider_name_required')
    if provider_name in SELF_PROVIDER_NAMES:
        raise ValueError('self_provider_not_allowed')

    cred_type = str(payload.get('type') or 'api_key').strip().lower()
    label = str(payload.get('label') or '').strip()
    raw = {
        'type': cred_type,
        'label': label or (cred_type if cred_type == 'oauth' else 'api-key'),
    }
    if cred_type == 'oauth':
        access = str(payload.get('accessToken') or payload.get('access') or payload.get('token') or '').strip()
        if not access:
            raise ValueError('oauth_access_token_required')
        raw['accessToken'] = access
        refresh = str(payload.get('refreshToken') or payload.get('refresh') or '').strip()
        if refresh:
            raw['refreshToken'] = refresh
        expires = payload.get('expires')
        if expires is not None:
            try:
                raw['expires'] = int(expires)
            except (TypeError, ValueError):
                pass
        profile = str(payload.get('profile') or '').strip()
        if profile:
            raw['profile'] = profile
        slot = 'oauthPaths'
    else:
        key = str(payload.get('key') or payload.get('apiKey') or payload.get('token') or '').strip()
        if not key:
            raise ValueError('api_key_required')
        raw['key'] = key
        slot = 'apiKeys'

    config = _load_app_provider_config_safe()
    config.setdefault('models', {}).setdefault('providers', {})
    providers_cfg = config['models']['providers']
    existing_app_cfg = providers_cfg.get(provider_name)
    cfg = existing_app_cfg
    if not isinstance(cfg, dict):
        cfg = {}
    runtime_provider = PROVIDERS.get(provider_name)
    creating_new_provider = not isinstance(existing_app_cfg, dict) and runtime_provider is None
    if not cfg and runtime_provider:
        cfg = {
            'api': runtime_provider.api_type,
            'baseUrl': runtime_provider.base_url,
        }
    # If creating a new provider, fill in defaults so it is usable.
    api_type = normalize_dashboard_api_type(payload.get('api') or cfg.get('api') or '')
    if not api_type:
        api_type = infer_api_type(provider_name, cfg, str(payload.get('baseUrl') or payload.get('base_url') or cfg.get('baseUrl') or ''))
    if api_type and not cfg.get('api'):
        cfg['api'] = api_type
    base_url = str(payload.get('baseUrl') or payload.get('base_url') or cfg.get('baseUrl') or '').strip()
    if not base_url:
        base_url = default_base_url_for_api(cfg.get('api') or api_type or '')
    if not base_url:
        raise ValueError('provider_endpoint_required')
    if base_url and not cfg.get('baseUrl'):
        cfg['baseUrl'] = base_url
    # If creating a new provider, fill in defaults so it is usable.
    if creating_new_provider:
        models = parse_model_list(payload.get('models'))
        if models:
            cfg.setdefault('models', models)
        else:
            cfg.setdefault('models', [])
        strategy = str(payload.get('credentialStrategy') or payload.get('strategy') or '').strip().lower()
        if strategy and strategy in CREDENTIAL_STRATEGIES:
            cfg.setdefault('credentialStrategy', strategy)
    existing = list(cfg.get(slot, []) or [])
    existing.append(raw)
    cfg[slot] = existing
    providers_cfg[provider_name] = cfg
    _save_app_provider_config(config)
    reload_configured_providers()
    return {
        'status': 'saved',
        'provider': provider_name,
        'slot': slot,
        'credentials': [mask_credential(c) for c in _app_provider_credentials(cfg)],
        'configured': sorted(PROVIDERS.keys()),
    }


def remove_setup_credential(payload):
    """Remove a credential from a provider's pool by label (and slot)."""
    provider_name = str(payload.get('provider') or payload.get('name') or '').strip().lower()
    provider_name = re.sub(r'[^a-z0-9_.-]+', '-', provider_name).strip('-')
    if not provider_name:
        raise ValueError('provider_name_required')
    label = str(payload.get('label') or '').strip()
    slot = str(payload.get('slot') or '').strip().lower()  # apiKeys | oauthPaths | apiKey
    if not label and not slot:
        raise ValueError('label_or_slot_required')

    config = _load_app_provider_config_safe()
    providers_cfg = (config.get('models') or {}).get('providers', {}) or {}
    cfg = providers_cfg.get(provider_name)
    if not isinstance(cfg, dict):
        raise ValueError('provider_not_found')
    removed = 0

    def _filter_list(key):
        nonlocal removed
        items = cfg.get(key)
        if not isinstance(items, list):
            return
        kept = []
        for raw in items:
            c = normalize_credential(raw)
            cur_label = (c or {}).get('label') or ''
            if label and cur_label == label:
                removed += 1
                continue
            kept.append(raw)
        cfg[key] = kept

    if slot == 'apikey' or slot == 'legacy':
        if cfg.get('apiKey'):
            cfg.pop('apiKey', None)
            removed += 1
    if slot in ('', 'apikeys'):
        _filter_list('apiKeys')
    if slot in ('', 'oauthpaths'):
        _filter_list('oauthPaths')
    providers_cfg[provider_name] = cfg
    _save_app_provider_config(config)
    reload_configured_providers()
    return {
        'status': 'removed' if removed else 'not_found',
        'provider': provider_name,
        'removed': removed,
        'credentials': [mask_credential(c) for c in _app_provider_credentials(cfg)],
        'configured': sorted(PROVIDERS.keys()),
    }


def cleanup_codex_oauth_sessions(now_ms=None):
    now_ms = now_ms or int(time.time() * 1000)
    expired = [
        sid for sid, session in OPENAI_CODEX_OAUTH_SESSIONS.items()
        if not isinstance(session, dict) or session.get('expiresAt', 0) <= now_ms
    ]
    for sid in expired:
        OPENAI_CODEX_OAUTH_SESSIONS.pop(sid, None)


def ensure_codex_oauth_enabled():
    if not OPENAI_CODEX_OAUTH_ENABLED:
        raise ValueError('codex_oauth_disabled')
    if not OPENAI_CODEX_OAUTH_AUTH_BASE_URL or not OPENAI_CODEX_OAUTH_CLIENT_ID:
        raise ValueError('codex_oauth_not_configured')


def start_codex_oauth_session():
    ensure_codex_oauth_enabled()
    status, text = post_oauth_request(
        f'{OPENAI_CODEX_OAUTH_AUTH_BASE_URL}/api/accounts/deviceauth/usercode',
        oauth_headers('application/json'),
        json.dumps({'client_id': OPENAI_CODEX_OAUTH_CLIENT_ID}),
    )
    data = parse_json_object(text)
    if status == 404:
        raise ValueError('codex_device_auth_unavailable')
    if status < 200 or status >= 300:
        error = data.get('error_description') or data.get('error') or text
        raise ValueError(f'codex_device_code_failed: {sanitize_oauth_error_text(error)}')

    device_auth_id = str(data.get('device_auth_id') or '').strip()
    user_code = str(data.get('user_code') or data.get('usercode') or '').strip()
    if not device_auth_id or not user_code:
        raise ValueError('codex_device_code_missing_fields')

    now_ms = int(time.time() * 1000)
    interval_ms = parse_positive_ms(data.get('interval'), OPENAI_CODEX_OAUTH_DEFAULT_INTERVAL_MS)
    expires_at = now_ms + OPENAI_CODEX_OAUTH_TIMEOUT_MS
    session_id = secrets.token_urlsafe(24)
    with OPENAI_CODEX_OAUTH_LOCK:
        cleanup_codex_oauth_sessions(now_ms)
        OPENAI_CODEX_OAUTH_SESSIONS[session_id] = {
            'deviceAuthId': device_auth_id,
            'userCode': user_code,
            'expiresAt': expires_at,
            'intervalMs': interval_ms,
            'nextPollAt': 0,
        }
    return {
        'status': 'waiting',
        'sessionId': session_id,
        'userCode': user_code,
        'verificationUrl': f'{OPENAI_CODEX_OAUTH_AUTH_BASE_URL}/codex/device',
        'expiresInMs': OPENAI_CODEX_OAUTH_TIMEOUT_MS,
        'intervalMs': interval_ms,
    }


def exchange_codex_device_authorization(authorization_code, code_verifier):
    body = urllib.parse.urlencode({
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': f'{OPENAI_CODEX_OAUTH_AUTH_BASE_URL}/deviceauth/callback',
        'client_id': OPENAI_CODEX_OAUTH_CLIENT_ID,
        'code_verifier': code_verifier,
    })
    status, text = post_oauth_request(
        f'{OPENAI_CODEX_OAUTH_AUTH_BASE_URL}/oauth/token',
        oauth_headers('application/x-www-form-urlencoded'),
        body,
    )
    data = parse_json_object(text)
    if status < 200 or status >= 300:
        error = data.get('error_description') or data.get('error') or text
        raise ValueError(f'codex_token_exchange_failed: {sanitize_oauth_error_text(error)}')
    access = str(data.get('access_token') or '').strip()
    refresh = str(data.get('refresh_token') or '').strip()
    if not access or not refresh:
        raise ValueError('codex_token_exchange_missing_fields')
    return {
        'access': access,
        'refresh': refresh,
        'expires': resolve_oauth_expires_at_ms(access, data.get('expires_in')),
        'accountId': resolve_oauth_account_id(access),
        'id_token': data.get('id_token') if isinstance(data.get('id_token'), str) else '',
    }


def poll_codex_oauth_session(payload):
    ensure_codex_oauth_enabled()
    session_id = str(payload.get('sessionId') or payload.get('session_id') or '').strip()
    if not session_id:
        raise ValueError('codex_oauth_session_required')
    now_ms = int(time.time() * 1000)
    with OPENAI_CODEX_OAUTH_LOCK:
        cleanup_codex_oauth_sessions(now_ms)
        session = OPENAI_CODEX_OAUTH_SESSIONS.get(session_id)
        if not session:
            raise ValueError('codex_oauth_session_expired')
        retry_after = int(session.get('nextPollAt', 0) - now_ms)
        if retry_after > 0:
            return {'status': 'waiting', 'retryAfterMs': retry_after, 'intervalMs': session.get('intervalMs', OPENAI_CODEX_OAUTH_DEFAULT_INTERVAL_MS)}
        session['nextPollAt'] = now_ms + int(session.get('intervalMs') or OPENAI_CODEX_OAUTH_DEFAULT_INTERVAL_MS)
        device_auth_id = session['deviceAuthId']
        user_code = session['userCode']
        interval_ms = int(session.get('intervalMs') or OPENAI_CODEX_OAUTH_DEFAULT_INTERVAL_MS)

    status, text = post_oauth_request(
        f'{OPENAI_CODEX_OAUTH_AUTH_BASE_URL}/api/accounts/deviceauth/token',
        oauth_headers('application/json'),
        json.dumps({'device_auth_id': device_auth_id, 'user_code': user_code}),
    )
    data = parse_json_object(text)
    if status in {403, 404}:
        return {'status': 'waiting', 'retryAfterMs': interval_ms, 'intervalMs': interval_ms}
    if status < 200 or status >= 300:
        error = data.get('error_description') or data.get('error') or text
        raise ValueError(f'codex_device_authorization_failed: {sanitize_oauth_error_text(error)}')

    authorization_code = str(data.get('authorization_code') or '').strip()
    code_verifier = str(data.get('code_verifier') or '').strip()
    if not authorization_code or not code_verifier:
        raise ValueError('codex_device_authorization_missing_fields')

    tokens = exchange_codex_device_authorization(authorization_code, code_verifier)
    with OPENAI_CODEX_OAUTH_LOCK:
        OPENAI_CODEX_OAUTH_SESSIONS.pop(session_id, None)
    saved = save_openai_codex_oauth_tokens(tokens)
    return {
        'status': 'saved',
        'codexConfigured': saved['codexConfigured'],
        'configured': saved['configured'],
    }


def cancel_codex_oauth_session(payload):
    session_id = str(payload.get('sessionId') or payload.get('session_id') or '').strip()
    with OPENAI_CODEX_OAUTH_LOCK:
        if session_id:
            OPENAI_CODEX_OAUTH_SESSIONS.pop(session_id, None)
    return {'status': 'cancelled'}


def authenticated_user(handler):
    user = supabase_user_for_bearer(bearer_token(handler))
    return user if user and user.get('id') else None


def require_user_customer(handler):
    user = authenticated_user(handler)
    if not user:
        handler.write_json(401, {'error': 'unauthorized'})
        return None, None
    try:
        customer = customer_for_user(user, create=True)
    except Exception as e:
        logger.warning(f'Customer lookup failed: {extract_http_error(e)}')
        handler.write_json(502, {'error': 'customer_store_unavailable'})
        return None, None
    return user, customer


def hosted_email_verification_required():
    return bool(SUPABASE_AUTH_ENABLED and REQUIRE_VERIFIED_EMAIL)


def user_email_verified(user):
    if not user:
        return False
    if user.get('email_confirmed_at') or user.get('confirmed_at'):
        return True
    for meta_key in ('user_metadata', 'app_metadata'):
        meta = user.get(meta_key) or {}
        if meta.get('email_verified') is True or str(meta.get('email_verified') or '').strip().lower() == 'true':
            return True
    return False


def user_email_verification_state(user):
    required = hosted_email_verification_required()
    verified = user_email_verified(user)
    return {
        'required': required,
        'verified': bool(verified or not required),
        'email': (user or {}).get('email') or ((user or {}).get('user_metadata') or {}).get('email') or '',
    }


def hydrate_auth_signups_to_customers(auth_user_rows=None, limit=1000):
    """Backfill inactive customer rows for Supabase Auth users missing one."""
    rows = read_launch_auth_user_rows(limit=limit) if auth_user_rows is None else auth_user_rows
    if not isinstance(rows, list):
        return {
            'status': 'unavailable',
            'authUsers': 0,
            'created': 0,
            'existing': 0,
            'failed': 0,
            'confirmedAuthUsers': 0,
            'privacy': {
                'containsEmails': False,
                'containsUserIds': False,
                'containsApiKeys': False,
            },
        }
    result = {
        'status': 'ok',
        'authUsers': 0,
        'created': 0,
        'existing': 0,
        'failed': 0,
        'confirmedAuthUsers': 0,
        'privacy': {
            'containsEmails': False,
            'containsUserIds': False,
            'containsApiKeys': False,
        },
    }
    for row in rows:
        if not isinstance(row, dict) or not row.get('id'):
            continue
        result['authUsers'] += 1
        if row.get('email_confirmed'):
            result['confirmedAuthUsers'] += 1
        user = {'id': str(row.get('id')), 'email': row.get('email') or ''}
        try:
            existing = customer_for_user({'id': user['id']}, create=False)
            if existing:
                result['existing'] += 1
                continue
            customer = customer_for_user(user, create=True)
            if customer and customer.get('id'):
                result['created'] += 1
            else:
                result['failed'] += 1
        except Exception as e:
            result['failed'] += 1
            logger.warning(f'Auth signup customer hydration failed: {extract_http_error(e)}')
    return result


def require_verified_account_user(handler, user):
    state = user_email_verification_state(user)
    if state.get('required') and not state.get('verified'):
        handler.write_json(403, {
            'error': 'email_verification_required',
            'message': 'Verify your email before creating API keys or starting paid routing.',
            'emailVerification': state,
        })
        return False
    return True


def form_encode(fields):
    return urllib.parse.urlencode({k: v for k, v in fields.items() if v is not None}).encode('utf-8')


def stripe_request(path, fields, timeout=10):
    if not STRIPE_SECRET_KEY:
        return None
    req = urllib.request.Request(
        'https://api.stripe.com' + path,
        data=form_encode(fields),
        method='POST',
        headers={
            'Authorization': f'Bearer {STRIPE_SECRET_KEY}',
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode('utf-8'))


def store_payment_intent(row):
    row.setdefault('id', uuid.uuid4().hex)
    row.setdefault('created_at_epoch', now_epoch())
    row.setdefault('updated_at_epoch', now_epoch())
    if customer_store_uses_supabase():
        rows = supabase_insert(SUPABASE_PAYMENT_INTENTS_TABLE, row)
        return rows[0] if rows else row
    data = local_customer_store()
    data['payment_intents'].append(row)
    write_local_customer_store(data)
    return row


def payment_intent_for_customer(customer_id, intent_id):
    if customer_store_uses_supabase():
        rows = supabase_select(
            SUPABASE_PAYMENT_INTENTS_TABLE,
            f'select=*&id=eq.{urllib.parse.quote(str(intent_id), safe="")}&customer_id=eq.{urllib.parse.quote(str(customer_id), safe="")}&limit=1',
        )
        return rows[0] if rows else None
    for row in local_customer_store().get('payment_intents', []):
        if row.get('id') == intent_id and row.get('customer_id') == customer_id:
            return row
    return None


def latest_payment_intent_for_customer(customer_id, statuses=None, kinds=None):
    customer_id = str(customer_id or '').strip()
    statuses = [str(status or '').strip() for status in (statuses or []) if str(status or '').strip()]
    kinds = [str(kind or '').strip() for kind in (kinds or []) if str(kind or '').strip()]
    if not customer_id:
        return None
    if customer_store_uses_supabase():
        filters = [
            'select=*',
            f'customer_id=eq.{urllib.parse.quote(customer_id, safe="")}',
            'order=created_at_epoch.desc',
            'limit=1',
        ]
        if statuses:
            encoded = ','.join(urllib.parse.quote(status, safe='') for status in statuses)
            filters.append(f'status=in.({encoded})')
        if kinds:
            encoded = ','.join(urllib.parse.quote(kind, safe='') for kind in kinds)
            filters.append(f'kind=in.({encoded})')
        rows = supabase_select(SUPABASE_PAYMENT_INTENTS_TABLE, '&'.join(filters), timeout=5)
        return rows[0] if rows else None
    rows = [
        row for row in local_customer_store().get('payment_intents', [])
        if row.get('customer_id') == customer_id
        and (not statuses or str(row.get('status') or '') in statuses)
        and (not kinds or str(row.get('kind') or '') in kinds)
    ]
    rows.sort(key=lambda row: int(row.get('created_at_epoch') or 0), reverse=True)
    return rows[0] if rows else None


def payment_intent_by_id(intent_id):
    intent_id = str(intent_id or '').strip()
    if not intent_id:
        return None
    if customer_store_uses_supabase():
        rows = supabase_select(
            SUPABASE_PAYMENT_INTENTS_TABLE,
            f'select=*&id=eq.{urllib.parse.quote(intent_id, safe="")}&limit=1',
        )
        return rows[0] if rows else None
    for row in local_customer_store().get('payment_intents', []):
        if row.get('id') == intent_id:
            return row
    return None


def update_payment_intent(intent_id, updates):
    intent_id = str(intent_id or '').strip()
    updates = dict(updates or {})
    updates['updated_at_epoch'] = now_epoch()
    if not intent_id:
        return None
    if customer_store_uses_supabase():
        rows = supabase_patch(SUPABASE_PAYMENT_INTENTS_TABLE, intent_id, updates)
        return rows[0] if rows else payment_intent_by_id(intent_id)
    data = local_customer_store()
    found = None
    for row in data.get('payment_intents', []):
        if row.get('id') == intent_id:
            row.update(updates)
            found = row
            break
    if found:
        write_local_customer_store(data)
    return found


def approve_manual_payment_intent(intent_id, settlement_reference='', reason_code='billing_review', requested_plan=''):
    intent = payment_intent_by_id(intent_id)
    if not intent:
        return None, None, None
    if str(intent.get('kind') or '') != 'crypto_manual':
        raise ValueError('invalid_payment_intent_kind')
    intent_status = str(intent.get('status') or '').strip().lower()
    if intent_status == 'settled_manual_review':
        raise ValueError('payment_intent_already_settled')
    if intent_status != 'pending_manual_review':
        raise ValueError('payment_intent_not_pending')
    customer_id = intent.get('customer_id')
    customer = customer_by_id(customer_id)
    if not customer:
        raise ValueError('customer_not_found')
    metadata = intent.get('metadata') if isinstance(intent.get('metadata'), dict) else {}
    plan = (
        normalize_stripe_plan(requested_plan)
        or normalize_stripe_plan(metadata.get('plan'))
        or normalize_stripe_plan(customer.get('plan'))
    )
    if not plan:
        raise ValueError('payment_plan_required')
    approved_at = now_epoch()
    updated_metadata = dict(metadata)
    updated_metadata.update({
        'settlement': 'manual',
        'automatic_settlement': False,
        'plan': plan,
        'approved_at_epoch': approved_at,
    })
    reference = bounded_payment_text(settlement_reference, 160)
    if reference:
        updated_metadata['settlement_reference'] = reference
    updated_intent = update_payment_intent(intent.get('id'), {
        'status': 'settled_manual_review',
        'metadata': updated_metadata,
    })
    status_before = str(customer.get('status') or '')
    desired_status = billing_status_for_customer(customer_id, 'active')
    updated_customer = update_customer(customer_id, {
        'plan': plan,
        'status': desired_status,
    })
    audit_event = record_operator_audit_event(
        'payment_intent.approve',
        customer_id,
        status_before=status_before,
        status_after=desired_status,
        revoked_api_keys_count=0,
        reason_code=reason_code,
    )
    return updated_customer or customer_by_id(customer_id), updated_intent or payment_intent_by_id(intent_id), audit_event


def stripe_webhook_event_seen(event_id):
    event_id = str(event_id or '').strip()
    if not event_id:
        return False
    quoted = urllib.parse.quote(event_id, safe='')
    if customer_store_uses_supabase():
        rows = supabase_select(
            SUPABASE_PAYMENT_INTENTS_TABLE,
            f'select=id&kind=eq.stripe_webhook&event_id=eq.{quoted}&limit=1',
            timeout=5,
        )
        return bool(rows)
    return any(
        row.get('kind') == 'stripe_webhook' and row.get('event_id') == event_id
        for row in local_customer_store().get('payment_intents', [])
    )


def store_stripe_webhook_event(event, customer_id=None):
    event_id = str((event or {}).get('id') or '').strip()
    row = {
        'id': f'stripe:{event_id}' if event_id else uuid.uuid4().hex,
        'kind': 'stripe_webhook',
        'customer_id': customer_id,
        'status': 'received',
        'event_type': (event or {}).get('type'),
        'event_id': event_id,
    }
    try:
        return store_payment_intent(row)
    except Exception as e:
        if event_id and '409' in extract_http_error(e):
            return row
        raise


def verify_stripe_signature(payload, signature_header, tolerance_seconds=300):
    if not STRIPE_WEBHOOK_SECRET:
        return False
    parts = {}
    for piece in (signature_header or '').split(','):
        if '=' in piece:
            k, v = piece.split('=', 1)
            parts.setdefault(k, []).append(v)
    timestamp = (parts.get('t') or [''])[0]
    try:
        timestamp_int = int(timestamp)
    except Exception:
        return False
    if tolerance_seconds and abs(now_epoch() - timestamp_int) > int(tolerance_seconds):
        return False
    expected = hmac.new(
        STRIPE_WEBHOOK_SECRET.encode('utf-8'),
        f'{timestamp}.{payload.decode("utf-8", errors="replace")}'.encode('utf-8'),
        hashlib.sha256,
    ).hexdigest()
    return any(hmac.compare_digest(expected, sig) for sig in parts.get('v1', []))


def get_latency_stat(intent_name, provider_name, model):
    return (((LATENCY_STATS.get('intents') or {}).get(intent_name) or {}).get(provider_name) or {}).get(model)


def get_intent_provider_stats(intent_name, provider_name):
    return (((LATENCY_STATS.get('intents') or {}).get(intent_name) or {}).get(provider_name) or {})


def get_health_stat(intent_name, provider_name, model):
    return get_latency_stat(intent_name, provider_name, model) or get_latency_stat('GENERAL', provider_name, model) or {}


def record_latency_outcome(intent_name, provider_name, model, elapsed_seconds, ok, error_text=''):
    elapsed_ms = max(1.0, float(elapsed_seconds) * 1000.0)
    now = int(time.time())
    error_meta = parse_error_meta(error_text)
    with LATENCY_STATS_LOCK:
        intents = LATENCY_STATS.setdefault('intents', {})
        intent_stats = intents.setdefault(intent_name, {})
        provider_stats = intent_stats.setdefault(provider_name, {})
        stat = provider_stats.setdefault(model, {
            'successes': 0,
            'failures': 0,
            'consecutive_failures': 0,
            'rate_limit_hits': 0,
            'timeout_hits': 0,
            'empty_output_hits': 0,
            'cooldown_until': 0,
            'latency_ewma_ms': elapsed_ms,
            'last_latency_ms': elapsed_ms,
            'updated_at': now,
        })

        stat['last_latency_ms'] = elapsed_ms
        stat['updated_at'] = now
        if ok:
            stat['successes'] = int(stat.get('successes', 0)) + 1
            stat['consecutive_failures'] = 0
            stat['cooldown_until'] = 0
            stat['timeout_hits'] = 0
            stat['empty_output_hits'] = 0
            stat['last_success_at'] = now
            previous = float(stat.get('latency_ewma_ms', elapsed_ms) or elapsed_ms)
            stat['latency_ewma_ms'] = round((LATENCY_EWMA_ALPHA * elapsed_ms) + ((1.0 - LATENCY_EWMA_ALPHA) * previous), 2)
            clear_temp_model_block(provider_name, model)
        else:
            stat['failures'] = int(stat.get('failures', 0)) + 1
            stat['consecutive_failures'] = int(stat.get('consecutive_failures', 0)) + 1
            cooldown_until = float(stat.get('cooldown_until', 0) or 0)
            if error_meta['rate_limited']:
                stat['rate_limit_hits'] = int(stat.get('rate_limit_hits', 0)) + 1
                cooldown_until = max(cooldown_until, now + min(1800, RATE_LIMIT_COOLDOWN_BASE_SECONDS * (2 ** max(0, stat['rate_limit_hits'] - 1))))
            if error_meta['timeout']:
                stat['timeout_hits'] = int(stat.get('timeout_hits', 0)) + 1
                if stat['consecutive_failures'] >= CONSECUTIVE_FAILURE_COOLDOWN_THRESHOLD:
                    timeout_backoff = min(1800, FAILURE_COOLDOWN_BASE_SECONDS * (2 ** max(0, stat['timeout_hits'] - 1)))
                    cooldown_until = max(cooldown_until, now + timeout_backoff)
                    set_temp_model_block(provider_name, model, timeout_backoff, 'timeout')
            if error_meta['empty_output']:
                stat['empty_output_hits'] = int(stat.get('empty_output_hits', 0)) + 1
                empty_backoff = min(1800, EMPTY_OUTPUT_COOLDOWN_SECONDS * max(1, stat['empty_output_hits']))
                cooldown_until = max(cooldown_until, now + empty_backoff)
                set_temp_model_block(provider_name, model, empty_backoff, 'empty_output')
            if error_meta['model_missing']:
                cooldown_until = max(cooldown_until, now + MODEL_MISSING_COOLDOWN_SECONDS)
                set_temp_model_block(provider_name, model, MODEL_MISSING_COOLDOWN_SECONDS, 'model_missing')
            if stat['consecutive_failures'] >= CONSECUTIVE_FAILURE_COOLDOWN_THRESHOLD and cooldown_until <= now:
                generic_backoff = min(1800, FAILURE_COOLDOWN_BASE_SECONDS * max(1, stat['consecutive_failures'] - CONSECUTIVE_FAILURE_COOLDOWN_THRESHOLD + 1))
                cooldown_until = now + generic_backoff
                set_temp_model_block(provider_name, model, generic_backoff, 'repeated_failures')
            stat['cooldown_until'] = cooldown_until

        save_latency_stats()
        invalidate_model_health_cache(provider_name, model)


def general_empirical_adjustment(provider, model):
    provider_name = provider.name
    stat = get_latency_stat('GENERAL', provider_name, model)
    provider_stats = get_intent_provider_stats('GENERAL', provider_name)
    if not stat:
        if provider.api_type == 'openclaw-gateway':
            return -4.0, 'cold-gateway'
        # openai-codex-responses is a direct external API, not the recursive
        # gateway — apply the same exploration bonus as other cold models.
        if provider_stats:
            return -2.0, 'provider-known,cold-model'
        return GENERAL_EMPIRICAL_EXPLORATION_BONUS, 'cold'

    successes = int(stat.get('successes', 0))
    failures = int(stat.get('failures', 0))
    samples = successes + failures
    exploration = GENERAL_EMPIRICAL_EXPLORATION_BONUS / math.sqrt(samples + 1)

    if successes <= 0:
        penalty = GENERAL_EMPIRICAL_FAILURE_PENALTY * failures
        return exploration - penalty, f'explore={exploration:.2f},fail={penalty:.2f}'

    latency_ewma_ms = float(stat.get('latency_ewma_ms', GENERAL_EMPIRICAL_LATENCY_PIVOT_MS) or GENERAL_EMPIRICAL_LATENCY_PIVOT_MS)
    exploration = min(exploration, GENERAL_EMPIRICAL_SUCCESS_EXPLORATION_CAP)
    speed_bonus = (GENERAL_EMPIRICAL_LATENCY_PIVOT_MS - latency_ewma_ms) / 250.0
    speed_bonus = max(-GENERAL_EMPIRICAL_LATENCY_BONUS_CAP, min(GENERAL_EMPIRICAL_LATENCY_BONUS_CAP, speed_bonus))
    penalty = GENERAL_EMPIRICAL_FAILURE_PENALTY * failures
    total = speed_bonus + exploration - penalty
    return total, f'ewma_ms={latency_ewma_ms:.0f},explore={exploration:.2f},fail={penalty:.2f}'



def route_latency_target_ms(route_mode: str, complexity: Complexity, thinking: ThinkingLevel):
    base = {
        'fast': 9000,
        'balanced': 14000,
        'best': 24000,
        'local-first': 11000,
        'realtime': 5000,
    }.get(route_mode, 14000)
    if complexity == Complexity.SIMPLE:
        base -= 2000
    elif complexity == Complexity.COMPLEX:
        base += 6000
    if thinking == ThinkingLevel.HIGH:
        base += 4000
    elif thinking == ThinkingLevel.LOW:
        base -= 1500
    return max(6000, min(45000, base))



def empirical_route_adjustment(provider, model, intent_name: str, route_mode: str, complexity: Complexity, thinking: ThinkingLevel):
    stat = get_health_stat(intent_name, provider.name, model)
    provider_stats = get_intent_provider_stats(intent_name, provider.name) or get_intent_provider_stats('GENERAL', provider.name)
    successes = int(stat.get('successes', 0))
    failures = int(stat.get('failures', 0))
    samples = successes + failures

    if samples <= 0:
        if route_mode == 'best':
            return 0.0, 'cold:best-mode'
        if provider.api_type == 'ollama':
            penalty = 6.0 if route_mode == 'balanced' else 4.0
        elif provider.api_type == 'google-generative-language':
            penalty = 10.0 if route_mode == 'balanced' else 12.0
        else:
            penalty = 18.0 if route_mode == 'balanced' else 22.0
        if provider_stats:
            penalty -= 2.0
        return -penalty, f'cold:penalty={penalty:.1f}'

    if successes <= 0:
        penalty = min(30.0, 12.0 + (failures * 3.5))
        if provider.api_type != 'ollama' and route_mode != 'best':
            penalty += 4.0
        if route_mode == 'best':
            penalty *= 0.7
        return -penalty, f'no-success:failures={failures}'

    target_ms = route_latency_target_ms(route_mode, complexity, thinking)
    ewma_ms = float(stat.get('latency_ewma_ms', target_ms) or target_ms)
    delta_seconds = (target_ms - ewma_ms) / 1000.0
    if delta_seconds >= 0:
        latency_adjustment = min(14.0, delta_seconds * 0.9)
    else:
        multiplier = 1.6 if route_mode in {'fast', 'local-first', 'realtime'} else 1.15 if route_mode == 'balanced' else 0.65
        latency_adjustment = -min(30.0, abs(delta_seconds) * multiplier)

    confidence_bonus = min(8.0, math.log2(successes + 1) * 2.0)
    failure_penalty = min(12.0, failures * 0.45)
    total = latency_adjustment + confidence_bonus - failure_penalty
    return total, f'ewma_ms={ewma_ms:.0f},target_ms={target_ms},succ={successes},fail={failures}'



def ollama_family_bonus(model: str, intent: Intent):
    model_l = (model or '').lower()
    best = 0
    for family, meta in OLLAMA_FAMILY_HINTS.items():
        if family in model_l and intent.name in meta['intents']:
            best = max(best, int(meta['bonus']))
    return best


def build_openclaw_gateway_prompt(messages):
    system_parts = []
    conversation_parts = []
    for msg in sanitize_replay_messages(messages):
        role = msg.get('role', 'user')
        content = (msg.get('content') or '').strip()
        if not content:
            continue
        if role in ('system', 'developer'):
            system_parts.append(content)
            continue
        sender = 'Assistant' if role == 'assistant' else 'Tool' if role == 'tool' else 'User'
        conversation_parts.append(f'{sender}: {content}')

    sections = []
    if system_parts:
        sections.append('System instructions:\n' + '\n\n'.join(system_parts))
    if conversation_parts:
        sections.append('Conversation so far:\n' + '\n'.join(conversation_parts))
    sections.append('Reply as the assistant to the latest user message.')
    return '\n\n'.join(section for section in sections if section).strip()


def fetch_ollama_manifest(provider: Provider):
    manifest_file = OLLAMA_MANIFEST_FILES.get(canonical_provider_env_key(provider.name), '')
    if manifest_file:
        try:
            with open(os.path.expanduser(manifest_file)) as f:
                payload = json.load(f)
            if isinstance(payload, dict) and isinstance(payload.get('models'), list):
                return payload, 'file'
        except Exception as e:
            logger.warning(f"Ollama manifest file {provider.name}: {e}")

    manifest_url = OLLAMA_MANIFEST_URLS.get(canonical_provider_env_key(provider.name), '')
    if manifest_url:
        try:
            req = urllib.request.Request(manifest_url, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT_SECONDS) as resp:
                payload = json.loads(resp.read())
            if isinstance(payload, dict) and isinstance(payload.get('models'), list):
                return payload, 'url'
        except Exception as e:
            logger.warning(f"Ollama manifest fetch {provider.name}: {extract_http_error(e)}")
    return None, None


def ollama_manifest_model_id(entry):
    if not isinstance(entry, dict):
        return ''
    return (entry.get('id') or entry.get('model') or entry.get('name') or '').strip()


def apply_ollama_manifest(provider: Provider, manifest):
    models = []
    meta = dict(provider.model_meta or {})
    servable_only = []
    for entry in manifest.get('models', []) or []:
        model_id = ollama_manifest_model_id(entry)
        if not model_id:
            continue
        servable = bool(entry.get('servable', True))
        models.append(model_id)
        meta[model_id] = {
            'reasoning': bool(entry.get('reasoning', False)),
            'contextWindow': entry.get('contextWindow'),
            'maxTokens': entry.get('maxTokens'),
            'input': entry.get('input') or ['text'],
            'servable': servable,
            'preferred': bool(entry.get('preferred', False)),
            'resident': bool(entry.get('resident', False)),
            'manifestReason': entry.get('reason'),
            'supportsChat': entry.get('supportsChat', True),
            'supportsTools': entry.get('supportsTools'),
            'supportsJson': entry.get('supportsJson'),
            'supportsStreaming': entry.get('supportsStreaming', True),
        }
        if servable:
            servable_only.append(model_id)
    provider.model_meta = meta
    provider.models = dedupe_keep_order(servable_only or models or provider.models or [])
    return provider.models


def fetch_ollama_models(provider: Provider):
    now = time.time()
    cached = OLLAMA_MODEL_CACHE.get(provider.name)
    if cached and now - cached['checked_at'] < OLLAMA_MODEL_REFRESH_TTL_SECONDS:
        return cached['models']

    manifest, manifest_source = fetch_ollama_manifest(provider)
    manifest_models = []
    if manifest:
        manifest_models = apply_ollama_manifest(provider, manifest)
    catalog_models = ollama_cloud_catalog_models()
    if catalog_models:
        meta = dict(provider.model_meta or {})
        for model_name in catalog_models:
            meta.setdefault(model_name, ollama_cloud_model_meta(model_name))
        provider.model_meta = meta

    tag_models = []
    try:
        url = provider.base_url.rstrip('/') + '/api/tags'
        req = urllib.request.Request(url, headers={'Content-Type': 'application/json'})
        if provider.api_key:
            req.add_header('Authorization', f'Bearer {provider.api_key}')
        with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT_SECONDS) as resp:
            payload = json.loads(resp.read())
        for model in payload.get('models', []) or []:
            model_name = (model.get('name') or model.get('model') or '').strip()
            if model_name:
                tag_models.append(model_name)
                meta = dict(provider.model_meta or {})
                details = model.get('details', {}) if isinstance(model.get('details'), dict) else {}
                existing = dict(meta.get(model_name) or {})
                existing.update({
                    'reasoning': bool(existing.get('reasoning', False)),
                    'contextWindow': existing.get('contextWindow') or details.get('context_length'),
                    'maxTokens': existing.get('maxTokens'),
                    'input': existing.get('input') or ['text'],
                    'servable': bool(existing.get('servable', True)),
                    'preferred': bool(existing.get('preferred', False)),
                    'resident': bool(existing.get('resident', False)),
                    'manifestReason': existing.get('manifestReason'),
                    'family': details.get('family', existing.get('family', '')),
                    'families': details.get('families') or existing.get('families') or [],
                })
                meta[model_name] = existing
                provider.model_meta = meta
    except Exception as e:
        logger.warning(f"Ollama model discovery {provider.name}: {extract_http_error(e)}")
    tag_models = dedupe_keep_order(tag_models)
    first_local_cloud = next((m for m in tag_models if is_local_cloud_ollama_model(provider, m)), None)
    if first_local_cloud:
        probe_local_ollama_cloud_auth(provider, first_local_cloud)
    known_models = dedupe_keep_order((provider.models or []) + manifest_models + catalog_models + tag_models)
    if known_models:
        provider.models = known_models
    source = 'tags'
    if manifest_models and tag_models:
        source = f'manifest:{manifest_source}+tags'
    elif manifest_models:
        source = f'manifest:{manifest_source}'
    # Cache installed/tagged models separately from configured/manifest-known models.
    OLLAMA_MODEL_CACHE[provider.name] = {'checked_at': now, 'models': tag_models, 'known_models': known_models, 'source': source}
    return tag_models


def parse_error_meta(error_text: str):
    raw = (error_text or '').lower()
    return {
        'rate_limited': 'http 429' in raw or 'rate limit' in raw or 'too many requests' in raw,
        'timeout': 'timed out' in raw or 'timeout' in raw,
        'model_missing': ('model' in raw and 'not found' in raw) or 'no such model' in raw,
        'empty_output': 'empty content' in raw or 'thinking-only output' in raw or 'empty visible content' in raw,
    }


def model_health_snapshot(provider: Provider, model: str, intent_name: str = 'GENERAL'):
    now = time.time()
    cache_key = f'{intent_name}:{provider.name}/{model}'
    cached = MODEL_HEALTH_CACHE.get(cache_key)
    if cached and now - cached['checked_at'] < HEALTH_SCORE_TTL_SECONDS:
        return cached
    stat = get_health_stat(intent_name, provider.name, model)
    successes = int(stat.get('successes', 0))
    failures = int(stat.get('failures', 0))
    consecutive_failures = int(stat.get('consecutive_failures', 0))
    rate_limit_hits = int(stat.get('rate_limit_hits', 0))
    timeout_hits = int(stat.get('timeout_hits', 0))
    empty_output_hits = int(stat.get('empty_output_hits', 0))
    cooldown_until = float(stat.get('cooldown_until', 0) or 0)
    last_success_at = stat.get('last_success_at')
    reachable = provider_endpoint_reachable(provider)
    temp_block = active_temp_model_block(provider.name, model)
    models_present = True
    if provider.api_type == 'ollama':
        live_models = fetch_ollama_models(provider)
        if is_cloud_ollama_model(model) and not is_local_ollama_provider(provider):
            models_present = model in (provider.models or [])
        else:
            models_present = (model in live_models) if live_models else (model in (provider.models or []))
    if temp_block:
        models_present = False
        cooldown_until = max(cooldown_until, float(temp_block.get('until', 0) or 0))
    latency_ewma_ms = float(stat.get('latency_ewma_ms', GENERAL_EMPIRICAL_LATENCY_PIVOT_MS) or GENERAL_EMPIRICAL_LATENCY_PIVOT_MS)
    score = 100.0
    if not reachable:
        score -= 60
    if not models_present:
        score -= 45
    score -= min(35, consecutive_failures * 8)
    score -= min(30, failures * 2)
    score -= min(30, rate_limit_hits * 10)
    score -= min(20, timeout_hits * 6)
    score -= min(15, empty_output_hits * 5)
    score += max(-20, min(20, (GENERAL_EMPIRICAL_LATENCY_PIVOT_MS - latency_ewma_ms) / 200.0))
    if cooldown_until > now:
        score -= 50
    if provider.api_type == 'ollama':
        score += 8
    meta = (provider.model_meta or {}).get(model, {})
    if meta.get('preferred'):
        score += 8
    if meta.get('resident'):
        score += 6
    health = {
        'checked_at': now,
        'reachable': reachable,
        'models_present': models_present,
        'temporarily_blocked': bool(temp_block),
        'temporary_block_reason': (temp_block or {}).get('reason'),
        'latency_ewma_ms': latency_ewma_ms,
        'successes': successes,
        'failures': failures,
        'consecutive_failures': consecutive_failures,
        'rate_limit_hits': rate_limit_hits,
        'timeout_hits': timeout_hits,
        'empty_output_hits': empty_output_hits,
        'cooldown_until': cooldown_until,
        'last_success_at': last_success_at,
        'score': round(score, 2),
    }
    MODEL_HEALTH_CACHE[cache_key] = health
    return health


def provider_endpoint_reachable(provider: Provider) -> bool:
    now = time.time()
    cached = PROVIDER_HEALTH_CACHE.get(provider.name)
    if cached and now - cached['checked_at'] < REACHABILITY_TTL_SECONDS:
        return cached['reachable']

    reachable = False
    try:
        parsed = urllib.parse.urlparse(provider.base_url)
        host = parsed.hostname
        port = parsed.port
        if not host:
            reachable = False
        else:
            if port is None:
                port = 443 if parsed.scheme == 'https' else 80
            with socket.create_connection((host, port), timeout=REACHABILITY_TIMEOUT_SECONDS):
                reachable = True
    except Exception:
        reachable = False

    PROVIDER_HEALTH_CACHE[provider.name] = {'reachable': reachable, 'checked_at': now}
    return reachable


def available_provider_names():
    return [
        name for name, provider in PROVIDERS.items()
        if name not in DISABLED_PROVIDERS and provider.models and provider_endpoint_reachable(provider)
    ]


# Patterns of models to auto-pull when discovered on any Ollama instance.
# Set via env: SAGE_ROUTER_OLLAMA_AUTO_PULL_PATTERNS=comma,separated,patterns
OLLAMA_AUTO_PULL_PATTERNS = [
    p.strip() for p in os.environ.get('SAGE_ROUTER_OLLAMA_AUTO_PULL_PATTERNS', ':cloud').split(',')
    if p.strip()
]
# How often to check for new models to pull (seconds)
OLLAMA_AUTO_PULL_INTERVAL_SECONDS = int(os.environ.get('SAGE_ROUTER_OLLAMA_AUTO_PULL_INTERVAL_SECONDS', '3600'))


def ollama_pattern_matches(pattern: str, model: str):
    pattern = (pattern or '').strip().lower()
    model_l = (model or '').strip().lower()
    if not pattern:
        return False
    if pattern in {'*', 'all'}:
        return True
    if pattern.endswith('*') and model_l.startswith(pattern[:-1]):
        return True
    if pattern.startswith('*') and model_l.endswith(pattern[1:]):
        return True
    return pattern in model_l


def ollama_model_auto_pull_compatible(provider: Provider, model: str):
    if not model or not model_is_servable(provider, model):
        return False
    if not is_chat_capable_model(provider, model):
        return False
    caps = model_capabilities(provider, model)
    return bool(caps.get('chat') and caps.get('streaming', True))


def ollama_auto_pull_new_models():
    """Pull missing compatible Ollama models that match configured patterns.

    Sources are merged from config, manifests, and live /api/tags.  This lets a
    fresh Umbrel Ollama app with zero local tags still pull configured/known
    compatible models instead of being invisible to routing.
    """
    now = time.time()
    last_pull_check_key = '_last_auto_pull_check'
    if now - OLLAMA_MODEL_CACHE.get(last_pull_check_key, 0) < OLLAMA_AUTO_PULL_INTERVAL_SECONDS:
        return
    OLLAMA_MODEL_CACHE[last_pull_check_key] = now

    if not OLLAMA_AUTO_PULL_PATTERNS:
        return

    for provider in PROVIDERS.values():
        if provider.api_type != 'ollama' or provider.name in DISABLED_PROVIDERS:
            continue
        manifest, _ = fetch_ollama_manifest(provider)
        manifest_models = []
        if manifest:
            manifest_models = [ollama_manifest_model_id(m) for m in manifest.get('models', []) or []]

        cache = OLLAMA_MODEL_CACHE.get(provider.name, {})
        available = set(fetch_ollama_models(provider))
        all_known = dedupe_keep_order((provider.models or []) + cache.get('known_models', []) + manifest_models)
        matching = []
        for model in all_known:
            if model in available:
                continue
            if not ollama_model_auto_pull_compatible(provider, model):
                continue
            if any(ollama_pattern_matches(pattern, model) for pattern in OLLAMA_AUTO_PULL_PATTERNS):
                matching.append(model)

        for model in dedupe_keep_order(matching):
            logger.info(f'Auto-pulling missing compatible Ollama model: {model} (provider={provider.name}, patterns={OLLAMA_AUTO_PULL_PATTERNS})')
            try:
                pull_url = provider.base_url.rstrip('/') + '/api/pull'
                data = json.dumps({'name': model, 'stream': False}).encode()
                req = urllib.request.Request(pull_url, data=data, headers={'Content-Type': 'application/json'})
                if provider.api_key:
                    req.add_header('Authorization', f'Bearer {provider.api_key}')
                with urllib.request.urlopen(req, timeout=600) as resp:
                    result = json.loads(resp.read())
                logger.info(f'Auto-pull complete: {model} -> {result.get("status", "ok")}')
                OLLAMA_MODEL_CACHE.pop(provider.name, None)
                fetch_ollama_models(provider)
                MODEL_HEALTH_CACHE.clear()
            except Exception as e:
                logger.warning(f'Auto-pull failed for {model}: {extract_http_error(e)}')


def background_refresh_detect_families():
    """Scan all Ollama providers' /api/tags for new model families.
    - Auto-register chat families into OLLAMA_FAMILY_HINTS with a default bonus.
    - Auto-register non-chat families into NON_CHAT_OLLAMA_FAMILIES.
    - Log newly discovered families for visibility.
    """
    new_chat = []
    new_nonchat = []
    for provider in PROVIDERS.values():
        if provider.api_type != 'ollama':
            continue
        meta = provider.model_meta or {}
        for model_name, info in meta.items():
            family = (info.get('family') or '').strip().lower()
            families = info.get('families') or []
            all_families = set()
            if family:
                all_families.add(family)
            for f in (families if isinstance(families, list) else []):
                if f and isinstance(f, str):
                    all_families.add(f.strip().lower())
            for fam in all_families:
                # Check if non-chat
                is_nonchat = any(pat in fam for pat in NON_CHAT_FAMILY_PATTERNS) or fam in NON_CHAT_OLLAMA_FAMILIES
                if is_nonchat:
                    if fam not in NON_CHAT_OLLAMA_FAMILIES:
                        NON_CHAT_OLLAMA_FAMILIES.add(fam)
                        new_nonchat.append(fam)
                else:
                    # Check if chat family is known
                    known = False
                    for hint_key in OLLAMA_FAMILY_HINTS:
                        if fam.startswith(hint_key) or hint_key.startswith(fam):
                            known = True
                            break
                    if not known and fam not in OLLAMA_FAMILY_HINTS:
                        # Auto-register new chat family with conservative defaults
                        OLLAMA_FAMILY_HINTS[fam] = {'bonus': 5, 'intents': {'GENERAL', 'CODE'}}
                        new_chat.append(fam)
    if new_chat:
        logger.info(f'Auto-registered new chat families: {new_chat}')
    if new_nonchat:
        logger.info(f'Auto-registered new non-chat families: {new_nonchat}')


def background_refresh_loop():
    while True:
        try:
            for provider in PROVIDERS.values():
                if provider.api_type == 'ollama':
                    fetch_ollama_models(provider)
                for model in dedupe_keep_order(provider.models or []):
                    model_health_snapshot(provider, model, 'GENERAL')
            background_refresh_detect_families()
            ollama_auto_pull_new_models()
        except Exception as e:
            logger.warning(f'Background refresh failed: {e}')
        time.sleep(max(30, min(OLLAMA_MODEL_REFRESH_TTL_SECONDS, HEALTH_SCORE_TTL_SECONDS)))


def ensure_background_refresh_started():
    global BACKGROUND_REFRESH_STARTED
    if BACKGROUND_REFRESH_STARTED:
        return
    thread = threading.Thread(target=background_refresh_loop, name='sage-router-refresh', daemon=True)
    thread.start()
    BACKGROUND_REFRESH_STARTED = True


def request_modalities(requirements, payload=None):
    """Return the set of input modalities present in a request.

    Derived from the normalized requirements (which already encode the deep-scan
    signals) with a direct payload re-check as a safety net. Always includes
    'text'. Possible members: text, image, audio, video, document.
    """
    requirements = requirements or {}
    mods = {'text'}
    if requirements.get('vision') or (payload is not None and payload_vision_signal(payload)):
        mods.add('image')
    if requirements.get('audio') or (payload is not None and payload_audio_signal(payload)):
        mods.add('audio')
    if requirements.get('video') or (payload is not None and payload_video_signal(payload)):
        mods.add('video')
    if requirements.get('document'):
        mods.add('document')
    return sorted(mods)


# ---------------------------------------------------------------------------
# Per-model modality ledger. Each time a model successfully serves a request,
# the request's modalities are recorded against that model. Unique modalities
# accumulate in a persisted JSON file so routing can learn, over time, which
# models actually handle which input modalities (and feed that back into
# model_capabilities). This is append-only and conservative: it only ever
# augments a model's declared capabilities, never removes them.
# ---------------------------------------------------------------------------

MODEL_MODALITIES: dict[str, dict] = {}
MODEL_MODALITIES_LOCK = threading.Lock()
_MODEL_MODALITIES_DIRTY = False
_MODEL_MODALITIES_LAST_SAVE = 0.0
_MODEL_MODALITIES_LAST_SHARED_LOAD = 0.0


def _model_modality_key(provider_name, model):
    return f'{provider_name}/{model}'


def model_modalities_shared_enabled():
    return bool(MODEL_MODALITIES_SHARED_ENABLED and SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY)


def model_modalities_shared_status():
    return {
        'enabled': model_modalities_shared_enabled(),
        'configured': bool(SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY),
        'refreshSeconds': MODEL_MODALITIES_SHARED_REFRESH_SECONDS,
        'table': SUPABASE_MODEL_MODALITIES_TABLE,
        'rpc': SUPABASE_MODEL_MODALITIES_RPC,
    }


def _normalize_model_modality_entry(entry, now_ms=None):
    entry = entry or {}
    now_ms = now_ms or int(time.time() * 1000)
    return {
        'modalities': normalize_model_modalities(entry.get('modalities') or []),
        'count': max(0, int(entry.get('count', 0) or 0)),
        'firstSeen': int(entry.get('firstSeen') or entry.get('first_seen_epoch_ms') or now_ms),
        'lastSeen': int(entry.get('lastSeen') or entry.get('last_seen_epoch_ms') or now_ms),
    }


def _merge_model_modality_entry(existing, incoming):
    incoming = _normalize_model_modality_entry(incoming)
    if not existing:
        return incoming
    existing = _normalize_model_modality_entry(existing, incoming.get('firstSeen'))
    return {
        'modalities': sorted(set(existing.get('modalities') or []) | set(incoming.get('modalities') or [])),
        'count': max(int(existing.get('count', 0) or 0), int(incoming.get('count', 0) or 0)),
        'firstSeen': min(int(existing.get('firstSeen') or incoming.get('firstSeen')), int(incoming.get('firstSeen') or existing.get('firstSeen'))),
        'lastSeen': max(int(existing.get('lastSeen') or incoming.get('lastSeen')), int(incoming.get('lastSeen') or existing.get('lastSeen'))),
    }


def merge_model_modalities(entries):
    changed = False
    for key, entry in (entries or {}).items():
        if not key or not isinstance(entry, dict):
            continue
        merged = _merge_model_modality_entry(MODEL_MODALITIES.get(key), entry)
        if MODEL_MODALITIES.get(key) != merged:
            MODEL_MODALITIES[key] = merged
            changed = True
    return changed


def refresh_model_modalities_from_shared(force=False):
    global _MODEL_MODALITIES_LAST_SHARED_LOAD, _MODEL_MODALITIES_DIRTY
    if not model_modalities_shared_enabled():
        return False
    now = time.time()
    if not force and (now - _MODEL_MODALITIES_LAST_SHARED_LOAD) < MODEL_MODALITIES_SHARED_REFRESH_SECONDS:
        return False
    shared = read_supabase_model_modalities()
    _MODEL_MODALITIES_LAST_SHARED_LOAD = now
    if not shared:
        return False
    with MODEL_MODALITIES_LOCK:
        changed = merge_model_modalities(shared)
        if changed:
            _MODEL_MODALITIES_DIRTY = True
    if changed:
        _persist_model_modalities()
    return changed


def read_supabase_model_modalities():
    if not model_modalities_shared_enabled():
        return {}
    try:
        rows = supabase_request(
            f'/rest/v1/{SUPABASE_MODEL_MODALITIES_TABLE}?select=key,modalities,count,first_seen_epoch_ms,last_seen_epoch_ms&order=last_seen_epoch_ms.desc',
            service=True,
            timeout=10,
        ) or []
        entries = {}
        for row in rows:
            if not isinstance(row, dict):
                continue
            key = str(row.get('key') or '').strip()
            if not key:
                continue
            entries[key] = {
                'modalities': row.get('modalities') or [],
                'count': row.get('count') or 0,
                'firstSeen': row.get('first_seen_epoch_ms') or 0,
                'lastSeen': row.get('last_seen_epoch_ms') or 0,
            }
        return entries
    except Exception as e:
        logger.debug(f'Supabase model modality read failed: {extract_http_error(e)}')
        return {}


def write_supabase_model_modalities(provider_name, model, modalities, entry=None):
    if not model_modalities_shared_enabled():
        return False
    modalities = normalize_model_modalities(modalities)
    if not provider_name or not model or not modalities:
        return False
    now_ms = int(time.time() * 1000)
    try:
        supabase_request(
            f'/rest/v1/rpc/{SUPABASE_MODEL_MODALITIES_RPC}',
            method='POST',
            body={
                'provider_name': provider_name,
                'model_name': model,
                'modalities_in': modalities,
                'seen_at_epoch_ms': int((entry or {}).get('lastSeen') or now_ms),
            },
            service=True,
            timeout=6,
        )
        return True
    except Exception as e:
        logger.debug(f'Supabase model modality RPC failed: {extract_http_error(e)}')
    try:
        key = _model_modality_key(provider_name, model)
        entry = _normalize_model_modality_entry(entry or {'modalities': modalities, 'count': 1, 'firstSeen': now_ms, 'lastSeen': now_ms}, now_ms)
        row = {
            'key': key,
            'provider': provider_name,
            'model': model,
            'modalities': entry['modalities'],
            'count': entry['count'],
            'first_seen_epoch_ms': entry['firstSeen'],
            'last_seen_epoch_ms': entry['lastSeen'],
            'updated_at_epoch_ms': now_ms,
        }
        supabase_request(f'/rest/v1/{SUPABASE_MODEL_MODALITIES_TABLE}', method='POST', body=row, service=True, timeout=6)
        return True
    except Exception as e:
        logger.debug(f'Supabase model modality upsert failed: {extract_http_error(e)}')
        return False


def set_supabase_model_modalities(provider_name, model, modalities, entry=None):
    if not model_modalities_shared_enabled():
        return False
    now_ms = int(time.time() * 1000)
    entry = _normalize_model_modality_entry(entry or {'modalities': modalities, 'count': 0, 'firstSeen': now_ms, 'lastSeen': now_ms}, now_ms)
    try:
        row = {
            'key': _model_modality_key(provider_name, model),
            'provider': provider_name,
            'model': model,
            'modalities': entry['modalities'],
            'count': entry['count'],
            'first_seen_epoch_ms': entry['firstSeen'],
            'last_seen_epoch_ms': entry['lastSeen'],
            'updated_at_epoch_ms': now_ms,
        }
        supabase_request(f'/rest/v1/{SUPABASE_MODEL_MODALITIES_TABLE}', method='POST', body=row, service=True, timeout=6)
        return True
    except Exception as e:
        logger.debug(f'Supabase model modality set failed: {extract_http_error(e)}')
        return False


def reset_supabase_model_modalities(provider=None, model=None):
    if not model_modalities_shared_enabled():
        return False
    try:
        if provider and model:
            key = urllib.parse.quote(_model_modality_key(provider, model), safe='')
            supabase_request(f'/rest/v1/{SUPABASE_MODEL_MODALITIES_TABLE}?key=eq.{key}', method='DELETE', service=True, timeout=6)
        else:
            supabase_request(f'/rest/v1/{SUPABASE_MODEL_MODALITIES_TABLE}?key=not.is.null', method='DELETE', service=True, timeout=10)
        return True
    except Exception as e:
        logger.debug(f'Supabase model modality reset failed: {extract_http_error(e)}')
        return False


def load_model_modalities():
    global MODEL_MODALITIES
    try:
        if os.path.exists(APP_MODEL_MODALITIES):
            with open(APP_MODEL_MODALITIES) as f:
                data = json.load(f)
            if isinstance(data, dict):
                MODEL_MODALITIES = {}
                merge_model_modalities(data)
        refresh_model_modalities_from_shared(force=True)
    except Exception as e:
        logger.debug(f'Model modality ledger load failed: {e}')
    return MODEL_MODALITIES


def _persist_model_modalities(force=False):
    global _MODEL_MODALITIES_DIRTY, _MODEL_MODALITIES_LAST_SAVE
    if not force and not _MODEL_MODALITIES_DIRTY:
        return
    # Throttle disk writes: at most once per 5s, unless forced.
    if not force and (time.time() - _MODEL_MODALITIES_LAST_SAVE) < 5:
        return
    try:
        atomic_write_json(APP_MODEL_MODALITIES, MODEL_MODALITIES)
        _MODEL_MODALITIES_DIRTY = False
        _MODEL_MODALITIES_LAST_SAVE = time.time()
    except Exception as e:
        logger.debug(f'Model modality ledger persist failed: {e}')


def record_model_modalities(provider_name, model, modalities):
    """Record that `model` served a request with the given modalities."""
    if not provider_name or not model or not modalities:
        return
    modalities = normalize_model_modalities(modalities)
    if not modalities:
        return
    key = _model_modality_key(provider_name, model)
    now_ms = int(time.time() * 1000)
    global _MODEL_MODALITIES_DIRTY
    with MODEL_MODALITIES_LOCK:
        entry = MODEL_MODALITIES.setdefault(key, {'modalities': [], 'count': 0, 'firstSeen': now_ms, 'lastSeen': now_ms})
        existing = set(entry.get('modalities') or [])
        changed = False
        for m in modalities:
            if m not in existing:
                existing.add(m)
                changed = True
        entry['modalities'] = sorted(existing)
        entry['count'] = int(entry.get('count', 0)) + 1
        entry['lastSeen'] = now_ms
        _MODEL_MODALITIES_DIRTY = True
        snapshot = dict(entry)
    _persist_model_modalities()
    write_supabase_model_modalities(provider_name, model, modalities, snapshot)


MODEL_MODALITY_VALUES = {'text', 'image', 'audio', 'video', 'document'}


def normalize_model_modalities(modalities):
    return sorted({str(m).strip().lower() for m in (modalities or []) if str(m).strip().lower() in MODEL_MODALITY_VALUES})


def requested_modalities_from_requirements(requirements):
    requirements = requirements or {}
    requested = set()
    if requirements.get('vision'):
        requested.add('image')
    if requirements.get('audio'):
        requested.add('audio')
    if requirements.get('video'):
        requested.add('video')
    if requirements.get('document'):
        requested.add('document')
    return requested


def set_model_modalities(payload):
    provider = str(payload.get('provider') or '').strip()
    model = str(payload.get('model') or '').strip()
    key = str(payload.get('key') or '').strip()
    if key and (not provider or not model) and '/' in key:
        provider, model = key.split('/', 1)
    if not provider or not model:
        raise ValueError('provider and model are required')
    modalities = normalize_model_modalities(payload.get('modalities') or [])
    if not modalities:
        raise ValueError('at least one valid modality is required')
    now_ms = int(time.time() * 1000)
    global _MODEL_MODALITIES_DIRTY
    with MODEL_MODALITIES_LOCK:
        entry = MODEL_MODALITIES.setdefault(_model_modality_key(provider, model), {'modalities': [], 'count': 0, 'firstSeen': now_ms, 'lastSeen': now_ms})
        entry['modalities'] = modalities
        entry['count'] = max(0, int(entry.get('count', 0)))
        entry.setdefault('firstSeen', now_ms)
        entry['lastSeen'] = now_ms
        _MODEL_MODALITIES_DIRTY = True
        snapshot = dict(entry)
    _persist_model_modalities(force=True)
    set_supabase_model_modalities(provider, model, modalities, snapshot)
    return {'status': 'ok', 'modelModalities': model_modalities_summary(), 'path': APP_MODEL_MODALITIES}


def reset_model_modalities(payload):
    provider = str((payload or {}).get('provider') or '').strip()
    model = str((payload or {}).get('model') or '').strip()
    key = str((payload or {}).get('key') or '').strip()
    if key and (not provider or not model) and '/' in key:
        provider, model = key.split('/', 1)
    global _MODEL_MODALITIES_DIRTY
    with MODEL_MODALITIES_LOCK:
        if provider and model:
            removed = 1 if MODEL_MODALITIES.pop(_model_modality_key(provider, model), None) is not None else 0
        else:
            removed = len(MODEL_MODALITIES)
            MODEL_MODALITIES.clear()
        _MODEL_MODALITIES_DIRTY = True
    _persist_model_modalities(force=True)
    reset_supabase_model_modalities(provider, model)
    return {'status': 'ok', 'removed': removed, 'modelModalities': model_modalities_summary(), 'path': APP_MODEL_MODALITIES}


def model_learned_modalities(provider_name, model):
    """Return the set of modalities learned for a model (empty if none)."""
    refresh_model_modalities_from_shared()
    with MODEL_MODALITIES_LOCK:
        entry = MODEL_MODALITIES.get(_model_modality_key(provider_name, model))
        if not entry:
            return set()
        return set(entry.get('modalities') or [])


def model_modalities_summary(force=False):
    """Dashboard-safe view of the ledger."""
    refresh_model_modalities_from_shared(force=force)
    with MODEL_MODALITIES_LOCK:
        return {
            key: {
                'modalities': list(entry.get('modalities') or []),
                'count': int(entry.get('count', 0)),
                'firstSeen': entry.get('firstSeen', 0),
                'lastSeen': entry.get('lastSeen', 0),
            }
            for key, entry in MODEL_MODALITIES.items()
        }


load_model_modalities()


def _capable_models_summary(cap_key):
    """Generic diagnostic: models whose model_capabilities[cap_key] is true."""
    summary = {}
    for name, provider in PROVIDERS.items():
        if name in DISABLED_PROVIDERS:
            continue
        reachable = provider_endpoint_reachable(provider)
        models = []
        for model in dedupe_keep_order(provider.models or []):
            caps = model_capabilities(provider, model)
            if not caps.get(cap_key):
                continue
            models.append({
                'id': model,
                'glm': is_glm_model(model),
                'reasoning': bool(caps.get('reasoning')),
                'servable': bool(caps.get('servable')),
                'reachable': reachable,
                'audio': bool(caps.get('audio')),
                'video': bool(caps.get('video')),
            })
        if models:
            summary[name] = models
    return summary


def image_capable_models_summary():
    """Which models are currently treated as image/vision-capable (incl. image-capable GLM variants)."""
    return _capable_models_summary('vision')


def audio_capable_models_summary():
    return _capable_models_summary('audio')


def video_capable_models_summary():
    return _capable_models_summary('video')


def reasoning_capabilities_summary():
    summary = {}
    for name, provider in PROVIDERS.items():
        if name in DISABLED_PROVIDERS:
            continue
        summary[name] = {
            'api': provider.api_type,
            'reachable': provider_endpoint_reachable(provider),
            'models': [
                {
                    'id': model,
                    'capabilities': model_capabilities(provider, model),
                    'health': model_health_snapshot(provider, model, 'GENERAL'),
                }
                for model in dedupe_keep_order(provider.models or [])
            ],
        }
    return summary


def classify_intent_with_local_model(text):
    """Optional tiny local/GPU model classifier for ambiguous routing.

    Enabled with SAGE_ROUTER_INTENT_CLASSIFIER_ENABLED=1. Providers:
    - ollama: POST /api/chat
    - llamacpp/openai-compatible: POST /v1/chat/completions
    """
    if not INTENT_CLASSIFIER_ENABLED:
        return None, {}, {'enabled': False}
    provider = (INTENT_CLASSIFIER_PROVIDER or 'ollama').strip().lower()
    # Small local classifiers are most valuable on vague requests. Keep the
    # prompt deliberately label-only because tiny Qwen/llama.cpp models are
    # more reliable at one-token classification than strict JSON.
    prompt = (
        'Classify this request for AI model routing.\n'
        'Reply with exactly one label and no extra text.\n'
        'Labels: GENERAL, CODE, ANALYSIS, CREATIVE, REALTIME.\n'
        'Use CODE for programming/debugging/implementation.\n'
        'Use REALTIME for current/latest/weather/price/news/time-sensitive facts.\n'
        'Use CREATIVE for writing/story/brainstorm/design ideation.\n'
        'Use ANALYSIS for compare/review/research/explain/why/how reasoning.\n'
        'Use GENERAL for ordinary chat or unclear requests.\n'
        'Examples:\n'
        'Fix this Python bug => CODE\n'
        'Weather today in Paris? => REALTIME\n'
        'Write a sci-fi story => CREATIVE\n'
        'Compare A vs B => ANALYSIS\n'
        f'Request: {text[:INTENT_CLASSIFIER_MAX_PROMPT_CHARS]}\n'
        'Label:'
    )
    started = time.time()
    try:
        if provider == 'ollama':
            payload = {
                'model': INTENT_CLASSIFIER_MODEL,
                'messages': [{'role': 'user', 'content': prompt}],
                'stream': False,
                'options': {'num_predict': 8, 'temperature': 0, 'num_ctx': 1024},
            }
            req = urllib.request.Request(
                INTENT_CLASSIFIER_BASE_URL.rstrip('/') + '/api/chat',
                data=json.dumps(payload).encode(),
                headers={'Content-Type': 'application/json'},
            )
            with urllib.request.urlopen(req, timeout=INTENT_CLASSIFIER_TIMEOUT_SECONDS) as resp:
                body = json.loads(resp.read())
            raw = (body.get('message') or {}).get('content') or ''
        elif provider in {'llamacpp', 'llama.cpp', 'openai-compatible', 'openai_compatible'}:
            payload = {
                'model': INTENT_CLASSIFIER_MODEL,
                'messages': [{'role': 'system', 'content': 'Reply with exactly one routing label.'}, {'role': 'user', 'content': prompt}],
                'stream': False,
                'max_tokens': 8,
                'temperature': 0,
            }
            headers = {'Content-Type': 'application/json'}
            if INTENT_CLASSIFIER_API_KEY:
                headers['Authorization'] = f'Bearer {INTENT_CLASSIFIER_API_KEY}'
            req = urllib.request.Request(
                openai_chat_completions_url(INTENT_CLASSIFIER_BASE_URL),
                data=json.dumps(payload).encode(),
                headers=headers,
            )
            with urllib.request.urlopen(req, timeout=INTENT_CLASSIFIER_TIMEOUT_SECONDS) as resp:
                body = json.loads(resp.read())
            raw = (((body.get('choices') or [{}])[0].get('message') or {}).get('content') or '')
        else:
            return None, {}, {'enabled': True, 'used': False, 'error': f'unsupported provider {provider}'}

        cleaned = raw.strip()
        if cleaned.startswith('```'):
            cleaned = _re.sub(r'^```(?:json)?\s*', '', cleaned, flags=_re.IGNORECASE).strip()
            cleaned = _re.sub(r'\s*```$', '', cleaned).strip()
        parsed = None
        intent_name = ''
        confidence = 0.9
        m = _re.search(r'\{.*\}', cleaned, flags=_re.DOTALL)
        if m:
            try:
                parsed = json.loads(m.group(0))
                intent_name = str(parsed.get('intent') or '').strip().upper()
                confidence = float(parsed.get('confidence') or confidence)
            except Exception:
                parsed = None
        if not intent_name:
            label_match = _re.search(r'\b(GENERAL|CODE|ANALYSIS|CREATIVE|REALTIME)\b', cleaned.upper())
            if label_match:
                intent_name = label_match.group(1)
        if intent_name in Intent.__members__ and confidence >= INTENT_CLASSIFIER_MIN_CONFIDENCE:
            scores = {i: 0 for i in Intent}
            scores[Intent[intent_name]] = max(1, int(confidence * 10))
            return Intent[intent_name], scores, {
                'enabled': True,
                'used': True,
                'provider': provider,
                'baseUrl': INTENT_CLASSIFIER_BASE_URL,
                'model': INTENT_CLASSIFIER_MODEL,
                'confidence': confidence,
                'elapsedMs': round((time.time() - started) * 1000.0, 2),
                'raw': parsed if parsed is not None else cleaned,
            }
        return None, {}, {'enabled': True, 'used': False, 'provider': provider, 'model': INTENT_CLASSIFIER_MODEL, 'confidence': confidence, 'intent': intent_name, 'elapsedMs': round((time.time() - started) * 1000.0, 2), 'raw': cleaned[:200], 'error': 'low confidence or invalid intent'}
    except Exception as e:
        return None, {}, {'enabled': True, 'used': False, 'provider': provider, 'model': INTENT_CLASSIFIER_MODEL, 'elapsedMs': round((time.time() - started) * 1000.0, 2), 'error': extract_http_error(e)}


def analysis_signal_score(text):
    tl = (text or '').lower()
    score = 0
    for kw in ANALYSIS_SIGNAL_TERMS:
        if kw in tl:
            score += 2 if ' ' in kw or '-' in kw else 1
    if '?' in tl and any(prefix in tl for prefix in ('can we', 'could we', 'should we', 'would it', 'do we', 'how ', 'why ', 'what would', 'what should')):
        score += 2
    if len(tl.split()) >= 40 and any(x in tl for x in ('because', 'but', 'however', 'tradeoff', 'risk', 'if ', 'when ')):
        score += 2
    return score


def heuristic_intent_scores(text):
    tl = text.lower(); scores = {i:0 for i in Intent}
    for kw in ['write','code','debug','fix','refactor','implement','function','bug','test','.py','.js']:
        if kw in tl: scores[Intent.CODE] += 1
    if '```' in text: scores[Intent.CODE] += 3
    for kw in ['analyze','explain','compare','research','why','how does','review','translate','summarize','summary','extract','parse','pdf','document','report','informe','conclusion','findings','medical report','mri','resonancia']:
        if kw in tl: scores[Intent.ANALYSIS] += 1
    scores[Intent.ANALYSIS] += analysis_signal_score(text)
    for kw in ['create','brainstorm','imagine','design','story']:
        if kw in tl: scores[Intent.CREATIVE] += 2
    for kw in ['now','today','current','latest','price','weather']:
        if kw in tl: scores[Intent.REALTIME] += 2
    return scores


def normalized_intent_pattern(text):
    """Collapse a request into a stable cache key for similar routing intent.

    Keep signal words, but strip volatile values so "fix foo.py line 41" and
    "fix bar.ts line 98" reuse the same classifier hint.
    """
    t = (text or '').lower()[:INTENT_CLASSIFIER_MAX_PROMPT_CHARS]
    t = _re.sub(r'```.*?```', ' <codeblock> ', t, flags=_re.DOTALL)
    t = _re.sub(r'`[^`]*`', ' <inline> ', t)
    t = _re.sub(r'https?://\S+', ' <url> ', t)
    t = _re.sub(r'(?<!\w)[~/./-]*[\w.-]+/(?:[\w./-]+)', ' <path> ', t)
    t = _re.sub(r'\b[\w.-]+\.(py|js|ts|tsx|jsx|json|md|yml|yaml|sh|sql|html|css)\b', ' <file> ', t)
    t = _re.sub(r'\b[0-9a-f]{7,40}\b', ' <hash> ', t)
    t = _re.sub(r'\b\d+(?:\.\d+)?\b', ' <num> ', t)
    t = _re.sub(r'[^a-z0-9_<>{}:+#./-]+', ' ', t)
    return _re.sub(r'\s+', ' ', t).strip()[:512]


def _intent_cache_get(pattern):
    if not pattern:
        return None
    now = time.time()
    with INTENT_CLASSIFIER_CACHE_LOCK:
        item = INTENT_CLASSIFIER_CACHE.get(pattern)
        if not item:
            return None
        if now - item.get('ts', 0) > INTENT_CLASSIFIER_CACHE_TTL_SECONDS:
            INTENT_CLASSIFIER_CACHE.pop(pattern, None)
            return None
        return dict(item)


def _intent_cache_put(pattern, intent, scores, meta):
    if not pattern or intent is None:
        return
    with INTENT_CLASSIFIER_CACHE_LOCK:
        if len(INTENT_CLASSIFIER_CACHE) >= INTENT_CLASSIFIER_CACHE_MAX:
            oldest = min(INTENT_CLASSIFIER_CACHE, key=lambda k: INTENT_CLASSIFIER_CACHE[k].get('ts', 0), default=None)
            if oldest:
                INTENT_CLASSIFIER_CACHE.pop(oldest, None)
        INTENT_CLASSIFIER_CACHE[pattern] = {
            'ts': time.time(),
            'intent': intent.name,
            'scores': {k.name: v for k, v in (scores or {}).items()},
            'meta': dict(meta or {}),
        }


def _warm_intent_cache_async(text, pattern, heuristic_winner, heuristic_score):
    def worker():
        model_intent, model_scores, model_meta = classify_intent_with_local_model(text)
        if model_intent is None:
            return
        if heuristic_score >= 2 and heuristic_winner != model_intent:
            return
        _intent_cache_put(pattern, model_intent, model_scores, model_meta)

    thread = threading.Thread(target=worker, name='sage-router-intent-cache', daemon=True)
    thread.start()


def classify_intent(text):
    heuristic_scores = heuristic_intent_scores(text)
    heuristic_winner = max(heuristic_scores, key=heuristic_scores.get)
    heuristic_score = heuristic_scores.get(heuristic_winner, 0)
    heuristic_intent = heuristic_winner if heuristic_score > 0 else Intent.GENERAL

    # Default path: deterministic heuristics only. This avoids adding a model
    # round trip before the real response starts.
    if not INTENT_CLASSIFIER_ENABLED:
        LAST_ROUTE_DEBUG['intentClassifier'] = {'enabled': False, 'used': False}
        return heuristic_intent, heuristic_scores

    pattern = normalized_intent_pattern(text)
    cached = _intent_cache_get(pattern)
    if cached and heuristic_score < INTENT_CLASSIFIER_ONLY_IF_HEURISTIC_BELOW:
        intent_name = cached.get('intent')
        if intent_name in Intent.__members__:
            scores = {i: 0 for i in Intent}
            for k, v in (cached.get('scores') or {}).items():
                if k in Intent.__members__:
                    scores[Intent[k]] = v
            meta = dict(cached.get('meta') or {})
            meta.update({'enabled': True, 'used': True, 'source': 'cache', 'pattern': pattern})
            LAST_ROUTE_DEBUG['intentClassifier'] = meta
            return Intent[intent_name], scores

    meta = {
        'enabled': True,
        'used': False,
        'source': 'heuristic',
        'heuristicIntent': heuristic_intent.name,
        'heuristicScore': heuristic_score,
        'threshold': INTENT_CLASSIFIER_ONLY_IF_HEURISTIC_BELOW,
        'pattern': pattern,
    }
    if heuristic_score >= INTENT_CLASSIFIER_ONLY_IF_HEURISTIC_BELOW:
        meta['skippedByHeuristic'] = True
    elif INTENT_CLASSIFIER_ASYNC:
        meta['asyncWarmupQueued'] = True
        _warm_intent_cache_async(text, pattern, heuristic_winner, heuristic_score)
    else:
        # Synchronous mode remains available for explicit tests, but should not
        # be enabled in normal operation.
        model_intent, model_scores, model_meta = classify_intent_with_local_model(text)
        if model_intent is not None:
            _intent_cache_put(pattern, model_intent, model_scores, model_meta)
        meta.update(model_meta or {})

    LAST_ROUTE_DEBUG['intentClassifier'] = meta
    return heuristic_intent, heuristic_scores

def estimate_complexity(text):
    w = len(text.split())
    analysis_score = analysis_signal_score(text)
    if w > 200 or analysis_score >= 6 or (analysis_score >= 4 and w >= 35):
        return Complexity.COMPLEX
    if w < 30 and analysis_score < 3:
        return Complexity.SIMPLE
    return Complexity.MEDIUM

def pick_model(prov, prefer=None):
    if not prov.models: return ''
    if prefer:
        for wanted in prefer:
            for m in prov.models:
                if m == wanted or wanted in m:
                    return m
    return prov.models[0]


def normalize_thinking(raw):
    if isinstance(raw, dict):
        raw = raw.get('effort') or raw.get('level') or raw.get('thinking')
    if raw is None:
        return DEFAULT_THINKING_LEVEL
    value = str(raw).strip().lower()
    if value in {'low', 'minimal'}:
        return ThinkingLevel.LOW
    if value in {'medium', 'normal', 'default'}:
        return ThinkingLevel.MEDIUM
    if value in {'high', 'max', 'deep'}:
        return ThinkingLevel.HIGH
    return DEFAULT_THINKING_LEVEL


def thinking_max_tokens(level: ThinkingLevel):
    if level == ThinkingLevel.LOW:
        return 4096
    if level == ThinkingLevel.HIGH:
        return 12288
    return 8192


def model_quality_tier(model):
    model_l = (model or '').lower()
    if any(h in model_l for h in WEAK_ANALYSIS_MODEL_HINTS) and not any(h in model_l for h in ('opus', 'sonnet', '-pro', ' pro')):
        return 'weak'
    if any(h in model_l for h in ANALYSIS_QUALITY_MODEL_HINTS):
        return 'strong'
    return 'medium'


ROUTER_PROFILE_CACHE = {'mtime': None, 'profiles': {}}


def builtin_router_profile(name):
    name = str(name or '').strip().lower()
    if name != 'auto':
        return None
    return {
        'description': 'Default reliable auto-routing for first requests and general hosted traffic.',
        'route': 'balanced',
        'thinking': 'medium',
        'defaultModel': 'google/gemini-2.5-flash',
        'allowProviders': ['google', 'google-vertex', 'openrouter', 'nvidia-nim', 'openai', 'openai-codex'],
        'fallbackProviders': ['google', 'google-vertex', 'openrouter', 'nvidia-nim', 'openai', 'openai-codex'],
        'allowModels': ['*gemini-2.5-flash*', '*gemini-3-flash*'],
        'suppressIntermediateToolText': True,
    }


def load_router_profiles():
    try:
        st = os.stat(ROUTER_PROFILES_PATH)
        if ROUTER_PROFILE_CACHE.get('mtime') == st.st_mtime:
            return ROUTER_PROFILE_CACHE.get('profiles') or {}
        with open(ROUTER_PROFILES_PATH) as f:
            data = json.load(f)
        profiles = data.get('profiles', data) if isinstance(data, dict) else {}
        if not isinstance(profiles, dict):
            profiles = {}
        ROUTER_PROFILE_CACHE.update({'mtime': st.st_mtime, 'profiles': profiles})
        return profiles
    except FileNotFoundError:
        ROUTER_PROFILE_CACHE.update({'mtime': None, 'profiles': {}})
        return {}
    except Exception as e:
        logger.warning(f'Failed to load router profiles: {e}')
        return ROUTER_PROFILE_CACHE.get('profiles') or {}


def resolve_router_profile_name(payload):
    if not isinstance(payload, dict):
        return None
    for key in ('profile', 'routerProfile', 'sageRouterProfile'):
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    model = str(payload.get('model') or '').strip()
    if model.startswith('sage-router/'):
        name = model.split('/', 1)[1]
        if name:
            return name
    elif model and '/' not in model and model not in PROVIDERS:
        return model
    return None


def apply_router_profile(payload):
    if not isinstance(payload, dict):
        return None
    profile_name = resolve_router_profile_name(payload)
    if not profile_name:
        return None
    profile = load_router_profiles().get(profile_name)
    if profile_name == 'auto':
        stale_allow = set((profile or {}).get('allowProviders') or [])
        stale_fallbacks = set((profile or {}).get('fallbackProviders') or [])
        if not isinstance(profile, dict) or (
            stale_allow <= {'ollama-cloud', 'ollama'}
            and stale_fallbacks <= {'ollama-cloud', 'ollama'}
        ):
            profile = builtin_router_profile(profile_name)
    if not isinstance(profile, dict):
        return None
    if profile.get('route'):
        payload['route'] = profile.get('route')
    if profile.get('thinking'):
        payload['thinking'] = {'effort': str(profile.get('thinking'))}
    req = payload.get('requirements')
    if not isinstance(req, dict):
        req = {}
    for key in ('qualitySensitive', 'reasoning', 'tools', 'preferTools', 'json', 'vision', 'audio', 'video', 'document', 'longContext', 'frontierOrReasoningTools', 'suppressToolCallContent', 'agentic'):
        if key in profile:
            req[key] = bool(profile.get(key))
    if profile.get('suppressIntermediateToolText'):
        req['suppressToolCallContent'] = True
    if profile.get('requiresQuality'):
        payload['requiresQuality'] = True
        req['qualitySensitive'] = True
    if profile.get('requiresReasoning'):
        payload['requiresReasoning'] = True
        req['reasoning'] = True
    if profile.get('requiresTools'):
        payload['requiresTools'] = True
        req['tools'] = True
    if profile.get('frontierLargeOnly'):
        req['frontierLargeOnly'] = True
    if profile.get('frontierOrReasoningTools'):
        req['frontierOrReasoningTools'] = True
    if profile.get('minParamsB') is not None:
        req['minParamsB'] = profile.get('minParamsB')
    for key in ('allowModels', 'denyModels', 'denyProviders'):
        if profile.get(key):
            req[key] = profile.get(key)
    # Merge allowProviders + fallbackProviders so fallbacks are allowed (with score penalty)
    allow = list(profile.get('allowProviders') or [])
    fallbacks = list(profile.get('fallbackProviders') or [])
    if allow or fallbacks:
        req['allowProviders'] = dedupe_keep_order(allow + fallbacks)
    if fallbacks:
        req['fallbackProviders'] = fallbacks
    payload['requirements'] = req
    if str(payload.get('model') or '').strip() in {profile_name, f'sage-router/{profile_name}'}:
        payload['model'] = str(profile.get('defaultModel') or 'sage-router/auto')
    return profile_name


def client_visible_model_for_request(payload, applied_profile=None, original_model=''):
    """Return the model id clients should see for router-profile requests."""
    original_model = str(original_model or '').strip()
    if applied_profile:
        if original_model.startswith('sage-router/') or original_model.startswith('smart-router/'):
            return f'sage-router/{applied_profile}'
        if original_model == applied_profile:
            return f'sage-router/{applied_profile}'
        if any(str((payload or {}).get(key) or '').strip() for key in ('profile', 'routerProfile', 'sageRouterProfile')):
            return f'sage-router/{applied_profile}'
    if original_model.startswith('sage-router/') or original_model.startswith('smart-router/'):
        return original_model.replace('smart-router/', 'sage-router/', 1)
    return ''


GOAL_CONTEXT_RE = re.compile(r'<codex_internal_context\b[^>]*source=["\']goal["\'][^>]*>.*?</codex_internal_context>', re.IGNORECASE | re.DOTALL)
GOAL_OBJECTIVE_RE = re.compile(r'<objective>\s*(.*?)\s*</objective>', re.IGNORECASE | re.DOTALL)
GOAL_SLASH_RE = re.compile(r'(?m)^\s*/goal(?:\s+(.*))?\s*$')


def _plain_xml_text(text):
    return re.sub(r'<[^>]+>', '', str(text or '')).strip()


def extract_goal_compat_text(text):
    """Return (clean_text, goal_items) for Codex/OpenClaw /goal compatibility."""
    raw = str(text or '')
    goal_items = []

    def remember_context(match):
        block = match.group(0)
        objective_match = GOAL_OBJECTIVE_RE.search(block)
        objective = _plain_xml_text(objective_match.group(1)) if objective_match else ''
        if not objective:
            objective = _plain_xml_text(block)
        if objective:
            goal_items.append({'kind': 'codex_internal_context', 'objective': objective})
        return ''

    cleaned = GOAL_CONTEXT_RE.sub(remember_context, raw)

    def remember_slash(match):
        value = (match.group(1) or '').strip()
        goal_items.append({'kind': 'slash_goal', 'objective': value or 'resume'})
        return ''

    cleaned = GOAL_SLASH_RE.sub(remember_slash, cleaned).strip()
    return cleaned, goal_items


def goal_compat_instruction(goal_items):
    if not goal_items:
        return ''
    objectives = []
    for item in goal_items:
        objective = str((item or {}).get('objective') or '').strip()
        if objective:
            objectives.append(objective)
    if not objectives:
        return ''
    unique = dedupe_keep_order(objectives)
    lines = [
        'Codex/OpenClaw goal mode is active.',
        'Treat the following user-provided goal objective as persistent task context; do not answer as if `/goal` is an unknown slash command.',
    ]
    for idx, objective in enumerate(unique, start=1):
        lines.append(f'Goal {idx}: {objective}')
    lines.extend([
        'Continue concrete work toward the goal, preserve tool-call compatibility, and avoid exposing internal control markup unless the user asks for it.',
    ])
    return '\n'.join(lines)


def apply_goal_compat(payload):
    if not isinstance(payload, dict):
        return False
    messages = payload.get('messages')
    if not isinstance(messages, list):
        return False
    updated = []
    goal_items = []
    for msg in messages:
        if not isinstance(msg, dict):
            updated.append(msg)
            continue
        content = msg.get('content')
        if isinstance(content, str):
            cleaned, found = extract_goal_compat_text(content)
            if found:
                goal_items.extend(found)
                msg = dict(msg)
                if cleaned:
                    msg['content'] = cleaned
                    updated.append(msg)
                continue
        updated.append(msg)
    instruction = goal_compat_instruction(goal_items)
    if not instruction:
        return False
    updated.insert(0, {'role': 'user', 'content': instruction})
    payload['messages'] = updated
    req = payload.get('requirements') if isinstance(payload.get('requirements'), dict) else {}
    req.update({
        'qualitySensitive': True,
        'reasoning': True,
        'longContext': True,
        'agentic': True,
        'suppressToolCallContent': True,
        'frontierOrReasoningTools': True,
    })
    payload['requirements'] = req
    payload.setdefault('route', 'best')
    payload.setdefault('thinking', {'effort': 'high'})
    metadata = payload.get('metadata') if isinstance(payload.get('metadata'), dict) else {}
    metadata['codexGoalMode'] = True
    metadata['goalObjectiveCount'] = len(goal_items)
    payload['metadata'] = metadata
    return True


def _match_any_pattern(value, patterns):
    if not patterns:
        return False
    value_l = str(value or '').lower()
    import fnmatch
    for pattern in patterns:
        pattern_l = str(pattern or '').lower()
        if not pattern_l:
            continue
        if any(ch in pattern_l for ch in '*?['):
            if fnmatch.fnmatch(value_l, pattern_l):
                return True
        elif pattern_l == value_l or pattern_l in value_l:
            return True
    return False


def _match_model_patterns(provider_name, model, patterns):
    if not patterns:
        return False
    model_key = f'{provider_name}/{model}'
    model_patterns = [p for p in patterns if '/' not in str(p or '')]
    keyed_patterns = [p for p in patterns if '/' in str(p or '')]
    return _match_any_pattern(model, model_patterns) or _match_any_pattern(model_key, keyed_patterns)


def estimate_model_params_b(model):
    model_l = (model or '').lower()
    import re
    nums = [float(x) for x in re.findall(r'(?<![a-z0-9])(\d+(?:\.\d+)?)\s*b(?![a-z])', model_l)]
    if nums:
        return max(nums)
    if any(h in model_l for h in ('405b', 'llama4-405b')):
        return 405
    if any(h in model_l for h in ('340b', 'nemotron-4-340b')):
        return 340
    if any(h in model_l for h in ('gpt-5', 'gpt-4.5', 'claude-opus', 'claude-sonnet-4', 'claude-4', 'gemini-3', 'gemini-2.5-pro', 'hunter-alpha', 'healer-alpha', 'kimi-k2', 'glm-5', 'deepseek-v4', 'qwen3.5', 'qwen3.6', 'minimax-m3', 'minimax-m2.7', 'mistral-large-3', 'z1-ultra')):
        return 999
    return 0


FRONTIER_LARGE_MODEL_HINTS = (
    'gpt-5', 'gpt-4.5', 'claude-opus', 'claude-sonnet-4', 'claude-4',
    'gemini-3', 'gemini-2.5-pro',
    'llama-3.1-405b', 'llama4-405b',
    'nemotron-4-340b', 'hunter-alpha', 'healer-alpha',
    'kimi-k2', 'kimi-k2.5', 'kimi-k2.6', 'glm-5', 'deepseek-v4', 'qwen3.5', 'qwen3.6', 'minimax-m3', 'minimax-m2.7', 'mistral-large-3', 'z1-ultra',
)


def model_is_frontier_large(model):
    model_l = (model or '').lower()
    return any(hint in model_l for hint in FRONTIER_LARGE_MODEL_HINTS)


def payload_discord_public_signal(payload):
    if not isinstance(payload, dict):
        return False
    model = str(payload.get('model') or '').strip().lower()
    if model in {'discord-public', 'sage-router/discord-public', 'frontier-public', 'sage-router/frontier-public'}:
        return True
    try:
        haystack = json.dumps({k: payload.get(k) for k in ('metadata', 'agent', 'agentId', 'sessionKey', 'source', 'messages')}, default=str)[:16000].lower()
    except Exception:
        haystack = str(payload)[:16000].lower()
    return 'discord-public' in haystack


def discord_public_allowed_providers():
    base = [
        'google', 'google-vertex', 'openai-codex', 'openai',
        'ollama-cyber', 'ollama', 'openrouter', 'nvidia-nim',
    ]
    discovered_ollama = [
        provider_name
        for provider_name, provider in PROVIDERS.items()
        if provider.api_type == 'ollama'
    ]
    return dedupe_keep_order(base + discovered_ollama)


def discord_public_relaxed_requirements(requirements):
    relaxed = dict(requirements or {})
    for key in ('allowModels', 'frontierLargeOnly', 'minParamsB'):
        relaxed.pop(key, None)
    relaxed['frontierOrReasoningTools'] = False
    return relaxed


def apply_discord_public_route_profile(payload):
    """Force public Discord traffic onto quality-first routing.

    Public channels are user-visible product surfaces, so cheap/mini/local-small
    models are not acceptable defaults.  This profile requires either a known
    frontier/large model, or a model that supports both reasoning and tools,
    then runs with high thinking and best route mode.
    """
    if not payload_discord_public_signal(payload):
        return False
    payload['thinking'] = {'effort': 'high'}
    payload['route'] = 'best'
    req = payload.get('requirements')
    if not isinstance(req, dict):
        req = {}
    existing_denies = list(req.get('denyModels') or [])
    existing_allows = list(req.get('allowModels') or [])
    provider_allow = discord_public_allowed_providers()
    provider_fallbacks = ['openrouter', 'nvidia-nim']
    req.update({
        'qualitySensitive': True,
        'reasoning': False,
        'frontierLargeOnly': False,
        'frontierOrReasoningTools': False,
        'suppressToolCallContent': True,
        'allowModels': dedupe_keep_order(existing_allows + [
            '*glm-5*',
            '*kimi-k2*',
            '*gpt-5*',
            '*deepseek-v4*',
            '*qwen3.[5-9]*',
            '*minimax-m3*',
            '*minimax-m2.[7-9]*',
            '*mistral-large-3*',
            '*gemini-2.5-flash*',
            'google/gemini-2.5-flash',
            'google/gemini-3-flash-preview',
            'google/gemini-2.5-pro',
            'openrouter/gemini-2.5-flash',
            'openrouter/google/gemini-2.5-flash',
            'google-vertex/gemini-2.5-flash',
            'google-vertex/gemini-3-flash-preview',
            'google-vertex/gemini-2.5-pro',
        ]),
        'allowProviders': dedupe_keep_order(provider_allow),
        'fallbackProviders': dedupe_keep_order(provider_fallbacks),
        # Merge instead of replace so the named profile's existing denyModels
        # (e.g. router-profiles.json's '*mini*') are preserved alongside the
        # discord-public hardcoded list.
        'denyModels': dedupe_keep_order(existing_denies + [
            '*1.2b*', '*2b*', '*3b*', '*4b*', '*7b*', '*8b*', '*12b*', '*14b*',
            '*-mini*', 'mini-*', 'mini:*', '*haiku*', '*flash-lite*', '*gemma-3n*', '*lfm-2.5*', '*laguna-xs*',
            '*deepseek-r1*', '*deepseek-v3*', '*glm-4*', '*minimax-m2.5*', '*mistral-large-2*',
            '*claude*', '*llama*', '*nemotron*', '*trinity*', '*nemo*',
        ]),
    })
    payload['requirements'] = req
    payload['requiresQuality'] = True
    payload.pop('requiresReasoning', None)
    return True


def score_provider_model(provider, model, intent, complexity, thinking=DEFAULT_THINKING_LEVEL, route_mode='balanced', estimated_tokens=0, debug_scores=None, requirements=None):
    requirements = requirements or {}
    intent_key = intent.name
    api_score = INTENT_API_SCORES.get(intent_key, {}).get(provider.api_type, 40)
    model_l = model.lower()
    provider_l = provider.name.lower()
    score = api_score
    contributions = [('api_base', round(api_score, 2))]

    fallback_providers = requirements.get('fallbackProviders') or []
    if provider.name in fallback_providers:
        score -= 250
        contributions.append(('profile_fallback_provider_penalty', -250))

    for idx, hint in enumerate(INTENT_MODEL_HINTS.get(intent_key, [])):
        if hint in model_l:
            bonus = max(1, 12 - idx)
            score += bonus
            contributions.append((f'intent_hint:{hint}', round(bonus, 2)))

    ctx_window = model_context_window(provider, model)
    if estimated_tokens and ctx_window and ctx_window < estimated_tokens * 1.2:
        score -= 20
        contributions.append(('context_window_penalty', -20))
    elif estimated_tokens and ctx_window and ctx_window >= max(64000, estimated_tokens * 2):
        score += 6
        contributions.append(('long_context_bonus', 6))

    if provider.api_type == 'anthropic-messages' and intent in (Intent.CODE, Intent.ANALYSIS, Intent.GENERAL):
        score += 4
        contributions.append(('anthropic_reasoning_bias', 4))
    # openclaw-gateway is recursive (routes through this router), so it gets
    # a fixed low base score - only used as a fallback, never preferred.
    # openai-codex-responses is a direct external API, so it does NOT get the
    # gateway penalty — it competes on its own merits like plain openai.
    if provider.api_type == 'openclaw-gateway':
        score = min(score, 40)
        contributions.append(('openclaw_gateway_recursive_cap', min(0, 40 - score)))
        score -= 4
        contributions.append(('openclaw_gateway_penalty', -4))

    if intent == Intent.CODE:
        if provider.name == 'openai-codex' or model_l.startswith('gpt-') or 'codex' in model_l:
            score += 14
            contributions.append(('user_pref_code_gpt', 14))
            if complexity == Complexity.COMPLEX:
                score += 8
                contributions.append(('complex_code_gpt_bonus', 8))
        elif provider.api_type == 'anthropic-messages':
            score -= 10
            contributions.append(('user_pref_code_non_gpt_penalty', -10))
            if complexity == Complexity.COMPLEX and 'opus' in model_l:
                score += 18
                contributions.append(('complex_code_dario_opus_bonus', 18))
            elif complexity != Complexity.COMPLEX and 'sonnet' in model_l:
                score += 14
                contributions.append(('simple_code_dario_sonnet_bonus', 14))
            elif 'haiku' in model_l:
                score -= 8
                contributions.append(('code_dario_haiku_penalty', -8))
        elif provider.api_type == 'ollama':
            if 'glm-5' in model_l:
                score += 18
                contributions.append(('user_pref_code_glm_bonus', 18))
                if complexity == Complexity.COMPLEX:
                    score += 8
                    contributions.append(('complex_code_glm_bonus', 8))
            elif 'kimi' in model_l:
                score += 6
                contributions.append(('user_pref_code_kimi_fallback', 6))
                if complexity == Complexity.COMPLEX:
                    score -= 4
                    contributions.append(('complex_code_kimi_penalty', -4))
            else:
                score -= 8
                contributions.append(('user_pref_code_other_ollama_penalty', -8))

    if intent == Intent.ANALYSIS:
        tier = model_quality_tier(model)
        if provider.api_type == 'ollama':
            score += 18
            contributions.append(('user_pref_analysis_ollama', 18))
        elif provider.name == 'openai-codex' or provider.api_type == 'openai-codex-responses':
            score += 64
            contributions.append(('user_pref_analysis_codex_subscription', 64))
        elif provider.api_type == 'openclaw-gateway':
            score -= 10
            contributions.append(('user_pref_analysis_gateway_penalty', -10))
        if tier == 'strong':
            score += 24
            contributions.append(('analysis_strong_model_bonus', 24))
        elif tier == 'weak':
            score -= 32
            contributions.append(('analysis_weak_model_penalty', -32))
        if complexity == Complexity.COMPLEX and tier != 'strong':
            score -= 16
            contributions.append(('complex_analysis_non_strong_penalty', -16))
        if requirements.get('qualitySensitive') and tier == 'strong':
            score += 12
            contributions.append(('quality_sensitive_strong_bonus', 12))
        elif requirements.get('qualitySensitive') and tier == 'weak':
            score -= 18
            contributions.append(('quality_sensitive_weak_penalty', -18))
    if complexity == Complexity.COMPLEX and any(hint in model_l for hint in COMPLEX_MODEL_HINTS):
        score += 5
        contributions.append(('complex_model_bonus', 5))
    if complexity == Complexity.COMPLEX and any(hint in model_l for hint in LIGHTWEIGHT_MODEL_HINTS):
        score -= 8
        contributions.append(('lightweight_complex_penalty', -8))
    if complexity == Complexity.SIMPLE and any(hint in model_l for hint in LIGHTWEIGHT_MODEL_HINTS):
        score += 2
        contributions.append(('lightweight_simple_bonus', 2))
    if requirements.get('qualitySensitive') and any(hint in model_l for hint in LIGHTWEIGHT_MODEL_HINTS):
        score -= 12
        contributions.append(('quality_sensitive_lightweight_penalty', -12))
    if requirements.get('frontierOrReasoningTools'):
        if model_is_frontier_large(model):
            score += 100
            contributions.append(('discord_public_frontier_large_bonus', 100))
        elif model_capabilities(provider, model).get('reasoning') and model_capabilities(provider, model).get('tools'):
            score += 70
            contributions.append(('discord_public_reasoning_tools_bonus', 70))
        else:
            score -= 120
            contributions.append(('discord_public_low_capability_penalty', -120))
    if requirements.get('frontierLargeOnly') and model_is_frontier_large(model):
        score += 120
        contributions.append(('profile_frontier_large_only_bonus', 120))
    if requirements.get('minParamsB') is not None:
        try:
            params_b = estimate_model_params_b(model)
            if params_b >= float(requirements.get('minParamsB')):
                bonus = min(80, params_b / 8)
                score += bonus
                contributions.append(('profile_min_params_bonus', round(bonus, 2)))
        except Exception:
            pass
    if is_nvidia_provider(provider) and (requirements.get('preferTools') or requirements.get('tools')):
        score -= 45
        contributions.append(('nvidia_tool_schema_leak_penalty', -45))
    if is_nvidia_provider(provider) and requirements.get('qualitySensitive'):
        score -= 25
        contributions.append(('quality_sensitive_nvidia_penalty', -25))
    if requirements.get('agentic'):
        if any(h in model_l for h in ('kimi-k2', 'codex', 'sonnet', 'opus', 'gpt-5', 'gpt-4o', 'claude')):
            score += 28
            contributions.append(('agentic_model_bonus', 28))
        if model_capabilities(provider, model).get('tools'):
            score += 20
            contributions.append(('agentic_tool_capability_bonus', 20))
        if any(h in model_l for h in ('nano', 'flash-lite', 'mini', 'haiku')) and complexity == Complexity.COMPLEX:
            score -= 18
            contributions.append(('agentic_complex_light_model_penalty', -18))
        if provider.api_type in ('openclaw-gateway', 'openai-codex-responses') and intent == Intent.CODE:
            score += 18
            contribution_name = 'agentic_code_codex_bonus' if provider.api_type == 'openai-codex-responses' else 'agentic_code_gateway_bonus'
            contributions.append((contribution_name, 18))
    if intent == Intent.GENERAL and provider.api_type == 'ollama':
        score -= 1
        contributions.append(('general_ollama_penalty', -1))
    if intent == Intent.GENERAL and provider.api_type == 'anthropic-messages':
        if 'haiku' in model_l:
            score += 34
            contributions.append(('general_dario_haiku_bonus', 34))
        elif 'sonnet' in model_l or 'opus' in model_l:
            score -= 6
            contributions.append(('general_dario_non_haiku_penalty', -6))
    if provider.api_type == 'ollama':
        family_bonus = ollama_family_bonus(model, intent)
        if family_bonus:
            score += family_bonus
            contributions.append(('ollama_family_bonus', family_bonus))
        if intent == Intent.CODE and 'glm-5' in model_l:
            score += 8
            contributions.append(('glm5_code_preference', 8))
        elif intent == Intent.CODE and 'kimi' in model_l:
            score += 3
            contributions.append(('kimi_code_fallback_bonus', 3))
        elif intent == Intent.CODE and ('qwen' in model_l or 'deepseek' in model_l):
            score -= 4
            contributions.append(('glm_beats_qwen_deepseek_for_code', -4))

    if route_mode == 'fast':
        if provider.api_type == 'ollama':
            score += 6
            contributions.append(('route_mode_fast_ollama_bonus', 6))
        if provider.api_type in {'anthropic-messages', 'openclaw-gateway'}:
            score -= 3
            contributions.append(('route_mode_fast_remote_penalty', -3))
    elif route_mode == 'realtime':
        # Realtime: prioritize speed above all else, minimal latency
        if provider.api_type == 'ollama':
            score += 15
            contributions.append(('route_mode_realtime_ollama_bonus', 15))
        if 'flash' in model_l or 'turbo' in model_l or 'mini' in model_l:
            score += 8
            contributions.append(('route_mode_realtime_speed_hint', 8))
        if provider.api_type in {'anthropic-messages', 'openclaw-gateway'}:
            score -= 8
            contributions.append(('route_mode_realtime_remote_penalty', -8))
    elif route_mode == 'best':
        if provider.api_type in {'openai-codex-responses', 'anthropic-messages', 'openclaw-gateway'}:
            score += 5
            contributions.append(('route_mode_best_frontier_bonus', 5))
    elif route_mode == 'local-first':
        if provider.api_type == 'ollama':
            score += 12
            contributions.append(('route_mode_local_first_ollama_bonus', 12))
        else:
            score -= 4
            contributions.append(('route_mode_local_first_remote_penalty', -4))

    if thinking == ThinkingLevel.HIGH:
        if any(hint in model_l for hint in COMPLEX_MODEL_HINTS):
            score += 6
            contributions.append(('thinking_high_complex_bonus', 6))
        if any(hint in model_l for hint in LIGHTWEIGHT_MODEL_HINTS):
            score -= 10
            contributions.append(('thinking_high_light_penalty', -10))
        if provider.api_type in {'anthropic-messages', 'openai-completions', 'openai-codex-responses', 'openclaw-gateway'}:
            score += 3
            contributions.append(('thinking_high_reasoning_bias', 3))
    elif thinking == ThinkingLevel.LOW:
        if any(hint in model_l for hint in LIGHTWEIGHT_MODEL_HINTS):
            score += 6
            contributions.append(('thinking_low_light_bonus', 6))
        if any(hint in model_l for hint in COMPLEX_MODEL_HINTS):
            score -= 4
            contributions.append(('thinking_low_complex_penalty', -4))
        if provider.api_type == 'openclaw-gateway':
            score -= 6
            contributions.append(('thinking_low_gateway_penalty', -6))
        if provider.api_type == 'ollama':
            score += 2
            contributions.append(('thinking_low_ollama_bonus', 2))

    if requirements.get('document'):
        if provider.name == 'openai-codex' or provider.api_type == 'openai-codex-responses':
            score += 65
            contributions.append(('document_codex_subscription_bonus', 65))
        elif provider.api_type == 'google-generative-language':
            score += 55
            contributions.append(('document_google_bonus', 55))
        elif provider.api_type in {'openai-completions', 'anthropic-messages'}:
            score += 30
            contributions.append(('document_frontier_bonus', 30))
        elif provider.api_type == 'ollama':
            if model_is_frontier_large(model):
                score += 10
                contributions.append(('document_frontier_ollama_bonus', 10))
            else:
                score -= 20
                contributions.append(('document_small_ollama_penalty', -20))
        if any(h in model_l for h in ('gemini', 'gpt-5', 'gpt-4o', 'opus', 'sonnet', 'qwen', 'kimi', 'minimax')):
            score += 10
            contributions.append(('document_model_hint_bonus', 10))
        if is_nvidia_provider(provider):
            score -= 25
            contributions.append(('document_nvidia_penalty', -25))
        if any(h in model_l for h in ('nano', 'tiny', 'tts', 'asr', 'embed', 'clip', 'nemotron', '1b', '3b', '7b')):
            score -= 35
            contributions.append(('document_weak_model_penalty', -35))

    requested_modalities = requested_modalities_from_requirements(requirements)
    if requested_modalities:
        learned_modalities = model_learned_modalities(provider.name, model)
        matched_modalities = sorted(requested_modalities & learned_modalities)
        if matched_modalities:
            bonus = min(60, 24 * len(matched_modalities))
            score += bonus
            contributions.append((f'learned_modality:{",".join(matched_modalities)}', bonus))

    health = model_health_snapshot(provider, model, intent.name)
    health_delta = max(-60, min(40, (health.get('score', 0) - 50) * 0.6))
    score += health_delta
    contributions.append(('health_score_delta', round(health_delta, 2)))
    if provider.api_type == 'ollama' and health.get('models_present'):
        score += 5
        contributions.append(('ollama_present_bonus', 5))
    if health.get('cooldown_until', 0) > time.time():
        score -= 100
        contributions.append(('cooldown_penalty', -100))

    empirical_bonus, empirical_note = empirical_route_adjustment(provider, model, intent.name, route_mode, complexity, thinking)
    score += empirical_bonus
    contributions.append((f'route_empirical:{empirical_note}', round(empirical_bonus, 2)))

    if intent == Intent.GENERAL:
        score = 50 + ((score - 50) * 0.35)
        contributions.append(('general_blend', 'applied'))
        general_bonus, general_note = general_empirical_adjustment(provider, model)
        score += general_bonus
        contributions.append((f'empirical:{general_note}', round(general_bonus, 2)))
        logger.debug(f"[scoring] GENERAL {provider.name}/{model}: route_empirical={empirical_bonus:.2f} ({empirical_note}), empirical={general_bonus:.2f} ({general_note}), health={health.get('score', 0):.2f}, final={score:.2f}")

    final_score = round(score, 2)
    if debug_scores is not None:
        debug_scores.append({'provider': provider.name, 'model': model, 'score': final_score, 'health': health, 'contributions': contributions})
    return final_score


def payload_tools_soft_preference(requirements):
    return bool((requirements or {}).get('preferTools'))

MODALITY_REQUIREMENT_KEYS = ('vision', 'audio', 'video', 'document', 'ocr')


def has_modality_requirement(requirements):
    requirements = requirements or {}
    return any(requirements.get(k) for k in MODALITY_REQUIREMENT_KEYS)


def modality_relaxed_requirements(requirements):
    """Drop profile allow-lists/size gates that block capable multimodal models.

    Keeps safety deny-lists (denyModels/denyProviders) and the modality
    requirements themselves; removes allowProviders/allowModels/frontierLargeOnly
    /minParamsB so a vision/audio/video/document-capable model can serve when a
    profile (e.g. auto/agentic) would otherwise leave no capable candidate.
    """
    relaxed = dict(requirements or {})
    for key in ('allowProviders', 'allowModels', 'frontierLargeOnly', 'minParamsB'):
        relaxed.pop(key, None)
    return relaxed


def select_model(intent, complexity, thinking=DEFAULT_THINKING_LEVEL, route_mode='balanced', requirements=None, estimated_tokens=0):
    """Score ALL models across ALL providers globally, then rank.

    Previous behavior picked the best model per provider first, then
    merged. This v3.1 approach scores every (provider, model) pair
    independently and takes the top N globally, which gives small but
    high-quality providers a fair shot against large model pools."""
    all_candidates = []
    debug_scores = []
    rejections = []
    requirements = requirements or {}
    for pn, provider in PROVIDERS.items():
        if pn in DISABLED_PROVIDERS:
            continue
        if provider.api_type == 'ollama':
            fetch_ollama_models(provider)
        if route_mode == 'local-first' and not provider_allowed_in_local_first(provider):
            rejections.append({'provider': pn, 'model': '*', 'reason': local_first_rejection_reason(provider)})
            continue
        if not provider.models or not provider_endpoint_reachable(provider):
            continue
        for model in dedupe_keep_order(provider.models):
            disabled_reason = model_disabled_reason(provider.name, model)
            if disabled_reason:
                rejections.append({'provider': pn, 'model': model, 'reason': disabled_reason})
                continue
            if route_mode == 'local-first' and provider.api_type == 'ollama' and is_cloud_ollama_model(model):
                rejections.append({'provider': pn, 'model': model, 'reason': 'excluded by local-first (:cloud model)'})
                continue
            if not is_chat_capable_model(provider, model):
                rejections.append({'provider': pn, 'model': model, 'reason': 'not chat-capable'})
                continue
            ok_req, reason = model_meets_requirements(provider, model, requirements, estimated_tokens)
            if not ok_req:
                rejections.append({'provider': pn, 'model': model, 'reason': reason})
                continue
            score = score_provider_model(provider, model, intent, complexity, thinking, route_mode, estimated_tokens, debug_scores, requirements)
            if payload_tools_soft_preference(requirements) and model_capabilities(provider, model).get('tools'):
                bonus = 30 if intent in (Intent.ANALYSIS, Intent.CODE) or complexity == Complexity.COMPLEX or requirements.get('qualitySensitive') else 55
                if model_quality_tier(model) == 'weak' and (intent == Intent.ANALYSIS or complexity == Complexity.COMPLEX or requirements.get('qualitySensitive')):
                    bonus -= 20
                score += bonus
                if debug_scores is not None:
                    for entry in reversed(debug_scores):
                        if entry.get('provider') == provider.name and entry.get('model') == model:
                            entry['score'] = round(score, 2)
                            entry.setdefault('contributions', []).append(('tools_soft_preference_bonus', bonus))
                            break
            scored = (score, pn, model)
            all_candidates.append(scored)

    all_candidates.sort(key=lambda item: (-item[0], item[1], item[2]))
    ranked_pairs = [(pn, model) for _, pn, model in all_candidates]
    chain = diversify_ranked_chain(ranked_pairs, MAX_PROVIDER_ATTEMPTS)
    if route_mode in {'balanced', 'best'}:
        chain = ensure_reliable_public_chat_fallback(chain, requirements, estimated_tokens, MAX_PROVIDER_ATTEMPTS)
    return chain, sorted(debug_scores, key=lambda item: item['score'], reverse=True), rejections


def diversify_ranked_chain(ranked_pairs, limit=MAX_PROVIDER_ATTEMPTS):
    """Keep best-first routing while reserving early failover slots by provider."""
    ranked_pairs = dedupe_keep_order(ranked_pairs or [])
    if len(ranked_pairs) <= 1:
        return ranked_pairs
    diversified = []
    seen = set()
    seen_providers = set()
    for provider_name, model in ranked_pairs:
        if provider_name in seen_providers:
            continue
        pair = (provider_name, model)
        diversified.append(pair)
        seen.add(pair)
        seen_providers.add(provider_name)
        if len(diversified) >= limit:
            return diversified
    for pair in ranked_pairs:
        if pair in seen:
            continue
        diversified.append(pair)
        if len(diversified) >= limit:
            break
    return diversified


RELIABLE_PUBLIC_CHAT_FALLBACKS = (
    ('openrouter', 'gemini-2.5-flash'),
    ('openrouter', 'google/gemini-2.5-flash'),
    ('nvidia-nim', 'meta/llama-3.1-8b-instruct'),
)


def ensure_reliable_public_chat_fallback(chain, requirements, estimated_tokens, limit=MAX_PROVIDER_ATTEMPTS):
    """Keep a known text-chat escape hatch inside hosted balanced/best chains."""
    chain = dedupe_keep_order(chain or [])
    requirements = requirements or {}
    if has_modality_requirement(requirements):
        return chain
    if requirements.get('tools') or requirements.get('preferTools') or requirements.get('agentic'):
        return chain
    if any((provider, model) in chain for provider, model in RELIABLE_PUBLIC_CHAT_FALLBACKS):
        return chain
    for provider_name, model in RELIABLE_PUBLIC_CHAT_FALLBACKS:
        provider = PROVIDERS.get(provider_name)
        if not provider or provider_name in DISABLED_PROVIDERS:
            continue
        if model not in (provider.models or []) and provider_name != 'openrouter':
            continue
        if not is_chat_capable_model(provider, model):
            continue
        ok_req, _reason = model_meets_requirements(provider, model, requirements, estimated_tokens)
        used_relaxed_gate = False
        if not ok_req:
            relaxed = dict(requirements)
            for key in ('allowModels', 'frontierLargeOnly', 'frontierOrReasoningTools', 'minParamsB', 'reasoning'):
                relaxed.pop(key, None)
            ok_req, _reason = model_meets_requirements(provider, model, relaxed, estimated_tokens)
            if not ok_req:
                continue
            used_relaxed_gate = True
        fallback = (provider_name, model)
        if used_relaxed_gate and chain:
            insert_at = min(2, len(chain))
            return dedupe_keep_order(chain[:insert_at] + [fallback] + chain[insert_at:])[:limit]
        if len(chain) < limit:
            return chain + [fallback]
        insert_at = min(2, len(chain))
        return dedupe_keep_order(chain[:insert_at] + [fallback] + chain[insert_at:])[:limit]
    return chain

def call_ollama(base_url, model, messages, api_key='', thinking=DEFAULT_THINKING_LEVEL):
    url = base_url.rstrip('/') + '/api/chat'
    payload = {"model": model, "messages": messages, "stream": False, "options": ollama_generation_options(thinking)}
    if ollama_model_supports_native_thinking(model):
        payload["think"] = thinking != ThinkingLevel.LOW

    hdrs = {'Content-Type': 'application/json'}
    if api_key:
        hdrs['Authorization'] = f'Bearer {api_key}'

    def _post_chat(chat_payload):
        data = json.dumps(chat_payload).encode()
        req = urllib.request.Request(url, data=data, headers=hdrs)
        with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT_SECONDS) as resp:
            return json.loads(resp.read())

    try:
        body = _post_chat(payload)
        message = body.get('message', {}) or {}
        content = message.get('content', '') or ''
        thinking_text = message.get('thinking', '') or ''
        content = sanitize_visible_output(content)
        if content:
            return True, content
        # Some Ollama thinking-capable models can spend the whole budget in
        # message.thinking and return empty content with done_reason=length.
        # Always retry with think=false to recover usable content. This is
        # cheaper than discarding the response entirely and re-routing.
        if thinking_text:
            retry_payload = dict(payload)
            retry_payload['think'] = False
            retry_body = _post_chat(retry_payload)
            retry_message = retry_body.get('message', {}) or {}
            retry_content = sanitize_visible_output(retry_message.get('content', '') or '')
            if retry_content:
                logger.info(f"Ollama {base_url} {model}: recovered empty-content thinking response with think=false retry")
                return True, retry_content
        if thinking_text:
            err = 'Ollama returned thinking-only output with empty visible content'
            logger.warning(f"Ollama {base_url} {model}: {err}")
            return False, err
        err = 'Ollama returned empty content'
        logger.warning(f"Ollama {base_url} {model}: {err}")
        return False, err
    except Exception as e:
        err = extract_http_error(e)
        if 'timed out' in err.lower():
            try:
                retry_payload = dict(payload)
                retry_payload['think'] = False
                retry_body = _post_chat(retry_payload)
                retry_message = retry_body.get('message', {}) or {}
                retry_content = sanitize_visible_output(retry_message.get('content', '') or '')
                if retry_content:
                    logger.info(f"Ollama {base_url} {model}: recovered timed-out response with think=false retry")
                    return True, retry_content
            except Exception as retry_err:
                err = extract_http_error(retry_err)
        logger.warning(f"Ollama {base_url} {model}: {err}")
        return False, err

def call_openai_compat(base_url, model, messages, api_key='', provider_name='', thinking=DEFAULT_THINKING_LEVEL, supports_reasoning=False, want_json=False):
    url = openai_chat_completions_url(base_url)
    payload = {"model": model, "messages": messages, "max_tokens": thinking_max_tokens(thinking)}
    if supports_reasoning:
        payload["reasoning"] = {"effort": thinking.value}
    if want_json:
        payload["response_format"] = {"type": "json_object"}
    try:
        data = json.dumps(payload).encode()
        hdrs = {'Content-Type': 'application/json'}
        add_openai_compat_headers(hdrs, provider_name)
        if api_key:
            hdrs['Authorization'] = f'Bearer {api_key}'
        req = urllib.request.Request(url, data=data, headers=hdrs)
        with urllib.request.urlopen(req, timeout=OPENAI_COMPAT_TIMEOUT_SECONDS) as resp:
            body = json.loads(resp.read())
        text = sanitize_visible_output(body.get('choices', [{}])[0].get('message', {}).get('content', '') or '')
        if text:
            return True, text
        err = 'OpenAI-compatible provider returned empty content'
        logger.warning(f"OpenAI-compat {provider_name or base_url} {model}: {err}")
        return False, err
    except Exception as e:
        logger.warning(f"OpenAI-compat {provider_name or base_url} {model}: {extract_http_error(e)}")
        return False, extract_http_error(e)


def call_openclaw_gateway(model, messages, provider_name='openai-codex', thinking=DEFAULT_THINKING_LEVEL, want_json=False, timeout_seconds=None):
    if not os.path.exists(OPENCLAW_GATEWAY_HELPER):
        return False, f'Missing OpenClaw gateway helper: {OPENCLAW_GATEWAY_HELPER}'

    effective_timeout = int(timeout_seconds or OPENCLAW_GATEWAY_TIMEOUT_SECONDS)
    payload = {
        'agentId': OPENCLAW_GATEWAY_AGENT_ID,
        'provider': provider_name,
        'model': model,
        'message': build_openclaw_gateway_prompt(messages),
        'timeoutMs': effective_timeout * 1000,
        'thinking': thinking.value,
        'responseFormat': 'json' if want_json else 'text',
    }

    try:
        proc = subprocess.run(
            ['node', OPENCLAW_GATEWAY_HELPER],
            input=json.dumps(payload),
            capture_output=True,
            text=True,
            timeout=effective_timeout,
            check=False,
        )
    except subprocess.TimeoutExpired:
        logger.warning(f'OpenClaw gateway {provider_name} {model}: timed out after {effective_timeout}s')
        return False, f'OpenClaw gateway timeout after {effective_timeout}s'
    except Exception as e:
        logger.warning(f'OpenClaw gateway {provider_name} {model}: {e}')
        return False, str(e)

    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or '').strip()
        logger.warning(f'OpenClaw gateway {provider_name} {model}: {detail[:500]}')
        return False, detail or f'OpenClaw gateway exited with code {proc.returncode}'

    try:
        result = json.loads(proc.stdout or '{}')
    except Exception:
        return False, (proc.stdout or proc.stderr or 'Invalid OpenClaw gateway response').strip()

    text = sanitize_visible_output(result.get('text', ''))
    if text:
        return True, text
    return False, json.dumps(result)



def chat_messages_to_responses_input(messages):
    """Convert OpenAI Chat Completions messages to Responses API input items.

    Handles assistant tool_calls -> function_call items and tool role messages
    -> function_call_output items, so the Codex model can see the tool result
    on the next turn.
    """
    items = []
    for msg in messages:
        if not isinstance(msg, dict):
            continue
        role = msg.get('role', 'user')
        content = msg.get('content', '')
        # system / developer are instruction-like roles — call_codex_completion
        # folds them into the Responses `instructions` field instead of
        # emitting them as input items (matches the OpenAI Responses API spec).
        if role in {'system', 'developer'}:
            continue
        if role == 'assistant':
            # Emit text content as a message item
            assistant_text = strip_assistant_replay_noise(normalize_content(content))
            if assistant_text:
                items.append({'role': 'assistant', 'content': assistant_text})
            # Emit each tool_call as a function_call item
            for tc in (msg.get('tool_calls') or []):
                if not isinstance(tc, dict):
                    continue
                fn = tc.get('function') or {}
                args = fn.get('arguments') or ''
                call_id = tc.get('id') or f'call_{uuid.uuid4().hex[:24]}'
                items.append({
                    'type': 'function_call',
                    'call_id': call_id,
                    'name': fn.get('name') or '',
                    'arguments': args if isinstance(args, str) else json.dumps(args, separators=(',', ':')),
                })
            continue
        if role == 'tool':
            call_id = msg.get('tool_call_id') or ''
            if not call_id:
                continue
            # Tool result -> function_call_output item
            items.append({
                'type': 'function_call_output',
                'call_id': call_id,
                'output': content if isinstance(content, str) else json.dumps(content, separators=(',', ':')),
            })
            continue
        # user / developer / etc. — preserve multimodal content for vision-capable
        # Codex models (gpt-5.4/5.5) by emitting input_image items for image
        # blocks rather than str()'ing the whole list (which would lose the
        # base64 URL).
        if isinstance(content, list):
            parts = []
            for block in content:
                if not isinstance(block, dict):
                    continue
                btype = block.get('type')
                if btype in ('image', 'image_url', 'input_image'):
                    image_payload = block.get('image_url') if btype == 'image_url' else block
                    if isinstance(image_payload, dict):
                        url = image_payload.get('url') or image_payload.get('image_url')
                    else:
                        url = image_payload
                    if url:
                        parts.append({'type': 'input_image', 'image_url': url})
                elif btype == 'text':
                    text_val = block.get('text', '')
                    if text_val:
                        parts.append({'type': 'input_text', 'text': text_val})
                else:
                    fallback_text = normalize_content(block)
                    if fallback_text:
                        parts.append({'type': 'input_text', 'text': fallback_text})
            if parts:
                # Single input message whose content mixes text + image parts
                # — matches the OpenAI Responses API schema.
                items.append({'role': role, 'content': parts})
                continue
        # Flatten block content (text + vision/file markers) to a string the
        # model can see, instead of str()'ing the list (which would produce a
        # Python repr like "[{'type': 'text', 'text': 'hi'}]").
        normalized = normalize_content(content)
        if normalized:
            items.append({'role': role, 'content': normalized})

    return items


def call_codex_completion(base_url, model, payload, api_key='', provider_name='', thinking=DEFAULT_THINKING_LEVEL, supports_reasoning=False, debug_mode=False, request_id=''):
    """Call OpenAI Codex Responses API with streaming SSE support"""
    url = base_url.rstrip('/') + '/responses'
    
    messages = payload.get('messages', [])
    instruction_parts = []
    for msg in messages:
        if not isinstance(msg, dict):
            continue
        if msg.get('role') in {'system', 'developer'}:
            text = normalize_content(msg.get('content', ''))
            if text:
                instruction_parts.append(text)
    instructions = '\n\n'.join(instruction_parts) if instruction_parts else 'You are a helpful assistant.'
    input_msgs = chat_messages_to_responses_input(messages) or [{'role': 'user', 'content': ''}]
    
    req_payload = {
        "model": model,
        "instructions": instructions,
        "input": input_msgs or [{"role": "user", "content": ""}],
        "store": False,
        "stream": True,
    }
    
    tools = responses_tool_definitions(payload.get('tools'))
    if tools:
        req_payload['tools'] = tools
        tool_choice = responses_tool_choice(payload.get('tool_choice'))
        if tool_choice is not None:
            req_payload['tool_choice'] = tool_choice
        if 'parallel_tool_calls' in payload:
            req_payload['parallel_tool_calls'] = bool(payload.get('parallel_tool_calls'))
    
    if supports_reasoning and thinking == ThinkingLevel.HIGH:
        req_payload["reasoning"] = {"effort": "high"}
    
    try:
        data = json.dumps(req_payload).encode()
        hdrs = {'Content-Type': 'application/json'}
        if api_key:
            hdrs['Authorization'] = f'Bearer {api_key}'
        
        req = urllib.request.Request(url, data=data, headers=hdrs)
        
        with urllib.request.urlopen(req, timeout=OPENAI_COMPAT_TIMEOUT_SECONDS) as resp:
            text, tool_calls = parse_responses_stream(resp)
        
        text = sanitize_visible_output(text)
        if text or tool_calls:
            leak_reason = reject_visible_tool_call_leak(payload, text, tool_calls)
            if leak_reason:
                logger.warning(f"Codex responses {provider_name or base_url} {model}: {leak_reason}")
                return False, leak_reason
            return True, build_openai_completion(
                provider_name or 'openai-codex', model, request_id, text, tool_calls,
                None, {'prompt_tokens': 0, 'completion_tokens': 0},
                debug_mode=debug_mode,
                allow_debug_prefix=payload.get('response_format', {}).get('type') != 'json_object',
                suppress_tool_call_content=bool((payload.get('requirements') or {}).get('suppressToolCallContent') or payload.get('suppressToolCallContent') or payload.get('suppressIntermediateToolText'))
            )
        return False, 'Empty Codex response'
    except Exception as e:
        return False, extract_http_error(e)


def audio_endpoint_kind(path):
    clean_path = urllib.parse.urlparse(path or '').path
    if clean_path in {'/v1/audio/transcriptions', '/audio/transcriptions'}:
        return 'stt'
    if clean_path in {'/v1/audio/speech', '/audio/speech'}:
        return 'tts'
    return ''


def audio_proxy_provider(kind):
    provider_name = AUDIO_TTS_PROVIDER if kind == 'tts' else AUDIO_STT_PROVIDER
    provider = PROVIDERS.get(provider_name)
    if not provider and provider_name == 'openrouter':
        provider = Provider(
            'openrouter',
            'openai-completions',
            env_first('SAGE_ROUTER_OPENROUTER_BASE_URL', 'OPENROUTER_BASE_URL') or 'https://openrouter.ai/api/v1',
            env_first('SAGE_ROUTER_OPENROUTER_API_KEY', 'OPENROUTER_API_KEY'),
            [],
        )
    if not provider:
        return None, f'audio_{kind}_provider_not_configured'
    if provider.api_type not in {'openai-completions'}:
        return None, f'audio_{kind}_provider_not_openai_compatible'
    if not provider.base_url:
        return None, f'audio_{kind}_provider_missing_base_url'
    if not provider.api_key:
        return None, f'audio_{kind}_provider_missing_api_key'
    return provider, ''


def upstream_audio_url(provider, kind):
    base = (provider.base_url or '').rstrip('/')
    suffix = '/audio/speech' if kind == 'tts' else '/audio/transcriptions'
    if base.endswith('/v1') or base.endswith('/api/v1'):
        return base + suffix
    return base + '/v1' + suffix


def proxy_audio_request(handler, kind, body, request_id):
    provider, error = audio_proxy_provider(kind)
    if error:
        handler.write_json(503, {'error': error}, extra_headers={'X-Sage-Router-Request-Id': request_id})
        return

    content_type = handler.headers.get('Content-Type') or 'application/octet-stream'
    headers = {
        'Authorization': f'Bearer {provider.api_key}',
        'Content-Type': content_type,
        'User-Agent': 'sage-router/audio-proxy',
    }
    if provider.name == 'openrouter':
        headers.setdefault('HTTP-Referer', 'https://sagerouter.dev')
        headers.setdefault('X-OpenRouter-Title', 'Sage Router')
    accept = handler.headers.get('Accept')
    if accept:
        headers['Accept'] = accept
    url = upstream_audio_url(provider, kind)
    started = time.time()
    try:
        req = urllib.request.Request(url, data=body, headers=headers, method='POST')
        with urllib.request.urlopen(req, timeout=AUDIO_PROXY_TIMEOUT_SECONDS) as resp:
            if kind == 'tts':
                # Stream TTS audio to the client using chunked transfer encoding
                handler.stream_binary_response(
                    resp,
                    extra_headers={
                        'X-Sage-Router-Request-Id': request_id,
                        'X-Sage-Router-Provider': provider.name,
                        'X-Sage-Router-Audio-Kind': kind,
                    },
                )
            else:
                # STT returns JSON — buffer and send
                resp_body = resp.read()
                resp_type = resp.headers.get('Content-Type') or 'application/json'
                handler.write_binary(
                    resp.status,
                    resp_body,
                    resp_type,
                    {
                        'X-Sage-Router-Request-Id': request_id,
                        'X-Sage-Router-Provider': provider.name,
                        'X-Sage-Router-Audio-Kind': kind,
                    },
                )
            logger.info(f'[{request_id}] Proxied audio {kind} via {provider.name} in {round((time.time() - started) * 1000, 2)}ms')
    except urllib.error.HTTPError as e:
        err_body = e.read()
        handler.write_binary(
            e.code,
            err_body,
            e.headers.get('Content-Type') or 'application/json',
            {
                'X-Sage-Router-Request-Id': request_id,
                'X-Sage-Router-Provider': provider.name,
                'X-Sage-Router-Audio-Kind': kind,
            },
        )
        logger.warning(f'[{request_id}] Audio {kind} proxy {provider.name} failed: HTTP {e.code}')
    except Exception as e:
        logger.warning(f'[{request_id}] Audio {kind} proxy {provider.name} failed: {extract_http_error(e)}')
        handler.write_json(
            502,
            {'error': 'audio_proxy_failed', 'provider': provider.name, 'detail': extract_http_error(e)},
            extra_headers={'X-Sage-Router-Request-Id': request_id},
        )



def call_anthropic(base_url, model, messages, api_key='', thinking=DEFAULT_THINKING_LEVEL, supports_reasoning=False, want_json=False):
    url = base_url.rstrip('/') + '/v1/messages'
    system_text = ''
    api_msgs = []
    for msg in messages:
        r, c = msg.get('role', 'user'), msg.get('content', '')
        if r == 'system':
            system_text += c + '\n'
        elif r in ('user', 'assistant'):
            api_msgs.append({"role": r, "content": c})
        else:
            label = r.upper() if isinstance(r, str) else 'MESSAGE'
            wrapped = f'[{label}]\n{c}'.strip() if c else f'[{label}]'
            api_msgs.append({"role": "user", "content": wrapped})
    if api_msgs and api_msgs[0].get('role') != 'user':
        api_msgs.insert(0, {"role": "user", "content": "Hello"})
    if not api_msgs:
        api_msgs = [{"role": "user", "content": "Hello"}]
    payload = {"model": model, "max_tokens": thinking_max_tokens(thinking), "messages": api_msgs}
    if supports_reasoning and thinking == ThinkingLevel.HIGH:
        payload["thinking"] = {"type": "enabled", "budget_tokens": 4096}
    if want_json:
        api_msgs.append({"role": "user", "content": "Return valid JSON only."})
    if system_text.strip():
        payload["system"] = system_text.strip()
    try:
        data = json.dumps(payload).encode()
        hdrs = {'Content-Type': 'application/json', 'anthropic-version': '2023-06-01'}
        if api_key:
            hdrs['x-api-key'] = api_key
        req = urllib.request.Request(url, data=data, headers=hdrs)
        with urllib.request.urlopen(req, timeout=ANTHROPIC_TIMEOUT_SECONDS) as resp:
            blocks = json.loads(resp.read()).get('content', [])
        text = sanitize_visible_output(''.join(b.get('text', '') for b in blocks if isinstance(b, dict) and b.get('type') == 'text'))
        if text:
            return True, text
        err = 'Anthropic returned empty content'
        logger.warning(f"Anthropic {base_url} {model}: {err}")
        return False, err
    except Exception as e:
        logger.warning(f"Anthropic {base_url} {model}: {extract_http_error(e)}")
        return False, extract_http_error(e)


GOOGLE_SCHEMA_UNSUPPORTED_KEYS = {
    '$defs',
    '$schema',
    'additionalProperties',
    'allOf',
    'all_of',
    'anyOf',
    'any_of',
    'const',
    'contains',
    'definitions',
    'dependentSchemas',
    'dependent_schemas',
    'else',
    'exclusiveMaximum',
    'exclusiveMinimum',
    'exclusive_maximum',
    'exclusive_minimum',
    'if',
    'maxContains',
    'max_contains',
    'minContains',
    'min_contains',
    'multipleOf',
    'multiple_of',
    'not',
    'oneOf',
    'one_of',
    'patternProperties',
    'pattern_properties',
    'prefixItems',
    'prefix_items',
    'propertyNames',
    'property_names',
    'then',
    'unevaluatedProperties',
    'unevaluated_properties',
}


def google_schema_for_tool(value):
    if isinstance(value, list):
        return [google_schema_for_tool(item) for item in value]
    if not isinstance(value, dict):
        return value
    cleaned = {}
    for key, item in value.items():
        if key in GOOGLE_SCHEMA_UNSUPPORTED_KEYS:
            continue
        if key == 'type' and isinstance(item, list):
            cleaned[key] = next((str(t) for t in item if isinstance(t, str) and t.lower() != 'null'), 'string')
            continue
        cleaned[key] = google_schema_for_tool(item)
    return cleaned


def google_tool_declarations(tools):
    declarations = []
    for tool in tools or []:
        if not isinstance(tool, dict):
            continue
        function = tool.get('function') if isinstance(tool.get('function'), dict) else {}
        if tool.get('type') != 'function' and not function:
            continue
        name = function.get('name') or tool.get('name')
        if not name:
            continue
        declaration = {'name': str(name)}
        if function.get('description'):
            declaration['description'] = str(function.get('description'))
        parameters = function.get('parameters')
        if isinstance(parameters, dict) and parameters:
            declaration['parameters'] = google_schema_for_tool(parameters)
        else:
            declaration['parameters'] = {'type': 'object', 'properties': {}}
        declarations.append(declaration)
    return declarations


def google_tool_config(tool_choice, declarations):
    if not declarations:
        return None
    names = [d.get('name') for d in declarations if d.get('name')]
    if isinstance(tool_choice, dict) and tool_choice.get('type') == 'function':
        name = ((tool_choice.get('function') or {}).get('name')) or tool_choice.get('name')
        config = {'mode': 'ANY'}
        if name:
            config['allowedFunctionNames'] = [str(name)]
        return {'functionCallingConfig': config}
    if tool_choice == 'required':
        return {'functionCallingConfig': {'mode': 'ANY', 'allowedFunctionNames': names}}
    if tool_choice == 'none':
        return {'functionCallingConfig': {'mode': 'NONE'}}
    return {'functionCallingConfig': {'mode': 'AUTO'}}


def google_text_from_content(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict):
                if isinstance(item.get('text'), str):
                    parts.append(item.get('text'))
                elif isinstance(item.get('content'), str):
                    parts.append(item.get('content'))
            elif isinstance(item, str):
                parts.append(item)
        return '\n'.join(p for p in parts if p)
    if content is None:
        return ''
    return str(content)


def build_google_generate_payload(messages, thinking=DEFAULT_THINKING_LEVEL, want_json=False, tools=None, tool_choice=None):
    system_text = ''
    contents = []
    tool_call_names = {}
    for msg in sanitize_replay_messages(messages):
        role = msg.get('role', 'user')
        content = google_text_from_content(msg.get('content', ''))
        tool_calls = normalize_tool_calls(msg.get('tool_calls'))
        if not content and not tool_calls and role != 'tool':
            continue
        if role in ('system', 'developer'):
            system_text += content + '\n'
            continue
        if role == 'assistant':
            gemini_role = 'model'
            parts = []
            if content:
                parts.append({'text': content})
            for tool_call in tool_calls:
                function = tool_call.get('function') or {}
                name = function.get('name') or 'tool'
                arguments = function.get('arguments') if 'arguments' in function else {}
                if isinstance(arguments, str):
                    try:
                        arguments = json.loads(arguments or '{}')
                    except Exception:
                        arguments = {'arguments': arguments}
                if not isinstance(arguments, dict):
                    arguments = {'arguments': arguments}
                tool_call_names[tool_call.get('id') or ''] = name
                parts.append({'functionCall': {'name': name, 'args': arguments}})
        elif role == 'user':
            gemini_role = 'user'
            parts = [{'text': content}]
        elif role == 'tool':
            gemini_role = 'user'
            name = msg.get('name') or tool_call_names.get(msg.get('tool_call_id') or '') or 'tool_result'
            response = {'result': content}
            parts = [{'functionResponse': {'name': str(name), 'response': response}}]
        else:
            label = role.upper() if isinstance(role, str) else 'MESSAGE'
            gemini_role = 'user'
            parts = [{'text': f'[{label}]\n{content}'.strip()}]
        if contents and contents[-1].get('role') == gemini_role:
            contents[-1].setdefault('parts', []).extend(parts)
        else:
            contents.append({'role': gemini_role, 'parts': parts})

    if contents and contents[0].get('role') != 'user':
        contents.insert(0, {'role': 'user', 'parts': [{'text': 'Hello'}]})
    if not contents:
        contents = [{'role': 'user', 'parts': [{'text': 'Hello'}]}]

    payload = {
        'contents': contents,
        'generationConfig': {'maxOutputTokens': thinking_max_tokens(thinking)},
    }
    if want_json:
        payload['generationConfig']['responseMimeType'] = 'application/json'
    if system_text.strip():
        payload['systemInstruction'] = {'parts': [{'text': system_text.strip()}]}
    declarations = google_tool_declarations(tools)
    if declarations:
        payload['tools'] = [{'functionDeclarations': declarations}]
        config = google_tool_config(tool_choice, declarations)
        if config:
            payload['toolConfig'] = config
    return payload


def parse_google_generate_text(result):
    parts = result.get('candidates', [{}])[0].get('content', {}).get('parts', [])
    return sanitize_visible_output(''.join(part.get('text', '') for part in parts if isinstance(part, dict) and isinstance(part.get('text'), str)))


def parse_google_generate_tool_calls(result):
    parts = result.get('candidates', [{}])[0].get('content', {}).get('parts', [])
    tool_calls = []
    for part in parts:
        if not isinstance(part, dict):
            continue
        call = part.get('functionCall') or part.get('function_call')
        if not isinstance(call, dict):
            continue
        name = call.get('name') or 'tool'
        args = call.get('args') if 'args' in call else call.get('arguments', {})
        if isinstance(args, str):
            arguments = args
        else:
            try:
                arguments = json.dumps(args if isinstance(args, dict) else {'arguments': args}, separators=(',', ':'))
            except Exception:
                arguments = '{}'
        tool_calls.append({
            'id': f"call_{uuid.uuid4().hex[:24]}",
            'type': 'function',
            'function': {'name': str(name), 'arguments': arguments},
        })
    return normalize_tool_calls(tool_calls)


def call_google(base_url, model, messages, api_key='', thinking=DEFAULT_THINKING_LEVEL, want_json=False, tools=None, tool_choice=None):
    # Ensure base_url has /v1beta for Google API
    if 'generativelanguage.googleapis.com' in base_url and '/v1beta' not in base_url:
        base_url = base_url.rstrip('/') + '/v1beta'
    url = base_url.rstrip('/') + f'/models/{urllib.parse.quote(model, safe="")}:generateContent'
    payload = build_google_generate_payload(messages, thinking=thinking, want_json=want_json, tools=tools, tool_choice=tool_choice)
    try:
        data = json.dumps(payload).encode()
        hdrs = {'Content-Type': 'application/json'}
        if api_key:
            hdrs['x-goog-api-key'] = api_key
        req = urllib.request.Request(url, data=data, headers=hdrs)
        with urllib.request.urlopen(req, timeout=GOOGLE_TIMEOUT_SECONDS) as resp:
            result = json.loads(resp.read())
        text = parse_google_generate_text(result)
        return (True, text) if text else (False, json.dumps(result)[:500])
    except Exception as e:
        logger.warning(f"Google {base_url} {model}: {extract_http_error(e)}")
        return False, extract_http_error(e)


def call_google_vertex(base_url, model, messages, thinking=DEFAULT_THINKING_LEVEL, want_json=False, tools=None, tool_choice=None):
    try:
        token = google_vertex_access_token()
        url = google_vertex_url(base_url, model, 'generateContent')
        payload = build_google_generate_payload(messages, thinking=thinking, want_json=want_json, tools=tools, tool_choice=tool_choice)
        req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'})
        with urllib.request.urlopen(req, timeout=GOOGLE_TIMEOUT_SECONDS) as resp:
            result = json.loads(resp.read())
        text = parse_google_generate_text(result)
        return (True, text) if text else (False, json.dumps(result)[:500])
    except Exception as e:
        logger.warning(f"Vertex AI {base_url or GOOGLE_VERTEX_PROJECT} {model}: {extract_http_error(e)}")
        return False, extract_http_error(e)



def build_cloudflare_workers_ai_payload(messages, thinking=DEFAULT_THINKING_LEVEL, want_json=False):
    cf_messages = []
    for msg in messages:
        role = msg.get('role', 'user')
        content = msg.get('content', '')
        if not content:
            continue
        if role == 'developer':
            role = 'system'
        if role not in {'system', 'user', 'assistant'}:
            content = f'[{str(role).upper()}]\n{content}'.strip()
            role = 'user'
        cf_messages.append({'role': role, 'content': content})
    if not cf_messages:
        cf_messages = [{'role': 'user', 'content': 'Hello'}]
    payload = {'messages': cf_messages, 'max_tokens': thinking_max_tokens(thinking)}
    if want_json:
        payload['response_format'] = {'type': 'json_object'}
    return payload


def parse_cloudflare_workers_ai_text(result):
    if isinstance(result, str):
        return sanitize_visible_output(result)
    if not isinstance(result, dict):
        return ''
    for key in ('response', 'text', 'output_text'):
        if isinstance(result.get(key), str):
            return sanitize_visible_output(result.get(key))
    if isinstance(result.get('choices'), list) and result['choices']:
        msg = result['choices'][0].get('message') or {}
        if isinstance(msg.get('content'), str):
            return sanitize_visible_output(msg.get('content'))
    if isinstance(result.get('content'), list):
        return sanitize_visible_output(''.join(part.get('text', '') for part in result['content'] if isinstance(part, dict)))
    return ''


def call_cloudflare_workers_ai(base_url, model, messages, api_key='', thinking=DEFAULT_THINKING_LEVEL, want_json=False):
    if not api_key:
        return False, 'missing Cloudflare API token'
    try:
        payload = build_cloudflare_workers_ai_payload(messages, thinking=thinking, want_json=want_json)
        req = urllib.request.Request(
            cloudflare_workers_ai_run_url(base_url, model),
            data=json.dumps(payload).encode(),
            headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'},
        )
        with urllib.request.urlopen(req, timeout=OPENAI_COMPAT_TIMEOUT_SECONDS) as resp:
            body = json.loads(resp.read())
        if isinstance(body, dict) and body.get('success') is False:
            return False, json.dumps(body.get('errors') or body)[:500]
        text = parse_cloudflare_workers_ai_text((body or {}).get('result', body) if isinstance(body, dict) else body)
        return (True, text) if text else (False, json.dumps(body)[:500])
    except Exception as e:
        logger.warning(f'Cloudflare Workers AI {base_url} {model}: {extract_http_error(e)}')
        return False, extract_http_error(e)


def call_cloudflare_workers_ai_completion(base_url, model, payload, api_key='', thinking=DEFAULT_THINKING_LEVEL, debug_mode=False, request_id=''):
    ok, text = call_cloudflare_workers_ai(base_url, model, payload.get('messages', []), api_key=api_key, thinking=thinking, want_json=payload.get('response_format', {}).get('type') == 'json_object')
    if not ok:
        return False, text
    return True, build_openai_completion('cloudflare-workers-ai', model, request_id, text, [], 'stop', {'prompt_tokens': 0, 'completion_tokens': 0}, debug_mode=debug_mode, allow_debug_prefix=payload.get('response_format', {}).get('type') != 'json_object', suppress_tool_call_content=bool((payload.get('requirements') or {}).get('suppressToolCallContent') or payload.get('suppressToolCallContent') or payload.get('suppressIntermediateToolText')))

def call_openai_compat_completion(base_url, model, payload, api_key='', provider_name='', thinking=DEFAULT_THINKING_LEVEL, supports_reasoning=False, debug_mode=False, request_id=''):
    url = openai_chat_completions_url(base_url)
    proxied = build_openai_proxy_payload(payload, model, stream=False, supports_reasoning=supports_reasoning, thinking=thinking)
    logger.info(f"[openai-compat] Sending to {provider_name} with tools: {bool(proxied.get('tools'))}")
    try:
        data = json.dumps(proxied).encode()
        hdrs = {'Content-Type': 'application/json'}
        add_openai_compat_headers(hdrs, provider_name)
        if api_key:
            hdrs['Authorization'] = f'Bearer {api_key}'
        req = urllib.request.Request(url, data=data, headers=hdrs)
        with urllib.request.urlopen(req, timeout=OPENAI_COMPAT_TIMEOUT_SECONDS) as resp:
            body = json.loads(resp.read())
        choice = (body.get('choices') or [{}])[0]
        message = choice.get('message') or {}
        text = sanitize_provider_visible_text(message.get('content', '') or '', provider_name, model)
        raw_tool_calls = message.get('tool_calls')
        logger.info(f"[openai-compat] Response tool_calls: {len(raw_tool_calls or [])}")
        tool_calls = normalize_tool_calls(raw_tool_calls)
        leak_reason = reject_visible_tool_call_leak(payload, text, tool_calls)
        if leak_reason:
            logger.warning(f"OpenAI-compat {provider_name or base_url} {model}: {leak_reason}")
            return False, leak_reason
        finish_reason = choice.get('finish_reason') or ('tool_calls' if tool_calls else 'stop')
        return True, build_openai_completion(provider_name, model, request_id, text, tool_calls, finish_reason, body.get('usage'), debug_mode=debug_mode, allow_debug_prefix=payload.get('response_format', {}).get('type') != 'json_object', suppress_tool_call_content=bool((payload.get('requirements') or {}).get('suppressToolCallContent') or payload.get('suppressToolCallContent') or payload.get('suppressIntermediateToolText')))
    except Exception as e:
        err = extract_http_error(e)
        logger.warning(f"OpenAI-compat {provider_name or base_url} {model}: {err}")
        return False, err


def call_ollama_completion(base_url, model, payload, api_key='', thinking=DEFAULT_THINKING_LEVEL, provider_name='ollama', debug_mode=False, request_id=''):
    url = base_url.rstrip('/') + '/api/chat'
    hdrs = {'Content-Type': 'application/json'}
    if api_key:
        hdrs['Authorization'] = f'Bearer {api_key}'
    try:
        body_payload = build_ollama_payload(model, payload, thinking=thinking, stream=False)
        logger.info(f"[ollama] Sending request to {url} with {len(body_payload.get('tools', []))} tools")
        req = urllib.request.Request(url, data=json.dumps(body_payload).encode(), headers=hdrs)
        with urllib.request.urlopen(req, timeout=OLLAMA_TIMEOUT_SECONDS) as resp:
            body = json.loads(resp.read())
        message = body.get('message', {}) or {}
        text = sanitize_provider_visible_text(message.get('content', '') or '', provider_name, model)
        raw_tool_calls = message.get('tool_calls')
        logger.info(f"[ollama] Response tool_calls: {len(raw_tool_calls or [])}")
        tool_calls = normalize_tool_calls(raw_tool_calls)
        leak_reason = reject_visible_tool_call_leak(payload, text, tool_calls)
        if leak_reason:
            logger.warning(f"Ollama {base_url} {model}: {leak_reason}")
            return False, leak_reason
        finish_reason = 'tool_calls' if tool_calls else (body.get('done_reason') or 'stop')
        return True, build_openai_completion(provider_name, model, request_id, text, tool_calls, finish_reason, {'prompt_tokens': 0, 'completion_tokens': 0}, debug_mode=debug_mode, allow_debug_prefix=payload.get('response_format', {}).get('type') != 'json_object', suppress_tool_call_content=bool((payload.get('requirements') or {}).get('suppressToolCallContent') or payload.get('suppressToolCallContent') or payload.get('suppressIntermediateToolText')))
    except Exception as e:
        err = extract_http_error(e)
        if is_cloud_ollama_model(model) and 'HTTP 401' in err:
            prov = PROVIDERS.get(provider_name)
            if prov and is_local_ollama_provider(prov):
                set_local_ollama_cloud_auth_block(provider_name, seconds=int(os.environ.get('SAGE_ROUTER_OLLAMA_CLOUD_AUTH_COOLDOWN_SECONDS', '3600')))
                logger.warning(f"Ollama Cloud auth unavailable for local provider {provider_name}; suppressing local :cloud routing temporarily")
        maybe_block_ollama_runtime_error(provider_name, model, err)
        logger.warning(f"Ollama {base_url} {model}: {err}")
        return False, err


def call_ollama_ocr(base_url, model, payload, request_id):
    url = base_url.rstrip("/") + "/api/generate"
    messages = payload.get("messages", [])
    prompt = "Extract all text from this image."
    images = []
    for msg in messages:
        content = msg.get("content", "")
        if isinstance(content, str):
            if content.startswith("http"):
                import base64
                try:
                    img_data = urllib.request.urlopen(content, timeout=30).read()
                    images.append(base64.b64encode(img_data).decode())
                except: pass
            else:
                prompt = content
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, dict):
                    if item.get("type") == "text":
                        prompt = item.get("text", prompt)
                    elif item.get("type") == "image_url":
                        img_url = item.get("image_url", {}).get("url", "")
                        if img_url.startswith("http"):
                            import base64
                            try:
                                img_data = urllib.request.urlopen(img_url, timeout=30).read()
                                images.append(base64.b64encode(img_data).decode())
                            except: pass
    req_payload = {"model": model, "prompt": prompt, "images": images if images else None, "stream": False}
    try:
        data = json.dumps(req_payload).encode()
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = json.loads(resp.read())
        text = sanitize_visible_output(body.get("response", ""))
        if text:
            return True, build_openai_completion("ollama", model, request_id, text, [], "stop", {"prompt_tokens": 0, "completion_tokens": 0})
        return False, "Empty OCR response"
    except Exception as e:
        return False, extract_http_error(e)


def call_ngc(base_url, model, payload, api_key='', request_id=''):
    url = openai_chat_completions_url(base_url)
    messages = payload.get('messages', [])
    headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {api_key}'}
    req_payload = {'model': model, 'messages': messages, 'max_tokens': 4096}
    try:
        data = json.dumps(req_payload).encode()
        req = urllib.request.Request(url, data=data, headers=headers)
        with urllib.request.urlopen(req, timeout=120) as resp:
            body = json.loads(resp.read())
        text = body.get('choices', [{}])[0].get('message', {}).get('content', '')
        if text:
            return True, build_openai_completion('nvidia-ngc', model, request_id, text, [], 'stop', {'prompt_tokens': 0, 'completion_tokens': 0})
        return False, 'Empty NGC response'
    except Exception as e:
        return False, extract_http_error(e)


def call_anthropic_completion(base_url, model, payload, api_key='', thinking=DEFAULT_THINKING_LEVEL, supports_reasoning=False, debug_mode=False, request_id='', provider_name='anthropic'):
    url = base_url.rstrip('/') + '/v1/messages'
    system_text, api_msgs = openai_messages_to_anthropic(payload.get('messages', []))
    request_payload = {'model': model, 'max_tokens': thinking_max_tokens(thinking), 'messages': api_msgs}
    tools = openai_tools_to_anthropic(payload.get('tools'))
    if tools:
        request_payload['tools'] = tools
        tool_choice = payload.get('tool_choice')
        if isinstance(tool_choice, dict) and tool_choice.get('type') == 'function':
            request_payload['tool_choice'] = {'type': 'tool', 'name': ((tool_choice.get('function') or {}).get('name'))}
        elif tool_choice == 'required':
            request_payload['tool_choice'] = {'type': 'any'}
    if supports_reasoning and thinking == ThinkingLevel.HIGH:
        request_payload['thinking'] = {'type': 'enabled', 'budget_tokens': 4096}
    if payload.get('response_format', {}).get('type') == 'json_object':
        api_msgs.append({'role': 'user', 'content': [{'type': 'text', 'text': 'Return valid JSON only.'}]})
    if system_text:
        request_payload['system'] = system_text
    try:
        hdrs = {'Content-Type': 'application/json', 'anthropic-version': '2023-06-01'}
        if api_key:
            hdrs['x-api-key'] = api_key
        req = urllib.request.Request(url, data=json.dumps(request_payload).encode(), headers=hdrs)
        with urllib.request.urlopen(req, timeout=ANTHROPIC_TIMEOUT_SECONDS) as resp:
            body = json.loads(resp.read())
        text, tool_calls, stop_reason, usage = parse_anthropic_response(body)
        finish_reason = anthropic_stop_reason_to_openai_finish_reason(stop_reason, bool(tool_calls))
        return True, build_openai_completion(provider_name, model, request_id, text, tool_calls, finish_reason, usage, debug_mode=debug_mode, allow_debug_prefix=payload.get('response_format', {}).get('type') != 'json_object', suppress_tool_call_content=bool((payload.get('requirements') or {}).get('suppressToolCallContent') or payload.get('suppressToolCallContent') or payload.get('suppressIntermediateToolText')))
    except Exception as e:
        err = extract_http_error(e)
        logger.warning(f"Anthropic {base_url} {model}: {err}")
        return False, err


def call_google_completion(base_url, model, payload, api_key='', thinking=DEFAULT_THINKING_LEVEL, debug_mode=False, request_id='', provider_name='google'):
    if 'generativelanguage.googleapis.com' in base_url and '/v1beta' not in base_url:
        base_url = base_url.rstrip('/') + '/v1beta'
    url = base_url.rstrip('/') + f'/models/{urllib.parse.quote(model, safe="")}:generateContent'
    body_payload = build_google_generate_payload(
        payload.get('messages', []),
        thinking=thinking,
        want_json=payload.get('response_format', {}).get('type') == 'json_object',
        tools=payload.get('tools'),
        tool_choice=payload.get('tool_choice'),
    )
    try:
        data = json.dumps(body_payload).encode()
        hdrs = {'Content-Type': 'application/json'}
        if api_key:
            hdrs['x-goog-api-key'] = api_key
        req = urllib.request.Request(url, data=data, headers=hdrs)
        with urllib.request.urlopen(req, timeout=OPENAI_COMPAT_TIMEOUT_SECONDS) as resp:
            body = json.loads(resp.read())
        text = parse_google_generate_text(body)
        tool_calls = parse_google_generate_tool_calls(body)
        if not text and not tool_calls:
            return False, json.dumps(body)[:500]
        leak_reason = reject_visible_tool_call_leak(payload, text, tool_calls)
        if leak_reason:
            logger.warning(f"Google {base_url} {model}: {leak_reason}")
            return False, leak_reason
        candidate = (body.get('candidates') or [{}])[0] or {}
        finish_reason = 'tool_calls' if tool_calls else google_finish_reason_to_openai_finish_reason(candidate.get('finishReason'))
        return True, build_openai_completion(provider_name, model, request_id, text, tool_calls, finish_reason, {'prompt_tokens': 0, 'completion_tokens': 0}, debug_mode=debug_mode, allow_debug_prefix=payload.get('response_format', {}).get('type') != 'json_object', suppress_tool_call_content=bool((payload.get('requirements') or {}).get('suppressToolCallContent') or payload.get('suppressToolCallContent') or payload.get('suppressIntermediateToolText')))
    except Exception as e:
        err = extract_http_error(e)
        logger.warning(f"Google {base_url} {model}: {err}")
        return False, err


def call_google_vertex_completion(base_url, model, payload, thinking=DEFAULT_THINKING_LEVEL, debug_mode=False, request_id='', provider_name='google-vertex'):
    try:
        token = google_vertex_access_token()
        url = google_vertex_url(base_url, model, 'generateContent')
        body_payload = build_google_generate_payload(
            payload.get('messages', []),
            thinking=thinking,
            want_json=payload.get('response_format', {}).get('type') == 'json_object',
            tools=payload.get('tools'),
            tool_choice=payload.get('tool_choice'),
        )
        req = urllib.request.Request(url, data=json.dumps(body_payload).encode(), headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {token}'})
        with urllib.request.urlopen(req, timeout=GOOGLE_TIMEOUT_SECONDS) as resp:
            body = json.loads(resp.read())
        text = parse_google_generate_text(body)
        tool_calls = parse_google_generate_tool_calls(body)
        if not text and not tool_calls:
            return False, json.dumps(body)[:500]
        leak_reason = reject_visible_tool_call_leak(payload, text, tool_calls)
        if leak_reason:
            logger.warning(f"Vertex AI {base_url or GOOGLE_VERTEX_PROJECT} {model}: {leak_reason}")
            return False, leak_reason
        candidate = (body.get('candidates') or [{}])[0] or {}
        finish_reason = 'tool_calls' if tool_calls else google_finish_reason_to_openai_finish_reason(candidate.get('finishReason'))
        return True, build_openai_completion(provider_name, model, request_id, text, tool_calls, finish_reason, {'prompt_tokens': 0, 'completion_tokens': 0}, debug_mode=debug_mode, allow_debug_prefix=payload.get('response_format', {}).get('type') != 'json_object', suppress_tool_call_content=bool((payload.get('requirements') or {}).get('suppressToolCallContent') or payload.get('suppressToolCallContent') or payload.get('suppressIntermediateToolText')))
    except Exception as e:
        err = extract_http_error(e)
        logger.warning(f"Vertex AI {base_url or GOOGLE_VERTEX_PROJECT} {model}: {err}")
        return False, err


def open_upstream_with_credential_failover(provider, build_request, timeout, stream=True):
    """Open an upstream HTTP connection, failing over across the provider's
    credential pool on auth/quota/transient errors (notably HTTP 429).

    ``build_request(api_key)`` must return a fresh ``urllib.request.Request``
    for a given credential. Returns the opened response object. The failover
    loop runs entirely before any bytes are committed to the downstream client,
    so a rate-limited (429) key transparently yields to the next credential.
    Providers with a single key behave exactly as before (one attempt).
    """
    strategy = provider_credential_strategy(provider)
    candidate_keys = select_credential_keys(provider)
    identities = select_credential_identities(provider) if strategy != 'failover' else []
    if not candidate_keys:
        candidate_keys = [provider.api_key]
    last_exc = None
    for idx, key in enumerate(candidate_keys):
        ident = identities[idx] if idx < len(identities) else ''
        if ident:
            mark_credential_used(provider.name, ident)
        req = build_request(key)
        try:
            resp = urllib.request.urlopen(req, timeout=timeout)
            if ident:
                mark_credential_success(provider.name, ident)
            return resp, key
        except urllib.error.HTTPError as e:
            err = extract_http_error(e)
            last_exc = e
            if ident:
                mark_credential_error(provider.name, ident)
            if is_credential_failover_error(err) and idx < len(candidate_keys) - 1:
                logger.warning(f"Provider {provider.name} credential #{idx + 1} failed at {'stream' if stream else 'request'} open ({err[:120]}); trying next credential (strategy={strategy})")
                continue
            raise
        except Exception:
            raise
    if last_exc:
        raise last_exc
    raise RuntimeError('no_upstream_response')


def stream_openai_compat_to_client(self, provider, model, payload, request_id, thinking=DEFAULT_THINKING_LEVEL, supports_reasoning=False, debug_mode=False):
    url = openai_chat_completions_url(provider.base_url)
    proxied = build_openai_proxy_payload(payload, model, stream=True, supports_reasoning=supports_reasoning, thinking=thinking)
    base_hdrs = {'Content-Type': 'application/json'}
    add_openai_compat_headers(base_hdrs, provider.name)
    body_data = json.dumps(proxied).encode()

    def _build_oa_req(key):
        hdrs = dict(base_hdrs)
        if key:
            hdrs['Authorization'] = f'Bearer {key}'
        return urllib.request.Request(url, data=body_data, headers=hdrs)

    resp, _used_key = open_upstream_with_credential_failover(provider, _build_oa_req, OPENAI_COMPAT_TIMEOUT_SECONDS)
    with resp:
        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.send_header('Cache-Control', 'no-cache')
        for key, value in self.routing_headers({'model': display_model_id(provider.name, model)}, request_id).items():
            if value:
                self.send_header(key, str(value))
        self.end_headers()
        prefix_text = streaming_debug_prefix(provider.name, model, request_id) if debug_mode and not payload.get('tools') and payload.get('response_format', {}).get('type') != 'json_object' else ''
        if prefix_text:
            debug_chunk = json.dumps({
                'id': f'chatcmpl-{int(time.time())}',
                'object': 'chat.completion.chunk',
                'created': int(time.time()),
                'model': display_model_id(provider.name, model),
                'choices': [{'index': 0, 'delta': {'role': 'assistant', 'content': prefix_text}, 'finish_reason': None}],
            })
            self.wfile.write(f'data: {debug_chunk}\n\n'.encode())
            self.wfile.flush()
        stream_sanitize_state = {'prefix_open': True, 'prefix_pending': ''}
        while True:
            line = resp.readline()
            if not line:
                break
            self.wfile.write(sanitize_openai_compat_stream_line(line, provider.name, model, state=stream_sanitize_state))
            self.wfile.flush()
    return True


def stream_ollama_to_client(self, provider, model, payload, request_id, thinking=DEFAULT_THINKING_LEVEL, debug_mode=False):
    url = provider.base_url.rstrip('/') + '/api/chat'
    body_data = json.dumps(build_ollama_payload(model, payload, thinking=thinking, stream=True)).encode()

    def _build_ollama_req(key):
        hdrs = {'Content-Type': 'application/json'}
        if key:
            hdrs['Authorization'] = f'Bearer {key}'
        return urllib.request.Request(url, data=body_data, headers=hdrs)

    resp, _used_key = open_upstream_with_credential_failover(provider, _build_ollama_req, OLLAMA_TIMEOUT_SECONDS)
    chat_id = f'chatcmpl-{int(time.time())}'
    router_model = f'{provider.name}/{model}'
    sent_role = False
    with resp:
        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.send_header('Cache-Control', 'no-cache')
        for key, value in self.routing_headers({'model': router_model}, request_id).items():
            if value:
                self.send_header(key, str(value))
        self.end_headers()
        prefix_text = streaming_debug_prefix(provider.name, model, request_id) if debug_mode and not payload.get('tools') and payload.get('response_format', {}).get('type') != 'json_object' else ''
        if prefix_text:
            debug_chunk = json.dumps({'id': chat_id, 'object': 'chat.completion.chunk', 'created': int(time.time()), 'model': router_model, 'choices': [{'index': 0, 'delta': {'role': 'assistant', 'content': prefix_text}, 'finish_reason': None}]})
            self.wfile.write(f'data: {debug_chunk}\n\n'.encode())
            self.wfile.flush()
            sent_role = True
        stream_sanitize_state = {'prefix_open': True, 'prefix_pending': ''}
        saw_tool_calls = False
        while True:
            raw = resp.readline()
            if not raw:
                break
            line = raw.decode('utf-8', errors='replace').strip()
            if not line:
                continue
            body = json.loads(line)
            message = body.get('message', {}) or {}
            content = sanitize_stream_content_fragment(
                message.get('content', '') or '',
                provider.name,
                model,
                state=stream_sanitize_state,
            )
            tool_calls = normalize_tool_calls(message.get('tool_calls'))
            if content:
                delta = {'content': content}
                if not sent_role:
                    delta['role'] = 'assistant'
                    sent_role = True
                chunk = json.dumps({'id': chat_id, 'object': 'chat.completion.chunk', 'created': int(time.time()), 'model': router_model, 'choices': [{'index': 0, 'delta': delta, 'finish_reason': None}]})
                self.wfile.write(f'data: {chunk}\n\n'.encode())
                self.wfile.flush()
            if tool_calls:
                saw_tool_calls = True
                delta = {'tool_calls': tool_calls}
                if not sent_role:
                    delta['role'] = 'assistant'
                    sent_role = True
                chunk = json.dumps({'id': chat_id, 'object': 'chat.completion.chunk', 'created': int(time.time()), 'model': router_model, 'choices': [{'index': 0, 'delta': delta, 'finish_reason': None}]})
                self.wfile.write(f'data: {chunk}\n\n'.encode())
                self.wfile.flush()
            if body.get('done'):
                finish_reason = 'tool_calls' if (tool_calls or saw_tool_calls) else (body.get('done_reason') or 'stop')
                done_chunk = json.dumps({'id': chat_id, 'object': 'chat.completion.chunk', 'created': int(time.time()), 'model': router_model, 'choices': [{'index': 0, 'delta': {}, 'finish_reason': finish_reason}]})
                self.wfile.write(f'data: {done_chunk}\n\n'.encode())
                self.wfile.write(b'data: [DONE]\n\n')
                self.wfile.flush()
                break
    return True


def stream_google_to_client(self, provider, model, payload, request_id, thinking=DEFAULT_THINKING_LEVEL, debug_mode=False):
    """Stream Google Generative AI responses via SSE."""
    base_url = provider.base_url
    # Ensure base_url has /v1beta for Google API
    if 'generativelanguage.googleapis.com' in base_url and '/v1beta' not in base_url:
        base_url = base_url.rstrip('/') + '/v1beta'
    
    # Build URL with API key as query param (required for streaming).
    # The key is selected per-credential by the failover opener below.
    stream_path = base_url.rstrip('/') + f'/models/{urllib.parse.quote(model, safe="")}:streamGenerateContent'

    # Build Google payload from OpenAI messages
    system_text = ''
    contents = []
    for msg in sanitize_replay_messages(payload.get('messages', [])):
        role = msg.get('role', 'user')
        content = msg.get('content', '')
        if not content:
            continue
        if role in ('system', 'developer'):
            system_text += content + '\n'
            continue
        if role == 'assistant':
            gemini_role = 'model'
        else:
            gemini_role = 'user'
        part = {'text': content}
        if contents and contents[-1].get('role') == gemini_role:
            contents[-1].setdefault('parts', []).append(part)
        else:
            contents.append({'role': gemini_role, 'parts': [part]})
    
    if contents and contents[0].get('role') != 'user':
        contents.insert(0, {'role': 'user', 'parts': [{'text': 'Hello'}]})
    if not contents:
        contents = [{'role': 'user', 'parts': [{'text': 'Hello'}]}]
    
    google_payload = {
        'contents': contents,
        'generationConfig': {'maxOutputTokens': thinking_max_tokens(thinking)},
    }
    if system_text.strip():
        google_payload['systemInstruction'] = {'parts': [{'text': system_text.strip()}]}
    
    # API key is in URL query param for streaming; fail over across the
    # provider's credential pool (e.g. on 429) before committing to the client.
    google_body = json.dumps(google_payload).encode()

    def _build_google_req(key):
        api_key_param = f"?key={urllib.parse.quote(key)}" if key else ""
        return urllib.request.Request(stream_path + api_key_param, data=google_body, headers={'Content-Type': 'application/json'})

    resp, _used_key = open_upstream_with_credential_failover(provider, _build_google_req, GOOGLE_TIMEOUT_SECONDS)
    chat_id = f'chatcmpl-{int(time.time())}'
    router_model = f'{provider.name}/{model}'

    with resp:
        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.send_header('Cache-Control', 'no-cache')
        for key, value in self.routing_headers({'model': router_model}, request_id).items():
            if value:
                self.send_header(key, str(value))
        self.end_headers()
        
        prefix_text = streaming_debug_prefix(provider.name, model, request_id) if debug_mode else ''
        if prefix_text:
            debug_chunk = json.dumps({
                'id': chat_id, 'object': 'chat.completion.chunk', 'created': int(time.time()),
                'model': router_model,
                'choices': [{'index': 0, 'delta': {'role': 'assistant', 'content': prefix_text}, 'finish_reason': None}],
            })
            self.wfile.write(f'data: {debug_chunk}\n\n'.encode())
            self.wfile.flush()
        
        sent_role = False
        for line in resp:
            if not line:
                continue
            line_str = line.decode('utf-8', errors='replace').strip()
            if not line_str:
                continue
            try:
                chunk = json.loads(line_str)
                candidates = chunk.get('candidates', [])
                if candidates:
                    content_parts = candidates[0].get('content', {}).get('parts', [])
                    text = ''.join(p.get('text', '') for p in content_parts if p.get('text'))
                    if text:
                        delta = {'content': text}
                        if not sent_role:
                            delta['role'] = 'assistant'
                            sent_role = True
                        sse_chunk = json.dumps({
                            'id': chat_id, 'object': 'chat.completion.chunk', 'created': int(time.time()),
                            'model': router_model,
                            'choices': [{'index': 0, 'delta': delta, 'finish_reason': None}],
                        })
                        self.wfile.write(f'data: {sse_chunk}\n\n'.encode())
                        self.wfile.flush()
                    
                    finish_reason_str = candidates[0].get('finishReason')
                    if finish_reason_str:
                        done_chunk = json.dumps({
                            'id': chat_id, 'object': 'chat.completion.chunk', 'created': int(time.time()),
                            'model': router_model,
                            'choices': [{'index': 0, 'delta': {}, 'finish_reason': 'stop'}],
                        })
                        self.wfile.write(f'data: {done_chunk}\n\n'.encode())
                        self.wfile.write(b'data: [DONE]\n\n')
                        self.wfile.flush()
                        break
            except json.JSONDecodeError:
                continue
    return True


def write_openai_completion_as_sse(self, result, request_id):
    chat_id = result.get('id') or f'chatcmpl-{int(time.time())}'
    model = result.get('model') or 'sage-router/auto'
    created = int(result.get('created') or time.time())
    choice = (result.get('choices') or [{}])[0] or {}
    message = choice.get('message') or {}
    content = strip_leading_model_prefixes_for_display(
        sanitize_visible_output(message.get('content') or ''),
        model,
    )
    tool_calls = message.get('tool_calls') or []
    try:
        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.send_header('Cache-Control', 'no-cache')
        for key, value in self.routing_headers(result, request_id).items():
            if value:
                self.send_header(key, str(value))
        self.end_headers()
        if content:
            chunk = json.dumps({'id': chat_id, 'object': 'chat.completion.chunk', 'created': created, 'model': model, 'choices': [{'index': 0, 'delta': {'role': 'assistant', 'content': content}, 'finish_reason': None}]})
            self.wfile.write(f'data: {chunk}\n\n'.encode())
        if tool_calls:
            chunk = json.dumps({'id': chat_id, 'object': 'chat.completion.chunk', 'created': created, 'model': model, 'choices': [{'index': 0, 'delta': {'role': 'assistant', 'tool_calls': tool_calls}, 'finish_reason': None}]})
            self.wfile.write(f'data: {chunk}\n\n'.encode())
        finish_reason = 'tool_calls' if tool_calls else (choice.get('finish_reason') or 'stop')
        done_chunk = json.dumps({'id': chat_id, 'object': 'chat.completion.chunk', 'created': created, 'model': model, 'choices': [{'index': 0, 'delta': {}, 'finish_reason': finish_reason}]})
        self.wfile.write(f'data: {done_chunk}\n\n'.encode())
        self.wfile.write(b'data: [DONE]\n\n')
        self.wfile.flush()
    except (BrokenPipeError, ConnectionResetError):
        logger.warning(f"[{request_id}] Client disconnected during Chat Completions SSE write")

def handle_openai_chat_completions(self, payload, request_id, started, force_realtime=False, return_result=False):
    if isinstance(payload.get('messages'), list):
        payload['messages'] = sanitize_replay_messages(payload.get('messages'))
    original_requested_model = str(payload.get('model') or '').strip()
    message_count = len(payload.get('messages', []) or [])
    if is_sage_router_fusion_request(payload):
        return handle_sage_router_fusion(self, payload, request_id, started, return_result=return_result)
    if fusion_server_tool_should_invoke(payload):
        return handle_sage_router_fusion(self, fusion_payload_from_server_tool(payload), request_id, started, return_result=return_result)
    payload = strip_fusion_server_tools_from_payload(payload)
    router_profile = apply_router_profile(payload)
    client_visible_model = client_visible_model_for_request(payload, router_profile, original_requested_model)
    discord_public_profile = apply_discord_public_route_profile(payload)
    thinking = normalize_thinking(payload.get('thinking') or payload.get('reasoning'))
    route_mode = normalize_route_mode(payload.get('route'))
    if force_realtime:
        route_mode = 'realtime'
        thinking = ThinkingLevel.LOW  # Force low thinking for speed
    requirements = normalize_requirements(payload, thinking)
    modalities = request_modalities(requirements, payload)
    LAST_ROUTE_DEBUG['modalities'] = modalities
    want_json = str(payload.get('responseFormat') or '').lower() == 'json' or payload.get('response_format', {}).get('type') == 'json_object'
    client_wants_stream = bool(payload.get('stream', False))
    # Buffer provider responses and synthesize SSE for client streaming. This preserves fallback/empty-output detection even when OpenClaw streams with tools.
    want_stream = False
    debug_mode = normalize_debug_mode(payload)
    logger.info(f"[{request_id}] Incoming /v1/chat/completions with {message_count} messages, thinking={thinking.value}, route={route_mode}, json={want_json}, requirements={requirements}, modalities={modalities}, routerProfile={router_profile}, discordPublicProfile={discord_public_profile}, debug={debug_mode}")
    goal_compat = apply_goal_compat(payload)
    if goal_compat:
        payload['messages'] = sanitize_replay_messages(payload.get('messages'))
        thinking = normalize_thinking(payload.get('thinking') or payload.get('reasoning'))
        route_mode = normalize_route_mode(payload.get('route'))
        requirements = normalize_requirements(payload, thinking)
        modalities = request_modalities(requirements, payload)
        LAST_ROUTE_DEBUG['goalCompat'] = {'enabled': True, 'source': 'codex_openclaw_goal'}
        client_visible_model = client_visible_model or client_visible_model_for_request(payload, router_profile, original_requested_model)

    # Resolve model switches across providers. If the client carries a stale
    # provider prefix, e.g. ollama/gpt-5.5, prefer the provider that actually
    # advertises the requested model instead of cooling down the stale provider.
    _fp, _rm = resolve_requested_provider_model(payload)
    normalized_messages, intent, complexity, estimated_tokens, chain = prepare_route(
        payload.get('messages', []),
        request_id=request_id,
        thinking=thinking,
        route_mode=route_mode,
        requirements=requirements,
        want_json=want_json,
        streaming_mode='native-pass-through' if want_stream else 'disabled',
        force_provider=_fp,
        requested_model=_rm,
    )

    provider_payload = payload
    # For document/text extraction requests, send provider-compatible text instead of raw
    # attachment blocks. Native image/vision requests keep the original multimodal payload.
    if requirements.get('document') and not requirements.get('vision'):
        provider_payload = dict(payload)
        provider_payload['messages'] = enrich_document_messages(payload.get('messages', []))

    attempts = []
    overall_started = time.time()
    for pn, model in chain:
        if pn in DISABLED_PROVIDERS or pn not in PROVIDERS:
            continue
        prov = PROVIDERS[pn]
        if model_disabled_reason(pn, model):
            continue
        supports_reasoning = provider_supports_reasoning(prov, model)
        attempt_payload = provider_payload
        if provider_payload.get('tools') and not model_capabilities(prov, model).get('tools'):
            attempt_payload = dict(provider_payload)
            attempt_payload.pop('tools', None)
            attempt_payload.pop('tool_choice', None)
        logger.info(f"[{request_id}] Trying {pn}/{model} (api={prov.api_type}, reasoning={supports_reasoning}, stream={want_stream}, tools={bool(attempt_payload.get('tools'))})")
        started_attempt = time.time()
        ok = False
        result = None
        error_detail = None
        try:
            if prov.api_type == 'openai-completions':
                if want_stream:
                    stream_openai_compat_to_client(self, prov, model, attempt_payload, request_id, thinking=thinking, supports_reasoning=supports_reasoning, debug_mode=debug_mode)
                    ok = True
                else:
                    ok, result = call_openai_compat_completion(prov.base_url, model, attempt_payload, api_key=prov.api_key, provider_name=pn, thinking=thinking, supports_reasoning=supports_reasoning, debug_mode=debug_mode, request_id=request_id)
                    if not ok:
                        error_detail = result
            elif prov.api_type == 'ollama':
                if is_ocr_model(model):
                    ok, result = call_ollama_ocr(prov.base_url, model, attempt_payload, request_id)
                    if not ok:
                        error_detail = result
                elif want_stream:
                    stream_ollama_to_client(self, prov, model, attempt_payload, request_id, thinking=thinking, debug_mode=debug_mode)
                    ok = True
                else:
                    ok, result = call_ollama_completion(prov.base_url, model, attempt_payload, api_key=prov.api_key, thinking=thinking, provider_name=pn, debug_mode=debug_mode, request_id=request_id)
                    if not ok:
                        error_detail = result
            elif prov.api_type == 'anthropic-messages':
                if want_stream:
                    error_detail = 'streaming passthrough not implemented for anthropic bridge'
                else:
                    ok, result = call_anthropic_completion(prov.base_url, model, attempt_payload, api_key=prov.api_key, thinking=thinking, supports_reasoning=supports_reasoning, debug_mode=debug_mode, request_id=request_id, provider_name=pn)
                    if not ok:
                        error_detail = result
            elif prov.api_type == 'google-generative-language':
                if want_stream:
                    stream_google_to_client(self, prov, model, attempt_payload, request_id, thinking=thinking, debug_mode=debug_mode)
                    ok = True
                else:
                    ok, result = call_google_completion(prov.base_url, model, attempt_payload, api_key=prov.api_key, thinking=thinking, debug_mode=debug_mode, request_id=request_id)
                    if not ok:
                        error_detail = result
            elif prov.api_type == 'google-vertex-ai':
                if want_stream:
                    error_detail = 'streaming not implemented for Vertex AI bridge'
                else:
                    ok, result = call_google_vertex_completion(prov.base_url, model, attempt_payload, thinking=thinking, debug_mode=debug_mode, request_id=request_id)
                    if not ok:
                        error_detail = result
            elif prov.api_type == 'cloudflare-workers-ai':
                if want_stream:
                    error_detail = 'streaming not implemented for Cloudflare Workers AI bridge'
                else:
                    ok, result = call_cloudflare_workers_ai_completion(prov.base_url, model, attempt_payload, api_key=prov.api_key, thinking=thinking, debug_mode=debug_mode, request_id=request_id)
                    if not ok:
                        error_detail = result
            elif prov.api_type == 'openai-codex-responses':
                if want_stream:
                    error_detail = 'streaming not implemented for Codex responses'
                else:
                    ok, result = call_codex_completion(prov.base_url, model, attempt_payload, api_key=prov.api_key, provider_name=pn, thinking=thinking, supports_reasoning=supports_reasoning, debug_mode=debug_mode, request_id=request_id)
                    if not ok:
                        error_detail = result
            elif prov.api_type == 'openclaw-gateway':
                if want_stream or attempt_payload.get('tools'):
                    error_detail = 'streaming/tool passthrough unsupported for openclaw gateway bridge'
                else:
                    ok_text, text = call_openclaw_gateway(model, attempt_payload.get('messages', []), pn, thinking, want_json)
                    ok = ok_text
                    if ok:
                        result = build_openai_completion(pn, model, request_id, text, [], 'stop', {'prompt_tokens': 0, 'completion_tokens': 0}, debug_mode=debug_mode, allow_debug_prefix=not want_json)
                    else:
                        error_detail = text
            else:
                if want_stream:
                    error_detail = f'streaming passthrough unsupported for {prov.api_type}'
                else:
                    ok, result = call_openai_compat_completion(prov.base_url, model, attempt_payload, api_key=prov.api_key, provider_name=pn, thinking=thinking, supports_reasoning=supports_reasoning, debug_mode=debug_mode, request_id=request_id)
                    if not ok:
                        error_detail = result
        except Exception as e:
            error_detail = extract_http_error(e)
            logger.warning(f"[{request_id}] Streaming/advanced call failed for {pn}/{model}: {error_detail}")
            ok = False

        if ok and not want_stream and not openai_completion_has_visible_output(result):
            ok = False
            error_detail = 'empty visible content'
        elapsed = time.time() - started_attempt
        record_latency_outcome(intent.name, pn, model, elapsed, ok, '' if ok else error_detail or '')
        attempts.append({'provider': pn, 'model': model, 'ok': ok, 'elapsedMs': round(elapsed * 1000.0, 2), 'detail': '' if ok else str(error_detail or '')[:240]})
        LAST_ROUTE_DEBUG['attempts'] = attempts[-12:]
        if ok:
            total_elapsed = time.time() - overall_started
            record_model_modalities(pn, model, modalities)
            if client_visible_model and isinstance(result, dict):
                result = dict(result)
                result['upstream_model'] = result.get('model')
                result['model'] = client_visible_model
            LAST_ROUTE_DEBUG.update({'selected': {'provider': pn, 'model': model}, 'status': 'ok', 'error': None, 'totalElapsedMs': round(total_elapsed * 1000.0, 2), 'modalities': modalities})
            append_route_event({'request_id': request_id, 'status': 'ok', 'intent': intent.name, 'complexity': complexity.name, 'thinking': thinking.value, 'routeMode': route_mode, 'estimatedTokens': estimated_tokens, 'json': want_json, 'stream': bool(want_stream), 'requirements': requirements, 'selected': {'provider': pn, 'model': model}, 'attempts': attempts[-12:], 'totalElapsedMs': round(total_elapsed * 1000.0, 2), 'chain': [{'provider': cp, 'model': cm} for cp, cm in chain[:MAX_PROVIDER_ATTEMPTS]]})
            logger.info(f"[{request_id}] OK: {pn}/{model} (provider={elapsed:.2f}s, total={total_elapsed:.2f}s, stream={want_stream})")
            if return_result:
                return 200, result, self.routing_headers(result, request_id)
            if client_wants_stream:
                write_openai_completion_as_sse(self, result, request_id)
                return
            self.write_json(200, result, extra_headers=self.routing_headers(result, request_id))
            logger.info(f"[{request_id}] Responded in {time.time() - started:.2f}s")
            return
        logger.warning(f"[{request_id}] Failed {pn}/{model} after {elapsed:.2f}s")

    total_elapsed = time.time() - overall_started
    LAST_ROUTE_DEBUG.update({'selected': None, 'attempts': attempts[-12:], 'status': 'failed', 'error': 'All providers failed', 'totalElapsedMs': round(total_elapsed * 1000.0, 2)})
    append_route_event({'request_id': request_id, 'status': 'failed', 'intent': intent.name, 'complexity': complexity.name, 'thinking': thinking.value, 'routeMode': route_mode, 'estimatedTokens': estimated_tokens, 'json': want_json, 'stream': bool(want_stream), 'requirements': requirements, 'selected': None, 'attempts': attempts[-12:], 'totalElapsedMs': round(total_elapsed * 1000.0, 2), 'chain': [{'provider': cp, 'model': cm} for cp, cm in chain[:MAX_PROVIDER_ATTEMPTS]], 'error': 'All providers failed'})
    failure = {'error': 'All providers failed', 'request_id': request_id, 'attempts': attempts, 'choices': [{'message': {'content': 'Error: No providers available'}}]}
    headers = {'X-Sage-Router-Request-Id': request_id}
    if return_result:
        return 503, failure, headers
    self.write_json(503, failure, extra_headers=headers)


def handle_openai_responses(self, payload, request_id, started):
    chat_payload = responses_payload_to_chat_payload(payload)
    logger.info(f"[{request_id}] Incoming /v1/responses with {len(chat_payload.get('messages') or [])} messages, model={chat_payload.get('model')}, stream={bool(payload.get('stream'))}")
    status, chat_result, headers = handle_openai_chat_completions(self, chat_payload, request_id, started, return_result=True)
    if status >= 400:
        self.write_json(status, {
            'error': {
                'type': 'api_error',
                'message': chat_result.get('error') or 'Sage Router request failed',
            },
            'request_id': request_id,
            'attempts': chat_result.get('attempts') or [],
        }, extra_headers=headers)
        return
    response = openai_chat_completion_to_responses(chat_result, payload, request_id)
    if payload.get('stream'):
        write_responses_as_sse(self, response, request_id, extra_headers=headers)
    else:
        self.write_json(200, response, extra_headers=headers)
    logger.info(f"[{request_id}] Responses compat responded in {time.time() - started:.2f}s")

def google_to_openai_messages(payload):
    """Convert Google Generative AI request format to OpenAI messages format."""
    messages = []
    system_instruction = payload.get('systemInstruction', {})
    if system_instruction:
        sys_parts = system_instruction.get('parts', [])
        sys_text = ' '.join(p.get('text', '') for p in sys_parts if isinstance(p, dict))
        if sys_text.strip():
            messages.append({'role': 'system', 'content': sys_text.strip()})
    for content in payload.get('contents', []):
        role = content.get('role', 'user')
        parts = content.get('parts', [])
        text_parts = [p.get('text', '') for p in parts if isinstance(p, dict) and p.get('text')]
        combined = '\n'.join(text_parts)
        if combined.strip():
            oai_role = 'assistant' if role == 'model' else 'user'
            messages.append({'role': oai_role, 'content': combined})
    return messages or [{'role': 'user', 'content': 'Hello'}]


def openai_to_google_response(result, request_model):
    """Convert OpenAI chat completion response to Google Generative AI format."""
    content = result.get('choices', [{}])[0].get('message', {}).get('content', '') or ''
    model = result.get('model', request_model or 'sage-router/auto')
    usage = result.get('usage', {})
    return {
        'candidates': [{
            'content': {
                'parts': [{'text': content}],
                'role': 'model'
            },
            'finishReason': 'STOP',
            'index': 0
        }],
        'modelVersion': model,
        'usageMetadata': {
            'promptTokenCount': usage.get('prompt_tokens', 0),
            'candidatesTokenCount': usage.get('completion_tokens', 0),
            'totalTokenCount': usage.get('prompt_tokens', 0) + usage.get('completion_tokens', 0)
        }
    }


def prepare_route(messages, request_id='req-unknown', thinking=DEFAULT_THINKING_LEVEL, route_mode='balanced', requirements=None, want_json=False, streaming_mode=None, force_provider=None, requested_model=None):
    normalized_messages = normalize_messages(messages)
    estimated_tokens = estimate_prompt_tokens(normalized_messages)
    user_text = latest_user_text(normalized_messages)
    intent, _ = classify_intent(user_text)
    complexity = estimate_complexity(user_text)
    requirements = requirements or {}
    logger.info(f"[{request_id}] Intent: {intent.name}, Complexity: {complexity.name}, Thinking: {thinking.value}, Route: {route_mode}, JSON: {want_json}, EstTokens: {estimated_tokens}, ForceProvider: {force_provider or 'none'}")

    if requested_model:
        explicit_google_provider = force_provider in {'google', 'google-vertex'}
        if force_provider and not explicit_google_provider and not requested_model_supported_by_provider(force_provider, requested_model):
            inferred_provider = infer_provider_for_requested_model(requested_model, avoid_provider=force_provider)
            if inferred_provider:
                logger.info(f"[{request_id}] Requested model {requested_model} is served by {inferred_provider}, not {force_provider}; switching forced provider")
                force_provider = inferred_provider
        elif not force_provider:
            inferred_provider = infer_provider_for_requested_model(requested_model)
            if inferred_provider:
                logger.info(f"[{request_id}] Inferred provider {inferred_provider} for requested model {requested_model}")
                force_provider = inferred_provider
    
    # If provider forced, build chain with only that provider's models
    if force_provider and force_provider in PROVIDERS and force_provider not in DISABLED_PROVIDERS:
        prov = PROVIDERS[force_provider]
        if route_mode == 'local-first' and not provider_allowed_in_local_first(prov):
            rejections = [{'provider': force_provider, 'model': requested_model or '*', 'reason': local_first_rejection_reason(prov)}]
            LAST_ROUTE_DEBUG.update({'updated_at': int(time.time()), 'request_id': request_id, 'intent': intent.name, 'complexity': complexity.name, 'thinking': thinking.value, 'routeMode': route_mode, 'requirements': requirements, 'estimatedTokens': estimated_tokens, 'json': want_json, 'chain': [], 'scores': [], 'rejections': rejections[:30], 'selected': None, 'attempts': [], 'streaming': streaming_mode or ('buffered-wrapper' if requirements.get('streaming') else 'disabled'), 'status': 'routing', 'error': 'forced provider rejected by local-first', 'totalElapsedMs': None, 'forcedProvider': force_provider})
            return normalized_messages, intent, complexity, estimated_tokens, []
        if prov.api_type == 'ollama':
            fetch_ollama_models(prov)
        # Explicit provider/model requests should be attempted directly. A
        # lightweight reachability probe can be stale or insufficient for
        # OAuth-backed providers such as openai-codex, and falling back here
        # makes a hard request like openai-codex/gpt-5.5 silently route to an
        # unrelated model.
        if prov.models and (provider_endpoint_reachable(prov) or requested_model):
            # Build chain, prioritizing the requested model if specified
            all_models = dedupe_keep_order(prov.models)
            if requested_model and requested_model not in all_models:
                # For Google and other API providers, allow any model name (passthrough)
                if prov.api_type in ('google-generative-language', 'google-generative-ai'):
                    chain = [(force_provider, requested_model)]
                    logger.info(f"[{request_id}] Chain (Google passthrough): {chain}")
                    LAST_ROUTE_DEBUG.update({'updated_at': int(time.time()), 'request_id': request_id, 'intent': intent.name, 'complexity': complexity.name, 'thinking': thinking.value, 'routeMode': route_mode, 'requirements': requirements, 'estimatedTokens': estimated_tokens, 'json': want_json, 'chain': chain, 'scores': [{'provider': force_provider, 'model': requested_model, 'score': 100}], 'rejections': [], 'selected': None, 'attempts': [], 'streaming': streaming_mode or ('buffered-wrapper' if requirements.get('streaming') else 'disabled'), 'status': 'routing', 'error': None, 'totalElapsedMs': None, 'forcedProvider': force_provider, 'passthrough': True})
                    return normalized_messages, intent, complexity, estimated_tokens, chain
                # Do not send impossible model IDs to Ollama. A stale prefix
                # like ollama/gpt-5.5 should fall through to valid candidates
                # instead of cooling down the Ollama lane for model_not_found.
                if prov.api_type != 'ollama':
                    all_models = [requested_model] + all_models
            elif requested_model and requested_model in all_models:
                # Honor explicit provider/model requests exactly. If that
                # precise model fails at runtime, outer fallback layers can
                # choose a different provider; do not fan out across sibling
                # models on the same provider first.
                all_models = [requested_model]
            filtered_models = []
            forced_rejections = []
            for model in all_models:
                disabled_reason = model_disabled_reason(prov.name, model)
                if disabled_reason:
                    forced_rejections.append({'provider': force_provider, 'model': model, 'reason': disabled_reason})
                    continue
                if route_mode == 'local-first' and prov.api_type == 'ollama' and is_cloud_ollama_model(model):
                    forced_rejections.append({'provider': force_provider, 'model': model, 'reason': 'excluded by local-first (:cloud model)'})
                    continue
                if not is_chat_capable_model(prov, model):
                    forced_rejections.append({'provider': force_provider, 'model': model, 'reason': 'not chat-capable'})
                    continue
                ok_req, reason = model_meets_requirements(prov, model, requirements, estimated_tokens)
                if not ok_req:
                    forced_rejections.append({'provider': force_provider, 'model': model, 'reason': reason})
                    continue
                filtered_models.append(model)
            chain = [(force_provider, model) for model in filtered_models[:MAX_PROVIDER_ATTEMPTS]]
            score_debug = [{'provider': force_provider, 'model': model, 'score': 100} for _, model in chain]
            rejections = forced_rejections
            if prov.api_type == 'ollama' and chain:
                # Hosted Ollama catalogs can advertise models that still fail
                # at runtime with subscription/auth errors. Honor the explicit
                # Ollama request first, then keep normal router fallbacks alive.
                fb_chain, fb_scores, fb_rejections = select_model(intent, complexity, thinking, route_mode, requirements, estimated_tokens)
                seen = set(chain)
                fallback_chain = [
                    (pn, model)
                    for pn, model in fb_chain
                    if pn != force_provider and (pn, model) not in seen
                ]
                if fallback_chain:
                    if requested_model:
                        remaining = max(0, MAX_PROVIDER_ATTEMPTS - len(chain))
                        chain = chain + fallback_chain[:remaining]
                    else:
                        fallback_slots = min(len(fallback_chain), max(1, MAX_PROVIDER_ATTEMPTS // 2))
                        forced_slots = max(1, MAX_PROVIDER_ATTEMPTS - fallback_slots)
                        selected_fallbacks = fallback_chain[:fallback_slots]
                        non_ollama_fallback = next(
                            (
                                item for item in fallback_chain
                                if (PROVIDERS.get(item[0]) and PROVIDERS[item[0]].api_type != 'ollama')
                            ),
                            None,
                        )
                        if (
                            non_ollama_fallback
                            and non_ollama_fallback not in selected_fallbacks
                            and all((PROVIDERS.get(pn) and PROVIDERS[pn].api_type == 'ollama') for pn, _model in selected_fallbacks)
                        ):
                            if selected_fallbacks:
                                selected_fallbacks[-1] = non_ollama_fallback
                            else:
                                selected_fallbacks.append(non_ollama_fallback)
                        chain = chain[:forced_slots] + selected_fallbacks
                    score_debug = score_debug + [
                        score for score in fb_scores
                        if score.get('provider') != force_provider
                    ][:MAX_PROVIDER_ATTEMPTS]
                    rejections = (rejections + fb_rejections)[:30]
            logger.info(f"[{request_id}] Chain (forced): {chain}")
            if not chain:
                fb_chain, fb_scores, fb_rejections = select_model(intent, complexity, thinking, route_mode, requirements, estimated_tokens)
                if fb_chain:
                    logger.info(f"[{request_id}] Forced provider had no eligible models; fallback chain: {fb_chain}")
                    LAST_ROUTE_DEBUG.update({'updated_at': int(time.time()), 'request_id': request_id, 'intent': intent.name, 'complexity': complexity.name, 'thinking': thinking.value, 'routeMode': route_mode, 'requirements': requirements, 'estimatedTokens': estimated_tokens, 'json': want_json, 'chain': fb_chain, 'scores': fb_scores[:12], 'rejections': (forced_rejections + fb_rejections)[:30], 'selected': None, 'attempts': [], 'streaming': streaming_mode or ('buffered-wrapper' if requirements.get('streaming') else 'disabled'), 'status': 'routing', 'error': None, 'totalElapsedMs': None, 'forcedProvider': force_provider, 'forcedProviderFallback': True})
                    return normalized_messages, intent, complexity, estimated_tokens, fb_chain
            # Image/vision requests must route strictly to image-capable models.
            # If the forced provider/profile only offered non-vision or GLM
            # models, relax profile allow-lists and re-select globally so an
            # image-capable model can serve instead of failing.
            if has_modality_requirement(requirements) and not chain:
                relaxed = modality_relaxed_requirements(requirements)
                fb_chain, fb_scores, fb_rejections = select_model(intent, complexity, thinking, route_mode, relaxed, estimated_tokens)
                if fb_chain:
                    logger.info(f"[{request_id}] Forced provider had no multimodal-capable model; modality-relaxed fallback chain: {fb_chain}")
                    LAST_ROUTE_DEBUG.update({'updated_at': int(time.time()), 'request_id': request_id, 'intent': intent.name, 'complexity': complexity.name, 'thinking': thinking.value, 'routeMode': route_mode, 'requirements': requirements, 'estimatedTokens': estimated_tokens, 'json': want_json, 'chain': fb_chain, 'scores': fb_scores[:12], 'rejections': (forced_rejections + fb_rejections)[:30], 'selected': None, 'attempts': [], 'streaming': streaming_mode or ('buffered-wrapper' if requirements.get('streaming') else 'disabled'), 'status': 'routing', 'error': None, 'totalElapsedMs': None, 'forcedProvider': force_provider, 'modalityRelaxed': True})
                    return normalized_messages, intent, complexity, estimated_tokens, fb_chain
            LAST_ROUTE_DEBUG.update({'updated_at': int(time.time()), 'request_id': request_id, 'intent': intent.name, 'complexity': complexity.name, 'thinking': thinking.value, 'routeMode': route_mode, 'requirements': requirements, 'estimatedTokens': estimated_tokens, 'json': want_json, 'chain': chain, 'scores': score_debug, 'rejections': rejections[:30], 'selected': None, 'attempts': [], 'streaming': streaming_mode or ('buffered-wrapper' if requirements.get('streaming') else 'disabled'), 'status': 'routing', 'error': None, 'totalElapsedMs': None, 'forcedProvider': force_provider})
            return normalized_messages, intent, complexity, estimated_tokens, chain
    
    chain, score_debug, rejections = select_model(intent, complexity, thinking, route_mode, requirements, estimated_tokens)
    # auto/agentic profiles constrain allowProviders/allowModels/frontierLargeOnly.
    # If a multimodal (image/audio/video/document) request has no capable model
    # under those constraints, relax them and re-select globally so the request
    # routes to a capable model instead of failing.
    if has_modality_requirement(requirements) and not chain:
        relaxed = modality_relaxed_requirements(requirements)
        fb_chain, fb_scores, fb_rejections = select_model(intent, complexity, thinking, route_mode, relaxed, estimated_tokens)
        if fb_chain:
            chain, score_debug = fb_chain, fb_scores
            rejections = (rejections + fb_rejections)
            logger.info(f"[{request_id}] Profile had no multimodal-capable model; modality-relaxed fallback chain: {chain}")
    if requirements.get('suppressToolCallContent') and not chain:
        relaxed = discord_public_relaxed_requirements(requirements)
        fb_chain, fb_scores, fb_rejections = select_model(intent, complexity, thinking, route_mode, relaxed, estimated_tokens)
        if fb_chain:
            chain, score_debug = fb_chain, fb_scores
            rejections = (rejections + fb_rejections)
            logger.info(f"[{request_id}] Public/tool-safe profile had no strict eligible model; relaxed fallback chain: {chain}")
    LAST_ROUTE_DEBUG.update({'updated_at': int(time.time()), 'request_id': request_id, 'intent': intent.name, 'complexity': complexity.name, 'thinking': thinking.value, 'routeMode': route_mode, 'requirements': requirements, 'estimatedTokens': estimated_tokens, 'json': want_json, 'chain': chain, 'scores': score_debug[:12], 'rejections': rejections[:30], 'selected': None, 'attempts': [], 'streaming': streaming_mode or ('buffered-wrapper' if requirements.get('streaming') else 'disabled'), 'status': 'routing', 'error': None, 'totalElapsedMs': None})
    logger.info(f"[{request_id}] Chain: {chain} (no mid-stream switching; each candidate tried sequentially until one succeeds)")
    return normalized_messages, intent, complexity, estimated_tokens, chain


def handle_google_generate(self, body, request_id, started, model_name, want_stream=False):
    """Handle Google Generative AI /v1beta/models/{model}:generateContent requests."""
    try:
        payload = json.loads(body or b'{}')
        messages = google_to_openai_messages(payload)
        gen_config = payload.get('generationConfig', {})
        want_json = gen_config.get('responseMimeType') == 'application/json'
        thinking = normalize_thinking(payload.get('thinking'))
        route_mode = normalize_route_mode(payload.get('route'))
        requirements = normalize_requirements(payload, thinking)

        logger.info(f'[{request_id}] Google compat {model_name} with {len(messages)} messages, stream={want_stream}')
        result = route_request(messages, request_id=request_id, thinking=thinking, route_mode=route_mode, requirements=requirements, want_json=want_json)

        is_error = isinstance(result, dict) and result.get('error')
        if is_error:
            self.write_json(503, {
                'error': {
                    'code': 503,
                    'message': result.get('error', 'Internal error'),
                    'status': 'UNAVAILABLE'
                }
            }, extra_headers=self.routing_headers(result, request_id))
        elif want_stream:
            content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
            model = result.get('model', model_name or 'sage-router/auto')
            # Google streaming format - SSE with chunked candidates
            sse_body = ''
            # Initial chunk with metadata
            chunk = json.dumps({'candidates': [{'content': {'parts': [{'text': content}], 'role': 'model'}, 'finishReason': 'STOP', 'index': 0}], 'modelVersion': model})
            sse_body += f'data: {chunk}\n\n'
            sse_body += 'data: [DONE]\n\n'
            sse_bytes = sse_body.encode()
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Content-Length', str(len(sse_bytes)))
            for key, value in self.routing_headers(result, request_id).items():
                if value:
                    self.send_header(key, str(value))
            self.end_headers()
            self.wfile.write(sse_bytes)
            self.wfile.flush()
        else:
            google_resp = openai_to_google_response(result, model_name)
            self.write_json(200, google_resp, extra_headers=self.routing_headers(result, request_id))
        logger.info(f'[{request_id}] Google compat responded in {time.time() - started:.2f}s')
    except Exception as e:
        logger.exception(f'[{request_id}] Google compat request failed')
        self.write_json(500, {
            'error': {'code': 500, 'message': str(e), 'status': 'INTERNAL'}
        }, extra_headers={'X-Sage-Router-Request-Id': request_id})


    for msg in reversed(messages or []):
        if msg.get('role') == 'user' and msg.get('content'):
            return msg.get('content', '')
    return messages[-1].get('content', '') if messages else ''


def latest_user_text(messages):
    for msg in reversed(messages or []):
        if msg.get('role') == 'user' and msg.get('content'):
            return msg.get('content', '')
    return messages[-1].get('content', '') if messages else ''


def route_request(messages, request_id='req-unknown', thinking=DEFAULT_THINKING_LEVEL, route_mode='balanced', requirements=None, want_json=False, force_provider=None, requested_model=None):
    requirements = requirements or {}
    normalized_messages, intent, complexity, estimated_tokens, chain = prepare_route(
        messages,
        request_id=request_id,
        thinking=thinking,
        route_mode=route_mode,
        requirements=requirements,
        want_json=want_json,
        streaming_mode='buffered-wrapper' if requirements.get('streaming') else 'disabled',
        force_provider=force_provider,
        requested_model=requested_model,
    )
    overall_started = time.time()
    attempts = []
    provider_payload = {
        'messages': normalized_messages,
        'response_format': {'type': 'json_object'} if want_json else {},
        'requirements': requirements,
    }
    for pn, model in chain:
        if pn in DISABLED_PROVIDERS:
            continue
        if pn not in PROVIDERS:
            continue
        prov = PROVIDERS[pn]
        supports_reasoning = provider_supports_reasoning(prov, model)
        logger.info(f"[{request_id}] Trying {pn}/{model} (api={prov.api_type}, reasoning={supports_reasoning})")
        started = time.time()
        ok = False
        result = None
        error_detail = None
        if prov.api_type == 'ollama':
            ok, result = call_ollama_completion(prov.base_url, model, provider_payload, prov.api_key, thinking, provider_name=pn, request_id=request_id)
        elif prov.api_type == 'openclaw-gateway':
            gateway_timeout = OPENCLAW_GATEWAY_CODE_TIMEOUT_SECONDS if intent == Intent.CODE else OPENCLAW_GATEWAY_TIMEOUT_SECONDS
            ok_text, text = call_openclaw_gateway(model, normalized_messages, pn, thinking, want_json, gateway_timeout)
            ok = ok_text
            if ok:
                result = build_openai_completion(pn, model, request_id, text, [], 'stop', {'prompt_tokens': 0, 'completion_tokens': 0})
            else:
                error_detail = text
        elif prov.api_type == 'anthropic-messages':
            ok, result = call_anthropic_completion(prov.base_url, model, provider_payload, prov.api_key, thinking, supports_reasoning, request_id=request_id, provider_name=pn)
        elif prov.api_type == 'google-generative-language':
            ok, result = call_google_completion(prov.base_url, model, provider_payload, prov.api_key, thinking, request_id=request_id, provider_name=pn)
        elif prov.api_type == 'google-vertex-ai':
            ok, result = call_google_vertex_completion(prov.base_url, model, provider_payload, thinking, request_id=request_id, provider_name=pn)
        elif prov.api_type == 'cloudflare-workers-ai':
            ok, result = call_cloudflare_workers_ai_completion(prov.base_url, model, provider_payload, prov.api_key, thinking, request_id=request_id)
        elif prov.api_type == 'openai-codex-responses':
            ok, result = call_codex_completion(prov.base_url, model, provider_payload, prov.api_key, pn, thinking, supports_reasoning, request_id=request_id)
        else:
            ok, result = call_openai_compat_completion(prov.base_url, model, provider_payload, prov.api_key, pn, thinking, supports_reasoning, request_id=request_id)
        if not ok:
            error_detail = error_detail or result
        if ok and not openai_completion_has_visible_output(result):
            ok = False
            error_detail = 'empty visible content'
        elapsed = time.time() - started
        record_latency_outcome(intent.name, pn, model, elapsed, ok, '' if ok else error_detail or '')
        attempts.append({'provider': pn, 'model': model, 'ok': ok, 'elapsedMs': round(elapsed * 1000.0, 2), 'detail': '' if ok else str(error_detail or '')[:240]})
        LAST_ROUTE_DEBUG['attempts'] = attempts[-12:]
        if ok:
            total_elapsed = time.time() - overall_started
            choice = (result.get('choices') or [{}])[0] or {}
            message = choice.get('message') or {}
            text = message.get('content') or ''
            logger.info(f"[{request_id}] OK: {pn}/{model} ({len(text)} chars, provider={elapsed:.2f}s, total={total_elapsed:.2f}s)")
            LAST_ROUTE_DEBUG.update({'selected': {'provider': pn, 'model': model}, 'status': 'ok', 'error': None, 'totalElapsedMs': round(total_elapsed * 1000.0, 2)})
            append_route_event({'request_id': request_id, 'status': 'ok', 'intent': intent.name, 'complexity': complexity.name, 'thinking': thinking.value, 'routeMode': route_mode, 'estimatedTokens': estimated_tokens, 'json': want_json, 'stream': False, 'requirements': requirements, 'selected': {'provider': pn, 'model': model}, 'attempts': attempts[-12:], 'totalElapsedMs': round(total_elapsed * 1000.0, 2), 'chain': [{'provider': cp, 'model': cm} for cp, cm in chain[:MAX_PROVIDER_ATTEMPTS]]})
            return result
        logger.warning(f"[{request_id}] Failed {pn}/{model} after {elapsed:.2f}s")
    total_elapsed = time.time() - overall_started
    logger.error(f"[{request_id}] All providers failed after {total_elapsed:.2f}s")
    LAST_ROUTE_DEBUG.update({'selected': None, 'attempts': attempts[-12:], 'status': 'failed', 'error': 'All providers failed', 'totalElapsedMs': round(total_elapsed * 1000.0, 2)})
    append_route_event({'request_id': request_id, 'status': 'failed', 'intent': intent.name, 'complexity': complexity.name, 'thinking': thinking.value, 'routeMode': route_mode, 'estimatedTokens': estimated_tokens, 'json': want_json, 'stream': False, 'requirements': requirements, 'selected': None, 'attempts': attempts[-12:], 'totalElapsedMs': round(total_elapsed * 1000.0, 2), 'chain': [{'provider': cp, 'model': cm} for cp, cm in chain[:MAX_PROVIDER_ATTEMPTS]], 'error': 'All providers failed'})
    return {"error": "All providers failed", "request_id": request_id, "attempts": attempts, "choices": [{"message": {"content": "Error: No providers available"}}]}

def openai_to_anthropic_response(openai_resp, request_model=None):
    """Translate an OpenAI chat completion response to Anthropic Messages API format."""
    choice = (openai_resp.get('choices') or [{}])[0]
    content_text = choice.get('message', {}).get('content', '') or ''
    finish_reason = choice.get('finish_reason', 'stop')
    model = openai_resp.get('model', request_model or 'sage-router/auto')
    usage = openai_resp.get('usage', {})
    return {
        'id': f'msg_{uuid.uuid4().hex[:24]}',
        'type': 'message',
        'role': 'assistant',
        'content': [{'type': 'text', 'text': content_text}],
        'model': model,
        'stop_reason': openai_finish_reason_to_anthropic_stop_reason(finish_reason),
        'stop_sequence': None,
        'usage': {
            'input_tokens': usage.get('prompt_tokens', 0),
            'output_tokens': usage.get('completion_tokens', 0),
        },
    }


def anthropic_to_openai_request(anthropic_payload):
    """Translate an Anthropic Messages API request to OpenAI chat completions format."""
    messages = []
    # Anthropic system is a top-level field, not a message
    system_text = anthropic_payload.get('system', '')
    if isinstance(system_text, list):
        # Anthropic system can be a list of content blocks
        system_text = ' '.join(b.get('text', '') for b in system_text if isinstance(b, dict) and b.get('type') == 'text')
    if system_text:
        messages.append({'role': 'system', 'content': system_text})
    for msg in (anthropic_payload.get('messages') or []):
        role = msg.get('role', 'user')
        content = msg.get('content', '')
        # Anthropic content can be a list of content blocks
        if isinstance(content, list):
            parts = []
            for block in content:
                if isinstance(block, dict):
                    if block.get('type') == 'text':
                        parts.append(str(block.get('text', '')))
                    elif block.get('type') == 'tool_use':
                        parts.append(f'[Tool Use: {block.get("name", "unknown")}] {json.dumps(block.get("input", {}))}')
                    elif block.get('type') == 'tool_result':
                        result_content = block.get('content', '')
                        if isinstance(result_content, list):
                            result_content = ' '.join(b.get('text', '') for b in result_content if isinstance(b, dict) and b.get('type') == 'text')
                        parts.append(f'[Tool Result: {block.get("tool_use_id", "?")}] {result_content}')
                    elif block.get('type') == 'image' and block.get('source', {}).get('type') == 'base64':
                        parts.append('[Image attached]')
                elif isinstance(block, str):
                    parts.append(block)
            content = '\n'.join(parts)
        if role in ('user', 'assistant', 'system'):
            messages.append({'role': role, 'content': content})
        else:
            messages.append({'role': 'user', 'content': f'[{role.upper()}] {content}'})
    # Ensure first message is user or system
    if messages and messages[0]['role'] not in ('system', 'user'):
        messages.insert(0, {'role': 'user', 'content': 'Hello'})
    if not messages:
        messages = [{'role': 'user', 'content': 'Hello'}]
    return {
        'model': anthropic_payload.get('model', 'sage-router/auto'),
        'messages': messages,
        'max_tokens': anthropic_payload.get('max_tokens', 4096),
        'stream': False,
        'temperature': anthropic_payload.get('temperature', 1.0),
        'route': anthropic_payload.get('route'),
        'thinking': anthropic_payload.get('thinking'),
        'reasoning': anthropic_payload.get('reasoning'),
        'requirements': anthropic_payload.get('requirements'),
    }


def handle_anthropic_messages(self, body, request_id, started):
    """Handle POST /v1/messages - Anthropic Messages API compatibility.
    Translates request to OpenAI format, routes, translates response back."""
    try:
        anthropic_payload = json.loads(body or b'{}')
        request_model = anthropic_payload.get('model', 'sage-router/auto')
        want_stream = anthropic_payload.get('stream', False)
        openai_payload = anthropic_to_openai_request(anthropic_payload)
        openai_payload['messages'] = sanitize_replay_messages(openai_payload.get('messages', []))
        message_count = len(openai_payload.get('messages', []))
        thinking = normalize_thinking(openai_payload.get('thinking') or openai_payload.get('reasoning'))
        router_profile = apply_router_profile(openai_payload)
        discord_public_profile = apply_discord_public_route_profile(openai_payload)
        goal_compat = apply_goal_compat(openai_payload)
        thinking = normalize_thinking(openai_payload.get('thinking') or openai_payload.get('reasoning'))
        route_mode = normalize_route_mode(openai_payload.get('route'))
        requirements = normalize_requirements(openai_payload, thinking)
        want_json = False
        logger.info(f"[{request_id}] Incoming /v1/messages (Anthropic compat) with {message_count} messages, model={request_model}, thinking={thinking.value}, route={route_mode}, stream={want_stream}")
        if goal_compat:
            LAST_ROUTE_DEBUG['goalCompat'] = {'enabled': True, 'source': 'codex_openclaw_goal'}
        _fp, _rm = resolve_requested_provider_model(openai_payload)
        result = route_request(openai_payload.get('messages', []), request_id=request_id, thinking=thinking, route_mode=route_mode, requirements=requirements, want_json=want_json, force_provider=_fp, requested_model=_rm)
        if isinstance(result, dict) and result.get('error'):
            # Error response - translate to Anthropic error format
            self.write_json(503, {
                'type': 'error',
                'error': {'type': 'api_error', 'message': result.get('error', 'Internal error')}
            }, extra_headers=self.routing_headers(result, request_id))
        elif want_stream:
            # Anthropic SSE streaming format
            content_text = result.get('choices', [{}])[0].get('message', {}).get('content', '') or ''
            finish_reason = (result.get('choices') or [{}])[0].get('finish_reason', 'stop')
            stop_reason = openai_finish_reason_to_anthropic_stop_reason(finish_reason)
            model = result.get('model', request_model or 'sage-router/auto')
            msg_id = f'msg_{uuid.uuid4().hex[:24]}'
            usage = result.get('usage', {})
            sse_events = []
            # message_start
            sse_events.append(f'event: message_start\ndata: {json.dumps({"type":"message_start","message":{"id":msg_id,"type":"message","role":"assistant","content":[],"model":model,"stop_reason":None,"stop_sequence":None,"usage":{"input_tokens":usage.get("prompt_tokens",0),"output_tokens":0}}})}')
            # content_block_start
            sse_events.append(f'event: content_block_start\ndata: {json.dumps({"type":"content_block_start","index":0,"content_block":{"type":"text","text":""}})}')
            # content_block_delta (send full text as one chunk for simplicity)
            sse_events.append(f'event: content_block_delta\ndata: {json.dumps({"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":content_text}})}')
            # content_block_stop
            sse_events.append(f'event: content_block_stop\ndata: {json.dumps({"type":"content_block_stop","index":0})}')
            # message_delta
            sse_events.append(f'event: message_delta\ndata: {json.dumps({"type":"message_delta","delta":{"stop_reason":stop_reason,"stop_sequence":None},"usage":{"output_tokens":usage.get("completion_tokens",len(content_text)//4)}})}')
            # message_stop
            sse_events.append(f'event: message_stop\ndata: {json.dumps({"type":"message_stop"})}')
            sse_body = '\n\n'.join(sse_events) + '\n\n'
            sse_bytes = sse_body.encode()
            self.send_response(200)
            self.send_header('Content-Type', 'text/event-stream')
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Content-Length', str(len(sse_bytes)))
            for key, value in self.routing_headers(result, request_id).items():
                if value:
                    self.send_header(key, str(value))
            self.end_headers()
            self.wfile.write(sse_bytes)
            self.wfile.flush()
        else:
            # Non-streaming - translate to Anthropic response format
            anthropic_resp = openai_to_anthropic_response(result, request_model)
            self.write_json(200, anthropic_resp, extra_headers=self.routing_headers(result, request_id))
        logger.info(f'[{request_id}] Anthropic compat responded in {time.time() - started:.2f}s')
    except Exception as e:
        logger.exception(f'[{request_id}] Anthropic compat request failed')
        self.write_json(500, {
            'type': 'error',
            'error': {'type': 'api_error', 'message': str(e)}
        }, extra_headers={'X-Sage-Router-Request-Id': request_id})


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *a):
        logger.info("%s - %s", self.address_string(), fmt % a)

    def routing_headers(self, payload=None, request_id=''):
        payload = payload or {}
        headers = {}
        model = payload.get('model') or ''
        if model:
            headers['X-Sage-Router-Model'] = model
            if '/' in model:
                provider, model_name = model.split('/', 1)
                headers['X-Sage-Router-Provider'] = provider
                headers['X-Sage-Router-Model-Name'] = model_name
        upstream_model = payload.get('upstream_model') or ''
        if upstream_model:
            headers['X-Sage-Router-Upstream-Model'] = upstream_model
            if '/' in upstream_model:
                upstream_provider, upstream_model_name = upstream_model.split('/', 1)
                headers['X-Sage-Router-Upstream-Provider'] = upstream_provider
                headers['X-Sage-Router-Upstream-Model-Name'] = upstream_model_name
        if request_id:
            headers['X-Sage-Router-Request-Id'] = request_id
        if LAST_ROUTE_DEBUG.get('intent'):
            headers['X-Sage-Router-Intent'] = LAST_ROUTE_DEBUG.get('intent')
        if LAST_ROUTE_DEBUG.get('routeMode'):
            headers['X-Sage-Router-Route-Mode'] = LAST_ROUTE_DEBUG.get('routeMode')
        if LAST_ROUTE_DEBUG.get('modalities'):
            headers['X-Sage-Router-Modalities'] = ','.join(LAST_ROUTE_DEBUG.get('modalities') or [])
        return headers

    def send_cors_headers(self):
        origin = self.headers.get('Origin') or ''
        allow_origin = '*'
        if CORS_ORIGINS and '*' not in CORS_ORIGINS:
            allow_origin = origin if origin in CORS_ORIGINS else CORS_ORIGINS[0]
        self.send_header('Access-Control-Allow-Origin', allow_origin)
        self.send_header('Access-Control-Allow-Headers', 'Authorization, Content-Type, Stripe-Signature')
        self.send_header('Access-Control-Allow-Methods', 'GET, HEAD, POST, OPTIONS')
        self.send_header('Vary', 'Origin')

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_cors_headers()
        self.end_headers()

    def write_json(self, status_code, payload, extra_headers=None):
        body = json.dumps(payload).encode()
        try:
            self.send_response(status_code)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.send_cors_headers()
            for key, value in (extra_headers or {}).items():
                if value:
                    self.send_header(key, str(value))
            self.end_headers()
            if self.command != 'HEAD':
                self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            logger.warning("Client disconnected before response could be written")

    def write_binary(self, status_code, body, content_type, extra_headers=None):
        try:
            self.send_response(status_code)
            self.send_header('Content-Type', content_type or 'application/octet-stream')
            self.send_header('Content-Length', str(len(body)))
            self.send_cors_headers()
            for key, value in (extra_headers or {}).items():
                if value:
                    self.send_header(key, str(value))
            self.end_headers()
            if self.command != 'HEAD':
                self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            logger.warning("Client disconnected before binary response could be written")

    def stream_binary_response(self, resp, extra_headers=None):
        try:
            resp_type = resp.headers.get('Content-Type') or 'application/octet-stream'
            self.send_response(resp.status)
            self.send_header('Content-Type', resp_type)
            self.send_header('Transfer-Encoding', 'chunked')
            self.send_cors_headers()
            for key, value in (extra_headers or {}).items():
                if value:
                    self.send_header(key, str(value))
            self.end_headers()
            while True:
                chunk = resp.read(8192)
                if not chunk:
                    break
                self.wfile.write(f'{len(chunk):x}\r\n'.encode())
                self.wfile.write(chunk)
                self.wfile.write(b'\r\n')
                self.wfile.flush()
            self.wfile.write(b'0\r\n\r\n')
            self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            logger.warning("Client disconnected during audio streaming")

    def do_GET(self):
        parsed_request = urllib.parse.urlparse(self.path or '')
        request_path = parsed_request.path or '/'
        query_params = urllib.parse.parse_qs(parsed_request.query)
        # Serve the bundled config dashboard when the browser hits the
        # root URL with an Accept: text/html header (Umbrel launches the
        # app at path: "" and expects the dashboard to come up).  Programmatic
        # clients that send Accept: application/json still get the JSON
        # root descriptor below.
        if request_path in ('', '/') and 'text/html' in (self.headers.get('Accept') or ''):
            if not require_operator_request(self):
                return
            try:
                with open(os.path.join(os.path.dirname(__file__), 'web', 'dashboard', 'index.html'), 'rb') as f:
                    body = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(body)))
                self.send_cors_headers()
                self.end_headers()
                if self.command != 'HEAD':
                    self.wfile.write(body)
            except OSError:
                self.write_json(500, {'error': 'dashboard_not_found'})
            return
        if request_path in ('', '/'):
            self.write_json(200, {
                "name": "Sage Router",
                "status": "ok",
                "description": "Local-first AI model router with OpenAI, Anthropic, Ollama, NVIDIA NIM, and agent-harness compatible endpoints.",
                "endpoints": {
                    "health": "/health",
                    "models": "/v1/models",
                    "responses": "/v1/responses",
                    "chatCompletions": "/v1/chat/completions",
                    "audioTranscriptions": "/v1/audio/transcriptions",
                    "audioSpeech": "/v1/audio/speech",
                    "anthropicMessages": "/v1/messages",
                    "googleGenerateContent": "/v1beta/models/{model}:generateContent",
                    "discovery": "/discovery",
                    "analytics": "/analytics?days=7",
                    "analyticsFunnel": "/analytics/funnel?days=30",
                    "dashboard": "/dashboard",
                    "account": "/account",
                    "apiKeys": "/account/api-keys",
                    "plan": "/account/plan",
                    "stripeCheckout": "/billing/stripe/checkout",
                    "stripeBillingPortal": "/billing/stripe/portal",
                    "cryptoPayment": "/billing/crypto/intent"
                },
                "docs": "https://sagerouter.dev",
                "source": "https://github.com/earlvanze/sage-router"
            })
        elif request_path == '/health':
            self.write_json(200, {
                "status": "ok",
                "providers": available_provider_names(),
                "configured": list(PROVIDERS.keys()),
                "disabled": sorted(DISABLED_PROVIDERS),
                "disabledModels": sorted(DISABLED_MODELS),
                "thinking": {
                    "default": DEFAULT_THINKING_LEVEL.value,
                    "accepted": [level.value for level in ThinkingLevel],
                    "routeModes": ["fast", "balanced", "deep", "best", "local-first", "local-strict", "realtime"],
                },
                "requirements": {
                    "supportedKeys": ["reasoning", "json", "tools", "longContext", "document", "vision", "streaming"]
                },
                "audio": {
                    "sttProvider": AUDIO_STT_PROVIDER,
                    "sttConfigured": audio_proxy_provider('stt')[1] == '',
                    "ttsProvider": AUDIO_TTS_PROVIDER,
                    "ttsConfigured": audio_proxy_provider('tts')[1] == '',
                    "endpoints": ["/v1/audio/transcriptions", "/v1/audio/speech"],
                    "timeoutSeconds": AUDIO_PROXY_TIMEOUT_SECONDS,
                },
                "intentClassifier": {
                    "enabled": INTENT_CLASSIFIER_ENABLED,
                    "provider": INTENT_CLASSIFIER_PROVIDER,
                    "baseUrl": INTENT_CLASSIFIER_BASE_URL,
                    "model": INTENT_CLASSIFIER_MODEL,
                    "timeoutSeconds": INTENT_CLASSIFIER_TIMEOUT_SECONDS,
                    "minConfidence": INTENT_CLASSIFIER_MIN_CONFIDENCE,
                },
                "dario": {
                    "baseUrl": DARIO_LOCAL_BASE_URL,
                    "autostart": DARIO_AUTOSTART,
                    "reachable": dario_endpoint_ready(timeout=0.1),
                    "bundled": bool(shutil.which('dario')),
                },
                "manifests": {
                    name: {
                        "url": OLLAMA_MANIFEST_URLS.get(canonical_provider_env_key(name), ''),
                        "file": OLLAMA_MANIFEST_FILES.get(canonical_provider_env_key(name), ''),
                        "cache": OLLAMA_MODEL_CACHE.get(name, {})
                    }
                    for name, provider in PROVIDERS.items()
                    if provider.api_type == 'ollama'
                },
                "reasoningCapabilities": reasoning_capabilities_summary(),
                "imageCapable": image_capable_models_summary(),
                "audioCapable": audio_capable_models_summary(),
                "videoCapable": video_capable_models_summary(),
                "modelModalities": model_modalities_shared_status(),
                "lastRoute": LAST_ROUTE_DEBUG,
                "blocks": {key: {"until": info["until"], "reason": info["reason"]} for key, info in TEMP_MODEL_BLOCKS.items()},
            })
        elif request_path == '/setup/state':
            if not require_operator_request(self):
                return
            self.write_json(200, setup_state_payload())
        elif request_path == '/setup/credentials':
            if not require_operator_request(self):
                return
            self.write_json(200, {'credentials': list_setup_credentials(), 'configured': sorted(PROVIDERS.keys())})
        elif request_path == '/setup/model-modalities':
            if not require_operator_request(self):
                return
            _persist_model_modalities(force=True)
            self.write_json(200, {'modelModalities': model_modalities_summary(force=True), 'path': APP_MODEL_MODALITIES, 'shared': model_modalities_shared_status()})
        elif request_path == '/dashboard':
            if not require_operator_request(self):
                return
            try:
                with open(os.path.join(os.path.dirname(__file__), 'web', 'dashboard', 'index.html'), 'rb') as f:
                    body = f.read()
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.send_header('Content-Length', str(len(body)))
                self.send_cors_headers()
                self.end_headers()
                if self.command != 'HEAD':
                    self.wfile.write(body)
            except OSError:
                self.write_json(500, {'error': 'dashboard_not_found'})
            return
        elif request_path in {'/pricing', '/plans'}:
            self.write_json(200, {**public_launch_metadata(), 'plans': public_plan_catalog(), 'agentNativeFeatures': PUBLIC_AGENT_NATIVE_FEATURES})
        elif request_path == '/model-catalog':
            self.write_json(200, {'modelCatalog': public_model_catalog(), **public_launch_metadata()})
        elif request_path == '/features/agent-native':
            self.write_json(200, {'agentNativeFeatures': PUBLIC_AGENT_NATIVE_FEATURES})
        elif request_path == '/account':
            user, customer = require_user_customer(self)
            if not customer:
                return
            self.write_json(200, {'customer': public_customer(customer), 'emailVerification': user_email_verification_state(user)})
        elif request_path == '/account/plan':
            user, customer = require_user_customer(self)
            if not customer:
                return
            self.write_json(200, {
                'plan': customer.get('plan') or 'free',
                'status': customer.get('status') or 'inactive',
                'routing_enabled': customer_is_active(customer),
                'customer': public_customer(customer),
                'emailVerification': user_email_verification_state(user),
                'plans': public_plan_catalog(),
                **public_launch_metadata(),
            })
        elif request_path == '/account/usage':
            user, customer = require_user_customer(self)
            if not customer:
                return
            usage = account_usage_for_customer(customer)
            self.write_json(200, {
                'usage': usage,
                'activation': account_activation_for_customer(customer, usage=usage),
                'emailVerification': user_email_verification_state(user),
            })
        elif request_path == '/account/api-keys':
            _user, customer = require_user_customer(self)
            if not customer:
                return
            self.write_json(200, {'api_keys': [public_api_key(k, customer) for k in api_keys_for_customer(customer.get('id'))]})
        elif request_path.startswith('/admin/customers'):
            if not require_operator_request(self):
                return
            parts = request_path.strip('/').split('/')
            qs = query_params
            if len(parts) >= 3 and parts[2]:
                customer_id = urllib.parse.unquote(parts[2])
                customer = customer_by_id(customer_id)
                if not customer:
                    self.write_json(404, {'error': 'customer_not_found'})
                    return
                self.write_json(200, operator_customer_summary(customer, include_audit=True))
                return
            query = (qs.get('q') or [''])[0]
            status = (qs.get('status') or [''])[0]
            limit = (qs.get('limit') or ['50'])[0]
            contact_export = str((qs.get('contactExport') or qs.get('contact_export') or [''])[0] or '').strip().lower()
            rows = operator_customer_rows(query=query, status=status, limit=limit)
            if contact_export in {'activation', 'no-key', 'no_key', 'signup_to_key_recovery'}:
                export = operator_activation_contact_export(rows)
                self.write_json(200, {
                    **export,
                    'limit': max(1, min(int(limit or 50) if str(limit or '').isdigit() else 50, 100)),
                    'query': query,
                    'status': status,
                })
                return
            customers = [operator_customer_summary(row, include_audit=False) for row in rows]
            self.write_json(200, {
                'customers': customers,
                'count': len(rows),
                'limit': max(1, min(int(limit or 50) if str(limit or '').isdigit() else 50, 100)),
                'query': query,
                'status': status,
                **operator_customer_listing_summary(customers),
                'privacy': {
                    'containsRawApiKeys': False,
                    'containsApiKeyHashes': False,
                    'containsProviderCredentials': False,
                    'containsPrompts': False,
                    'operatorOnly': True,
                },
            })
        elif request_path.startswith('/analytics/funnel'):
            if not analytics_authorized(self):
                self.write_json(401, {'error': 'unauthorized'})
                return
            qs = query_params
            days = float((qs.get('days') or ['30'])[0] or 30)
            limit = int((qs.get('limit') or [ANALYTICS_EVENT_LIMIT])[0] or ANALYTICS_EVENT_LIMIT)
            self.write_json(200, build_launch_funnel_snapshot(days * 24 * 3600, limit))
        elif request_path.startswith('/analytics'):
            if not analytics_authorized(self):
                self.write_json(401, {'error': 'unauthorized'})
                return
            qs = query_params
            days = float((qs.get('days') or ['7'])[0] or 7)
            limit = int((qs.get('limit') or [ANALYTICS_EVENT_LIMIT])[0] or ANALYTICS_EVENT_LIMIT)
            self.write_json(200, build_analytics_snapshot(days * 24 * 3600, limit))
        elif request_path.startswith('/account/analytics'):
            user = authenticated_user(self)
            generated = verify_generated_api_key(bearer_token(self))
            customer = customer_for_user(user, create=False) if user else (generated or {}).get('customer')
            if not customer_is_active(customer):
                self.write_json(401, {'error': 'unauthorized'})
                return
            qs = query_params
            days = float((qs.get('days') or ['7'])[0] or 7)
            limit = int((qs.get('limit') or [ANALYTICS_EVENT_LIMIT])[0] or ANALYTICS_EVENT_LIMIT)
            snapshot = build_analytics_snapshot(days * 24 * 3600, limit, customer_id=customer.get('id'))
            snapshot['account'] = {'customer_id': customer.get('id'), 'plan': customer.get('plan'), 'status': customer.get('status')}
            self.write_json(200, snapshot)
        elif request_path.startswith('/billing/crypto/status'):
            _user, customer = require_user_customer(self)
            if not customer:
                return
            qs = query_params
            intent_id = (qs.get('id') or [''])[0]
            intent = (
                payment_intent_for_customer(customer.get('id'), intent_id)
                if intent_id else latest_payment_intent_for_customer(
                    customer.get('id'),
                    statuses=['pending_manual_review', 'settled_manual_review'],
                    kinds=['crypto_manual'],
                )
            )
            if not intent:
                self.write_json(404, {'error': 'payment_intent_not_found'})
                return
            self.write_json(200, {'intent': public_payment_intent(intent)})
        elif request_path == '/admin/clear-blocks':
            if not require_operator_request(self):
                return
            count = len(TEMP_MODEL_BLOCKS)
            TEMP_MODEL_BLOCKS.clear()
            MODEL_HEALTH_CACHE.clear()
            self.write_json(200, {"cleared": count, "status": "ok"})
        elif request_path == '/admin/blocks':
            if not require_operator_request(self):
                return
            self.write_json(200, {
                "blocks": {key: {"until": info["until"], "reason": info["reason"], "expiresInSeconds": max(0, info["until"] - time.time())} for key, info in TEMP_MODEL_BLOCKS.items()},
                "count": len(TEMP_MODEL_BLOCKS)
            })
        elif request_path == '/discovery':
            if not require_operator_request(self):
                return
            # Return discovered providers from GitHub manifests, CLI, and fallbacks
            openclaw_github = discover_openclaw_github_manifests()
            hermes_github = discover_hermes_github_manifests()
            openclaw_cli = discover_openclaw_cli_providers(timeout_seconds=12)
            hermes_cli = discover_hermes_cli_providers(timeout_seconds=8)
            openclaw_file = discover_openclaw_core_providers()
            hermes_file = discover_hermes_core_providers()
            openclaw_agent_auth = discover_openclaw_agent_auth_providers()
            self.write_json(200, {
                "openclaw": {
                    "github": {
                        "source": "openclaw/openclaw repo",
                        "manifests": openclaw_github,
                        "count": len(openclaw_github)
                    },
                    "cli": {
                        "command": "openclaw models list --all",
                        "providers": openclaw_cli,
                        "count": len(openclaw_cli) if isinstance(openclaw_cli, dict) else 0
                    },
                    "config": {
                        "source": "~/.openclaw/openclaw.json",
                        "providers": openclaw_file,
                        "count": len(openclaw_file)
                    }
                },
                "hermes": {
                    "github": {
                        "source": "NousResearch/hermes-agent repo",
                        "manifests": hermes_github,
                        "count": len(hermes_github)
                    },
                    "cli": {
                        "command": "hermes status --json",
                        "providers": hermes_cli,
                        "count": len(hermes_cli) if isinstance(hermes_cli, dict) else 0
                    },
                    "config": {
                        "source": "~/.hermes/config.yaml + auth.json",
                        "providers": hermes_file,
                        "count": len(hermes_file)
                    }
                },
                "totalProviders": len(openclaw_file) + len(hermes_file)
            })
        elif request_path == '/v1/models' or request_path.startswith('/v1/models/'):
            if not client_request_authorized(self):
                self.write_json(401, model_api_auth_error_payload(), extra_headers=model_api_auth_error_headers())
                return
            self.write_json(200, openai_models_payload())
        elif request_path.startswith('/v1beta/models'):
            if not client_request_authorized(self):
                self.write_json(401, model_api_auth_error_payload(), extra_headers=model_api_auth_error_headers())
                return
            # Google Generative AI models listing endpoint.
            self.write_json(200, google_models_payload())
        else:
            self.send_response(404)
            self.end_headers()

    def do_HEAD(self):
        self.do_GET()

    def do_POST(self):
        parsed_request = urllib.parse.urlparse(self.path or '')
        request_path = parsed_request.path or '/'
        if request_path == '/setup/provider':
            if not require_operator_request(self):
                return
            try:
                self.write_json(200, save_setup_provider(read_json_body(self)))
            except ValueError as e:
                self.write_json(400, {'error': str(e)})
            except Exception as e:
                logger.exception('Provider setup failed')
                self.write_json(500, {'error': 'provider_setup_failed', 'detail': str(e)})
            return
        if request_path == '/setup/codex-auth':
            if not require_operator_request(self):
                return
            try:
                self.write_json(200, save_codex_setup_auth(read_json_body(self)))
            except json.JSONDecodeError:
                self.write_json(400, {'error': 'invalid_json'})
            except ValueError as e:
                self.write_json(400, {'error': str(e)})
            except Exception as e:
                logger.exception('Codex auth setup failed')
                self.write_json(500, {'error': 'codex_auth_setup_failed', 'detail': str(e)})
            return
        if request_path == '/setup/codex-oauth/start':
            if not require_operator_request(self):
                return
            try:
                self.write_json(200, start_codex_oauth_session())
            except ValueError as e:
                self.write_json(400, {'error': str(e)})
            except Exception as e:
                logger.exception('Codex OAuth start failed')
                self.write_json(500, {'error': 'codex_oauth_start_failed', 'detail': str(e)})
            return
        if request_path == '/setup/codex-oauth/poll':
            if not require_operator_request(self):
                return
            try:
                self.write_json(200, poll_codex_oauth_session(read_json_body(self)))
            except ValueError as e:
                self.write_json(400, {'error': str(e)})
            except Exception as e:
                logger.exception('Codex OAuth poll failed')
                self.write_json(500, {'error': 'codex_oauth_poll_failed', 'detail': str(e)})
            return
        if request_path == '/setup/codex-oauth/cancel':
            if not require_operator_request(self):
                return
            try:
                self.write_json(200, cancel_codex_oauth_session(read_json_body(self)))
            except Exception:
                self.write_json(200, {'status': 'cancelled'})
            return
        if request_path == '/setup/credentials/add':
            if not require_operator_request(self):
                return
            try:
                self.write_json(200, save_setup_credential(read_json_body(self)))
            except ValueError as e:
                self.write_json(400, {'error': str(e)})
            except Exception as e:
                logger.exception('Credential add failed')
                self.write_json(500, {'error': 'credential_add_failed', 'detail': str(e)})
            return
        if request_path == '/setup/credentials/remove':
            if not require_operator_request(self):
                return
            try:
                self.write_json(200, remove_setup_credential(read_json_body(self)))
            except ValueError as e:
                self.write_json(400, {'error': str(e)})
            except Exception as e:
                logger.exception('Credential remove failed')
                self.write_json(500, {'error': 'credential_remove_failed', 'detail': str(e)})
            return
        if request_path == '/setup/credentials/strategy':
            if not require_operator_request(self):
                return
            try:
                self.write_json(200, set_setup_credential_strategy(read_json_body(self)))
            except ValueError as e:
                self.write_json(400, {'error': str(e)})
            except Exception as e:
                logger.exception('Credential strategy set failed')
                self.write_json(500, {'error': 'credential_strategy_failed', 'detail': str(e)})
            return
        if request_path == '/setup/provider/enabled':
            if not require_operator_request(self):
                return
            try:
                self.write_json(200, set_setup_provider_enabled(read_json_body(self)))
            except ValueError as e:
                self.write_json(400, {'error': str(e)})
            except Exception as e:
                logger.exception('Provider enablement update failed')
                self.write_json(500, {'error': 'provider_enablement_failed', 'detail': str(e)})
            return
        if request_path == '/setup/model/enabled':
            if not require_operator_request(self):
                return
            try:
                self.write_json(200, set_setup_model_enabled(read_json_body(self)))
            except ValueError as e:
                self.write_json(400, {'error': str(e)})
            except Exception as e:
                logger.exception('Model enablement update failed')
                self.write_json(500, {'error': 'model_enablement_failed', 'detail': str(e)})
            return
        if request_path == '/setup/model-modalities/update':
            if not require_operator_request(self):
                return
            try:
                self.write_json(200, set_model_modalities(read_json_body(self)))
            except ValueError as e:
                self.write_json(400, {'error': str(e)})
            except Exception as e:
                logger.exception('Model modality update failed')
                self.write_json(500, {'error': 'model_modality_update_failed', 'detail': str(e)})
            return
        if request_path == '/setup/model-modalities/reset':
            if not require_operator_request(self):
                return
            try:
                self.write_json(200, reset_model_modalities(read_json_body(self)))
            except ValueError as e:
                self.write_json(400, {'error': str(e)})
            except Exception as e:
                logger.exception('Model modality reset failed')
                self.write_json(500, {'error': 'model_modality_reset_failed', 'detail': str(e)})
            return
        if request_path == '/admin/customers/hydrate-auth-users':
            if not require_operator_request(self):
                return
            try:
                payload = read_json_body(self)
                limit = max(1, min(int(payload.get('limit') or 1000), 5000))
                self.write_json(200, hydrate_auth_signups_to_customers(limit=limit))
            except Exception as e:
                logger.exception('Auth signup customer hydration failed')
                self.write_json(500, {'error': 'auth_signup_customer_hydration_failed', 'detail': str(e)})
            return
        if request_path == '/admin/customers/send-activation-followups':
            if not require_trusted_browser_origin(self):
                return
            if not require_operator_request(self):
                return
            try:
                payload = read_json_body(self)
                dry_run = bool(payload.get('dryRun') or payload.get('dry_run'))
                if not dry_run and payload.get('sendConfirmation') != ACTIVATION_FOLLOWUP_SEND_CONFIRMATION:
                    self.write_json(400, {
                        'error': 'activation_followup_send_confirmation_required',
                        'requiredConfirmation': ACTIVATION_FOLLOWUP_SEND_CONFIRMATION,
                        'dryRunSupported': True,
                    })
                    return
                limit = max(1, min(int(payload.get('limit') or ACTIVATION_EMAIL_MAX_BATCH), ACTIVATION_EMAIL_MAX_BATCH))
                rows = operator_customer_rows(
                    query=payload.get('q') or payload.get('query') or '',
                    status=payload.get('status') or 'inactive',
                    limit=limit,
                )
                result = operator_activation_followup_send(
                    rows,
                    segment=payload.get('segment') or '',
                    limit=limit,
                    dry_run=dry_run,
                )
                self.write_json(200 if result.get('configured') or result.get('dryRun') else 503, result)
            except Exception as e:
                logger.exception('Activation follow-up send failed')
                self.write_json(500, {'error': 'activation_followup_send_failed', 'detail': extract_http_error(e)})
            return
        if request_path == '/api/restart':
            if not require_operator_request(self):
                return
            # Restart the router process. Only honored in environments where
            # SAGE_ROUTER_ALLOW_RESTART=1 (set by the Umbrel/Cyber compose
            # so the bundled supervisor can pick the process back up). We
            # do NOT os.execv from inside a request thread, so the actual
            # exit happens in a daemon thread a moment later; the response
            # is sent first so the dashboard can poll /health for recovery.
            from configparser import RawConfigParser
            from os import _exit, getpid, getenv
            from threading import Thread
            if not (os.environ.get('SAGE_ROUTER_ALLOW_RESTART') or '').strip():
                self.write_json(403, {'error': 'restart_disabled', 'detail': 'SAGE_ROUTER_ALLOW_RESTART is not set'})
                return
            self.write_json(202, {'status': 'restarting', 'pid': getpid()})
            def _die():
                try:
                    time.sleep(0.5)
                    _exit(0)
                except Exception:
                    pass
            Thread(target=_die, daemon=True).start()
            return
        if request_path.startswith('/admin/customers/') and request_path.endswith('/suspend'):
            if not require_trusted_browser_origin(self):
                return
            if not require_operator_request(self):
                return
            parts = request_path.split('/')
            customer_id = urllib.parse.unquote(parts[3] if len(parts) > 3 else '')
            if not customer_id:
                self.write_json(400, {'error': 'customer_id_required'})
                return
            payload = read_json_body(self)
            customer, revoked, audit_event = suspend_customer_for_operator(
                customer_id,
                payload.get('reasonCode') or payload.get('reason_code') or 'operator_review',
            )
            if not customer:
                self.write_json(404, {'error': 'customer_not_found'})
                return
            self.write_json(200, {
                'customer': public_customer(customer),
                'revokedApiKeys': len(revoked),
                'auditEvent': audit_event,
                'status': 'suspended',
            })
            return
        if request_path.startswith('/admin/customers/') and request_path.endswith('/unsuspend'):
            if not require_trusted_browser_origin(self):
                return
            if not require_operator_request(self):
                return
            parts = request_path.split('/')
            customer_id = urllib.parse.unquote(parts[3] if len(parts) > 3 else '')
            if not customer_id:
                self.write_json(400, {'error': 'customer_id_required'})
                return
            payload = read_json_body(self)
            try:
                customer, audit_event = unsuspend_customer_for_operator(
                    customer_id,
                    payload.get('status') or 'inactive',
                    payload.get('reasonCode') or payload.get('reason_code') or 'operator_review',
                )
            except ValueError as e:
                self.write_json(400, {'error': str(e)})
                return
            if not customer:
                self.write_json(404, {'error': 'customer_not_found'})
                return
            self.write_json(200, {
                'customer': public_customer(customer),
                'auditEvent': audit_event,
                'revokedApiKeysRemainRevoked': True,
                'status': customer.get('status') or 'inactive',
            })
            return
        if request_path.startswith('/admin/payment-intents/') and request_path.endswith('/approve'):
            if not require_trusted_browser_origin(self):
                return
            if not require_operator_request(self):
                return
            parts = request_path.split('/')
            intent_id = urllib.parse.unquote(parts[3] if len(parts) > 3 else '')
            if not intent_id:
                self.write_json(400, {'error': 'payment_intent_id_required'})
                return
            payload = read_json_body(self)
            try:
                customer, intent, audit_event = approve_manual_payment_intent(
                    intent_id,
                    payload.get('settlementReference') or payload.get('settlement_reference') or '',
                    payload.get('reasonCode') or payload.get('reason_code') or 'billing_review',
                    payload.get('plan') or '',
                )
            except ValueError as e:
                error = str(e)
                if error in ('payment_intent_already_settled', 'payment_intent_not_pending'):
                    self.write_json(409, {'error': error})
                else:
                    self.write_json(400, {'error': error})
                return
            if not intent:
                self.write_json(404, {'error': 'payment_intent_not_found'})
                return
            self.write_json(200, {
                'customer': public_customer(customer),
                'intent': public_payment_intent(intent),
                'auditEvent': audit_event,
                'routingEnabled': customer_is_active(customer),
                'status': intent.get('status') or 'settled_manual_review',
            })
            return
        if request_path == '/account/api-keys':
            if not require_trusted_browser_origin(self):
                return
            user, customer = require_user_customer(self)
            if not customer:
                return
            payload = read_json_body(self)
            try:
                raw_key, row = create_api_key_for_customer(customer, payload.get('name') or 'Default')
            except ValueError as e:
                detail = str(e)
                if detail.startswith('active_api_key_limit_reached:'):
                    limit = int(detail.split(':', 1)[1])
                    self.write_json(409, {
                        'error': 'active_api_key_limit_reached',
                        'maxActiveApiKeysPerCustomer': limit,
                        'message': f'Revoke an existing API key before creating another. Active key limit: {limit}.',
                    })
                    return
                raise
            self.write_json(201, {
                'api_key': public_api_key(row, customer),
                'key': raw_key,
                'emailVerification': user_email_verification_state(user),
            })
            return
        if request_path.startswith('/account/api-keys/') and request_path.endswith('/revoke'):
            if not require_trusted_browser_origin(self):
                return
            _user, customer = require_user_customer(self)
            if not customer:
                return
            key_id = request_path.split('/')[3]
            existing_key = next((row for row in api_keys_for_customer(customer.get('id')) if row.get('id') == key_id), None)
            row = revoke_api_key_for_customer(customer.get('id'), key_id)
            if not row:
                self.write_json(404, {'error': 'api_key_not_found'})
                return
            audit_event = None
            if str((existing_key or {}).get('status') or 'active').lower() != 'revoked':
                audit_event = record_operator_audit_event(
                    'api_key.revoke',
                    customer.get('id'),
                    status_before=customer.get('status') or '',
                    status_after=customer.get('status') or '',
                    revoked_api_keys_count=1,
                    reason_code='customer_request',
                    actor='customer',
                )
            self.write_json(200, {'api_key': public_api_key(row, customer), 'auditEvent': audit_event})
            return
        if request_path == '/billing/stripe/checkout':
            if not require_trusted_browser_origin(self):
                return
            user, customer = require_user_customer(self)
            if not customer:
                return
            if not require_verified_account_user(self, user):
                return
            payload = read_json_body(self)
            requested_plan = payload.get('plan') or 'pro'
            plan = normalize_stripe_plan(requested_plan)
            if not plan:
                self.write_json(400, {
                    'error': 'invalid_plan',
                    'message': 'Choose a configured hosted checkout plan.',
                    'plan': str(requested_plan or '').strip().lower(),
                    'validPlans': sorted(stripe_price_ids_by_plan().keys() or ['lite', 'pro', 'max']),
                })
                return
            price_ids = stripe_price_ids_by_plan()
            price_id = price_ids.get(plan)
            if not (STRIPE_SECRET_KEY and price_id):
                self.write_json(503, {'error': 'stripe_not_configured', 'plan': plan, 'required_env': ['STRIPE_SECRET_KEY or SAGE_ROUTER_STRIPE_SECRET_KEY', 'SAGE_ROUTER_STRIPE_PRICE_IDS=lite=price_x,pro=price_y,max=price_z or SAGE_ROUTER_STRIPE_PRICE_ID/STRIPE_PRICE_ID for pro']})
                return
            try:
                stripe_customer_id = str(customer.get('stripe_customer_id') or '').strip()
                checkout_fields = {
                    'mode': 'subscription',
                    'line_items[0][price]': price_id,
                    'line_items[0][quantity]': '1',
                    'success_url': f'{APP_BASE_URL}/account.html?checkout=success&plan={urllib.parse.quote(plan, safe="")}&session_id={{CHECKOUT_SESSION_ID}}',
                    'cancel_url': f'{APP_BASE_URL}/account.html?checkout=cancel&plan={urllib.parse.quote(plan, safe="")}',
                    'client_reference_id': customer.get('id'),
                    'customer': stripe_customer_id or None,
                    'customer_email': None if stripe_customer_id else (customer.get('email') or None),
                    'metadata[customer_id]': customer.get('id'),
                    'metadata[user_id]': customer.get('user_id'),
                    'metadata[plan]': plan,
                    'subscription_data[metadata][customer_id]': customer.get('id'),
                    'subscription_data[metadata][user_id]': customer.get('user_id'),
                    'subscription_data[metadata][plan]': plan,
                }
                session = stripe_request('/v1/checkout/sessions', checkout_fields)
                self.write_json(200, {'checkout_url': session.get('url'), 'session_id': session.get('id')})
            except Exception as e:
                logger.warning(f'Stripe checkout failed: {extract_http_error(e)}')
                self.write_json(502, {'error': 'stripe_checkout_failed'})
            return
        if request_path == '/billing/stripe/portal':
            if not require_trusted_browser_origin(self):
                return
            _user, customer = require_user_customer(self)
            if not customer:
                return
            stripe_customer_id = str(customer.get('stripe_customer_id') or '').strip()
            if not STRIPE_SECRET_KEY:
                self.write_json(503, {'error': 'stripe_not_configured', 'required_env': ['STRIPE_SECRET_KEY or SAGE_ROUTER_STRIPE_SECRET_KEY']})
                return
            if not stripe_customer_id:
                self.write_json(409, {'error': 'stripe_customer_missing', 'message': 'Complete Stripe checkout before opening the billing portal.'})
                return
            try:
                session = stripe_request('/v1/billing_portal/sessions', {
                    'customer': stripe_customer_id,
                    'return_url': f'{APP_BASE_URL}/account.html?billing=portal',
                })
                self.write_json(200, {'portal_url': session.get('url'), 'session_id': session.get('id')})
            except Exception as e:
                logger.warning(f'Stripe billing portal failed: {extract_http_error(e)}')
                self.write_json(502, {'error': 'stripe_portal_failed'})
            return
        if request_path == '/billing/stripe/webhook':
            length = int(self.headers.get('Content-Length', 0) or 0)
            raw = self.rfile.read(length) if length else b'{}'
            if not STRIPE_WEBHOOK_SECRET:
                self.write_json(503, {'error': 'stripe_webhook_not_configured', 'required_env': ['STRIPE_WEBHOOK_SECRET or SAGE_ROUTER_STRIPE_WEBHOOK_SECRET']})
                return
            if not verify_stripe_signature(raw, self.headers.get('Stripe-Signature') or ''):
                self.write_json(400, {'error': 'invalid_signature'})
                return
            try:
                event = json.loads(raw or b'{}')
            except Exception:
                event = {}
            event_type = event.get('type')
            event_id = str(event.get('id') or '').strip()
            if event_id and stripe_webhook_event_seen(event_id):
                self.write_json(200, {'received': True, 'duplicate': True, 'event_id': event_id})
                return
            obj = ((event.get('data') or {}).get('object') or {}) if isinstance(event, dict) else {}
            try:
                customer_id = resolve_stripe_webhook_customer_id(obj)
            except ValueError as e:
                logger.warning(f'Stripe webhook customer binding rejected: {str(e)} event={event_id or "unknown"}')
                self.write_json(409, {'error': str(e), 'event_id': event_id})
                return
            if customer_id and event_type in {'checkout.session.completed', 'checkout.session.async_payment_succeeded'}:
                if event_type == 'checkout.session.async_payment_succeeded' or stripe_checkout_session_entitles_routing(obj):
                    update_customer(customer_id, {
                        'plan': stripe_plan_from_object(obj, fallback_customer_id=customer_id),
                        'status': billing_status_for_customer(customer_id, 'active'),
                        'stripe_customer_id': obj.get('customer') or '',
                        'stripe_subscription_id': obj.get('subscription') or '',
                    })
                else:
                    logger.info(
                        'Stripe checkout session completed without paid fulfillment; '
                        f'event={event_id or "unknown"} customer={customer_id} payment_status={obj.get("payment_status") or "missing"}'
                    )
            elif customer_id and event_type in {'customer.subscription.updated', 'customer.subscription.created'}:
                status = obj.get('status') or 'active'
                update_customer(customer_id, {
                    'plan': stripe_plan_from_object(obj, fallback_customer_id=customer_id),
                    'status': billing_status_for_customer(customer_id, 'active' if status in {'active', 'trialing'} else status),
                    'stripe_customer_id': obj.get('customer') or '',
                    'stripe_subscription_id': obj.get('id') or '',
                })
            elif customer_id and event_type == 'customer.subscription.deleted':
                update_customer(customer_id, {'status': billing_status_for_customer(customer_id, 'inactive')})
            elif customer_id and event_type in {'invoice.payment_failed', 'invoice.marked_uncollectible'}:
                update_customer(customer_id, {
                    'status': billing_status_for_customer(customer_id, 'past_due'),
                    'stripe_customer_id': obj.get('customer') or '',
                    'stripe_subscription_id': obj.get('subscription') or '',
                })
            elif customer_id and event_type in {'invoice.payment_succeeded', 'invoice.paid'}:
                update_customer(customer_id, {
                    'plan': stripe_plan_from_object(obj, fallback_customer_id=customer_id),
                    'status': billing_status_for_customer(customer_id, 'active'),
                    'stripe_customer_id': obj.get('customer') or '',
                    'stripe_subscription_id': obj.get('subscription') or '',
                })
            store_stripe_webhook_event(event, customer_id=customer_id)
            self.write_json(200, {'received': True, 'event_id': event_id})
            return
        if request_path == '/billing/crypto/intent':
            if not require_trusted_browser_origin(self):
                return
            user, customer = require_user_customer(self)
            if not customer:
                return
            if not require_verified_account_user(self, user):
                return
            if CRYPTO_PROCESSOR_URL and CRYPTO_PROCESSOR_KEY:
                self.write_json(501, {'error': 'crypto_processor_not_implemented', 'message': 'Processor configuration is present, but this incremental build only supports manual crypto intents.'})
                return
            if not CRYPTO_PAYMENT_ADDRESS:
                self.write_json(503, {'error': 'crypto_not_configured', 'required_env': ['SAGE_ROUTER_CRYPTO_PAYMENT_ADDRESS']})
                return
            payload = read_json_body(self)
            amount = str(payload.get('amount') or '').strip() or manual_payment_amount_for_plan(payload.get('plan'))
            plan = normalize_stripe_plan(payload.get('plan'))
            intent = store_payment_intent({
                'kind': 'crypto_manual',
                'customer_id': customer.get('id'),
                'user_id': customer.get('user_id'),
                'status': 'pending_manual_review',
                'asset': payload.get('asset') or CRYPTO_PAYMENT_ASSET,
                'network': payload.get('network') or CRYPTO_PAYMENT_NETWORK,
                'amount': amount,
                'address': CRYPTO_PAYMENT_ADDRESS,
                'metadata': {
                    'settlement': 'manual',
                    'automatic_settlement': False,
                    'plan': plan,
                    'amount_source': 'request' if str(payload.get('amount') or '').strip() else ('public_plan_catalog' if amount else 'manual_review'),
                    'note': payload.get('note') or '',
                },
            })
            self.write_json(201, {'intent': public_payment_intent(intent)})
            return

        audio_kind = audio_endpoint_kind(request_path)
        model_endpoint = (
            request_path in ['/v1/responses', '/responses', '/v1/chat/completions', '/chat/completions', '/v1/messages', '/messages', '/v1/realtime', '/realtime']
            or bool(audio_kind)
            or ':generateContent' in request_path
            or ':streamGenerateContent' in request_path
        )
        auth_context = None
        if model_endpoint:
            auth_context = client_auth_context(self)
            if not auth_context:
                self.write_json(401, model_api_auth_error_payload(), extra_headers=model_api_auth_error_headers())
                return
            set_route_auth_context(auth_context)

        try:
            if request_path in ['/v1/responses', '/responses']:
                body = self.rfile.read(int(self.headers.get('Content-Length', 0)))
                request_id = uuid.uuid4().hex[:8]
                started = time.time()
                try:
                    payload = json.loads(body or b'{}')
                    handle_openai_responses(self, payload, request_id, started)
                except Exception as e:
                    logger.exception(f"[{request_id}] Responses request handling failed")
                    self.write_json(500, {"error": str(e)}, extra_headers={'X-Sage-Router-Request-Id': request_id})
            elif request_path in ['/v1/chat/completions', '/chat/completions']:
                body = self.rfile.read(int(self.headers.get('Content-Length', 0)))
                request_id = uuid.uuid4().hex[:8]
                started = time.time()
                try:
                    payload = json.loads(body or b'{}')
                    handle_openai_chat_completions(self, payload, request_id, started)
                except Exception as e:
                    logger.exception(f"[{request_id}] Request handling failed")
                    self.write_json(500, {"error": str(e)}, extra_headers={'X-Sage-Router-Request-Id': request_id})
            elif request_path in ['/v1/messages', '/messages']:
                body = self.rfile.read(int(self.headers.get('Content-Length', 0)))
                request_id = uuid.uuid4().hex[:8]
                started = time.time()
                handle_anthropic_messages(self, body, request_id, started)
            elif request_path in ['/v1/realtime', '/realtime']:
                # Ultra-low-latency realtime endpoint with aggressive streaming
                body = self.rfile.read(int(self.headers.get('Content-Length', 0)))
                request_id = uuid.uuid4().hex[:8]
                started = time.time()
                try:
                    payload = json.loads(body or b'{}')
                    # Force realtime route mode and streaming
                    payload['route'] = 'realtime'
                    payload['stream'] = True
                    handle_openai_chat_completions(self, payload, request_id, started, force_realtime=True)
                except Exception as e:
                    logger.exception(f"[{request_id}] Realtime request failed")
                    self.write_json(500, {"error": str(e)}, extra_headers={'X-Sage-Router-Request-Id': request_id})
            elif audio_kind:
                content_length = self.headers.get('Content-Length')
                if not content_length or int(content_length) <= 0:
                    self.write_json(411, {'error': 'content_length_required', 'detail': 'Audio endpoints require a valid Content-Length header'})
                    return
                body = self.rfile.read(int(content_length))
                request_id = uuid.uuid4().hex[:8]
                proxy_audio_request(self, audio_kind, body, request_id)
            elif ':generateContent' in request_path or ':streamGenerateContent' in request_path:
                # Google Generative AI compat: /v1beta/models/{model}:generateContent
                import re
                match = re.match(r'.*/models/([^:]+):(generateContent|streamGenerateContent)', request_path)
                if match:
                    body = self.rfile.read(int(self.headers.get('Content-Length', 0)))
                    request_id = uuid.uuid4().hex[:8]
                    started = time.time()
                    model_name = match.group(1)
                    want_stream = match.group(2) == 'streamGenerateContent'
                    handle_google_generate(self, body, request_id, started, model_name, want_stream)
                else:
                    self.send_response(404)
                    self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()
        finally:
            if auth_context is not None:
                clear_route_auth_context()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--port',type=int,default=8790); args = parser.parse_args()
    ensure_background_refresh_started()
    server = ThreadingHTTPServer(('0.0.0.0', args.port), Handler)
    logger.info(f"Router on :{args.port} | configured={list(PROVIDERS.keys())} | disabled={sorted(DISABLED_PROVIDERS)} disabledModels={sorted(DISABLED_MODELS)}")
    server.serve_forever()
