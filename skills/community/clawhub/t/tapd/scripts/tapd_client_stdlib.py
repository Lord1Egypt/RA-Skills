"""
TAPD API 客户端（仅使用 Python 标准库）。

依赖：urllib.request, json, os, base64, argparse。
环境变量：TAPD_ACCESS_TOKEN 或 TAPD_API_USER + TAPD_API_PASSWORD；
         TAPD_API_BASE_URL（可选，默认 https://api.tapd.cn）；可选 TAPD_BASE_URL（默认 https://www.tapd.cn）, BOT_URL, CURRENT_USER_NICK。

命令行用法（AI 可直接调用）：
    python tapd_client_stdlib.py projects [--nick NICK]
    python tapd_client_stdlib.py workspace --workspace-id ID
    python tapd_client_stdlib.py stories --workspace-id ID [--entity-type stories|tasks] [--limit N] [--page N] [--id ID] [--name NAME] [--status STATUS]
    python tapd_client_stdlib.py bugs --workspace-id ID [--limit N] [--page N] [--id ID]
    python tapd_client_stdlib.py iterations --workspace-id ID [--limit N] [--page N]
    python tapd_client_stdlib.py releases --workspace-id ID [--limit N] [--page N]
    python tapd_client_stdlib.py get --endpoint "stories/count" -p workspace_id=123 -p entity_type=stories
    python tapd_client_stdlib.py post --endpoint "stories" -b '{"workspace_id":123,"name":"需求标题"}'

Python 调用示例：
    from tapd_client_stdlib import request, get_stories, get_workspace_info
    resp = request("GET", "stories", params={"workspace_id": 123, "limit": 10})
    stories = get_stories(123, {"entity_type": "stories", "limit": 5})
"""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from base64 import b64encode
from typing import Any, Optional


# 默认 TAPD 云环境地址，未配置环境变量时使用
DEFAULT_TAPD_API_BASE_URL = "https://api.tapd.cn"
DEFAULT_TAPD_BASE_URL = "https://www.tapd.cn"


def _get_base_url() -> str:
    base = os.environ.get("TAPD_API_BASE_URL", DEFAULT_TAPD_API_BASE_URL)
    return base.rstrip("/")


def _get_headers() -> dict:
    token = os.environ.get("TAPD_ACCESS_TOKEN")
    if token:
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Via": "mcp",
        }
    user = os.environ.get("TAPD_API_USER")
    password = os.environ.get("TAPD_API_PASSWORD")
    if not user or not password:
        raise ValueError(
            "请设置 TAPD_ACCESS_TOKEN 或 TAPD_API_USER + TAPD_API_PASSWORD"
        )
    auth = b64encode(f"{user}:{password}".encode()).decode()
    return {
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json",
        "Via": "mcp",
    }


def _is_cloud() -> bool:
    base = os.environ.get("TAPD_API_BASE_URL", DEFAULT_TAPD_API_BASE_URL)
    return "api.tapd.cn" in base


def to_long_id(short_id: str, workspace_id: int) -> str:
    """将短 ID（≤9 位数字）转为 TAPD 长 ID。"""
    s = str(short_id).strip()
    if not s.isdigit() or len(s) > 9:
        return s
    prefix = "11" if _is_cloud() else "10"
    return f"{prefix}{workspace_id}{s.zfill(9)}"


def request(
    method: str,
    endpoint: str,
    params: Optional[dict] = None,
    data: Optional[dict] = None,
    timeout: int = 30,
) -> dict:
    """
    发送 TAPD API 请求。URL 自动追加 ?s=mcp 或 &s=mcp。

    :param method: GET 或 POST
    :param endpoint: 路径，如 "stories", "workspaces/get_workspace_info"
    :param params: GET 查询参数或 POST 时也可拼在 URL（部分接口习惯用 query）
    :param data: POST 请求体（JSON）
    :param timeout: 超时秒数
    :return: 响应 JSON（dict）
    """
    base = _get_base_url()
    url = f"{base}/{endpoint.lstrip('/')}"
    sep = "&" if "?" in url else "?"
    url = f"{url}{sep}s=mcp"

    if params:
        encoded = urllib.parse.urlencode(params, doseq=True)
        url = f"{url}&{encoded}" if "?" in url else f"{url}?{encoded}"

    headers = _get_headers()
    req_body = None
    if method.upper() == "POST" and data is not None:
        req_body = json.dumps(data).encode("utf-8")

    req = urllib.request.Request(url, data=req_body, headers=headers, method=method.upper())
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_stories(
    workspace_id: int,
    options: Optional[dict] = None,
) -> dict:
    """
    获取需求或任务列表。entity_type 在 options 中指定为 stories 或 tasks。
    """
    opts = options or {}
    entity_type = opts.get("entity_type", "stories")
    endpoint = "stories" if entity_type == "stories" else "tasks"
    params = {"workspace_id": workspace_id, "page": 1, "limit": 10}
    params.update(opts)
    return request("GET", endpoint, params=params)


def get_workspace_info(workspace_id: int) -> dict:
    """根据项目 ID 获取项目信息。"""
    return request(
        "GET",
        f"workspaces/get_workspace_info?workspace_id={workspace_id}",
    )


def get_user_participant_projects(nick: str) -> dict:
    """获取用户参与的项目列表。"""
    return request("GET", "workspaces/user_participant_projects", params={"nick": nick})


def get_bugs(workspace_id: int, options: Optional[dict] = None) -> dict:
    """获取缺陷列表。"""
    params = {"workspace_id": workspace_id, "page": 1, "limit": 10}
    if options:
        params.update(options)
    return request("GET", "bugs", params=params)


def get_iterations(workspace_id: int, options: Optional[dict] = None) -> dict:
    """获取迭代列表。"""
    params = {"workspace_id": workspace_id}
    if options:
        params.update(options)
    return request("GET", "iterations", params=params)


def get_releases(workspace_id: int, options: Optional[dict] = None) -> dict:
    """获取发布计划列表。"""
    params = {"workspace_id": workspace_id}
    if options:
        params.update(options)
    return request("GET", "releases", params=params)


def _cli():
    parser = argparse.ArgumentParser(
        description="TAPD API 命令行客户端（仅标准库）。需设置 TAPD_ACCESS_TOKEN 或 TAPD_API_USER/TAPD_API_PASSWORD；TAPD_API_BASE_URL 可选（默认 https://api.tapd.cn）。"
    )
    sub = parser.add_subparsers(dest="command", required=True, help="子命令")

    # projects
    p_projects = sub.add_parser("projects", help="获取用户参与的项目列表")
    p_projects.add_argument("--nick", default=os.environ.get("CURRENT_USER_NICK", ""), help="用户昵称，默认 CURRENT_USER_NICK")

    # workspace
    p_ws = sub.add_parser("workspace", help="获取项目信息")
    p_ws.add_argument("--workspace-id", type=int, required=True, dest="workspace_id", help="项目 ID")

    # stories（含 tasks）
    p_stories = sub.add_parser("stories", help="获取需求或任务列表")
    p_stories.add_argument("--workspace-id", type=int, required=True, dest="workspace_id")
    p_stories.add_argument("--entity-type", choices=("stories", "tasks"), default="stories", dest="entity_type")
    p_stories.add_argument("--limit", type=int, default=10)
    p_stories.add_argument("--page", type=int, default=1)
    p_stories.add_argument("--id", dest="id_", metavar="ID", help="需求/任务 ID，支持逗号分隔多 ID")
    p_stories.add_argument("--name", help="标题模糊匹配")
    p_stories.add_argument("--status", help="状态")
    p_stories.add_argument("--fields", help="返回字段，逗号分隔")

    # bugs
    p_bugs = sub.add_parser("bugs", help="获取缺陷列表")
    p_bugs.add_argument("--workspace-id", type=int, required=True, dest="workspace_id")
    p_bugs.add_argument("--limit", type=int, default=10)
    p_bugs.add_argument("--page", type=int, default=1)
    p_bugs.add_argument("--id", dest="id_", metavar="ID", help="缺陷 ID")
    p_bugs.add_argument("--title", help="标题")

    # iterations
    p_iter = sub.add_parser("iterations", help="获取迭代列表")
    p_iter.add_argument("--workspace-id", type=int, required=True, dest="workspace_id")
    p_iter.add_argument("--limit", type=int, default=30)
    p_iter.add_argument("--page", type=int, default=1)
    p_iter.add_argument("--name", help="迭代名称")

    # releases
    p_rel = sub.add_parser("releases", help="获取发布计划列表")
    p_rel.add_argument("--workspace-id", type=int, required=True, dest="workspace_id")
    p_rel.add_argument("--limit", type=int, default=30)
    p_rel.add_argument("--page", type=int, default=1)

    # 通用 get / post
    p_get = sub.add_parser("get", help="通用 GET：--endpoint 路径，-p key=val 多个参数")
    p_get.add_argument("--endpoint", required=True, help="API 路径，如 stories、bugs/count")
    p_get.add_argument("-p", "--param", dest="params", action="append", default=[], metavar="KEY=VAL", help="查询参数，可多次")

    p_post = sub.add_parser("post", help="通用 POST：--endpoint 路径，-b JSON 或 -p key=val")
    p_post.add_argument("--endpoint", required=True, help="API 路径，如 stories、comments")
    p_post.add_argument("-b", "--body", help="JSON 请求体")
    p_post.add_argument("-p", "--param", dest="params", action="append", default=[], metavar="KEY=VAL", help="作为 body 的键值，可多次（与 -b 二选一）")

    args = parser.parse_args()
    out = None

    if args.command == "projects":
        nick = (args.nick or "").strip()
        if not nick:
            print(json.dumps({"error": "请提供 --nick 或设置 CURRENT_USER_NICK"}, ensure_ascii=False), file=sys.stderr)
            raise SystemExit(1)
        out = get_user_participant_projects(nick)
    elif args.command == "workspace":
        out = get_workspace_info(args.workspace_id)
    elif args.command == "stories":
        opts = {"entity_type": args.entity_type, "limit": args.limit, "page": args.page}
        if getattr(args, "id_", None):
            opts["id"] = args.id_
        if getattr(args, "name", None):
            opts["name"] = args.name
        if getattr(args, "status", None):
            opts["status"] = args.status
        if getattr(args, "fields", None):
            opts["fields"] = args.fields
        out = get_stories(args.workspace_id, opts)
    elif args.command == "bugs":
        opts = {"limit": args.limit, "page": args.page}
        if getattr(args, "id_", None):
            opts["id"] = args.id_
        if getattr(args, "title", None):
            opts["title"] = args.title
        out = get_bugs(args.workspace_id, opts)
    elif args.command == "iterations":
        opts = {"limit": args.limit, "page": args.page}
        if getattr(args, "name", None):
            opts["name"] = args.name
        out = get_iterations(args.workspace_id, opts)
    elif args.command == "releases":
        out = get_releases(args.workspace_id, {"limit": args.limit, "page": args.page})
    elif args.command == "get":
        params = {}
        for s in args.params:
            if "=" in s:
                k, v = s.split("=", 1)
                params[k.strip()] = v.strip()
        out = request("GET", args.endpoint, params=params if params else None)
    elif args.command == "post":
        if args.body:
            try:
                data = json.loads(args.body)
            except json.JSONDecodeError as e:
                print(json.dumps({"error": f"无效 JSON: {e}"}, ensure_ascii=False), file=sys.stderr)
                raise SystemExit(1)
        else:
            data = {}
            for s in args.params:
                if "=" in s:
                    k, v = s.split("=", 1)
                    data[k.strip()] = v.strip()
        out = request("POST", args.endpoint, data=data if data else None)

    if out is not None:
        print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    _cli()
