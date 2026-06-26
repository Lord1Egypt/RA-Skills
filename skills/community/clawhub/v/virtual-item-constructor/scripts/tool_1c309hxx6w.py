#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tool 调用脚本（Freemarker 渲染）

Freemarker 占位符：
  - ${toolCode}       工具编码
  - ${toolName}       工具名称
  - ${toolVersion}    工具版本
  - ${toolTechType}   工具技术类型
  - ${agentCode}      Agent 编码
  - ${agentVersion}   Agent 版本
  - ${taskCode}       Task 编码
  - ${taskVersion}    Task 版本
  - ${baseUrl}        TBMCP 服务地址

无外部依赖，仅使用 Python 标准库

使用方式（渲染后）：
  python3 tool_invoke.py '{"param": "value"}'
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error

# ============================================================
# Freemarker 占位符（渲染时替换为真实值）
# ============================================================
TOOL_CODE = "tool_1c309hxx6w"
TOOL_NAME = "通过商家id与属性查找商品"
TOOL_VERSION = "0.0.3"
TOOL_TECH_TYPE = 3
AGENT_CODE = "agent_34a7cjmxpx"
AGENT_VERSION = "draft"
TASK_CODE = "task_8db1233n1x"
TASK_VERSION = "draft"
BASE_URL = "https://tbmcp.alibaba-inc.com"

# ============================================================
# 预设的系统参数（导出时由 SkillExportRequest 注入）
# ============================================================
DEFAULT_SYSTEM_PARAMS = json.loads('{}')

# ============================================================
# 默认配置
# ============================================================
REQUEST_TIMEOUT = 120


def _get_skill_dir():
    """定位 Skill 根目录（脚本在 scripts/ 子目录下，根目录在上一层）"""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _load_skill_token():
    """从 SKILL.md frontmatter 中读取 skill-token"""
    skill_md = os.path.join(_get_skill_dir(), "SKILL.md")
    if not os.path.exists(skill_md):
        return None
    with open(skill_md, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None
    for line in match.group(1).split('\n'):
        line = line.strip()
        if line.startswith('skill-token:'):
            return line.split(':', 1)[1].strip().strip('"').strip("'")
    return None


def invoke_tool(params, system_params=None):
    """调用 TBMCP 工具接口"""
    merged_system_params = {**DEFAULT_SYSTEM_PARAMS, **(system_params or {})}

    skill_token = _load_skill_token()
    if skill_token:
        url = f"{BASE_URL}/api/skill/tool/invoke"
    else:
        url = f"{BASE_URL}/api/tool/invoke"

    payload = {
        "toolName": TOOL_NAME,
        "toolCode": TOOL_CODE,
        "toolVersion": TOOL_VERSION,
        "toolTechType": TOOL_TECH_TYPE,
        "params": params,
        "systemParams": merged_system_params,
        "platformParams": {
            "agentCode": AGENT_CODE,
            "agentVersion": AGENT_VERSION,
            "taskCode": TASK_CODE,
            "taskVersion": TASK_VERSION
        }
    }

    data = json.dumps(payload).encode("utf-8")
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if skill_token:
        headers["X-Skill-Token"] = skill_token
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            trace_id = resp.headers.get("EagleEye-TraceId", "")
            body = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        trace_id = e.headers.get("EagleEye-TraceId", "") if e.headers else ""
        print(f"HTTP 错误: {e.code}, traceId={trace_id}", file=sys.stderr)
        try:
            print(e.read().decode("utf-8"), file=sys.stderr)
        except Exception:
            pass
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"请求失败: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"请求失败: {e}", file=sys.stderr)
        sys.exit(1)

    if not body.get("success"):
        err_code = body.get("errCode", "UNKNOWN")
        err_msg = body.get("errMsg", "未知错误")
        print(f"调用失败: [{err_code}] {err_msg}, traceId={trace_id}", file=sys.stderr)
        sys.exit(1)

    return body.get("data")


def main():
    if len(sys.argv) < 2:
        print("用法: python3 " + sys.argv[0] + " '<json_params>'", file=sys.stderr)
        sys.exit(1)

    try:
        params = json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败: {e}", file=sys.stderr)
        sys.exit(1)

    system_params = params.pop("systemParams", {})
    result = invoke_tool(params, system_params)

    if result is not None:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

