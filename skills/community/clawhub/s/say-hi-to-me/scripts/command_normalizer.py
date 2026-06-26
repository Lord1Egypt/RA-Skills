#!/usr/bin/env python3
"""
Normalize `/hi` commands and natural-language requests into canonical intents.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any, Dict, List


GREETING_HINTS = ("hi", "hello", "hey", "你好", "嗨", "在吗", "打个招呼")
INIT_HINTS = ("初始化", "开始配置", "初始配置", "setup", "set up")
STATUS_HINTS = ("状态", "配置", "当前设置", "现在什么角色", "what is current role")


def to_half_width(text: str) -> str:
    result = []
    for ch in text:
        code = ord(ch)
        if code == 0x3000:
            result.append(" ")
        elif 0xFF01 <= code <= 0xFF5E:
            result.append(chr(code - 0xFEE0))
        else:
            result.append(ch)
    return "".join(result)


def normalize_text(text: str) -> str:
    text = to_half_width(text).strip()
    text = re.sub(r"\s+", " ", text)
    return text


def parse_freq(token: str) -> str | None:
    token = token.lower()
    mapping = {
        "低": "low",
        "中": "mid",
        "高": "high",
        "low": "low",
        "mid": "mid",
        "middle": "mid",
        "high": "high",
    }
    return mapping.get(token)


def parse_command(text: str) -> Dict[str, Any] | None:
    if not text.lower().startswith("/hi"):
        return None

    parts = text.split(" ")
    if len(parts) == 1:
        return {"source": "command", "intent": "greeting_checkin", "args": {}}

    p1 = parts[1].lower()
    rest = parts[2:]

    if p1 in ("帮助", "help"):
        return {"source": "command", "intent": "help", "args": {}}
    if p1 in ("开", "on"):
        return {"source": "command", "intent": "config_proactive_on", "args": {}}
    if p1 in ("关", "off"):
        return {"source": "command", "intent": "config_proactive_off", "args": {}}
    if p1 in ("状态", "status"):
        return {"source": "command", "intent": "status_query", "args": {}}
    if p1 in ("重置", "reset"):
        return {"source": "command", "intent": "config_reset", "args": {}}

    if p1 in ("频率", "freq"):
        if not rest:
            return {"source": "command", "intent": "invalid", "args": {"reason": "missing_frequency"}}
        freq = parse_freq(rest[0])
        if not freq:
            return {"source": "command", "intent": "invalid", "args": {"reason": "invalid_frequency"}}
        return {"source": "command", "intent": "config_frequency", "args": {"frequency": freq}}

    if p1 in ("免打扰", "quiet"):
        if not rest:
            return {"source": "command", "intent": "invalid", "args": {"reason": "missing_quiet_hours"}}
        if not re.match(r"^\d{1,2}:\d{2}-\d{1,2}:\d{2}$", rest[0]):
            return {"source": "command", "intent": "invalid", "args": {"reason": "invalid_quiet_hours"}}
        return {"source": "command", "intent": "config_quiet_hours", "args": {"range": rest[0]}}

    if p1 in ("暂停", "pause"):
        if not rest:
            return {"source": "command", "intent": "invalid", "args": {"reason": "missing_pause_duration"}}
        return {"source": "command", "intent": "config_pause", "args": {"duration": rest[0]}}

    if p1 in ("角色", "role"):
        if not rest:
            return {"source": "command", "intent": "invalid", "args": {"reason": "missing_role_subcommand"}}
        sub = rest[0].lower()
        tail = rest[1:]

        if sub in ("列表", "list"):
            return {"source": "command", "intent": "role_list", "args": {}}
        if sub in ("当前", "current"):
            return {"source": "command", "intent": "role_current", "args": {}}
        if sub in ("预览", "preview"):
            return {"source": "command", "intent": "role_preview", "args": {}}
        if sub in ("确认", "confirm", "activate", "启用"):
            return {"source": "command", "intent": "role_confirm_activation", "args": {}}

        if sub in ("切换", "use", "switch"):
            if not tail:
                return {"source": "command", "intent": "invalid", "args": {"reason": "missing_role_name"}}
            return {"source": "command", "intent": "role_switch", "args": {"name": " ".join(tail)}}

        if sub in ("保存", "save"):
            if not tail:
                return {"source": "command", "intent": "invalid", "args": {"reason": "missing_role_name"}}
            return {"source": "command", "intent": "role_save", "args": {"name": " ".join(tail)}}

        if sub in ("模板", "template"):
            if not tail:
                return {"source": "command", "intent": "invalid", "args": {"reason": "missing_template_name"}}
            return {"source": "command", "intent": "role_template_apply", "args": {"template": tail[0]}}

        if sub in ("新建", "new"):
            if not tail:
                return {"source": "command", "intent": "invalid", "args": {"reason": "missing_prompt"}}
            return {"source": "command", "intent": "role_create", "args": {"prompt": " ".join(tail)}}

        if sub in ("编辑", "edit"):
            if len(tail) < 2:
                return {"source": "command", "intent": "invalid", "args": {"reason": "missing_field_or_value"}}
            return {"source": "command", "intent": "role_edit", "args": {"field": tail[0], "value": " ".join(tail[1:])}}

    return {"source": "command", "intent": "invalid", "args": {"reason": "unknown_command"}}


def parse_natural_language(text: str) -> Dict[str, Any]:
    low = text.lower()

    if any(k in text for k in ("确认启用", "确认使用", "同意启用", "同意使用")) or any(
        k in low for k in ("confirm activation", "activate it", "confirm use")
    ):
        return {"source": "nl", "intent": "role_confirm_activation", "args": {}}

    if any(h in text for h in INIT_HINTS) or any(h in low for h in INIT_HINTS):
        return {"source": "nl", "intent": "init_config", "args": {}}

    m_save = re.search(r"(?:保存(?:为)?|save as)\s*([A-Za-z0-9\u4e00-\u9fff_-]{1,40})", text, re.IGNORECASE)
    if m_save:
        return {"source": "nl", "intent": "role_save", "args": {"name": m_save.group(1)}}

    m_switch = re.search(r"(?:切换到|切到|switch to|use)\s*([A-Za-z0-9\u4e00-\u9fff_-]{1,40})", text, re.IGNORECASE)
    if m_switch:
        return {"source": "nl", "intent": "role_switch", "args": {"name": m_switch.group(1)}}

    if ("模板" in text or "template" in low) and ("洛水" in text or "阿洛" in text or "luoshui" in low):
        return {"source": "nl", "intent": "role_template_apply", "args": {"template": "luoshui"}}

    if "角色" in text and ("创建" in text or "新建" in text or "create" in low):
        return {"source": "nl", "intent": "role_create", "args": {"prompt": text}}

    if ("角色" in text or "人设" in text) and ("切换" in text or "switch" in low):
        return {"source": "nl", "intent": "role_switch", "args": {"prompt": text}}

    if ("角色" in text or "人设" in text) and ("改" in text or "编辑" in text or "调整" in text or "edit" in low):
        return {"source": "nl", "intent": "role_edit", "args": {"prompt": text}}

    if any(hint in low for hint in GREETING_HINTS) or any(hint in text for hint in GREETING_HINTS):
        return {"source": "nl", "intent": "greeting_checkin", "args": {}}

    if ("主动" in text and ("开启" in text or "打开" in text)) or "proactive on" in low:
        return {"source": "nl", "intent": "config_proactive_on", "args": {}}

    if ("主动" in text and ("关闭" in text or "关掉" in text)) or "proactive off" in low:
        return {"source": "nl", "intent": "config_proactive_off", "args": {}}

    m_freq = re.search(r"(?:频率|freq).{0,4}(低|中|高|low|mid|middle|high)", text, re.IGNORECASE)
    if m_freq:
        freq = parse_freq(m_freq.group(1))
        if freq:
            return {"source": "nl", "intent": "config_frequency", "args": {"frequency": freq}}

    m_quiet = re.search(r"(\d{1,2}:\d{2}-\d{1,2}:\d{2})", text)
    if ("免打扰" in text or "quiet" in low) and m_quiet:
        return {"source": "nl", "intent": "config_quiet_hours", "args": {"range": m_quiet.group(1)}}

    if any(h in text for h in STATUS_HINTS) or any(h in low for h in STATUS_HINTS):
        return {"source": "nl", "intent": "status_query", "args": {}}

    return {"source": "nl", "intent": "casual_companion_chat", "args": {}}


def normalize_input(text: str) -> Dict[str, Any]:
    text = normalize_text(text)
    cmd = parse_command(text)
    if cmd is not None:
        return cmd
    return parse_natural_language(text)


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(description="Normalize /hi command or natural language into canonical intent")
    parser.add_argument("text", help="Raw user input")
    args = parser.parse_args(argv)

    result = normalize_input(args.text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
