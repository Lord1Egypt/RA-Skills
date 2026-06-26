#!/usr/bin/env python3
"""
飞书 Wiki 知识库工具
用法:
  python3 wiki.py spaces                      # 列出知识库
  python3 wiki.py nodes <space_id>             # 列出节点
  python3 wiki.py create <space_id> <parent_node> <title> <content>
"""
import os
import sys
import json
import time
import urllib.request
import argparse

APP_ID = os.environ.get("LARK_APP_ID", "")
APP_SECRET = os.environ.get("LARK_APP_SECRET", "")
SPACE_ID = os.environ.get("LARK_SPACE_ID", "")

_cache = {'token': None, 'exp': 0}

def get_token():
    if _cache['token'] and time.time() < _cache['exp']:
        return _cache['token']
    
    url = "https://open.larksuite.com/open-apis/auth/v3/tenant_access_token/internal"
    data = json.dumps({"app_id": APP_ID, "app_secret": APP_SECRET}).encode()
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    with urllib.request.urlopen(req, timeout=10) as resp:
        result = json.loads(resp.read())
        _cache['token'] = result['tenant_access_token']
        _cache['exp'] = time.time() + result.get('expire', 7200) - 300
        return _cache['token']

def api(method, url, body=None):
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            'Authorization': f'Bearer {get_token()}',
            'Content-Type': 'application/json'
        }
    )
    return json.loads(urllib.request.urlopen(req, timeout=15).read())

def list_spaces():
    url = "https://open.larksuite.com/open-apis/wiki/v2/spaces"
    return api("GET", url)

def list_nodes(space_id):
    url = f"https://open.larksuite.com/open-apis/wiki/v2/spaces/{space_id}/nodes"
    return api("GET", url)

def create_doc(space_id, parent_node_id, title):
    url = "https://open.larksuite.com/open-apis/docx/v1/documents"
    data = {
        "document_request": {
            "node_type": "docx",
            "parent_node_id": parent_node_id,
            "space_id": space_id,
            "title": title
        }
    }
    return api("POST", url, data)

def write_content(doc_token, content):
    url = f"https://open.larksuite.com/open-apis/docx/v1/documents/{doc_token}/blocks"
    blocks = []
    for line in content.split('\n'):
        if line.strip():
            blocks.append({
                "block_type": "paragraph",
                "paragraph": {
                    "elements": [{
                        "text_element": {"content": line, "type": "text"}
                    }]
                }
            })
    return api("POST", url, {"blocks": blocks})

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='cmd')
    
    sub.add_parser('spaces')
    n = sub.add_parser('nodes')
    n.add_argument('space_id', nargs='?', default=SPACE_ID)
    c = sub.add_parser('create')
    c.add_argument('space_id', nargs='?', default=SPACE_ID)
    c.add_argument('parent_node')
    c.add_argument('title')
    c.add_argument('content', nargs='*')
    
    args = parser.parse_args()
    
    if args.cmd == 'spaces':
        result = list_spaces()
        items = result.get('data', {}).get('items', [])
        for s in items:
            print(f"{s.get('name')}: {s.get('space_id')}")
    
    elif args.cmd == 'nodes':
        result = list_nodes(args.space_id)
        items = result.get('data', {}).get('items', [])
        for n in items:
            print(f"{n.get('node_token')}: {n.get('title')}")
    
    elif args.cmd == 'create':
        title = args.title
        content = ' '.join(args.content)
        result = create_doc(args.space_id, args.parent_node, title)
        doc_token = result['data']['document']['token']
        write_content(doc_token, content)
        print(f"文档创建成功: {doc_token}")

if __name__ == '__main__':
    main()
