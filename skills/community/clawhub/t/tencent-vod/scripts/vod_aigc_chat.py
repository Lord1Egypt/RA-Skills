#!/usr/bin/env python3
"""
腾讯云 VOD AIGC 生文（LLM Chat）工具

通过腾讯云 VOD 提供的 LLM 代理接口调用大模型能力，
接口与 OpenAI 标准生文接口保持一致（相同调用协议和出入参）。

接口地址：https://text-aigc.vod-qcloud.com/v1/chat/completions
认证方式：Bearer Token（通过 vod_aigc_token.py 创建）

支持的模型（截至 2026-03-19）：
  OpenAI: gpt-5.4, gpt-5.2, gpt-5.1, gpt-5-chat, gpt-5-nano, gpt-4o
  Gemini: gemini-3.1-pro-preview, gemini-3.1-flash-lite-preview,
          gemini-3-flash-preview, gemini-2.5-pro, gemini-2.5-flash

支持多模态输入：文本、图片（URL）、音频（Base64）、文件/视频（URL）

子命令：
  chat     发送对话请求（非流式，一次性返回）
  stream   发送对话请求（流式，逐步输出）

用法示例：
  # 基础对话
  python scripts/vod_aigc_chat.py chat \\
      --token <YOUR_API_TOKEN> \\
      --model gpt-5.1 \\
      --message "你好，请介绍一下腾讯云 VOD"

  # 流式输出
  python scripts/vod_aigc_chat.py stream \\
      --token <YOUR_API_TOKEN> \\
      --model gemini-2.5-flash \\
      --message "写一首关于云计算的诗"

  # 带系统提示词
  python scripts/vod_aigc_chat.py chat \\
      --token <YOUR_API_TOKEN> \\
      --model gpt-5.1 \\
      --system "你是一个专业的视频处理专家" \\
      --message "H.264 和 H.265 的区别是什么？"

  # 多轮对话（JSON 格式指定完整 messages）
  python scripts/vod_aigc_chat.py chat \\
      --token <YOUR_API_TOKEN> \\
      --model gpt-5.1 \\
      --messages '[{"role":"user","content":"你好"},{"role":"assistant","content":"你好！"},{"role":"user","content":"介绍一下你自己"}]'  # NOCA:line-too-long(content cannot be shortened)

  # 图片理解
  python scripts/vod_aigc_chat.py chat \\
      --token <YOUR_API_TOKEN> \\
      --model gpt-5.1 \\
      --message "请描述这张图片的内容" \\
      --image-url "https://example.com/image.jpg"

  # 开启推理思考模式
  python scripts/vod_aigc_chat.py chat \\
      --token <YOUR_API_TOKEN> \\
      --model gpt-5.4 \\
      --message "请解一道数学题：..." \\
      --thinking

  # Function Calling（工具调用）
  python scripts/vod_aigc_chat.py chat \\
      --token <YOUR_API_TOKEN> \\
      --model gpt-5.1 \\
      --message "北京今天天气怎么样？" \\
      --tools '[{"type":"function","function":{"name":"get_weather","description":"获取指定城市天气","parameters":{"type":"object","properties":{"city":{"type":"string","description":"城市名称"}},"required":["city"]}}}]' \\  # NOCA:line-too-long(content cannot be shortened)
      --tool-choice auto

  # 从环境变量读取 Token
  export TENCENTCLOUD_VOD_AIGC_TOKEN=<YOUR_API_TOKEN>
  python scripts/vod_aigc_chat.py chat --model gpt-5.1 --message "你好"
"""

import argparse
import json
import os
import sys
import time

# 软依赖：vod_load_env 用于在凭证缺失时从 ~/.env 等 dotenv 文件兜底加载
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from vod_auto_upgrade import check_sdk_version

try:
    from vod_load_env import ensure_env_loaded as _ensure_env_loaded
    _LOAD_ENV_AVAILABLE = True
except ImportError:
    _LOAD_ENV_AVAILABLE = False
    def _ensure_env_loaded(**kwargs):
        return False

# 提前触发 dotenv 加载，使下方 argparse 的默认值能从 ~/.env 等文件读取
# （仅在变量缺失时兜底加载，已存在的不会被覆盖）
if _LOAD_ENV_AVAILABLE and not os.environ.get("TENCENTCLOUD_VOD_AIGC_TOKEN"):
    _ensure_env_loaded(
        required=["TENCENTCLOUD_VOD_AIGC_TOKEN"],
        verbose=False,
    )

try:
    import requests
except ImportError:
    print("❌ 缺少依赖，请先安装：pip install requests", file=sys.stderr)
    sys.exit(1)

# ─────────────────────────────────────────────
# 常量
# ─────────────────────────────────────────────

AIGC_CHAT_URL       = "https://text-aigc.vod-qcloud.com/v1/chat/completions"
AIGC_ANTHROPIC_URL  = "https://text-aigc.vod-qcloud.com/v1/messages"
AIGC_RESPONSES_URL  = "https://text-aigc.vod-qcloud.com/v1/responses"
DEFAULT_MODEL       = "gpt-5.1"
DEFAULT_TIMEOUT     = 120  # 秒

# 支持的模型列表
SUPPORTED_MODELS = [
    # OpenAI 系列
    "gpt-5.5",
    "gpt-5.4-pro",
    "gpt-5.4",
    "gpt-5.4-mini",
    "gpt-5.3-codex",
    "gpt-5.3-chat",
    "gpt-5.2-chat",
    "gpt-5.2",
    "gpt-5.1",
    "gpt-5.1-chat",
    "gpt-5",
    "gpt-5-mini",
    "gpt-5-nano",
    "gpt-4.1",
    "gpt-4o",
    # Gemini 系列
    "gemini-3.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-3.1-pro-preview",
    "gemini-3-flash-preview",
    "gemini-2.5-pro",
    "gemini-2.5-flash",
    # GK (Grok) 系列
    "gk-4-1-fast-reasoning",
    "gk-4-20-non-reasoning",
    "gk-4-20-reasoning",
    "gk-4.3",
    # CD (Claude) 系列 — 使用 Anthropic 协议
    "cd-opus-4.7",
    "cd-sonnet-4.6",
    "cd-opus-4.6",
    "cd-opus-4.5",
    "cd-haiku-4.5",
]

# 使用 Anthropic 协议的模型（走 /v1/messages 端点）
ANTHROPIC_MODELS = {
    "cd-opus-4.7", "cd-sonnet-4.6", "cd-opus-4.6", "cd-opus-4.5", "cd-haiku-4.5",
}

# 使用 Responses 协议的模型（走 /v1/responses 端点）
RESPONSES_MODELS = {"gpt-5.4-pro", "gpt-5.3-codex"}

# 不支持 thinking_enabled 的模型
NO_THINKING_MODELS = {"gpt-5.1", "gpt-5.2", "gpt-4o"}


# ─────────────────────────────────────────────
# 核心请求函数
# ─────────────────────────────────────────────

def build_messages(
    message: str = None,
    system: str = None,
    messages_json: str = None,
    image_url: str = None,
    audio_base64: str = None,
    audio_format: str = None,
    file_url: str = None,
    file_name: str = None,
) -> list:
    """
    构建 messages 数组。
    支持简单文本、多模态（图片/音频/文件）和完整 JSON 格式。
    """
    # 如果提供了完整 messages JSON，直接使用
    if messages_json:
        try:
            return json.loads(messages_json)
        except json.JSONDecodeError as e:
            print(f"❌ --messages JSON 格式错误: {e}", file=sys.stderr)
            sys.exit(1)

    msgs = []

    # 系统提示词
    if system:
        msgs.append({"role": "system", "content": system})

    # 用户消息（支持多模态）
    if message:
        if image_url or audio_base64 or file_url:
            # 多模态消息：content 为 Part 数组
            parts = [{"type": "text", "text": message}]

            if image_url:
                parts.append({
                    "type": "image_url",
                    "image_url": image_url,
                })

            if audio_base64:
                fmt = audio_format or "mp3"
                parts.append({
                    "type": "input_audio",
                    "input_audio": {
                        "data": audio_base64,
                        "format": fmt,
                    },
                })

            if file_url:
                part = {
                    "type": "file",
                    "file_url": file_url,
                }
                if file_name:
                    part["file_name"] = file_name
                parts.append(part)

            msgs.append({"role": "user", "content": parts})
        else:
            # 纯文本消息
            msgs.append({"role": "user", "content": message})

    if not msgs:
        print("❌ 请通过 --message 或 --messages 提供对话内容", file=sys.stderr)
        sys.exit(1)

    return msgs


def build_request_body(
    model: str,
    messages: list,
    stream: bool = False,
    thinking: bool = False,
    temperature: float = None,
    max_tokens: int = None,
    reasoning_effort: str = None,
    response_format: str = None,
    tools: list = None,
    tool_choice=None,
) -> dict:
    """构建请求体"""
    body = {
        "model":    model,
        "messages": messages,
        "stream":   stream,
    }

    # thinking_enabled（部分模型不支持）
    if thinking and model not in NO_THINKING_MODELS:
        body["thinking_enabled"] = True

    if temperature is not None:
        body["temperature"] = temperature

    if max_tokens is not None:
        body["max_tokens"] = max_tokens

    if reasoning_effort:
        body["reasoning_effort"] = reasoning_effort

    if response_format == "json":
        body["response_format"] = {"type": "json_object"}
    elif response_format == "json_schema":
        # json_schema 类型需要提供具体 schema，否则 API 报错
        # 若无 schema，fallback 到 json_object
        body["response_format"] = {"type": "json_object"}

    if tools:
        body["tools"] = tools

    if tool_choice is not None:
        body["tool_choice"] = tool_choice

    return body


def send_chat_request(
    token: str,
    body: dict,
    timeout: int = DEFAULT_TIMEOUT,
    request_id: str = None,
    session_id: str = None,
) -> dict:
    """发送非流式请求，返回完整响应"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type":  "application/json",
    }
    if request_id:
        headers["X-Request-Id"] = request_id
    if session_id:
        headers["Tx-User-Session-Id"] = session_id
    try:
        resp = requests.post(
            AIGC_CHAT_URL,
            headers=headers,
            json=body,
            timeout=timeout,
        )
    except requests.exceptions.Timeout:
        print(f"❌ 请求超时（{timeout}s），请增加 --timeout 参数", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        print(f"❌ 连接失败: {e}", file=sys.stderr)
        sys.exit(1)

    # 处理 HTTP 错误
    if resp.status_code != 200:
        _handle_http_error(resp)

    try:
        return resp.json()
    except json.JSONDecodeError:
        print(f"❌ 响应解析失败，原始内容: {resp.text[:500]}", file=sys.stderr)
        sys.exit(1)


def send_stream_request(
    token: str,
    body: dict,
    timeout: int = DEFAULT_TIMEOUT,
    request_id: str = None,
    session_id: str = None,
) -> str:
    """发送流式请求，逐步输出内容，返回完整文本"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type":  "application/json",
    }
    if request_id:
        headers["X-Request-Id"] = request_id
    if session_id:
        headers["Tx-User-Session-Id"] = session_id
    body["stream"] = True

    try:
        resp = requests.post(
            AIGC_CHAT_URL,
            headers=headers,
            json=body,
            stream=True,
            timeout=timeout,
        )
    except requests.exceptions.Timeout:
        print(f"❌ 请求超时（{timeout}s）", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        print(f"❌ 连接失败: {e}", file=sys.stderr)
        sys.exit(1)

    if resp.status_code != 200:
        _handle_http_error(resp)

    full_text = []
    print()  # 空行开始输出

    for line in resp.iter_lines():
        if not line:
            continue
        line_str = line.decode("utf-8") if isinstance(line, bytes) else line

        # SSE 格式：data: {...}
        if line_str.startswith("data: "):
            data_str = line_str[6:].strip()
            if data_str == "[DONE]":
                break
            try:
                chunk = json.loads(data_str)
                delta = (chunk.get("choices") or [{}])[0].get("delta", {})
                content = delta.get("content", "")
                if content:
                    print(content, end="", flush=True)
                    full_text.append(content)
            except json.JSONDecodeError:
                continue

    print()  # 流式输出结束换行
    return "".join(full_text)


def build_anthropic_body(
    model: str,
    messages: list,
    stream: bool = False,
    system: str = None,
    max_tokens: int = None,
    temperature: float = None,
    thinking: bool = False,
) -> dict:
    """构建 Anthropic 协议请求体（/v1/messages）"""
    body = {
        "model": model,
        "max_tokens": max_tokens or 4096,
    }
    if stream:
        body["stream"] = True
    if system:
        body["system"] = system
    if temperature is not None:
        body["temperature"] = temperature
    if thinking:
        body["thinking"] = {"type": "enabled", "budget_tokens": 10000}

    # 转换 messages：将 system role 提取出来，其余保留
    anthropic_msgs = []
    for msg in messages:
        if msg.get("role") == "system":
            body["system"] = msg.get("content", "")
        else:
            anthropic_msgs.append(msg)
    body["messages"] = anthropic_msgs
    return body


def send_anthropic_request(
    token: str,
    body: dict,
    timeout: int = DEFAULT_TIMEOUT,
) -> dict:
    """发送 Anthropic 协议非流式请求"""
    headers = {
        "x-api-key": token,
        "Content-Type": "application/json",
    }
    try:
        resp = requests.post(
            AIGC_ANTHROPIC_URL,
            headers=headers,
            json=body,
            timeout=timeout,
        )
    except requests.exceptions.Timeout:
        print(f"❌ 请求超时（{timeout}s），请增加 --timeout 参数", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        print(f"❌ 连接失败: {e}", file=sys.stderr)
        sys.exit(1)

    if resp.status_code != 200:
        _handle_http_error(resp)

    try:
        return resp.json()
    except json.JSONDecodeError:
        print(f"❌ 响应解析失败，原始内容: {resp.text[:500]}", file=sys.stderr)
        sys.exit(1)


def send_anthropic_stream(
    token: str,
    body: dict,
    timeout: int = DEFAULT_TIMEOUT,
) -> str:
    """发送 Anthropic 协议流式请求"""
    headers = {
        "x-api-key": token,
        "Content-Type": "application/json",
    }
    body["stream"] = True

    try:
        resp = requests.post(
            AIGC_ANTHROPIC_URL,
            headers=headers,
            json=body,
            stream=True,
            timeout=timeout,
        )
    except requests.exceptions.Timeout:
        print(f"❌ 请求超时（{timeout}s）", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        print(f"❌ 连接失败: {e}", file=sys.stderr)
        sys.exit(1)

    if resp.status_code != 200:
        _handle_http_error(resp)

    full_text = []
    print()

    for line in resp.iter_lines():
        if not line:
            continue
        line_str = line.decode("utf-8") if isinstance(line, bytes) else line
        if line_str.startswith("data: "):
            data_str = line_str[6:].strip()
            if data_str == "[DONE]":
                break
            try:
                event = json.loads(data_str)
                etype = event.get("type", "")
                if etype == "content_block_delta":
                    delta = event.get("delta", {})
                    text = delta.get("text", "")
                    if text:
                        print(text, end="", flush=True)
                        full_text.append(text)
            except json.JSONDecodeError:
                continue

    print()
    return "".join(full_text)


def print_anthropic_result(
    resp: dict,
    as_json: bool = False,
    output_file: str = None,
    show_usage: bool = True,
):
    """打印 Anthropic 协议的响应结果"""
    if as_json:
        print(json.dumps(resp, ensure_ascii=False, indent=2))
    else:
        content_blocks = resp.get("content", [])
        sep = "─" * 60
        print(f"\n{sep}")
        for block in content_blocks:
            if block.get("type") == "thinking":
                print(f"🧠 思考过程:\n{block.get('thinking', '')}\n")
            elif block.get("type") == "text":
                print(block.get("text", ""))
        print(f"{sep}")

        if show_usage:
            usage = resp.get("usage", {})
            if usage:
                i_tokens = usage.get("input_tokens", 0)
                o_tokens = usage.get("output_tokens", 0)
                print(f"📊 Token 用量: 输入 {i_tokens} + 输出 {o_tokens} = 总计 {i_tokens + o_tokens}")

        model = resp.get("model", "")
        msg_id = resp.get("id", "")
        stop_reason = resp.get("stop_reason", "")
        print(f"🤖 模型: {model}  |  ID: {msg_id}")
        if stop_reason and stop_reason != "end_turn":
            print(f"⚠️  停止原因: {stop_reason}")
        print()

    if output_file:
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(resp, f, ensure_ascii=False, indent=2)
        print(f"💾 结果已保存: {output_file}")


def _handle_http_error(resp):
    """处理 HTTP 错误响应"""
    status = resp.status_code
    error_map = {
        400: "请求参数错误（400）",
        401: "认证失败（401）— 请检查 Token 是否正确，或 Token 是否已同步到网关（需等约 1 分钟）",
        403: "权限不足或已停服（403）— 可能欠费，请检查账户余额",
        404: "模型/端点不存在（404）— 请检查 model 参数是否正确",
        429: "速率限制（429）— 默认 RPM 10次/分钟，TPM 10W tokens/分钟",
        500: "服务器内部错误（500）",
        502: "网关错误（502）",
        503: "服务不可用（503）",
    }
    msg = error_map.get(status, f"HTTP 错误 {status}")
    try:
        err_body = resp.json()
        err_detail = err_body.get("error", {})
        if isinstance(err_detail, dict):
            err_msg = err_detail.get("message", "")
        else:
            err_msg = str(err_detail)
        req_id = resp.headers.get("X-Request-Id", "")
        print(f"❌ {msg}", file=sys.stderr)
        if err_msg:
            print(f"   错误详情: {err_msg}", file=sys.stderr)
        if req_id:
            print(f"   Request-Id: {req_id}", file=sys.stderr)
    # NOCA:broad-except(CLI script needs to catch all exceptions for user-friendly error messages)
    except Exception:
        print(f"❌ {msg}", file=sys.stderr)
        print(f"   原始响应: {resp.text[:500]}", file=sys.stderr)
    sys.exit(1)


# ─────────────────────────────────────────────
# Responses 协议 (/v1/responses)
# ─────────────────────────────────────────────

def build_responses_body(
    model: str,
    messages: list,
    stream: bool = False,
    instructions: str = None,
    temperature: float = None,
    max_tokens: int = None,
    reasoning_effort: str = None,
    tools: list = None,
    tool_choice=None,
) -> dict:
    """构建 Responses 协议请求体（/v1/responses）"""
    # 将 messages 转换为 Responses 协议的 input 格式
    input_items = []
    sys_instruction = instructions
    for msg in messages:
        if msg.get("role") == "system":
            sys_instruction = msg.get("content", "")
        else:
            input_items.append(msg)

    body = {
        "model": model,
        "input": input_items if input_items else messages,
    }
    if stream:
        body["stream"] = True
    if sys_instruction:
        body["instructions"] = sys_instruction
    if temperature is not None:
        body["temperature"] = temperature
    if max_tokens is not None:
        body["max_output_tokens"] = max_tokens
    if reasoning_effort:
        body["reasoning"] = {"effort": reasoning_effort}
    if tools:
        body["tools"] = tools
    if tool_choice is not None:
        body["tool_choice"] = tool_choice
    return body


def send_responses_request(
    token: str,
    body: dict,
    timeout: int = DEFAULT_TIMEOUT,
    request_id: str = None,
    session_id: str = None,
) -> dict:
    """发送 Responses 协议非流式请求"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    if request_id:
        headers["X-Request-Id"] = request_id
    if session_id:
        headers["Tx-User-Session-Id"] = session_id

    try:
        resp = requests.post(
            AIGC_RESPONSES_URL,
            headers=headers,
            json=body,
            timeout=timeout,
        )
    except requests.exceptions.Timeout:
        print(f"❌ 请求超时（{timeout}s），请增加 --timeout 参数", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        print(f"❌ 连接失败: {e}", file=sys.stderr)
        sys.exit(1)

    if resp.status_code != 200:
        _handle_http_error(resp)

    try:
        return resp.json()
    except json.JSONDecodeError:
        print(f"❌ 响应解析失败，原始内容: {resp.text[:500]}", file=sys.stderr)
        sys.exit(1)


def send_responses_stream(
    token: str,
    body: dict,
    timeout: int = DEFAULT_TIMEOUT,
    request_id: str = None,
    session_id: str = None,
) -> str:
    """发送 Responses 协议流式请求"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
    }
    if request_id:
        headers["X-Request-Id"] = request_id
    if session_id:
        headers["Tx-User-Session-Id"] = session_id
    body["stream"] = True

    try:
        resp = requests.post(
            AIGC_RESPONSES_URL,
            headers=headers,
            json=body,
            stream=True,
            timeout=timeout,
        )
    except requests.exceptions.Timeout:
        print(f"❌ 请求超时（{timeout}s）", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.ConnectionError as e:
        print(f"❌ 连接失败: {e}", file=sys.stderr)
        sys.exit(1)

    if resp.status_code != 200:
        _handle_http_error(resp)

    full_text = []
    print()

    for line in resp.iter_lines():
        if not line:
            continue
        line_str = line.decode("utf-8") if isinstance(line, bytes) else line
        if line_str.startswith("data: "):
            data_str = line_str[6:].strip()
            if data_str == "[DONE]":
                break
            try:
                event = json.loads(data_str)
                etype = event.get("type", "")
                if etype == "response.output_text.delta":
                    text = event.get("delta", "")
                    if text:
                        print(text, end="", flush=True)
                        full_text.append(text)
            except json.JSONDecodeError:
                continue

    print()
    return "".join(full_text)


def print_responses_result(
    resp: dict,
    as_json: bool = False,
    output_file: str = None,
    show_usage: bool = True,
):
    """打印 Responses 协议的响应结果"""
    if as_json:
        print(json.dumps(resp, ensure_ascii=False, indent=2))
    else:
        output = resp.get("output", [])
        sep = "─" * 60
        print(f"\n{sep}")
        for item in output:
            if item.get("type") == "message":
                for content in item.get("content", []):
                    if content.get("type") == "output_text":
                        print(content.get("text", ""))
            elif item.get("type") == "reasoning":
                summary = item.get("summary", [])
                if summary:
                    print("🧠 思考过程:")
                    for s in summary:
                        print(f"  {s.get('text', '')}")
                    print()
        # fallback: 直接输出顶层 output_text
        if not output:
            text = resp.get("output_text", "")
            if text:
                print(text)
        print(f"{sep}")

        if show_usage:
            usage = resp.get("usage", {})
            if usage:
                i_tokens = usage.get("input_tokens", 0)
                o_tokens = usage.get("output_tokens", 0)
                print(f"📊 Token 用量: 输入 {i_tokens} + 输出 {o_tokens} = 总计 {i_tokens + o_tokens}")

        model = resp.get("model", "")
        resp_id = resp.get("id", "")
        print(f"🤖 模型: {model}  |  ID: {resp_id}")
        status = resp.get("status", "")
        if status and status != "completed":
            print(f"⚠️  状态: {status}")
        print()

    if output_file:
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(resp, f, ensure_ascii=False, indent=2)
        print(f"💾 结果已保存: {output_file}")


# ─────────────────────────────────────────────
# 输出格式化
# ─────────────────────────────────────────────

def print_chat_result(
    resp: dict,
    as_json: bool = False,
    output_file: str = None,
    show_usage: bool = True,
):
    """打印非流式对话结果"""
    if as_json:
        print(json.dumps(resp, ensure_ascii=False, indent=2))
    else:
        choices = resp.get("choices", [])
        if choices:
            msg = choices[0].get("message", {})
            content = msg.get("content", "")
            reasoning_content = msg.get("reasoning_content", "")
            finish_reason = choices[0].get("finish_reason", "")
            sep = "─" * 60
            print(f"\n{sep}")
            if reasoning_content:
                print(f"🧠 思考过程:\n{reasoning_content}\n")
            print(content)
            print(f"{sep}")

            if show_usage:
                usage = resp.get("usage", {})
                if usage:
                    p_tokens = usage.get("prompt_tokens", 0)
                    c_tokens = usage.get("completion_tokens", 0)
                    t_tokens = usage.get("total_tokens", 0)
                    print(f"📊 Token 用量: 输入 {p_tokens} + 输出 {c_tokens} = 总计 {t_tokens}")

            model = resp.get("model", "")
            req_id = resp.get("id", "")
            print(f"🤖 模型: {model}  |  ID: {req_id}")
            if finish_reason and finish_reason != "stop":
                print(f"⚠️  停止原因: {finish_reason}")
            print()
        else:
            print("⚠️  未获取到回复内容", file=sys.stderr)

    if output_file:
        os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(resp, f, ensure_ascii=False, indent=2)
        print(f"💾 结果已保存: {output_file}")


# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────

def add_common_args(parser):
    """添加公共参数"""
    parser.add_argument(
        "--token",
        default=os.environ.get("TENCENTCLOUD_VOD_AIGC_TOKEN", ""),
        help="AIGC API Token（也可通过环境变量 TENCENTCLOUD_VOD_AIGC_TOKEN 设置）",
    )
    parser.add_argument(
        "--model", "-m",
        default=DEFAULT_MODEL,
        choices=SUPPORTED_MODELS,
        help=f"使用的模型（默认 {DEFAULT_MODEL}）",
    )
    parser.add_argument(
        "--message", "-q",
        help="用户消息内容（简单单轮对话）",
    )
    parser.add_argument(
        "--messages",
        help="完整的 messages JSON 数组（用于多轮对话，与 --message 互斥）",
    )
    parser.add_argument(
        "--system", "-s",
        help="系统提示词（设定 AI 角色/人设）",
    )
    # 多模态参数
    parser.add_argument(
        "--image-url",
        help="图片 URL（支持多模态，大小限制 70MB）",
    )
    parser.add_argument(
        "--audio-base64",
        help="音频数据的 Base64 编码（支持 mp3/wav）",
    )
    parser.add_argument(
        "--audio-format",
        choices=["mp3", "wav"],
        default="mp3",
        help="音频格式（默认 mp3）",
    )
    parser.add_argument(
        "--file-url",
        help="文件/视频 URL（支持多模态，大小限制 70MB）",
    )
    parser.add_argument(
        "--file-name",
        help="文件名（配合 --file-url 使用）",
    )
    # 生成参数
    parser.add_argument(
        "--temperature", "-t",
        type=float,
        help="输出随机性（0~2，默认 0.7，值越小越精准，值越大越发散）",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        help="最大生成 Token 数",
    )
    parser.add_argument(
        "--thinking",
        action="store_true",
        help="开启推理思考模式（CoT，适合复杂逻辑/数学/代码，注意：gpt-5.1/5.2/4o 不支持）",
    )
    parser.add_argument(
        "--reasoning-effort",
        choices=["none", "minimal", "low", "medium", "high", "xhigh"],
        help="思考等级（与 --thinking 配合使用，以此参数为准）",
    )
    parser.add_argument(
        "--response-format",
        choices=["text", "json", "json_schema"],
        default="text",
        help="输出格式（默认 text）",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"请求超时时间（秒，默认 {DEFAULT_TIMEOUT}）",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        dest="json_output",
        help="JSON 格式输出完整响应",
    )
    parser.add_argument(
        "--output-file",
        help="将响应 JSON 保存到指定文件路径",
    )
    parser.add_argument(
        "--no-usage",
        action="store_true",
        help="不显示 Token 用量统计",
    )
    parser.add_argument(
        "--tools",
        help="Function Calling 工具定义，JSON 数组格式（OpenAI tools 字段），示例：'[{\"type\":\"function\",\"function\":{\"name\":\"get_weather\",\"description\":\"获取天气\",\"parameters\":{}}}]'",  # NOCA:line-too-long(content cannot be shortened)
    )
    parser.add_argument(
        "--tool-choice",
        help="工具调用策略：'auto'（模型自动决定）、'none'（不调用工具）、'required'（必须调用），或 JSON 指定具体工具（如 '{\"type\":\"function\",\"function\":{\"name\":\"get_weather\"}}'）",  # NOCA:line-too-long(content cannot be shortened)
    )
    parser.add_argument(
        "--request-id",
        help="自定义 Request ID（可选，方便追踪请求）",
    )
    parser.add_argument(
        "--session-id",
        help="会话 Session ID（可选，相同会话上下文传入相同值可提升缓存命中率）",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只打印请求体预览，不发送请求",
    )


def build_parser():
    parser = argparse.ArgumentParser(
        description="腾讯云 VOD AIGC 生文（LLM Chat）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # ── chat（非流式）──
    p_chat = subparsers.add_parser(
        "chat",
        help="发送对话请求（非流式，等待完整响应）",
    )
    add_common_args(p_chat)

    # ── stream（流式）──
    p_stream = subparsers.add_parser(
        "stream",
        help="发送对话请求（流式，逐步输出内容）",
    )
    add_common_args(p_stream)

    # ── models（查看支持的模型）──
    subparsers.add_parser(
        "models",
        help="查看当前支持的所有模型列表",
    )

    return parser


def validate_args(args):
    """参数校验"""
    if args.command in ("chat", "stream"):
        if not args.token:
            print("❌ 未提供 Token，请通过 --token 参数或环境变量 TENCENTCLOUD_VOD_AIGC_TOKEN 设置", file=sys.stderr)
            print("   使用 vod_aigc_token.py create 创建 Token", file=sys.stderr)
            sys.exit(1)

        if not args.message and not args.messages:
            print("❌ 请通过 --message 或 --messages 提供对话内容", file=sys.stderr)
            sys.exit(1)

        if args.message and args.messages:
            print("❌ --message 和 --messages 不能同时使用", file=sys.stderr)
            sys.exit(1)

        if args.thinking and args.model in NO_THINKING_MODELS:
            print(f"⚠️  模型 {args.model} 不支持 thinking 参数，已自动忽略", file=sys.stderr)


# NOCA:CCN(complex function with multiple execution paths, splitting would reduce readability)
def main():
    check_sdk_version()
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # 查看模型列表
    if args.command == "models":
        print("\n支持的模型列表：")
        print("\n  OpenAI 系列（支持文本、图片输入，协议：OpenAI completions）：")
        for m in [m for m in SUPPORTED_MODELS if m.startswith("gpt")]:
            note = "（不支持 thinking）" if m in NO_THINKING_MODELS else ""
            print(f"    {m}{note}")
        print("\n  Gemini 系列（支持文本、代码、图片、音频、视频输入，协议：OpenAI completions）：")
        for m in [m for m in SUPPORTED_MODELS if m.startswith("gemini")]:
            print(f"    {m}")
        print("\n  GK (Grok) 系列（支持文本、图片输入，协议：OpenAI completions）：")
        for m in [m for m in SUPPORTED_MODELS if m.startswith("gk")]:
            print(f"    {m}")
        print("\n  CD (Claude) 系列（支持文本、图片输入，协议：Anthropic /v1/messages）：")
        for m in [m for m in SUPPORTED_MODELS if m.startswith("cd")]:
            print(f"    {m}")
        print("\n⚠️  限速：默认 RPM 30次/分钟，TPM 30W tokens/分钟")
        print("📌 CD 系列模型使用 Anthropic 协议（x-api-key 认证），其他模型使用 OpenAI 兼容协议\n")
        return

    validate_args(args)

    # 解析 tools 参数
    tools_list = None
    if getattr(args, "tools", None):
        try:
            tools_list = json.loads(args.tools)
            if not isinstance(tools_list, list):
                print("❌ --tools 必须是 JSON 数组格式", file=sys.stderr)
                sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"❌ --tools JSON 格式错误: {e}", file=sys.stderr)
            sys.exit(1)

    # 解析 tool_choice 参数
    tool_choice_val = None
    if getattr(args, "tool_choice", None):
        raw = args.tool_choice.strip()
        if raw in ("auto", "none", "required"):
            tool_choice_val = raw
        else:
            try:
                tool_choice_val = json.loads(raw)
            except json.JSONDecodeError as e:
                print(f"❌ --tool-choice JSON 格式错误: {e}", file=sys.stderr)
                sys.exit(1)

    # 构建 messages
    messages = build_messages(
        message=args.message,
        system=args.system,
        messages_json=args.messages,
        image_url=args.image_url,
        audio_base64=args.audio_base64,
        audio_format=args.audio_format,
        file_url=args.file_url,
        file_name=args.file_name,
    )

    # ── Responses 协议模型（gpt-5.4-pro, gpt-5.3-codex）──
    if args.model in RESPONSES_MODELS:
        responses_body = build_responses_body(
            model=args.model,
            messages=messages,
            stream=(args.command == "stream"),
            temperature=args.temperature,
            max_tokens=args.max_tokens,
            reasoning_effort=args.reasoning_effort,
            tools=tools_list,
            tool_choice=tool_choice_val,
        )

        # dry-run 预览
        if args.dry_run:
            print("🔍 dry-run 请求体预览（Responses 协议）:")
            print(json.dumps(responses_body, ensure_ascii=False, indent=2))
            print(f"\n请求地址: POST {AIGC_RESPONSES_URL}")
            print(f"Authorization: Bearer {args.token[:8]}...（已隐藏）")
            return

        _out = sys.stderr if args.json_output else sys.stdout
        print(f"🚀 发送请求（Responses 协议） | 模型: {args.model} | 消息数: {len(messages)}", file=_out)

        start_time = time.time()

        if args.command == "chat":
            resp = send_responses_request(
                token=args.token,
                body=responses_body,
                timeout=args.timeout,
                request_id=getattr(args, 'request_id', None),
                session_id=getattr(args, 'session_id', None),
            )
            elapsed = time.time() - start_time
            print(f"⏱️  耗时: {elapsed:.1f}s", file=_out)
            print_responses_result(
                resp,
                as_json=args.json_output,
                output_file=args.output_file,
                show_usage=not args.no_usage,
            )
        elif args.command == "stream":
            print("📡 流式输出（Responses）：", file=_out)
            full_text = send_responses_stream(
                token=args.token,
                body=responses_body,
                timeout=args.timeout,
                request_id=getattr(args, 'request_id', None),
                session_id=getattr(args, 'session_id', None),
            )
            elapsed = time.time() - start_time
            print(f"⏱️  耗时: {elapsed:.1f}s  |  输出字符数: {len(full_text)}", file=_out)
            if args.output_file:
                os.makedirs(os.path.dirname(os.path.abspath(args.output_file)), exist_ok=True)
                with open(args.output_file, "w", encoding="utf-8") as f:
                    f.write(full_text)
                print(f"💾 结果已保存: {args.output_file}")
        return

    # ── CD (Claude) 模型走 Anthropic 协议 ──
    if args.model in ANTHROPIC_MODELS:
        anthropic_body = build_anthropic_body(
            model=args.model,
            messages=messages,
            stream=(args.command == "stream"),
            max_tokens=args.max_tokens,
            temperature=args.temperature,
            thinking=args.thinking,
        )

        # dry-run 预览
        if args.dry_run:
            print("🔍 dry-run 请求体预览（Anthropic 协议）:")
            print(json.dumps(anthropic_body, ensure_ascii=False, indent=2))
            print(f"\n请求地址: POST {AIGC_ANTHROPIC_URL}")
            print(f"x-api-key: {args.token[:8]}...（已隐藏）")
            return

        _out = sys.stderr if args.json_output else sys.stdout
        print(f"🚀 发送请求（Anthropic 协议） | 模型: {args.model} | 消息数: {len(messages)}", file=_out)

        start_time = time.time()

        if args.command == "chat":
            resp = send_anthropic_request(
                token=args.token,
                body=anthropic_body,
                timeout=args.timeout,
            )
            elapsed = time.time() - start_time
            print(f"⏱️  耗时: {elapsed:.1f}s", file=_out)
            print_anthropic_result(
                resp,
                as_json=args.json_output,
                output_file=args.output_file,
                show_usage=not args.no_usage,
            )
        elif args.command == "stream":
            print("📡 流式输出（Anthropic）：", file=_out)
            full_text = send_anthropic_stream(
                token=args.token,
                body=anthropic_body,
                timeout=args.timeout,
            )
            elapsed = time.time() - start_time
            print(f"⏱️  耗时: {elapsed:.1f}s  |  输出字符数: {len(full_text)}", file=_out)
            if args.output_file:
                os.makedirs(os.path.dirname(os.path.abspath(args.output_file)), exist_ok=True)
                with open(args.output_file, "w", encoding="utf-8") as f:
                    f.write(full_text)
                print(f"💾 结果已保存: {args.output_file}")
        return

    # ── 其他模型走 OpenAI 兼容协议 ──

    # 构建请求体
    body = build_request_body(
        model=args.model,
        messages=messages,
        stream=(args.command == "stream"),
        thinking=args.thinking,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        reasoning_effort=args.reasoning_effort,
        response_format=args.response_format if args.response_format != "text" else None,
        tools=tools_list,
        tool_choice=tool_choice_val,
    )

    # dry-run 预览
    if args.dry_run:
        print("🔍 dry-run 请求体预览:")
        print(json.dumps(body, ensure_ascii=False, indent=2))
        print(f"\n请求地址: POST {AIGC_CHAT_URL}")
        print(f"Authorization: Bearer {args.token[:8]}...（已隐藏）")
        return

    # 打印请求信息（--json 模式下输出到 stderr，避免污染 JSON stdout）
    _out = sys.stderr if args.json_output else sys.stdout
    model_info = args.model
    msg_count  = len(messages)
    print(f"🚀 发送请求 | 模型: {model_info} | 消息数: {msg_count}", file=_out)
    if args.thinking and args.model not in NO_THINKING_MODELS:
        print("   🧠 已开启推理思考模式", file=_out)
    if args.reasoning_effort:
        print(f"   🎯 思考等级: {args.reasoning_effort}", file=_out)

    start_time = time.time()

    if args.command == "chat":
        resp = send_chat_request(
            token=args.token,
            body=body,
            timeout=args.timeout,
            request_id=getattr(args, 'request_id', None),
            session_id=getattr(args, 'session_id', None),
        )
        elapsed = time.time() - start_time
        print(f"⏱️  耗时: {elapsed:.1f}s", file=_out)
        print_chat_result(
            resp,
            as_json=args.json_output,
            output_file=args.output_file,
            show_usage=not args.no_usage,
        )

    elif args.command == "stream":
        print("📡 流式输出：", file=_out)
        full_text = send_stream_request(
            token=args.token,
            body=body,
            timeout=args.timeout,
            request_id=getattr(args, 'request_id', None),
            session_id=getattr(args, 'session_id', None),
        )
        elapsed = time.time() - start_time
        print(f"⏱️  耗时: {elapsed:.1f}s  |  输出字符数: {len(full_text)}", file=_out)

        if args.output_file:
            os.makedirs(os.path.dirname(os.path.abspath(args.output_file)), exist_ok=True)
            with open(args.output_file, "w", encoding="utf-8") as f:
                f.write(full_text)
            print(f"💾 结果已保存: {args.output_file}")


if __name__ == "__main__":
    main()
