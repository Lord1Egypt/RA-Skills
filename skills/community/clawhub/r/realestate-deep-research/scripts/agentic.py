#!/usr/bin/env python3
"""
Agentic CLI — 深度智联 Agentic 智能体全功能命令行工具。
通过子命令调用，覆盖任务创建、轮询、成果获取、文件管理、Token 续期等全部能力。
"""

import argparse
import base64
import json
import os
import sys
import time
from datetime import datetime

import requests

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------
BASE_URL = "https://agentic.dichanai.com"
SKILL_API_URLS = [                        # check-update 接口候选地址（按优先级）
    f"{BASE_URL}/v1/skill",
]
SKILL_NAME = "realestate-deep-research"
SKILL_VERSION = "1.1.0"                  # 当前已安装的 Skill 版本
TOKEN_RENEW_BUFFER_DAYS = 10          # Token 过期前 10 天自动续期
TOKEN_RENEW_DURATION = 2592000        # 续期时长 30 天（秒）
POLL_INTERVAL = 120                   # 轮询间隔（秒）
POLL_TIMEOUT = 3600                   # 轮询超时（秒）


def get_token():
    """从环境变量获取 AGENTIC_TOKEN。"""
    token = os.environ.get("AGENTIC_TOKEN")
    if not token:
        print("ERROR: 环境变量 AGENTIC_TOKEN 未设置。请先配置 Token。")
        sys.exit(1)
    return token


def headers(token=None, json_content=True):
    """构造通用请求头。"""
    token = token or get_token()
    h = {"Authorization": f"Bearer {token}"}
    if json_content:
        h["Content-Type"] = "application/json"
    return h


def api(method, path, token=None, **kwargs):
    """统一 API 请求封装，自动处理错误。"""
    url = f"{BASE_URL}{path}"
    token = token or get_token()
    resp = requests.request(method, url, headers=headers(token, json_content="files" not in kwargs), **kwargs)
    if not resp.ok:
        print(f"ERROR: {method} {path} → {resp.status_code}")
        try:
            print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
        except Exception:
            print(resp.text[:500])
        sys.exit(1)
    # 批量下载接口返回二进制，不做 JSON 解析
    if resp.headers.get("Content-Type", "").startswith("application/json"):
        return resp.json()
    return resp


def decode_jwt_exp(token):
    """从 JWT token 中解码 exp 字段（不验证签名）。"""
    try:
        payload = token.split(".")[1]
        # 补齐 base64 padding
        payload += "=" * (4 - len(payload) % 4)
        data = json.loads(base64.urlsafe_b64decode(payload))
        exp = data.get("exp")
        if exp is None:
            return None
        # exp 可能是浮点数（如 1775020367.744）
        return float(exp)
    except Exception:
        return None


# ========================== 子命令实现 ==========================

def cmd_check_token(args):
    """检查 Token 有效期，如果距过期不足 10 天则自动续期。"""
    token = get_token()
    exp = decode_jwt_exp(token)
    if exp is None:
        print("WARNING: 无法解析 Token 过期时间，跳过自动续期检查。")
        return

    now = time.time()
    remaining_days = (exp - now) / 86400
    exp_str = datetime.fromtimestamp(exp).strftime("%Y-%m-%d %H:%M:%S")

    if remaining_days <= 0:
        print(f"CRITICAL: Token 已于 {exp_str} 过期！无法自动续期，请重新获取 Token。")
        sys.exit(1)
    elif remaining_days <= TOKEN_RENEW_BUFFER_DAYS:
        print(f"Token 将于 {exp_str} 过期（剩余 {remaining_days:.1f} 天），正在自动续期...")
        result = api("POST", "/v1/token", json={"expires_in": TOKEN_RENEW_DURATION})
        new_token = result["data"]["token"]
        new_exp = result["data"]["expires"]
        new_exp_str = datetime.fromtimestamp(new_exp).strftime("%Y-%m-%d %H:%M:%S")
        print(f"SUCCESS: Token 已续期，新过期时间：{new_exp_str}")
        print(f"NEW_TOKEN={new_token}")
        print("请将上面的 NEW_TOKEN 值更新到你的 AGENTIC_TOKEN 环境变量中。")
    else:
        print(f"Token 状态正常，过期时间：{exp_str}（剩余 {remaining_days:.1f} 天）")


def cmd_profile(args):
    """获取用户资料。"""
    result = api("GET", "/v1/profile")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_create(args):
    """创建并运行任务（可选附带文件上传）。"""
    token = get_token()
    chat_id = args.chat_id

    # 如果有文件，先上传
    if args.file:
        print(f"正在上传文件: {args.file} ...")
        with open(args.file, "rb") as f:
            params = {}
            if chat_id:
                params["chat_id"] = chat_id
            result = api("POST", "/v1/workspace/file", token=token,
                         params=params, files={"files": (os.path.basename(args.file), f)})
            chat_id = result["data"]
            print(f"文件上传成功，chat_id: {chat_id}")

    # 创建任务
    payload = {
        "query": args.query,
        "agent": "general",
        "router": "default",
        "enabled_mcps": [],
    }
    if chat_id:
        payload["chat_id"] = chat_id

    result = api("POST", "/v1/chat", json=payload)
    task_id = result.get("data", {}).get("id", "unknown")
    print(f"SUCCESS: 任务已创建，chat_id: {task_id}")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_schedule(args):
    """创建计划任务（定时执行）。"""
    dt = datetime.strptime(args.time, "%Y-%m-%d %H:%M:%S")
    scheduled_ts = int(dt.timestamp() * 1000)

    payload = {"query": args.query, "scheduled": scheduled_ts}
    if args.chat_id:
        payload["chat_id"] = args.chat_id

    result = api("POST", "/v1/chat/schedule", json=payload)
    print(f"SUCCESS: 计划任务已创建")
    print(json.dumps(result, indent=2, ensure_ascii=False))


def cmd_status(args):
    """查询单个任务的状态。"""
    result = api("GET", f"/v1/chat/{args.chat_id}")
    data = result.get("data", {})
    sending = data.get("sending", False)
    last_status = data.get("last_status", "")
    title = data.get("title", "")
    messages = data.get("messages", [])

    # 优先使用 last_status 字段判断，回退到 sending 字段
    if last_status:
        status = last_status  # e.g. "finished", "running", "error" 等
    else:
        status = "运行中" if sending else "已完成"
    print(f"任务: {title}")
    print(f"状态: {status}")
    print(f"消息数: {len(messages)}")

    # 输出最后一条助手消息摘要
    for msg in reversed(messages):
        if msg.get("role") == "assistant" and msg.get("content_type") == "text":
            text = msg.get("content", {}).get("text", "")
            preview = text[:300] + ("..." if len(text) > 300 else "")
            print(f"最新回复: {preview}")
            break

    print(f"\nlast_status={last_status}, sending={sending}")


def cmd_poll(args):
    """轮询任务直到完成，然后自动获取成果文件下载链接。"""
    chat_id = args.chat_id
    interval = args.interval or POLL_INTERVAL
    timeout = args.timeout or POLL_TIMEOUT
    start = time.time()

    print(f"开始轮询任务 {chat_id}，间隔 {interval}s，超时 {timeout}s ...")

    while True:
        elapsed = time.time() - start
        if elapsed > timeout:
            print(f"TIMEOUT: 已等待 {int(elapsed)}s，超过超时时间 {timeout}s。任务可能仍在运行。")
            sys.exit(1)

        result = api("GET", f"/v1/chat/{chat_id}")
        data = result.get("data", {})
        last_status = data.get("last_status", "")
        sending = data.get("sending", False)

        # 优先使用 last_status 字段判断完成（API 文档推荐），回退到 sending 字段
        is_finished = (last_status == "finished") if last_status else (not sending)

        if is_finished:
            print("任务已完成！")
            # 自动获取成果文件
            _fetch_results(chat_id)
            return
        else:
            # 输出进度
            status_hint = f"last_status={last_status}" if last_status else "运行中"
            messages = data.get("messages", [])
            for msg in reversed(messages):
                if msg.get("role") == "assistant" and msg.get("content_type") == "text":
                    text = msg.get("content", {}).get("text", "")
                    preview = text[:200] + ("..." if len(text) > 200 else "")
                    print(f"[{int(elapsed)}s] {status_hint} — {preview}")
                    break
            else:
                print(f"[{int(elapsed)}s] {status_hint}")

        time.sleep(interval)


def _fetch_results(chat_id):
    """列出 /成果 目录并获取所有文件的下载链接。"""
    result = api("GET", f"/v1/chat/{chat_id}/workspace/file", params={"path": "/成果"})
    data = result.get("data", [])

    files = _extract_files(data)
    if not files:
        print("成果目录为空或不存在。")
        return

    print(f"\n找到 {len(files)} 个成果文件:")
    for f in files:
        print(f"  - {f['path']} ({f['size']} bytes)")

    print("\n获取下载链接:")
    for f in files:
        share = api("POST", f"/v1/chat/{chat_id}/workspace/file/share", json={"path": f["path"]})
        url = share.get("data", {}).get("url", "无法获取")
        print(f"  {f['name']}: {url}")


def _extract_files(nodes):
    """递归从目录树中提取所有文件。"""
    files = []
    if isinstance(nodes, list):
        for node in nodes:
            files.extend(_extract_files(node))
    elif isinstance(nodes, dict):
        if not nodes.get("isBranch", False) and nodes.get("metadata"):
            files.append({
                "name": nodes["name"],
                "path": nodes["metadata"]["path"],
                "size": nodes["metadata"].get("size", 0),
            })
        for child in nodes.get("children", []):
            files.extend(_extract_files(child))
    return files


def cmd_files(args):
    """列出任务工作空间中的文件。"""
    path = args.path or "/"
    result = api("GET", f"/v1/chat/{args.chat_id}/workspace/file", params={"path": path})
    files = _extract_files(result.get("data", []))

    if not files:
        print(f"目录 {path} 为空或不存在。")
        return

    print(f"目录 {path} 下共 {len(files)} 个文件:")
    for f in files:
        print(f"  {f['path']}  ({f['size']} bytes)")


def cmd_download(args):
    """获取指定文件的临时下载链接。"""
    result = api("POST", f"/v1/chat/{args.chat_id}/workspace/file/share",
                 json={"path": args.path})
    data = result.get("data", {})
    url = data.get("url", "")
    name = data.get("name", "")
    size = data.get("size", 0)
    print(f"文件: {name} ({size} bytes)")
    print(f"下载链接（有效期约1小时）: {url}")


def cmd_upload(args):
    """上传文件到任务工作空间。"""
    params = {}
    if args.chat_id:
        params["chat_id"] = args.chat_id

    with open(args.file, "rb") as f:
        result = api("POST", "/v1/workspace/file",
                     params=params, files={"files": (os.path.basename(args.file), f)})

    chat_id = result.get("data", "")
    print(f"SUCCESS: 文件已上传，chat_id: {chat_id}")


def cmd_list(args):
    """列出用户的所有任务。"""
    params = {}
    if args.keyword:
        params["keyword"] = args.keyword
    if args.page:
        params["page"] = args.page
    if args.page_size:
        params["page_size"] = args.page_size

    result = api("GET", "/v1/chat", params=params)
    items = result.get("data", {}).get("items", [])

    if not items:
        print("没有找到任务。")
        return

    print(f"共 {len(items)} 个任务:")
    for item in items:
        last_status = item.get("last_status", "")
        if last_status:
            status = last_status
        else:
            status = "运行中" if item.get("sending") else "已完成"
        title = item.get("title", "无标题")
        created = item.get("created", "")[:19]
        print(f"  [{status}] {item['id']}  {title}  ({created})")


def cmd_abort(args):
    """中止正在运行的任务。"""
    api("POST", f"/v1/chat/{args.chat_id}/abort")
    print(f"SUCCESS: 任务 {args.chat_id} 已中止。")


def cmd_delete(args):
    """删除任务。"""
    api("DELETE", f"/v1/chat/{args.chat_id}")
    print(f"SUCCESS: 任务 {args.chat_id} 已删除。")


def cmd_share(args):
    """分享任务（设为公开）。"""
    api("POST", f"/v1/chat/{args.chat_id}/share")
    url = f"{BASE_URL}/share/?chat_id={args.chat_id}"
    print(f"SUCCESS: 任务已分享。查看链接: {url}")


def cmd_rename(args):
    """修改任务标题。"""
    api("PUT", f"/v1/chat/{args.chat_id}", json={"title": args.title})
    print(f"SUCCESS: 任务标题已修改为「{args.title}」")


def cmd_plan(args):
    """获取任务行动计划。"""
    result = api("GET", f"/v1/chat/{args.chat_id}/plan")
    steps = result.get("data", {}).get("steps", [])

    if not steps:
        print("暂无行动计划。")
        return

    print(f"行动计划（{len(steps)} 步）:")
    for i, step in enumerate(steps, 1):
        deleted = " [已删除]" if step.get("deleted") else ""
        print(f"  {i}. {step.get('description', '无描述')}{deleted}")


def cmd_schedules(args):
    """列出所有计划任务。"""
    result = api("GET", "/v1/chat/schedule")
    items = result.get("data", [])

    if not items:
        print("没有计划任务。")
        return

    print(f"共 {len(items)} 个计划任务:")
    for item in items:
        scheduled = item.get("scheduled", "")[:19]
        status = item.get("status", "")
        query = item.get("user_message", {}).get("content", {}).get("text", "")[:60]
        print(f"  [{status}] {item['id']}  {scheduled}  {query}")


def cmd_renew_token(args):
    """手动续期 Token。"""
    expires_in = args.expires_in or TOKEN_RENEW_DURATION
    result = api("POST", "/v1/token", json={"expires_in": expires_in})
    new_token = result["data"]["token"]
    new_exp = result["data"]["expires"]
    new_exp_str = datetime.fromtimestamp(new_exp).strftime("%Y-%m-%d %H:%M:%S")
    print(f"SUCCESS: Token 已续期，新过期时间：{new_exp_str}")
    print(f"NEW_TOKEN={new_token}")


def cmd_check_update(args):
    """检查 Skill 是否有新版本可用。无需鉴权。依次尝试候选 URL。"""
    data = None
    last_err = None
    for url in SKILL_API_URLS:
        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            break
        except Exception as e:
            last_err = e
            continue

    if data is None:
        print(f"WARNING: 无法检查更新（所有候选地址均失败） — {last_err}")
        return

    skills = data.get("data", {}).get("skills", [])
    target = None
    for s in skills:
        if s.get("name") == SKILL_NAME:
            target = s
            break

    if target is None:
        print(f"WARNING: 未在服务器上找到 Skill '{SKILL_NAME}' 的信息。")
        return

    remote_version = target.get("version", "unknown")
    release_date = target.get("release_date", "unknown")
    download_url = target.get("url", "")

    print(f"当前安装版本: {SKILL_VERSION}")
    print(f"服务器最新版本: {remote_version}")
    print(f"发布时间: {release_date}")

    if remote_version != SKILL_VERSION:
        print(f"\nUPDATE_AVAILABLE: 发现新版本 {remote_version}（当前 {SKILL_VERSION}）")
        print(f"下载地址: {download_url}")
        print("请下载最新版本的 Skill 文件并替换当前安装的文件，以获得最新功能和修复。")
    else:
        print("\nSKILL_UP_TO_DATE: 当前已是最新版本，无需更新。")


def cmd_batch_download(args):
    """批量下载多个文件（打包为 zip）。"""
    file_list = [f.strip() for f in args.files.split(",")]
    # 步骤一：准备打包
    result = api("POST", "/v1/workspace/file/batch",
                 json={"chat_id": args.chat_id, "files": file_list})
    filename = result.get("data", {}).get("filename", "")
    if not filename:
        print("ERROR: 准备打包失败。")
        sys.exit(1)

    # 步骤二：下载
    download_url = f"{BASE_URL}/v1/workspace/file/batch?filename={filename}"
    print(f"下载链接（仅可使用一次）: {download_url}")


# ========================== 主入口 ==========================

def main():
    parser = argparse.ArgumentParser(
        description="深度智联 Agentic 智能体 CLI — 全功能命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="command", help="可用子命令")

    # --- check-token ---
    p = sub.add_parser("check-token", help="检查 Token 有效期，距过期不足 10 天时自动续期")

    # --- profile ---
    p = sub.add_parser("profile", help="获取用户资料")

    # --- create ---
    p = sub.add_parser("create", help="创建并运行任务")
    p.add_argument("--query", required=True, help="任务需求描述（原样传递，不要修改）")
    p.add_argument("--file", help="要上传的附件文件路径")
    p.add_argument("--chat-id", help="已有任务 ID（用于继续对话）")

    # --- schedule ---
    p = sub.add_parser("schedule", help="创建计划任务（定时执行）")
    p.add_argument("--query", required=True, help="任务需求描述")
    p.add_argument("--time", required=True, help="执行时间，格式 YYYY-MM-DD HH:MM:SS")
    p.add_argument("--chat-id", help="已有任务 ID")

    # --- status ---
    p = sub.add_parser("status", help="查询任务状态")
    p.add_argument("--chat-id", required=True, help="任务 ID")

    # --- poll ---
    p = sub.add_parser("poll", help="轮询任务直到完成，自动获取成果下载链接")
    p.add_argument("--chat-id", required=True, help="任务 ID")
    p.add_argument("--interval", type=int, help=f"轮询间隔秒数（默认 {POLL_INTERVAL}）")
    p.add_argument("--timeout", type=int, help=f"超时秒数（默认 {POLL_TIMEOUT}）")

    # --- files ---
    p = sub.add_parser("files", help="列出任务工作空间中的文件")
    p.add_argument("--chat-id", required=True, help="任务 ID")
    p.add_argument("--path", help="目录路径（默认 /）")

    # --- download ---
    p = sub.add_parser("download", help="获取指定文件的临时下载链接")
    p.add_argument("--chat-id", required=True, help="任务 ID")
    p.add_argument("--path", required=True, help="文件在工作空间的完整路径")

    # --- upload ---
    p = sub.add_parser("upload", help="上传文件到任务工作空间")
    p.add_argument("--file", required=True, help="本地文件路径")
    p.add_argument("--chat-id", help="任务 ID（不传则自动创建新任务）")

    # --- list ---
    p = sub.add_parser("list", help="列出所有任务")
    p.add_argument("--keyword", help="搜索关键词")
    p.add_argument("--page", type=int, help="页码")
    p.add_argument("--page-size", type=int, help="每页条目数")

    # --- abort ---
    p = sub.add_parser("abort", help="中止正在运行的任务")
    p.add_argument("--chat-id", required=True, help="任务 ID")

    # --- delete ---
    p = sub.add_parser("delete", help="删除任务")
    p.add_argument("--chat-id", required=True, help="任务 ID")

    # --- share ---
    p = sub.add_parser("share", help="分享任务（设为公开）")
    p.add_argument("--chat-id", required=True, help="任务 ID")

    # --- rename ---
    p = sub.add_parser("rename", help="修改任务标题")
    p.add_argument("--chat-id", required=True, help="任务 ID")
    p.add_argument("--title", required=True, help="新标题")

    # --- plan ---
    p = sub.add_parser("plan", help="获取任务行动计划")
    p.add_argument("--chat-id", required=True, help="任务 ID")

    # --- schedules ---
    p = sub.add_parser("schedules", help="列出所有计划任务")

    # --- renew-token ---
    p = sub.add_parser("renew-token", help="手动续期 Token")
    p.add_argument("--expires-in", type=int, help=f"有效期秒数（默认 {TOKEN_RENEW_DURATION}，最大 2592000）")

    # --- check-update ---
    p = sub.add_parser("check-update", help="检查 Skill 是否有新版本可用（无需 Token）")

    # --- batch-download ---
    p = sub.add_parser("batch-download", help="批量下载多个文件（打包为 zip）")
    p.add_argument("--chat-id", required=True, help="任务 ID")
    p.add_argument("--files", required=True, help="文件路径列表，逗号分隔")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    # 路由到子命令
    commands = {
        "check-token": cmd_check_token,
        "profile": cmd_profile,
        "create": cmd_create,
        "schedule": cmd_schedule,
        "status": cmd_status,
        "poll": cmd_poll,
        "files": cmd_files,
        "download": cmd_download,
        "upload": cmd_upload,
        "list": cmd_list,
        "abort": cmd_abort,
        "delete": cmd_delete,
        "share": cmd_share,
        "rename": cmd_rename,
        "plan": cmd_plan,
        "schedules": cmd_schedules,
        "renew-token": cmd_renew_token,
        "check-update": cmd_check_update,
        "batch-download": cmd_batch_download,
    }
    commands[args.command](args)


if __name__ == "__main__":
    main()
