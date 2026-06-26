#!/usr/bin/env python3
"""
深蓝 AI 分析师 API 客户端
Shenlan AI Analyst API Client

用于 AI Agent Skill 的 API 封装，提供 AI 内容分析、Agent 编辑内容流、TTS 语音播报等能力。
"""

import json
import sys
import urllib.request
import urllib.parse

BASE_URL = "https://www.shenlannews.com/api/v2"

def fetch(endpoint: str, params: dict = None) -> dict:
    """发起 GET 请求并返回 JSON 响应"""
    url = f"{BASE_URL}{endpoint}"
    if params:
        params = {k: v for k, v in params.items() if v is not None}
        if params:
            url += "?" + urllib.parse.urlencode(params)

    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "User-Agent": "ShenlanAIAnalyst-Skill/1.0"
    })

    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


# ---- AI 内容分析 ----

def get_analysis_types(content_type: str, content_id: int):
    """获取可用的分析类型"""
    return fetch(f"/contents/{content_type}/{content_id}/ai-analysis/types")


def get_all_analysis(content_type: str, content_id: int):
    """获取所有分析结果"""
    return fetch(f"/contents/{content_type}/{content_id}/ai-analysis")


def get_analysis(content_type: str, content_id: int, analysis_type: str):
    """获取特定类型的分析"""
    return fetch(f"/contents/{content_type}/{content_id}/ai-analysis/{analysis_type}")


# ---- AI Agent 编辑 ----

def get_agents():
    """获取所有 AI Agent 编辑"""
    return fetch("/agents")


def get_agent(slug: str):
    """获取 Agent 详情"""
    return fetch(f"/agents/{slug}")


def get_agent_contents(slug: str, per_page=20, page=1):
    """获取 Agent 内容流"""
    return fetch(f"/agents/{slug}/contents", {"per_page": per_page, "page": page})


def get_agent_feed(per_page=20, page=1):
    """获取所有 Agent 聚合内容流"""
    return fetch("/agents/feed", {"per_page": per_page, "page": page})


# ---- TTS 语音播报 ----

def get_tts_voices():
    """获取可用 TTS 音色"""
    return fetch("/public/tts/voices")


def get_article_audio(article_id: int):
    """获取文章语音播报"""
    return fetch(f"/public/tts/article/{article_id}")


# ---- 辅助：带 AI 字段的文章/快讯 ----

def get_article_with_ai(article_id: int):
    """获取文章详情（含内置AI字段）"""
    return fetch(f"/articles/{article_id}")


def get_dispatches_with_sentiment(search=None, per_page=50):
    """获取快讯列表（含 AI 情感分析字段）"""
    return fetch("/dispatches", {"search": search, "per_page": per_page, "status": "published"})


# ---- CLI 入口 ----
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python api.py <command> [args...]")
        print()
        print("AI 分析命令:")
        print("  analysis-types <content_type> <content_id>    可用分析类型")
        print("  analyze <content_type> <content_id>           获取所有分析")
        print("  analyze <content_type> <content_id> <type>    获取特定分析")
        print()
        print("AI Agent 命令:")
        print("  agents                    Agent 列表")
        print("  agent <slug>              Agent 详情")
        print("  agent-contents <slug>     Agent 内容流")
        print("  agent-feed                所有 Agent 聚合 Feed")
        print()
        print("TTS 命令:")
        print("  tts-voices                可用音色")
        print("  tts-article <article_id>  文章语音播报")
        print()
        print("content_type 可选值: article, dispatch, post, interview, shenlantong_article")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "analysis-types":
        result = get_analysis_types(sys.argv[2], int(sys.argv[3]))
    elif cmd == "analyze":
        if len(sys.argv) >= 5:
            result = get_analysis(sys.argv[2], int(sys.argv[3]), sys.argv[4])
        else:
            result = get_all_analysis(sys.argv[2], int(sys.argv[3]))
    elif cmd == "agents":
        result = get_agents()
    elif cmd == "agent":
        result = get_agent(sys.argv[2])
    elif cmd == "agent-contents":
        result = get_agent_contents(sys.argv[2])
    elif cmd == "agent-feed":
        result = get_agent_feed()
    elif cmd == "tts-voices":
        result = get_tts_voices()
    elif cmd == "tts-article":
        result = get_article_audio(int(sys.argv[2]))
    elif cmd == "sentiment":
        search = sys.argv[2] if len(sys.argv) >= 3 else None
        result = get_dispatches_with_sentiment(search=search)
    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))
