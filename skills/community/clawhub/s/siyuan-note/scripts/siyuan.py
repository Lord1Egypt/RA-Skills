#!/usr/bin/env python3
"""
思源笔记 API 辅助脚本
用法: python siyuan.py <命令> [参数]

依赖: pip install requests

示例:
  python siyuan.py list-notebooks
  python siyuan.py create-doc <notebook> <path> <markdown>
  python siyuan.py search <keyword>
  python siyuan.py sql "SELECT * FROM blocks LIMIT 5"
"""

import json
import sys
import os

try:
    import requests
except ImportError:
    print("需要安装 requests: pip install requests")
    sys.exit(1)

BASE_URL = "http://127.0.0.1:6806"
TOKEN = os.environ.get("SIYUAN_TOKEN", "")


def headers():
    h = {"Content-Type": "application/json"}
    if TOKEN:
        h["Authorization"] = f"Token {TOKEN}"
    return h


def post(endpoint, data=None):
    r = requests.post(f"{BASE_URL}{endpoint}", json=data or {}, headers=headers(), timeout=10)
    r.raise_for_status()
    resp = r.json()
    if resp.get("code") != 0:
        raise Exception(f"API 错误 {resp.get('code')}: {resp.get('msg')}")
    return resp.get("data")


def list_notebooks():
    """列出所有笔记本"""
    data = post("/api/notebook/lsNotebooks")
    print(json.dumps(data, indent=2, ensure_ascii=False))


def create_doc(notebook, path, markdown):
    """通过 Markdown 创建文档"""
    doc_id = post("/api/filetree/createDocWithMd", {
        "notebook": notebook,
        "path": path,
        "markdown": markdown
    })
    print(f"文档创建成功，ID: {doc_id}")
    return doc_id


def search(keyword, limit=20):
    """全文搜索"""
    results = post("/api/query/sql", {
        "stmt": f"SELECT id, hpath, content FROM blocks WHERE content LIKE '%{keyword}%' LIMIT {limit}"
    })
    print(json.dumps(results, indent=2, ensure_ascii=False))
    return results


def search_titles(keyword, limit=20):
    """搜索文档标题"""
    results = post("/api/query/sql", {
        "stmt": f"SELECT id, hpath, title FROM blocks WHERE type = 'd' AND title LIKE '%{keyword}%' LIMIT {limit}"
    })
    print(json.dumps(results, indent=2, ensure_ascii=False))
    return results


def list_docs(notebook):
    """列出笔记本下所有文档"""
    results = post("/api/query/sql", {
        "stmt": f"SELECT id, title, hpath FROM blocks WHERE notebook = '{notebook}' AND type = 'd'"
    })
    print(json.dumps(results, indent=2, ensure_ascii=False))
    return results


def append_block(parent_id, data, data_type="markdown"):
    """向块追加子块"""
    result = post("/api/block/appendBlock", {
        "data": data,
        "dataType": data_type,
        "parentID": parent_id
    })
    block_id = result[0]["doOperations"][0]["id"]
    print(f"块插入成功，ID: {block_id}")
    return block_id


def update_block(block_id, data, data_type="markdown"):
    """更新块内容"""
    post("/api/block/updateBlock", {
        "dataType": data_type,
        "data": data,
        "id": block_id
    })
    print(f"块 {block_id} 更新成功")


def delete_block(block_id):
    """删除块"""
    post("/api/block/deleteBlock", {"id": block_id})
    print(f"块 {block_id} 删除成功")


def export_md(doc_id):
    """导出文档为 Markdown"""
    result = post("/api/export/exportMdContent", {"id": doc_id})
    print(f"路径: {result['hPath']}")
    print(f"---\n{result['content']}")
    return result


def run_sql(stmt):
    """执行 SQL 查询"""
    results = post("/api/query/sql", {"stmt": stmt})
    print(json.dumps(results, indent=2, ensure_ascii=False))
    return results


def get_version():
    """获取系统版本"""
    version = post("/api/system/version")
    print(f"思源笔记版本: {version}")


def render_sprig(template):
    """渲染 Sprig 模板"""
    result = post("/api/template/renderSprig", {"template": template})
    print(result)
    return result


def push_notification(msg, timeout=7000):
    """推送通知"""
    result = post("/api/notification/pushMsg", {"msg": msg, "timeout": timeout})
    print(f"通知已推送，ID: {result['id']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1].replace("-", "_")

    if not TOKEN:
        print("警告: 未设置 SIYUAN_TOKEN 环境变量，部分 API 可能无法调用")

    try:
        if cmd == "list_notebooks":
            list_notebooks()
        elif cmd == "create_doc" and len(sys.argv) >= 5:
            notebook, path, markdown = sys.argv[2], sys.argv[3], sys.argv[4]
            create_doc(notebook, path, markdown)
        elif cmd == "search" and len(sys.argv) >= 3:
            search(sys.argv[2])
        elif cmd == "search_titles" and len(sys.argv) >= 3:
            search_titles(sys.argv[2])
        elif cmd == "list_docs" and len(sys.argv) >= 3:
            list_docs(sys.argv[2])
        elif cmd == "append_block" and len(sys.argv) >= 4:
            append_block(sys.argv[2], sys.argv[3])
        elif cmd == "update_block" and len(sys.argv) >= 4:
            update_block(sys.argv[2], sys.argv[3])
        elif cmd == "delete_block" and len(sys.argv) >= 3:
            delete_block(sys.argv[2])
        elif cmd == "export_md" and len(sys.argv) >= 3:
            export_md(sys.argv[2])
        elif cmd == "sql" and len(sys.argv) >= 3:
            run_sql(sys.argv[2])
        elif cmd == "version":
            get_version()
        elif cmd == "render_sprig" and len(sys.argv) >= 3:
            render_sprig(sys.argv[2])
        elif cmd == "push_notification" and len(sys.argv) >= 3:
            push_notification(sys.argv[2])
        else:
            print("未知命令或参数不足")
            print(__doc__)
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
