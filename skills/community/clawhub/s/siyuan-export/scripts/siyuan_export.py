#!/usr/bin/env python3
"""
思源笔记文档导出工具（Word）

通过思源笔记 API 将文档导出为 Word(.docx) 格式。
支持单文档导出和批量导出子文档，返回结构化 JSON 输出。

配置（优先级：环境变量 > config.json > config.example.json）:
    环境变量:
        SIYUAN_BASE_URL   - 思源笔记地址（默认 http://127.0.0.1:6806）
        SIYUAN_TOKEN      - API Token
    配置文件: config.json 或 config.example.json
    Token 获取: 思源笔记 → 设置 → 关于 → 复制 Token

用法:
    # 按文档名搜索导出（1个匹配自动执行）
    python siyuan_export.py -s "关键词" -o C:/Desktop

    # 搜索+批量子文档
    python siyuan_export.py -s "关键词" -c -o C:/Desktop

    # 单文档导出
    python siyuan_export.py --doc-id <id> --output <dir>

    # 导出文档下所有子文档
    python siyuan_export.py --doc-id <id> -c --output C:/Desktop/Midjourney

多匹配时: 返回文档列表 JSON，不阻塞等待输入。
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError


def format_time(ts) -> str:
    """思源时间格式 yyyymmddhhmmss 转为 年-月-日 时:分:秒"""
    if not ts:
        return ""
    try:
        ts = str(ts)
        if len(ts) == 14:
            return f"{ts[:4]}-{ts[4:6]}-{ts[6:8]} {ts[8:10]}:{ts[10:12]}:{ts[12:14]}"
        elif len(ts) == 13:
            # 毫秒时间戳
            return datetime.fromtimestamp(int(ts) / 1000).strftime("%Y-%m-%d %H:%M:%S")
        return ts
    except Exception:
        return str(ts)


def get_config():
    """获取配置（优先级：环境变量 > config.json > config.example.json）

    环境变量:
        SIYUAN_BASE_URL   - 思源笔记地址（默认 http://127.0.0.1:6806）
        SIYUAN_TOKEN      - API Token
        SIYUAN_TIMEOUT    - 超时时间 ms（默认 30000）

    配置文件字段: baseURL, token, timeout
    """
    base_url = os.environ.get("SIYUAN_BASE_URL", "http://127.0.0.1:6806")
    token = os.environ.get("SIYUAN_TOKEN", "")
    timeout = int(os.environ.get("SIYUAN_TIMEOUT", "10000"))

    skill_dir = Path(__file__).parent.parent
    config_paths = [
        skill_dir / "config.json",
        skill_dir / "config.example.json",
    ]

    for cp in config_paths:
        if cp.exists():
            try:
                with open(cp, "r", encoding="utf-8") as f:
                    cfg = json.load(f)
                if not token and cfg.get("token"):
                    token = cfg["token"]
                if cfg.get("baseURL"):
                    base_url = cfg["baseURL"]
                if cfg.get("timeout"):
                    timeout = cfg["timeout"]
            except Exception:
                pass

    return {"base_url": base_url, "token": token, "timeout": timeout}


def api_call(endpoint: str, data: dict, config: dict) -> dict:
    """调用思源 API"""
    url = f"{config['base_url']}{endpoint}"
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    req = Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Token {config['token']}",
        },
        method="POST",
    )
    try:
        timeout_sec = int(config.get("timeout", 30000)) / 1000
        with urlopen(req, timeout=timeout_sec) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        return {"code": e.code, "msg": str(e)}
    except URLError as e:
        return {"code": -1, "msg": str(e)}


def search_docs(keyword: str, config: dict) -> list[dict]:
    """按文档名搜索"""
    stmt = f"SELECT id, content, hpath, created, updated FROM blocks WHERE content LIKE '%{keyword}%' AND type = 'd' ORDER BY updated DESC LIMIT 20"
    result = api_call("/api/query/sql", {"stmt": stmt}, config)
    if result.get("code") == 0:
        return result.get("data", [])
    return []


def get_child_docs(doc_id: str, config: dict) -> list[dict]:
    """获取子文档列表"""
    doc_info = api_call("/api/query/sql", {"stmt": f"SELECT hpath FROM blocks WHERE id = '{doc_id}' AND type = 'd'"}, config)
    if doc_info.get("code") != 0 or not doc_info.get("data"):
        return []
    parent_hpath = doc_info["data"][0]["hpath"]
    escaped_hpath = parent_hpath.replace("'", "''")
    result = api_call("/api/query/sql", {"stmt": f"SELECT id, content FROM blocks WHERE hpath LIKE '{escaped_hpath}/%' AND type = 'd' ORDER BY hpath"}, config)
    return result.get("data", []) if result.get("code") == 0 else []


def export_docx(doc_id: str, output: str, config: dict) -> dict:
    """导出文档为 Word 格式"""
    save_dir = Path(output)
    save_dir.mkdir(parents=True, exist_ok=True)
    save_path = str(save_dir).replace("\\", "/")

    result = api_call("/api/export/exportDocx", {"id": doc_id, "savePath": save_path, "removeAssets": True}, config)

    if result.get("code") != 0:
        return {"success": False, "error": "api_error", "message": result.get("msg", "")}

    api_path = result.get("data", {}).get("path", "")
    if not api_path:
        return {"success": False, "error": "no_path_returned", "message": "API 未返回文件路径"}

    final_path = Path(api_path)
    file_size = final_path.stat().st_size if final_path.exists() else 0

    return {
        "success": True,
        "data": {
            "path": str(final_path),
            "size_bytes": file_size,
            "size_kb": round(file_size / 1024, 1),
        },
    }


def resolve_doc_id(path_or_id: str, config: dict) -> str | None:
    """将路径转换为文档 ID"""
    if not path_or_id:
        return None
    if len(path_or_id) == 22 and path_or_id[14] == "-":
        return path_or_id
    if path_or_id.startswith("/"):
        result = api_call("/api/filetree/getDocByPath", {"path": path_or_id}, config)
        if result.get("code") == 0 and result.get("data"):
            return result["data"].get("id") if isinstance(result["data"], dict) else str(result["data"])
    return path_or_id


def batch_export(doc_id: str, output: str, config: dict, include_self=False):
    """批量导出（父+子 或 仅子）"""
    children = get_child_docs(doc_id, config)
    ok = fail = 0
    results = []

    if include_self or not children:
        r = export_docx(doc_id, output, config)
        ok += 1 if r["success"] else 0
        fail += 1 if not r["success"] else 0
        if include_self:
            results.append({"id": doc_id, "title": "(parent)", "success": r["success"]})

    for child in children:
        r = export_docx(child["id"], output, config)
        ok += 1 if r["success"] else 0
        fail += 1 if not r["success"] else 0
        results.append({"id": child["id"], "title": child.get("content", ""), "success": r["success"]})

    total = len(children) + (1 if (include_self or not children) else 0)
    print(json.dumps({
        "success": fail == 0,
        "total": total,
        "ok": ok,
        "fail": fail,
        "details": results,
    }, ensure_ascii=False, indent=2))
    return fail == 0


def main():
    parser = argparse.ArgumentParser(
        description="思源笔记文档导出工具（Word）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python siyuan_export.py -s "关键词" -o C:/Desktop
  python siyuan_export.py -s "关键词" -c -o C:/Desktop
  python siyuan_export.py --doc-id <ID> -c -o C:/Desktop
        """,
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--doc-id", "-i", help="文档 ID")
    group.add_argument("--path", "-p", help="文档路径")
    group.add_argument("--search", "-s", help="按文档名搜索")

    parser.add_argument("--output", "-o", default="", help="输出目录（默认：桌面）")
    parser.add_argument("--children", "-c", action="store_true", help="导出所有子文档")
    parser.add_argument("--include-self", action="store_true", help="同时导出父文档")

    args = parser.parse_args()
    config = get_config()
    output = args.output or os.path.join(os.path.expanduser("~"), "Desktop")

    if not config["token"]:
        print(json.dumps({"success": False, "error": "no_token", "message": "请在 config.json 配置 token"}))
        sys.exit(1)

    # ====== 搜索模式 ======
    if args.search:
        docs = search_docs(args.search, config)
        if not docs:
            print(json.dumps({"success": False, "error": "not_found", "message": f"未找到包含 '{args.search}' 的文档"}))
            sys.exit(1)

        # 多个匹配 → 返回列表，让调用方决定
        if len(docs) > 1:
            print(f"\n找到 {len(docs)} 个匹配文档:\n")
            print(f"{'#':<4} {'ID':<24} {'标题':<20} {'创建时间':<19}")
            print("-" * 75)
            for i, d in enumerate(docs):
                created = format_time(d.get("created", ""))
                title = d.get("content", "")[:18]
                doc_id = d.get("id", "")
                print(f"{i+1:<4} {doc_id:<24} {title:<20} {created:<19}")
            print(f"\n请选择序号（1-{len(docs)}）或提供更精确的关键词")
            sys.exit(2)

        # 单个匹配
        doc = docs[0]
        doc_id = doc["id"]
        children = get_child_docs(doc_id, config)
        has_children = len(children) > 0

        # 有 -c 或没有子文档 → 直接执行
        if args.children or not has_children:
            success = batch_export(doc_id, output, config, include_self=args.include_self)
            sys.exit(0 if success else 1)

        # 无 -c 且有子文档 → 返回信息让调用方决定范围
        child_titles = [c.get("content", "") for c in children]
        print(json.dumps({
            "action": "select_scope",
            "doc_id": doc_id,
            "title": doc.get("content", ""),
            "children_count": len(children),
            "children": [{"id": c["id"], "title": c.get("content", "")} for c in children],
            "hint": "该文档有子文档，请确认导出范围",
        }, ensure_ascii=False, indent=2))
        sys.exit(2)

    # ====== 非搜索模式 (-i / -p) ======
    doc_id = resolve_doc_id(args.doc_id or args.path, config)
    if not doc_id:
        print(json.dumps({"success": False, "error": "resolve_failed", "message": "无法识别文档"}))
        sys.exit(1)

    if args.children:
        success = batch_export(doc_id, output, config, include_self=args.include_self)
    else:
        r = export_docx(doc_id, output, config)
        print(json.dumps(r, ensure_ascii=False, indent=2))
        success = r.get("success", False)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
