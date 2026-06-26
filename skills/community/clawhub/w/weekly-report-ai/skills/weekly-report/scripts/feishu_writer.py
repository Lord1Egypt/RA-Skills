#!/usr/bin/env python3
"""
飞书文档写入脚本
将周报写入飞书文档
"""

import argparse
import requests
from datetime import datetime


def create_doc(token: str, title: str, content: str) -> dict:
    """创建飞书文档"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    url = "https://open.feishu.cn/open-apis/doc/v1/documents"
    
    # 构建文档块
    blocks = [
        {
            "block_type": 1,  # paragraph
            "paragraph": {
                "style": {"bold": True, "font_size": 20},
                "elements": [
                    {
                        "element_type": "text",
                        "text": {"content": title, "link": None}
                    }
                ]
            }
        }
    ]
    
    # 按行解析Markdown内容
    for line in content.split('\n'):
        if not line.strip():
            continue
            
        # 解析标题
        if line.startswith('# '):
            blocks.append({
                "block_type": 1,
                "paragraph": {
                    "style": {"bold": True, "font_size": 18},
                    "elements": [{
                        "element_type": "text",
                        "text": {"content": line[2:]}
                    }]
                }
            })
        elif line.startswith('## '):
            blocks.append({
                "block_type": 1,
                "paragraph": {
                    "style": {"bold": True, "font_size": 16},
                    "elements": [{
                        "element_type": "text",
                        "text": {"content": line[3:]}
                    }]
                }
            })
        elif line.startswith('### '):
            blocks.append({
                "block_type": 1,
                "paragraph": {
                    "style": {"bold": True, "font_size": 14},
                    "elements": [{
                        "element_type": "text",
                        "text": {"content": line[4:]}
                    }]
                }
            })
        elif line.startswith('- '):
            blocks.append({
                "block_type": 2,  # bullet
                "paragraph": {
                    "elements": [{
                        "element_type": "text",
                        "text": {"content": line[2:]}
                    }]
                }
            })
        else:
            # 普通段落
            blocks.append({
                "block_type": 1,
                "paragraph": {
                    "elements": [{
                        "element_type": "text",
                        "text": {"content": line}
                    }]
                }
            })
    
    data = {
        "document_id": "",
        "parent_id": "",
        "node_type": "origin",
        "title": title,
        "blocks": blocks
    }
    
    resp = requests.post(url, headers=headers, json=data)
    
    if resp.status_code == 200:
        result = resp.json()
        doc_token = result.get("data", {}).get("document_id")
        return {
            "success": True,
            "document_id": doc_token,
            "url": f"https://open.feishu.cn/document/{doc_token}"
        }
    else:
        return {
            "success": False,
            "error": resp.text
        }


def append_content(token: str, document_id: str, content: str) -> dict:
    """向已有文档追加内容"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    url = f"https://open.feishu.cn/open-apis/doc/v1/documents/{document_id}/blocks"
    
    # 构建块
    blocks = []
    for line in content.split('\n'):
        if not line.strip():
            continue
            
        if line.startswith('# '):
            blocks.append({
                "block_type": 1,
                "paragraph": {
                    "style": {"bold": True, "font_size": 20},
                    "elements": [{"element_type": "text", "text": {"content": line[2:]}}]
                }
            })
        elif line.startswith('## '):
            blocks.append({
                "block_type": 1,
                "paragraph": {
                    "style": {"bold": True, "font_size": 16},
                    "elements": [{"element_type": "text", "text": {"content": line[3:]}}]
                }
            })
        elif line.startswith('- '):
            blocks.append({
                "block_type": 2,
                "paragraph": {
                    "elements": [{"element_type": "text", "text": {"content": line[2:]}}]
                }
            })
        else:
            blocks.append({
                "block_type": 1,
                "paragraph": {
                    "elements": [{"element_type": "text", "text": {"content": line}}]
                }
            })
    
    data = {"children": blocks}
    resp = requests.post(url, headers=headers, json=data)
    
    return {"success": resp.status_code == 200, "response": resp.text}


def main():
    parser = argparse.ArgumentParser(description="写入飞书文档")
    parser.add_argument("--token", required=True, help="飞书Access Token")
    parser.add_argument("--title", required=True, help="文档标题")
    parser.add_argument("--content", required=True, help="文档内容 (Markdown)")
    parser.add_argument("--doc-id", help="已有文档ID（追加模式）")
    
    args = parser.parse_args()
    
    if args.doc_id:
        result = append_content(args.token, args.doc_id, args.content)
    else:
        result = create_doc(args.token, args.title, args.content)
    
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
