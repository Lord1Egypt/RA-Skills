#!/usr/bin/env python3
"""
WotoHub API Configuration

All API base URLs live here.
Default to the production gateway unless `WOTOHUB_BASE_URL` explicitly overrides it.
"""
import os
from pathlib import Path

# ── Cache TTL ────────────────────────────────────────────────────────────────
CACHE_TTL_SECONDS: int = 300   # 5-minute cache TTL for search results

# Recommendation scoring limits
RECOMMENDATION_MAX_ITEMS: int = 30  # score at most top-N raw creators for speed

# ── Base URLs ─────────────────────────────────────────────────────────────────
DEFAULT_BASE_URL = "https://api.wotohub.com/api-gateway"
BASE_URL = os.environ.get("WOTOHUB_BASE_URL") or DEFAULT_BASE_URL

# ── Sourceapp ─────────────────────────────────────────────────────────────────
DEFAULT_SOURCEAPP = os.environ.get("WOTOHUB_SOURCEAPP", "hub")

# ── API key policy ───────────────────────────────────────────────────────────
# Publishing-safe: never hardcode a real default token in the skill.
# Priority: CLI --token > env WOTOHUB_API_KEY > saved settings
DEFAULT_API_KEY = None

# ── Internal: path helpers (keep in sync with API docs) ───────────────────────
OPEN_SEARCH_PATH         = "/search/openSearch"
CLAW_SEARCH_PATH         = "/search/clawSearch"
SEND_EMAIL_PATH          = "/email/writeMultipleEmailClaw"
INBOX_LIST_PATH          = "/email/selInboxClaw"
EMAIL_DETAIL_PATH        = "/email/inboxDetailClaw/{id}"
INBOX_DIALOGUE_PATH      = "/email/inboxDialogueClaw"

# ── Resolved paths (relative — compatible with common.request_json) ───────────
def open_search_path()     -> str: return OPEN_SEARCH_PATH
def claw_search_path()     -> str: return CLAW_SEARCH_PATH
def send_email_path()      -> str: return SEND_EMAIL_PATH
def inbox_list_path()      -> str: return INBOX_LIST_PATH
def email_detail_path()         -> str: return EMAIL_DETAIL_PATH
def inbox_dialogue_path()       -> str: return INBOX_DIALOGUE_PATH
