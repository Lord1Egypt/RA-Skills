#!/usr/bin/env python3
"""
自然语言工具调用器

将自然语言转换为工具调用
用法: python3 run_nlp.py "帮我读取 /etc/hostname 文件"
"""

import sys
import json
import asyncio
import re
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from __init__ import load_all_tools, get_registry
from schema import ToolRegistry


# 意图映射规则
INTENT_PATTERNS = [
    # ===== Agent Teams =====
    (r"创建\s*团队\s*(.+)", "team_create", "team_name"),
    (r"团队\s*列表", "team_list", None),
    (r"添加\s*(.+?)\s*到\s*团队", "team_add_agent", "team_agent"),
    (r"团队\s*执行\s*(.+)", "team_run_task", "team_task"),
    (r"让\s*(.+?)\s*团队\s*(.+)", "team_run_task", "team_task2"),
    (r"(?:创建|添加)\s*(.+?)\s*Agent", "team_add_agent", "add_agent"),
    
    # ===== Shell 执行 =====
    (r"^(ls|cd|pwd|cat|rm|mkdir|touch|echo)\s*(.*)$", "shell_exec", "shell_command"),
    (r"执行\s+(.+)$", "shell_exec", "shell_command"),
    (r"运行\s+(.+)$", "shell_exec", "shell_command"),
    
    # 文件操作 - 绝对路径
    (r"读取\s+(/\S+)", "file_read", "path"),
    (r"查看\s+(/\S+)", "file_read", "path"),
    (r"cat\s+(/\S+)", "file_read", "path"),
    (r"删除\s+(/\S+)", "file_delete", "path"),
    (r"搜索\s+(\S+)\s*文件", "file_glob", "pattern"),
    (r"列出\s+(\S+)\s*目录", "file_list", "path"),
    
    # Git 操作
    (r"git\s+status", "git_status", "path=."),
    (r"查看\s*Git\s*状态", "git_status", "path=."),
    (r"git\s+log", "git_log", "path=."),
    (r"git\s+diff", "git_diff", "path=."),
    (r"git\s+commit\s+([^-]+)", "git_commit", "message"),
    (r"提交\s+(.+)", "git_commit", "message"),
    (r"git\s+push", "git_push", "path=."),
    (r"推送", "git_push", "path=."),
    (r"git\s+pull", "git_pull", "path=."),
    (r"拉取", "git_pull", "path=."),
    (r"git\s+branch", "git_branch", "path=."),
    
    # 系统信息
    (r"系统信息", "system_info", None),
    (r"我的\s*IP", "shell_exec", "command=curl -s ifconfig.me"),
    (r"天气", "http_request", "url=http://wttr.in/Shanghai?format=j1"),
    
    # 网页搜索
    (r"搜索\s+(.+)", "web_search", "query"),
    (r"查一下\s+(.+)", "web_search", "query"),
    (r"找\s+(.+?)(?:的|信息|资料)", "web_search", "query"),
    
    # 记忆系统
    (r"记住(.+)", "memory_remember", "content"),
    (r"记一下(.+)", "memory_remember", "content"),
    (r"记录(.+)", "memory_remember", "content"),
    (r"记得\s*(.+)", "memory_recall", "query"),
    (r"搜索\s*记忆\s*(.+)", "memory_recall", "query"),
    (r"记忆\s*统计", "memory_stats", None),
    (r"整理\s*记忆", "memory_dream", "dry_run=false"),
]


def parse_path_from_intent(text: str) -> str:
    """从文本中提取路径"""
    # 去除引号
    text = text.strip().strip("'\"").strip()
    # 展开 ~
    if text.startswith("~"):
        text = str(Path.home()) + text[1:]
    # 转换为绝对路径
    return str(Path(text).expanduser().resolve())


def extract_command(text: str) -> str:
    """从文本中提取命令"""
    return text.strip().strip("'\"").strip()


async def process_intent(text: str) -> dict:
    """处理自然语言，返回工具调用结果"""
    load_all_tools()
    registry = get_registry()
    
    text = text.strip()
    
    # 尝试匹配意图
    for pattern, tool_name, default_param in INTENT_PATTERNS:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # 构建参数
            params = {}
            
            # 处理默认参数（key=value 格式）
            if default_param and "=" in str(default_param):
                key, value = str(default_param).split("=", 1)
                params[key] = value
            elif default_param is None:
                pass  # 无参数
            elif default_param == "path":
                params["path"] = parse_path_from_intent(match.group(1))
            elif default_param == "command":
                params["command"] = match.group(1).strip()
            elif default_param == "shell_command":
                # 组合命令 (cmd + args)
                cmd = match.group(1).strip()
                args = match.group(2).strip() if match.lastindex and match.lastindex >= 2 else ""
                params["command"] = f"{cmd} {args}".strip()
            elif default_param == "content":
                params["content"] = match.group(1).strip()
                params["importance"] = 3
            elif default_param == "query":
                params["query"] = match.group(1).strip()
                params["limit"] = 5
            elif default_param == "message":
                params["path"] = "."
                params["message"] = match.group(1).strip()
            elif default_param == "pattern":
                params["pattern"] = match.group(1).strip()
            
            # ===== Agent Teams 参数处理 =====
            elif default_param == "team_name":
                # "创建团队 我的团队" → team_id, name
                params["team_id"] = match.group(1).strip().replace(" ", "_").lower()
                params["name"] = match.group(1).strip()
            elif default_param == "team_agent":
                # "添加 coder 到团队" → team_id, agent_id, name
                agent_name = match.group(1).strip()
                params["team_id"] = "myteam"  # 默认
                params["agent_id"] = agent_name.replace(" ", "_").lower()
                params["name"] = agent_name
            elif default_param == "team_task":
                # "团队执行 任务"
                params["team_id"] = "myteam"  # 默认
                params["task"] = match.group(1).strip()
            elif default_param == "team_task2":
                # "让 coder 团队 任务"
                params["team_id"] = match.group(1).strip().replace(" ", "_").lower()
                params["task"] = match.group(2).strip()
            elif default_param == "add_agent":
                # "添加 coder Agent"
                agent_name = match.group(1).strip()
                params["team_id"] = "myteam"
                params["agent_id"] = agent_name.replace(" ", "_").lower()
                params["name"] = agent_name
            
            # 执行工具
            try:
                result = await registry.execute(tool_name, **params)
                
                if result.success:
                    return {
                        "intent": tool_name,
                        "success": True,
                        "data": result.data,
                        "params": params
                    }
                else:
                    return {
                        "intent": tool_name,
                        "success": False,
                        "error": result.error,
                        "params": params
                    }
            except Exception as e:
                return {
                    "intent": tool_name,
                    "success": False,
                    "error": str(e),
                    "params": params
                }
    
    # 没有匹配到意图，返回提示
    return {
        "intent": None,
        "success": False,
        "error": f"无法理解: {text}",
        "suggestion": "可以尝试: '读取 /etc/hostname', 'ls /tmp', '搜索 Python', '记住 重要事项', '系统信息', '天气'"
    }


def format_result(result: dict) -> str:
    """格式化结果为自然语言"""
    if not result["success"]:
        return f"❌ {result.get('error', '未知错误')}"
    
    data = result.get("data", {})
    intent = result.get("intent", "")
    
    # 根据不同工具格式化输出
    if intent == "file_read":
        return f"📄 文件内容:\n{data.get('content', '').strip()}"
    
    elif intent == "system_info":
        return f"💻 系统信息:\n" + "\n".join(f"  {k}: {v}" for k, v in data.items())
    
    elif intent == "shell_exec":
        return data.get("stdout", "").strip() or data.get("stderr", "").strip()
    
    elif intent == "memory_remember":
        return f"✅ 已记住: {result['params'].get('content', '')}"
    
    elif intent == "memory_recall":
        results = data.get("results", [])
        if not results:
            return "没有找到相关记忆"
        return "📝 相关记忆:\n" + "\n".join(
            f"  - {r['content'][:80]}" for r in results[:3]
        )
    
    elif intent == "memory_stats":
        by_type = data.get("by_type", {})
        total = data.get("total", 0)
        return f"📊 记忆统计: 共 {total} 条\n" + "\n".join(
            f"  {k}: {v} 条" for k, v in by_type.items()
        )
    
    elif intent == "web_search":
        results = data.get("results", [])
        if not results:
            return "没有找到相关结果"
        return "🔍 搜索结果:\n" + "\n".join(
            f"  {i+1}. {r['title'][:50]}\n     {r['url'][:60]}"
            for i, r in enumerate(results[:5])
        )
    
    elif intent == "http_request" and "weather" in str(data):
        try:
            current = data.get("body", {}).get("current_condition", [{}])[0]
            temp = current.get("temp_C", "N/A")
            desc = current.get("weatherDesc", "N/A")
            return f"🌤️ 上海天气: {temp}°C, {desc}"
        except:
            pass
    
    # 默认格式化
    if isinstance(data, dict):
        return "\n".join(f"{k}: {v}" for k, v in data.items())
    return str(data)


async def main():
    # 读取输入
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
    else:
        print("用法: python3 run_nlp.py \"帮我读取 /etc/hostname\"")
        sys.exit(1)
    
    # 处理意图
    result = await process_intent(text)
    
    # 格式化输出
    output = format_result(result)
    print(output)
    
    # 如果是 JSON 模式
    if "--json" in sys.argv:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())