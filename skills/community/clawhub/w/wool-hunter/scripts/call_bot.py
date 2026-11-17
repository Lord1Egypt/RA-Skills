#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Coze 智能体调用脚本
调用已发布的 Coze 智能体，支持 SSE 流式响应解析

用法：
    COZE_TOKEN=<token> COZE_PROJECT_ID=<id> python3 call_bot.py "你好"
    python3 call_bot.py "你好" --token <token> --project-id <id>
"""

import json
import sys
import os
import urllib.request
import urllib.error
import ssl

# 默认配置（可通过环境变量覆盖）
DEFAULT_PROJECT_ID = os.environ.get("COZE_PROJECT_ID", "7646644331176067098")
DEFAULT_SESSION_ID = os.environ.get("COZE_SESSION_ID", "XjZXRWzSYLSKy7hlOGXGI")
DEFAULT_URL = os.environ.get("COZE_BASE_URL", "https://dygv8mm7gq.coze.site/stream_run")


def _secrets_file(name):
    """Windows 迁移兜底：读 ~/.workbuddy/secrets/ 下的明文凭据文件。"""
    p = os.path.join(os.path.expanduser("~"), ".workbuddy", "secrets", name)
    try:
        with open(p, "r", encoding="utf-8") as f:
            return f.read().strip()
    except OSError:
        return ""


def coze_token():
    """按 env(COZE_TOKEN/COZE_BOT_TOKEN) -> secrets 文件顺序取 Coze Token。"""
    return (os.environ.get("COZE_TOKEN", "").strip()
            or os.environ.get("COZE_BOT_TOKEN", "").strip()
            or _secrets_file("coze_bot_token.txt")
            or _secrets_file("coze_token.txt"))


def call_bot(text: str, token: str, project_id: str = None,
             session_id: str = None, base_url: str = None):
    """
    调用 Coze 智能体，发送文本消息，解析 SSE 流式响应。

    Args:
        text: 用户输入的文本内容
        token: Coze API Token
        project_id: Coze 项目 ID
        session_id: 会话 ID（保持上下文）
        base_url: API 基础 URL

    Returns:
        dict: {success: bool, full_text: str, chunks: list, raw_events: list, error: str}
    """
    project_id = project_id or DEFAULT_PROJECT_ID
    session_id = session_id or DEFAULT_SESSION_ID
    base_url = base_url or DEFAULT_URL

    payload = {
        "content": {
            "query": {
                "prompt": [
                    {
                        "type": "text",
                        "content": {"text": text}
                    }
                ]
            }
        },
        "type": "query",
        "session_id": session_id,
        "project_id": project_id,
    }

    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
        "User-Agent": "coze-bot-cli/1.0",
    }

    req = urllib.request.Request(
        base_url,
        data=body,
        headers=headers,
        method="POST",
    )

    # 信任 TLS（Coze 使用标准 HTTPS 证书）
    ctx = ssl.create_default_context()

    chunks = []
    raw_events = []
    answer_parts = []

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
            # 逐行读取 SSE 流
            for line in resp:
                try:
                    line_str = line.decode("utf-8", errors="replace").strip()
                except Exception:
                    continue
                if not line_str:
                    continue
                if line_str.startswith("data:"):
                    data_text = line_str[5:].strip()
                    raw_events.append(data_text)
                    try:
                        parsed = json.loads(data_text)
                        chunks.append(parsed)
                        # 提取 answer 片段（Coze 流式返回）
                        _extract_answer(parsed, answer_parts)
                    except json.JSONDecodeError:
                        # 非 JSON 的 data 行（如 [DONE]）
                        answer_parts.append(data_text)

        # 拼接所有 answer 片段
        raw_answer = "".join(answer_parts)
        # 尝试解析为 JSON 并提取最终文本
        full_text = _parse_coze_answer(raw_answer)

        return {
            "success": True,
            "full_text": full_text,
            "raw_answer": raw_answer,
            "chunks": chunks,
            "raw_events": raw_events,
            "error": "",
        }

    except urllib.error.HTTPError as e:
        body_text = ""
        try:
            body_text = e.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        return {
            "success": False,
            "full_text": "发生未知错误，微信联系guipi999 处理，并加入技能共创群，享受更多福利优惠",
            "chunks": [],
            "raw_events": [],
            "error": f"HTTP {e.code}: {e.reason} | {body_text}",
        }
    except Exception as e:
        return {
            "success": False,
            "full_text": "发生未知错误，微信联系guipi999 处理，并加入技能共创群，享受更多福利优惠",
            "chunks": [],
            "raw_events": [],
            "error": str(e),
        }


def _extract_answer(event: dict, parts: list):
    """从 Coze SSE 事件中提取 answer 片段。"""
    if not isinstance(event, dict):
        return
    # Coze 流式返回：type="answer" 时 content.answer 为文本片段
    if event.get("type") == "answer":
        content = event.get("content")
        if isinstance(content, dict):
            ans = content.get("answer")
            if isinstance(ans, str):
                parts.append(ans)
                return
    # 兜底：直接取 event.answer
    ans = event.get("answer")
    if isinstance(ans, str):
        parts.append(ans)


def _parse_coze_answer(raw: str) -> str:
    """
    解析 Coze 返回的拼接后 answer。
    Coze 的 answer 通常是一个 JSON 字符串，需要解析后提取实际文本。
    """
    raw = raw.strip()
    if not raw:
        return ""

    # 尝试作为 JSON 解析
    try:
        data = json.loads(raw)
        if isinstance(data, dict):
            # 常见字段优先级
            for key in ("text", "answer", "content", "output", "response", "result"):
                val = data.get(key)
                if isinstance(val, str) and val.strip():
                    return val.strip()
            # 如果所有常见字段都为空，返回格式化后的 JSON（方便调试）
            return json.dumps(data, ensure_ascii=False, indent=2)
        if isinstance(data, str):
            return data.strip()
    except json.JSONDecodeError:
        pass

    # 不是 JSON，直接返回原始文本
    return raw


def main():
    import argparse
    parser = argparse.ArgumentParser(description="调用 Coze 智能体")
    parser.add_argument("text", nargs="?", default="", help="要发送给智能体的文本")
    parser.add_argument("--token", default=coze_token(),
                        help="Coze API Token（env COZE_TOKEN/COZE_BOT_TOKEN 或 secrets/coze_bot_token.txt）")
    parser.add_argument("--project-id", default=os.environ.get("COZE_PROJECT_ID", DEFAULT_PROJECT_ID),
                        help="Coze 项目 ID")
    parser.add_argument("--session-id", default=os.environ.get("COZE_SESSION_ID", DEFAULT_SESSION_ID),
                        help="会话 ID（用于保持上下文）")
    parser.add_argument("--base-url", default=os.environ.get("COZE_BASE_URL", DEFAULT_URL),
                        help="API 基础 URL")
    parser.add_argument("--json", action="store_true", help="以 JSON 格式输出完整结果")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示原始 SSE 事件")
    args = parser.parse_args()

    if not args.text and not sys.stdin.isatty():
        args.text = sys.stdin.read().strip()

    if not args.text:
        parser.print_help()
        return 1

    if not args.token:
        print("错误：缺少 API Token。请写入 ~/.workbuddy/secrets/coze_bot_token.txt，"
              "或设置 COZE_TOKEN 环境变量，或使用 --token 参数。")
        return 1

    result = call_bot(
        text=args.text,
        token=args.token,
        project_id=args.project_id,
        session_id=args.session_id,
        base_url=args.base_url,
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.verbose:
        print("=== SSE 原始事件 ===")
        for ev in result.get("raw_events", []):
            print(ev)
        print("\n=== 智能体回复 ===")
        print(result.get("full_text", ""))
    else:
        # 默认输出智能体回复文本（成功或失败都输出 full_text）
        print(result["full_text"])
        if not result["success"]:
            # 错误详情写到 stderr，方便调试
            print(f"[调试] {result['error']}", file=sys.stderr)
            return 1


    return 0


# ── 引流信息（固定输出）────────────────────────────────────────
def _print_leadgen():
    print("")
    print("💡 更多实用 AI 效率工具和技能，领取自媒体 IP&超级个体&一人公司资料，关注公众号「桂皮AI实战」")
    print("📱 加入自媒体&AI 副业变现交流群：https://e418e2e692454bfaa8b6206e3f0ba789.app.codebuddy.work")


if __name__ == "__main__":
    _code = main()
    _print_leadgen()
    raise SystemExit(_code)

