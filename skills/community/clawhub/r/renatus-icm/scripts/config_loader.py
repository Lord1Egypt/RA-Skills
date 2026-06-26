#!/usr/bin/env python3
"""
config_loader.py

Loads renatus-icm config from config.json.
Scripts import this to get unified access to all config values.

Usage:
  from config_loader import load_config
  cfg = load_config()          # reads ./config.json first, then env, then defaults
  cfg = load_config(required=False)  # returns defaults even if file missing

Paths checked (first found wins):
  1. ./config.json              (workspace root — gitignored, your personal config)
  2. ../config.json             (one level up from scripts/)
  3. ./config.json.example      (fallback for fresh installs)

Environment variables override config file values:
  RENATUS_SUPABASE_REF, RENATUS_SUPABASE_URL, RENATUS_SUPABASE_KEY,
  RENATUS_LEAD_TOKEN, RENATUS_USERNAME, RENATUS_PASSWORD, RENATUS_EVENT_ID,
  RENATUS_SENDER, RENATUS_PROVIDER, RENATUS_TEMPLATE, RENATUS_UNSUB_URL,
  RENATUS_SITE_URL, RENATUS_REGISTRATION_URL
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any

CONFIG_FILENAME = "config.json"
EXAMPLE_FILENAME = "config.json.example"


def _find_config_file() -> Path | None:
    """Find config.json in common locations relative to this script or cwd."""
    candidates = []

    script_dir = Path(__file__).parent.resolve() if "__file__" in globals() else Path.cwd()
    candidates = [
        script_dir.parent / CONFIG_FILENAME,         # ../config.json  (from scripts/)
        script_dir.parent.parent / CONFIG_FILENAME,   # ../../config.json
        Path.cwd() / CONFIG_FILENAME,                # ./config.json   (workspace root)
        Path.cwd() / EXAMPLE_FILENAME,              # ./config.json.example fallback
        script_dir.parent / EXAMPLE_FILENAME,         # ../config.json.example
    ]

    for p in candidates:
        if p.exists() and p.is_file():
            return p
    return None


def _deep_get(d: dict, *keys, default: Any = None) -> Any:
    for k in keys:
        if isinstance(d, dict):
            d = d.get(k, default)
        else:
            return default
    return d


def _str(v: Any) -> str:
    if v is None:
        return ""
    return str(v)


def load_config(required: bool = False) -> dict:
    """
    Load merged config: file → env → defaults.
    Returns a flat(ish) dict with keys matching the expected script variable names.
    """
    # Defaults
    cfg: dict[str, Any] = {
        "supabase_ref":  "YOUR_PROJECT_REF",
        "supabase_url":   "https://YOUR_PROJECT_REF.supabase.co",
        "supabase_key":   "",
        "lead_token":     "",
        "renatus_user":   "",
        "renatus_pass":   "",
        "event_id":       "",
        "sender":         "YOUR_SENDER@gmail.com",
        "provider":       "auto",
        "template_path":   "email/commercial-core-day1.html",
        "subject":        "Free Real Estate Training",
        "unsub_url":      "https://YOUR_DOMAIN/unsubscribe.html",
        "site_url":       "https://YOUR_DOMAIN",
        "registration_url": "https://YOUR_DOMAIN/commercial/",
        "instructor_photo": "https://YOUR_INSTRUCTOR_PHOTO_URL.jpg",
        "_config_path":   None,
        "_is_example":    False,
    }

    # Load file
    config_file = _find_config_file()
    if config_file:
        try:
            raw = json.loads(config_file.read_text())
            cfg["_config_path"] = str(config_file)
            cfg["_is_example"] = config_file.name == EXAMPLE_FILENAME

            # Supabase
            supa = raw.get("supabase", {})
            cfg["supabase_ref"]  = _str(_deep_get(supa, "project_ref")) or cfg["supabase_ref"]
            cfg["supabase_url"]  = _str(_deep_get(supa, "url")) or cfg["supabase_url"]
            cfg["supabase_key"]  = _str(_deep_get(supa, "service_role_key")) or cfg["supabase_key"]
            cfg["lead_token"]    = _str(_deep_get(supa, "lead_admin_token")) or cfg["lead_token"]

            # Renatus
            ren = raw.get("renatus", {})
            cfg["renatus_user"]  = _str(_deep_get(ren, "username")) or cfg["renatus_user"]
            cfg["renatus_pass"]  = _str(_deep_get(ren, "password")) or cfg["renatus_pass"]
            cfg["event_id"]      = _str(_deep_get(ren, "event_id")) or cfg["event_id"]

            # Email
            em = raw.get("email", {})
            cfg["sender"]        = _str(_deep_get(em, "sender_account")) or cfg["sender"]
            cfg["provider"]       = _str(_deep_get(em, "provider")) or cfg["provider"]
            cfg["template_path"]  = _str(_deep_get(em, "template_path")) or cfg["template_path"]
            cfg["subject"]        = _str(_deep_get(em, "subject")) or cfg["subject"]
            cfg["unsub_url"]      = _str(_deep_get(em, "unsub_base_url")) or cfg["unsub_url"]

            # Domains
            dom = raw.get("domains", {})
            cfg["site_url"]        = _str(_deep_get(dom, "site_url")) or cfg["site_url"]
            cfg["registration_url"] = _str(_deep_get(dom, "registration_page")) or cfg["registration_url"]
            cfg["instructor_photo"] = _str(_deep_get(dom, "instructor_photo_url")) or cfg["instructor_photo"]

        except (json.JSONDecodeError, OSError) as e:
            if required:
                print(f"Warning: Could not parse config file {config_file}: {e}", file=sys.stderr)
            # Fall through to env overrides
    elif required:
        print(f"Warning: No config.json found. Run: cp config.json.example config.json", file=sys.stderr)

    # Env var overrides (always win if set)
    env_overrides = {
        "supabase_ref":  "RENATUS_SUPABASE_REF",
        "supabase_url":  "RENATUS_SUPABASE_URL",
        "supabase_key":  "RENATUS_SUPABASE_KEY",
        "lead_token":    "RENATUS_LEAD_TOKEN",
        "renatus_user":  "RENATUS_USERNAME",
        "renatus_pass":  "RENATUS_PASSWORD",
        "event_id":      "RENATUS_EVENT_ID",
        "sender":        "RENATUS_SENDER",
        "provider":      "RENATUS_PROVIDER",
        "template_path": "RENATUS_TEMPLATE",
        "unsub_url":     "RENATUS_UNSUB_URL",
        "site_url":      "RENATUS_SITE_URL",
        "registration_url": "RENATUS_REGISTRATION_URL",
    }
    for key, env_var in env_overrides.items():
        val = os.environ.get(env_var)
        if val is not None:
            cfg[key] = val

    return cfg


def example_config() -> str:
    """Return the path to config.json.example if found."""
    f = _find_config_file()
    return str(f) if f else "(not found)"

def get_events() -> list[dict]:
    """
    Return the events list from config.
    Each event: {id, name, renatus_url, registration_url, landing_page_path, ...}
    
    Reads the raw JSON directly (not from load_config() flat map) so that
    scripts can access events without needing individual env vars for each one.
    """
    config_file = _find_config_file()
    if config_file:
        try:
            raw = json.loads(config_file.read_text())
            return raw.get("events", [])
        except (json.JSONDecodeError, OSError):
            return []
    return []


def get_event_by_id(event_id: str) -> dict | None:
    """Find an event by its ID in config."""
    for ev in get_events():
        if ev.get("id") == event_id:
            return ev
    return None


def active_events() -> list[dict]:
    """Return only events where active == True."""
    return [e for e in get_events() if e.get("active", True)]
