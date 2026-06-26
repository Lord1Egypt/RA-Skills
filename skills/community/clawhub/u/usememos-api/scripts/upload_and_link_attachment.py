#!/usr/bin/env python3
"""Upload an attachment and link it to an existing memo in UseMemos."""
import os
import sys
import json
import base64
import urllib.request
import urllib.error
import urllib.parse

# Auto-load .env from skill directory
import load_env

def main():
    base_url = os.environ.get('USEMEMOS_URL', '').rstrip('/')
    token = os.environ.get('USEMEMOS_TOKEN', '')

    if not base_url or not token:
        print("Error: USEMEMOS_URL and USEMEMOS_TOKEN must be set", file=sys.stderr)
        sys.exit(1)

    if len(sys.argv) < 3:
        print("Usage: upload_and_link_attachment.py <memo_id> <filepath> [filename] [type]", file=sys.stderr)
        sys.exit(1)

    raw_memo_id = sys.argv[1]
    # Strip 'memos/' prefix if the full resource name was passed
    if raw_memo_id.startswith('memos/'):
        raw_memo_id = raw_memo_id[len('memos/'):]
    memo_id = urllib.parse.quote(raw_memo_id, safe='')
    filepath = sys.argv[2]
    filename = sys.argv[3] if len(sys.argv) > 3 else os.path.basename(filepath)
    filetype = sys.argv[4] if len(sys.argv) > 4 else 'image/jpeg'

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    # Step 1: Upload attachment
    with open(filepath, 'rb') as f:
        raw = f.read()

    encoded = base64.b64encode(raw).decode('utf-8')

    upload_payload = json.dumps({
        'filename': filename,
        'content': encoded,
        'type': filetype
    }).encode()

    req = urllib.request.Request(
        f"{base_url}/api/v1/attachments",
        data=upload_payload,
        headers=headers,
        method='POST'
    )

    try:
        with urllib.request.urlopen(req) as resp:
            attachment = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Upload failed: {e.code} - {e.read().decode()}", file=sys.stderr)
        sys.exit(1)

    attachment_name = attachment['name']
    attachment_size = int(attachment.get('size', 0))
    print(f"Uploaded [{attachment_name}] ({attachment_size} bytes)")

    if attachment_size == 0:
        print(f"Error: attachment uploaded with size 0 — file may be empty or upload failed", file=sys.stderr)
        sys.exit(1)

    # Step 2: Get existing memo to preserve current attachments
    get_req = urllib.request.Request(
        f"{base_url}/api/v1/memos/{memo_id}",
        headers=headers,
        method='GET'
    )

    try:
        with urllib.request.urlopen(get_req) as resp:
            memo_data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Failed to get memo: {e.code} - {e.read().decode()}", file=sys.stderr)
        print(f"Attachment was uploaded as {attachment_name} but not linked.", file=sys.stderr)
        sys.exit(1)

    # Step 3: Append new attachment to existing list
    existing_attachments = memo_data.get('attachments', [])
    existing_attachments.append({
        'name': attachment_name,
        'filename': filename,
        'type': filetype
    })

    link_payload = json.dumps({
        'attachments': existing_attachments
    }).encode()

    req = urllib.request.Request(
        f"{base_url}/api/v1/memos/{memo_id}",
        data=link_payload,
        headers=headers,
        method='PATCH'
    )

    try:
        with urllib.request.urlopen(req) as resp:
            json.loads(resp.read().decode())
            print(f"Linked to memo [{memo_id}]")
    except urllib.error.HTTPError as e:
        print(f"Link failed: {e.code} - {e.read().decode()}", file=sys.stderr)
        print(f"Attachment was uploaded as {attachment_name} but not linked.", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
