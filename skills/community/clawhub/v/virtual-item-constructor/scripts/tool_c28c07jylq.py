#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agent Tool 调用脚本模版（Freemarker 渲染）

Freemarker 占位符：
  - ${agentCode}      Agent 编码
  - ${agentVersion}   Agent 版本
  - ${baseUrl}        服务基础地址，如 http://localhost:8080

无外部依赖，仅使用 Python 标准库

使用方式（渲染后）：
  python3 agent_tool_invoke.py '{"question": "你好", "systemParams": {}, "variables": {}}'
"""

import json
import sys
import urllib.request
import urllib.error

# ============================================================
# Freemarker 占位符（渲染时替换为真实值）
# ============================================================
AGENT_CODE = "agent_ce98dp66vb"
AGENT_VERSION = "0.0.3"
BASE_URL = "https://tao-agent-runtime.alibaba-inc.com"

# ============================================================
# 预设的系统参数与变量（导出时由 SkillExportRequest 注入）
# ============================================================
DEFAULT_SYSTEM_PARAMS = json.loads('{}')
DEFAULT_VARIABLES = json.loads('{}')

# ============================================================
# 默认配置
# ============================================================
POLLING_TIMEOUT_MS = 10000
MAX_POLLING_ROUNDS = 60
REQUEST_TIMEOUT = 600


def _do_post(url, payload):
    """通用 POST 请求方法"""
    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json; charset=utf-8"}
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            trace_id = resp.headers.get("EagleEye-TraceId", "")
            body = json.loads(resp.read().decode("utf-8"))
            return body, trace_id, None
    except urllib.error.HTTPError as e:
        trace_id = e.headers.get("EagleEye-TraceId", "") if e.headers else ""
        return None, trace_id, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return None, "", str(e.reason)
    except Exception as e:
        return None, "", str(e)


def simple_async_invoke(question, intent_code=None, media_list=None,
                        system_params=None, variables=None):
    """发起简化版异步 Agent Tool 调用，返回 (conversationId, messageId)"""
    merged_system_params = {**DEFAULT_SYSTEM_PARAMS, **(system_params or {})}
    merged_variables = {**DEFAULT_VARIABLES, **(variables or {})}

    url = f"{BASE_URL}/test/simpleAsyncInvoke"
    payload = {
        "agentCode": AGENT_CODE,
        "agentVersion": AGENT_VERSION,
        "question": question,
        "systemParams": merged_system_params,
        "variables": merged_variables,
    }
    if intent_code:
        payload["intentCode"] = intent_code
    if media_list:
        payload["mediaList"] = media_list

    body, trace_id, err = _do_post(url, payload)
    if err:
        print(f"simpleAsyncInvoke 请求失败, {err}, traceId={trace_id}")
        sys.exit(1)

    if not body.get("success"):
        print(f"simpleAsyncInvoke 失败: [{body.get('errCode')}] {body.get('errMsg')}, traceId={trace_id}")
        sys.exit(1)

    data = body["data"]
    return data["conversationId"], data["messageId"]


def long_polling(conversation_id, message_id):
    """长轮询获取 Agent Tool 执行结果"""
    url = f"{BASE_URL}/test/longPolling"
    payload = {
        "conversationId": conversation_id,
        "messageId": message_id,
        "timeout": POLLING_TIMEOUT_MS,
    }

    for i in range(1, MAX_POLLING_ROUNDS + 1):
        body, trace_id, err = _do_post(url, payload)
        if err:
            print(f"longPolling 请求失败, {err}, traceId={trace_id}")
            sys.exit(1)

        if not body.get("success"):
            print(f"longPolling 失败: [{body.get('errCode')}] {body.get('errMsg')}, traceId={trace_id}")
            sys.exit(1)

        data = body.get("data")
        if data is not None:
            return data

    print(f"长轮询超过最大轮次 {MAX_POLLING_ROUNDS}，Agent 未返回结果")
    sys.exit(1)


def main():
    if len(sys.argv) < 2:
        print("用法: python3 agent_tool_invoke.py '<json_string>'")
        sys.exit(1)

    params = json.loads(sys.argv[1])
    question = params.get("question", "")
    intent_code = params.get("intentCode")
    media_list = params.get("mediaList")
    system_params = params.get("systemParams", {})
    variables = params.get("variables", {})

    conversation_id, message_id = simple_async_invoke(
        question, intent_code, media_list, system_params, variables
    )

    result = long_polling(conversation_id, message_id)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

