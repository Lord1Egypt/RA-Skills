#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库搜索工具调用脚本模版（Freemarker 渲染）

Freemarker 占位符：
  - ${agentCode}      Agent 编码
  - ${agentVersion}   Agent 版本
  - ${baseUrl}        服务基础地址，如 http://localhost:8080
  - ${actionCode}     工具 actionCode
  - ${taskCode}       任务编码

无外部依赖，仅使用 Python 标准库

使用方式（渲染后）：
  python3 knowledge_search.py '{"query": "你好"}'
"""

import json
import sys
import urllib.request
import urllib.error

# ============================================================
# Freemarker 占位符（渲染时替换为真实值）
# ============================================================
AGENT_CODE = "agent_34a7cjmxpx"
AGENT_VERSION = "draft"
BASE_URL = "https://tao-agent-runtime.alibaba-inc.com"
ACTION_CODE = "a502f2ab-9102-460e-9b25-360939256f63"
TASK_CODE = "task_8db1233n1x"

# ============================================================
# 默认配置
# ============================================================
REQUEST_TIMEOUT = 600  # 10 分钟


def knowledge_search(query):
    """调用知识库搜索接口，仅返回 ResponseBody 原始文本"""
    url = f"{BASE_URL}/test/knowledgeSearch"
    payload = {
        "agentCode": AGENT_CODE,
        "agentVersion": AGENT_VERSION,
        "taskCode": TASK_CODE,
        "actionCode": ACTION_CODE,
        "query": query,
    }

    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json; charset=utf-8"}
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            trace_id = resp.headers.get("EagleEye-TraceId", "")
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        trace_id = e.headers.get("EagleEye-TraceId", "") if e.headers else ""
        err_body = ""
        try:
            err_body = e.read().decode("utf-8")
        except Exception:
            pass
        print(json.dumps({
            "success": False,
            "httpStatus": e.code,
            "traceId": trace_id,
            "errMsg": err_body,
        }, ensure_ascii=False))
        sys.exit(1)
    except urllib.error.URLError as e:
        print(json.dumps({"success": False, "errMsg": str(e.reason)}, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"success": False, "errMsg": str(e)}, ensure_ascii=False))
        sys.exit(1)

    if not body.get("success"):
        print(json.dumps({
            "success": False,
            "traceId": trace_id,
            "errCode": body.get("errCode"),
            "errMsg": body.get("errMsg"),
        }, ensure_ascii=False))
        sys.exit(1)

    print(body.get("data", ""))


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"success": False, "errMsg": "缺少参数，用法: python3 knowledge_search.py '{\"query\": \"你好\"}'"}, ensure_ascii=False))
        sys.exit(1)

    params = json.loads(sys.argv[1])
    query = params.get("query", "")
    knowledge_search(query)


if __name__ == "__main__":
    main()

