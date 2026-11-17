#!/usr/bin/env python3
"""smart-message-plus: message templates ({{var}} substitution)."""
from __future__ import annotations

import re

from . import config as C


def template_dir():
    d = C.data_dir() / "templates"
    d.mkdir(exist_ok=True)
    return d


def render(name: str, vars_list: list[str]) -> str:
    p = template_dir() / f"{name}.txt"
    if not p.exists():
        available = [f.stem for f in template_dir().glob("*.txt")]
        hint = f"可用模板: {', '.join(available)}" if available else "暂无模板，请先创建"
        raise ValueError(f"模板不存在: {name}（{hint}；目录: {template_dir()}）")
    text = p.read_text(encoding="utf-8")
    varmap = {}
    for item in vars_list or []:
        if "=" not in item:
            raise ValueError(f"--vars 格式应为 key=value，收到: {item}")
        k, v = item.split("=", 1)
        varmap[k.strip()] = v
    text = re.sub(r"\{\{(\w+)\}\}", lambda m: varmap.get(m.group(1), m.group(0)), text)
    unresolved = re.findall(r"\{\{(\w+)\}\}", text)
    if unresolved:
        raise ValueError(f"模板变量未提供值: {', '.join(sorted(set(unresolved)))}")
    return text
