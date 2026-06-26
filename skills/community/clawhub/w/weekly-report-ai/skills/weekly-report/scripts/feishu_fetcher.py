#!/usr/bin/env python3
"""
飞书文档/知识库更新获取脚本
"""

import argparse
import requests
from datetime import datetime


def get_feishu_docs(token: str, docs: list, since_date: str, until_date: str):
    """获取飞书文档更新"""
    since = datetime.fromisoformat(since_date)
    until = datetime.fromisoformat(until_date)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    results = {
        "docs": [],
        "wiki": []
    }
    
    for doc in docs:
        try:
            if doc.startswith("docx:"):
                # 文档
                doc_token = doc.replace("docx:", "")
                url = f"https://open.feishu.cn/open-apis/doc/v1/documents/{doc_token}"
                resp = requests.get(url, headers=headers)
                if resp.status_code == 200:
                    data = resp.json().get("data", {})
                    results["docs"].append({
                        "type": "docx",
                        "token": doc_token,
                        "title": data.get("title", "未命名文档"),
                        "url": f"https://open.feishu.cn/document/{doc_token}"
                    })
            elif doc.startswith("wiki:"):
                # 知识库
                wiki_token = doc.replace("wiki:", "")
                # 获取知识库节点
                url = f"https://open.feishu.cn/open-apis/wiki/v2/spaces/{wiki_token}/nodes"
                resp = requests.get(url, headers=headers)
                if resp.status_code == 200:
                    data = resp.json().get("data", {})
                    for node in data.get("items", []):
                        results["wiki"].append({
                            "type": "wiki",
                            "space": wiki_token,
                            "title": node.get("obj_type", "doc"),
                            "token": node.get("token"),
                            "name": node.get("name")
                        })
        except Exception as e:
            print(f"Error fetching {doc}: {e}")
    
    return results


def main():
    parser = argparse.ArgumentParser(description="获取飞书文档更新")
    parser.add_argument("--token", required=True, help="飞书Access Token")
    parser.add_argument("--docs", nargs="+", required=True, help="文档/知识库列表")
    parser.add_argument("--since", required=True, help="开始日期")
    parser.add_argument("--until", required=True, help="结束日期")
    
    args = parser.parse_args()
    
    results = get_feishu_docs(args.token, args.docs, args.since, args.until)
    import json
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
