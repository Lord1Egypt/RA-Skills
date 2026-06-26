#!/usr/bin/env python3
"""Manage comments on memos in UseMemos.

Subcommands:
    list   <memo_id>                         List comments on a memo
    add    <memo_id> <content> [visibility]   Add a comment to a memo
    delete <comment_id>                       Delete a comment
"""
import os
import sys
import json
import urllib.request
import urllib.error
import urllib.parse

# Auto-load .env from skill directory
import load_env


def strip_memo_prefix(memo_id):
    """Strip 'memos/' prefix if the full resource name was passed."""
    if memo_id.startswith('memos/'):
        return memo_id[len('memos/'):]
    return memo_id


def api_request(base_url, token, path, method='GET', data=None):
    body = json.dumps(data).encode() if data else None
    req = urllib.request.Request(
        f"{base_url}{path}",
        data=body,
        headers={
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        method=method,
    )
    with urllib.request.urlopen(req) as resp:
        raw = resp.read().decode()
        return json.loads(raw) if raw else {}


def list_comments(base_url, token, memo_id):
    memo_id = strip_memo_prefix(memo_id)
    safe_id = urllib.parse.quote(memo_id, safe='')
    data = api_request(base_url, token, f"/api/v1/memos/{safe_id}/comments")
    comments = data.get('memos', [])
    if not comments:
        print("No comments")
        return
    for c in comments:
        cid = c['name'].split('/')[-1]
        creator = c.get('creator', '?')
        time = c.get('createTime', '?')
        snippet = c['content'][:120].replace('\n', ' ')
        print(f"[{cid}] {time} by {creator}")
        print(f"  {snippet}")


def add_comment(base_url, token, memo_id, content, visibility='PRIVATE'):
    memo_id = strip_memo_prefix(memo_id)
    safe_id = urllib.parse.quote(memo_id, safe='')
    result = api_request(
        base_url, token,
        f"/api/v1/memos/{safe_id}/comments",
        method='POST',
        data={
            'content': content,
            'visibility': visibility,
        },
    )
    comment_id = result['name'].split('/')[-1]
    print(f"Comment [{comment_id}] added to memo [{memo_id}]")


def delete_comment(base_url, token, comment_id):
    comment_id = strip_memo_prefix(comment_id)
    safe_id = urllib.parse.quote(comment_id, safe='')
    api_request(base_url, token, f"/api/v1/memos/{safe_id}", method='DELETE')
    print(f"Deleted comment [{comment_id}]")


def main():
    base_url = os.environ.get('USEMEMOS_URL', '').rstrip('/')
    token = os.environ.get('USEMEMOS_TOKEN', '')

    if not base_url or not token:
        print("Error: USEMEMOS_URL and USEMEMOS_TOKEN must be set", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: memo_comments.py <list|add|delete> [args...]", file=sys.stderr)
        print("  list   <memo_id>                        List comments on a memo", file=sys.stderr)
        print("  add    <memo_id> <content> [visibility]  Add a comment to a memo", file=sys.stderr)
        print("  delete <comment_id>                      Delete a comment", file=sys.stderr)
        sys.exit(1)

    action = sys.argv[1]

    try:
        if action == 'list':
            if len(sys.argv) < 3:
                print("Usage: memo_comments.py list <memo_id>", file=sys.stderr)
                sys.exit(1)
            list_comments(base_url, token, sys.argv[2])

        elif action == 'add':
            if len(sys.argv) < 4:
                print("Usage: memo_comments.py add <memo_id> <content> [visibility]", file=sys.stderr)
                sys.exit(1)
            visibility = sys.argv[4] if len(sys.argv) > 4 else 'PRIVATE'
            add_comment(base_url, token, sys.argv[2], sys.argv[3], visibility)

        elif action == 'delete':
            if len(sys.argv) < 3:
                print("Usage: memo_comments.py delete <comment_id>", file=sys.stderr)
                sys.exit(1)
            delete_comment(base_url, token, sys.argv[2])

        else:
            print(f"Unknown action: {action}", file=sys.stderr)
            print("Use: list, add, or delete", file=sys.stderr)
            sys.exit(1)

    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.read().decode()}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
