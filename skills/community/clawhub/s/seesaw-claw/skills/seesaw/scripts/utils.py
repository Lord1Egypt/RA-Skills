import os
import json
import subprocess
import requests
import argparse
import sys
import re

# Paths
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILLS_DIR = os.path.dirname(CURRENT_DIR)
WORKSPACE_SKILLS_DIR = os.path.dirname(SKILLS_DIR)
TAVILY_SCRIPT = os.path.join(WORKSPACE_SKILLS_DIR, "tavily-search", "scripts", "search.mjs")
CONFIG_FILE = os.path.join(os.path.dirname(CURRENT_DIR), "config.json")

# Environment Variables
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_CHANNEL_ID = os.getenv("SLACK_CHANNEL_ID")

# Default Config
DEFAULT_CONFIG = {
    "max_position_size": 100,
    "max_daily_loss": 500,
    "dry_run": False
}

def load_config():
    """Load configuration from file or use defaults."""
    config = DEFAULT_CONFIG.copy()
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                user_config = json.load(f)
                config.update(user_config)
        except Exception as e:
            print(f"Warning: Failed to load config file: {e}")
    return config

def parse_args(description):
    """Parse command line arguments including standard ones like --dry-run."""
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--dry-run", action="store_true", help="Simulate actions without executing")
    parser.add_argument("--yes", action="store_true", help="Skip confirmation prompts")
    return parser.parse_args()

def search_web(query, topic=None, days=3, max_results=5, include_images=False):
    import os
    import requests
    brave_key = os.getenv("BRAVE_API_KEY")
    if not brave_key:
        return {"text": "No recent updates found.", "images": []}
    
    headers = {"Accept": "application/json", "X-Subscription-Token": brave_key}
    if include_images:
        url = "https://api.search.brave.com/res/v1/images/search"
        params = {"q": query, "count": max_results}
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=10)
            data = resp.json()
            images = [item.get("properties", {}).get("url") for item in data.get("results", [])]
            return {"text": "", "images": [img for img in images if img]}
        except Exception as e:
            print("Image search failed:", e)
            return {"text": "", "images": []}
    else:
        url = "https://api.search.brave.com/res/v1/web/search"
        params = {"q": query, "count": max_results}
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=10)
            data = resp.json()
            text = "\n".join([f"- {r.get('title')}: {r.get('description')}" for r in data.get("web", {}).get("results", [])])
            return {"text": text, "images": []}
        except Exception as e:
            print("Web search failed:", e)
            return {"text": "Search failed.", "images": []}

def search_image(query):
    """
    Search specifically for an image URL.
    """
    # Use tavily with topic="general" (or "news" if relevant) to find images
    res = search_web(query, topic="general", max_results=5, include_images=True)
    if res["images"]:
        return res["images"][0]
    return None

def send_slack_message(text, channel=None, dry_run=False):
    """
    Send a message to Slack.
    """
    if dry_run:
        print(f"[DRY-RUN] Would send Slack message: {text}")
        return True

    token = SLACK_BOT_TOKEN
    channel = channel or SLACK_CHANNEL_ID
    
    if not token or not channel:
        print(f"Skipping Slack message (no token/channel): {text}")
        return False

    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": channel,
        "text": text
    }
    
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        if not data.get("ok"):
            print(f"Slack API Error: {data.get('error')}")
            return False
        return True
    except Exception as e:
        print(f"Failed to send Slack message: {e}")
        return False

def call_llm(messages, model="gemini-2.5-flash", temperature=0.7):
    """
    Call an LLM using Gemini API directly.
    """
    import os
    gemini_key = os.getenv("GEMINI_API_KEY")

    if not gemini_key:
        print("Skipping LLM call (no GEMINI_API_KEY)")
        return None

    # Convert messages to Gemini format
    gemini_contents = []
    for msg in messages:
        role = msg.get("role", "user")
        if role == "system":
            role = "user"
        gemini_contents.append({
            "role": role,
            "parts": [{"text": msg.get("content", "")}]
        })

    # Gemini API endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={gemini_key}"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": gemini_contents,
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": 4096
        }
    }

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=60)
        resp.raise_for_status()
        data = resp.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(f"LLM call failed: {e}")
        return None

def load_json(path):
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Failed to decode JSON from {path}")
            return {}
    return {}

def save_json(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def clean_json_block(text):
    """Clean markdown code blocks from JSON string."""
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return text.strip()
