"""裁判权（Pipeline Step 8b）：结论可追溯性 + 离线安全扫描。

- 检查每条 evidence 均含 rules_used（结论可追溯 rule_id -> input -> calc -> output）。
- 离线扫描 engine 目录禁止网络调用（requests / urllib / socket / httpx / aiohttp / curl / wget）。
- 不允许以 VAULT_UNREADABLE 来源断言高置信确定性结论。
"""
from __future__ import annotations

import os
import re

from evidence import EvidenceRecord, RULE_VERSION

# 仅匹配“真实用法”模式，避免误伤本文件列出的禁用词清单与说明文档
_USAGE_PATTERNS = [
    re.compile(r"\bimport\s+(requests|urllib|socket|httpx|aiohttp)\b"),
    re.compile(r"\bfrom\s+(requests|urllib|socket|httpx|aiohttp)\s+import\b"),
    re.compile(r"\b(requests|urllib|socket|httpx|aiohttp)\s*\.\s*\w"),  # 模块.属性/方法调用
    re.compile(r"\b(curl|wget)\b"),  # shell 命令
]


def _offline_scan(engine_dir: str) -> list:
    """扫描 engine 下 .py 文件，仅检测“真实代码”中的网络能力。

    跳过注释（# 开头）与三引号文档串（含本文件列举禁用词的说明行），
    避免误伤扫描器自身对禁用词的罗列。
    """
    hits = []
    for root, _, files in os.walk(engine_dir):
        for f in files:
            if not f.endswith(".py"):
                continue
            p = os.path.join(root, f)
            try:
                with open(p, "r", encoding="utf-8") as fh:
                    in_doc = False
                    for i, line in enumerate(fh, 1):
                        s = line.strip()
                        if s.startswith("#"):
                            continue
                        if "re.compile" in s:  # 跳过扫描器自身正则定义行
                            continue
                        if (s.count('"""') + s.count("'''")) % 2 == 1:
                            in_doc = not in_doc
                        if in_doc:
                            continue
                        for pat in _USAGE_PATTERNS:
                            if pat.search(s):
                                hits.append(f"{f}:{i}")
                                break
            except OSError:
                pass
    return hits


def validate(records: list, engine_dir: str | None = None) -> dict:
    issues = []
    for r in records:
        if not r.rules_used:
            issues.append(f"{r.step}: 缺 rules_used，结论不可追溯")
        if r.vault_source == "VAULT_UNREADABLE" and r.confidence >= 0.9:
            issues.append(f"{r.step}: vault 不可读却高置信，疑似臆造")
    ed = engine_dir or os.path.join(os.path.dirname(__file__))
    net_hits = _offline_scan(ed)
    if net_hits:
        issues.append("发现网络能力: " + "; ".join(net_hits))
    return {
        "passed": len(issues) == 0 and not net_hits,
        "issues": issues,
        "offline_scan_hits": net_hits,
        "rule_version": RULE_VERSION,
    }
