#!/usr/bin/env python3
"""
teams-delegate core CLI

Usage:
  python3 teams.py whoami          # Get your user ID (run this first)
  python3 teams.py inbox           # List recent chats
  python3 teams.py read <chatId>   # Show messages in a chat
  python3 teams.py reply <chatId> "message"
  python3 teams.py summary         # AI-ready summary of all chats
"""

import json, re, sys, urllib.request, urllib.parse, urllib.error
from datetime import datetime

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from auth import get_token, GRAPH_BASE

CONFIG_DIR = __file__.rsplit("/", 2)[0]

def graph_get(path, token):
    url = f"{GRAPH_BASE}{path}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    })
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"Graph API error {e.code} on {path}:", file=sys.stderr)
        try:
            err = json.loads(body)
            print(f"  {err.get('error', {}).get('code')}: {err.get('error', {}).get('message')}", file=sys.stderr)
        except:
            print(f"  {body[:300]}", file=sys.stderr)
        sys.exit(1)

def graph_post(path, token, payload):
    url = f"{GRAPH_BASE}{path}"
    req = urllib.request.Request(url,
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {token}",
                 "Content-Type": "application/json",
                 "Accept": "application/json"},
        method="POST")
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def strip_html(text):
    return re.sub(r"<[^<]+?>", "", text or "").strip()

def fmt_time(iso):
    try:
        dt = datetime.fromisoformat(iso.replace("Z", "+00:00"))
        return dt.astimezone().strftime("%m/%d %I:%M %p")
    except:
        return iso

def get_user_id(token):
    # For app-only tokens, list users and pick first
    # For delegated tokens, use /me
    try:
        me = graph_get("/me", token)
        return me["id"], me.get("displayName", "You")
    except SystemExit:
        # App-only token — need to list users
        users = graph_get("/users?$top=5", token)
        if not users.get("value"):
            print("No users found. Make sure User.Read.All permission is granted.", file=sys.stderr)
            sys.exit(1)
        print("\nAvailable users (app-only mode):")
        for i, u in enumerate(users["value"]):
            print(f"  {i+1}. {u.get('displayName')} — {u.get('mail') or u.get('userPrincipalName')} (id: {u['id']})")
        choice = input("\nWhich user? Enter number: ").strip()
        user = users["value"][int(choice)-1]
        return user["id"], user.get("displayName", "User")

def get_chats(user_id, token):
    return graph_get(f"/users/{user_id}/chats?$expand=lastMessagePreview&$top=20", token).get("value", [])

def get_messages(user_id, chat_id, token, top=10):
    return graph_get(f"/users/{user_id}/chats/{chat_id}/messages?$top={top}", token).get("value", [])

def send_reply(user_id, chat_id, message, token):
    return graph_post(f"/users/{user_id}/chats/{chat_id}/messages", token,
                      {"body": {"contentType": "text", "content": message}})

def cmd_whoami(token):
    uid, name = get_user_id(token)
    print(f"User: {name}\nID:   {uid}")

def cmd_inbox(token):
    uid, name = get_user_id(token)
    chats = get_chats(uid, token)
    if not chats:
        print("No recent chats."); return
    print(f"\nInbox for {name}\n{'─'*80}")
    for c in chats:
        chat_id   = c["id"]
        chat_type = c.get("chatType", "?")
        preview   = c.get("lastMessagePreview", {})
        sender    = preview.get("from", {}).get("user", {}).get("displayName", "?")
        content   = strip_html(preview.get("body", {}).get("content", ""))[:50]
        t         = fmt_time(preview.get("createdDateTime", ""))
        print(f"[{t}] {chat_type:<10} {sender}: {content}")
        print(f"  ID: {chat_id}\n")

def cmd_read(chat_id, token):
    uid, _ = get_user_id(token)
    msgs = get_messages(uid, chat_id, token)
    msgs.reverse()
    print(f"\nChat: {chat_id}\n{'='*60}")
    for m in msgs:
        sender  = m.get("from", {}).get("user", {}).get("displayName", "?")
        content = strip_html(m.get("body", {}).get("content", ""))
        t       = fmt_time(m.get("createdDateTime", ""))
        flag    = " [URGENT]" if m.get("importance") == "urgent" else ""
        print(f"\n[{t}]{flag} {sender}:\n  {content}")

def cmd_summary(token):
    uid, name = get_user_id(token)
    chats = get_chats(uid, token)
    print(f"\n=== TEAMS INBOX SUMMARY — {name} ===\n")
    for c in chats[:10]:
        preview = c.get("lastMessagePreview", {})
        sender  = preview.get("from", {}).get("user", {}).get("displayName", "?")
        content = strip_html(preview.get("body", {}).get("content", ""))
        t       = fmt_time(preview.get("createdDateTime", ""))
        imp     = preview.get("importance", "normal")
        print(f"CHAT_ID: {c['id']}")
        print(f"  Type: {c.get('chatType')} | From: {sender} | Time: {t} | Importance: {imp}")
        print(f"  Preview: {content[:120]}\n")

def cmd_reply(chat_id, message, token):
    uid, _ = get_user_id(token)
    result = send_reply(uid, chat_id, message, token)
    print(f"Reply sent (id: {result.get('id')})")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    token = get_token()
    cmd   = sys.argv[1]
    if   cmd == "whoami":                          cmd_whoami(token)
    elif cmd == "inbox":                           cmd_inbox(token)
    elif cmd == "read"   and len(sys.argv) >= 3:  cmd_read(sys.argv[2], token)
    elif cmd == "reply"  and len(sys.argv) >= 4:  cmd_reply(sys.argv[2], sys.argv[3], token)
    elif cmd == "summary":                         cmd_summary(token)
    else: print(__doc__); sys.exit(1)
