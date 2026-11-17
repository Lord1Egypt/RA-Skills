from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

PATTERNS = [
    ("api_key", re.compile(r"(?i)\b(?:sk-[a-z0-9_-]{12,}|AIza[\w-]{20,}|gh[pousr]_[A-Za-z0-9_]{20,})\b")),
    ("bearer", re.compile(r"(?i)(bearer\s+)[A-Za-z0-9._~+/=-]{12,}")),
    ("email", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("cn_mobile", re.compile(r"(?<!\d)1[3-9]\d{9}(?!\d)")),
    ("cn_id", re.compile(r"(?<!\d)\d{17}[\dXx](?!\d)")),
    ("private_key", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----")),
]

def _replace(text: str, words: list[str]) -> tuple[str, Counter]:
    counter: Counter = Counter(); cache: dict[str, str] = {}
    patterns = PATTERNS + [("custom", re.compile(re.escape(w))) for w in words if w]
    def one(category: str, match: re.Match) -> str:
        raw = match.group(0); prefix = match.group(1) if category == "bearer" else ""
        key = f"{category}:{raw}"
        if key not in cache:
            counter[category] += 1; cache[key] = f"[{category.upper()}_{counter[category]}]"
        return prefix + cache[key]
    for category, pattern in patterns:
        text = pattern.sub(lambda m: one(category, m), text)
    return text, counter

def redact(source: Path, output: Path, words: list[str]) -> dict:
    if source.resolve() == output.resolve(): raise ValueError("输出路径不得覆盖原文件")
    if source.suffix.lower() not in (".txt", ".md", ".json", ".csv", ""):
        raise ValueError("该文件类型尚不支持脱敏")
    raw = source.read_text(encoding="utf-8")
    if source.suffix.lower() == ".json":
        try: json.loads(raw)
        except json.JSONDecodeError as exc: raise ValueError("输入 JSON 无效") from exc
    value, counts = _replace(raw, words)
    if source.suffix.lower() == ".json": json.loads(value) # verify replacements preserve JSON validity
    output.parent.mkdir(parents=True, exist_ok=True); output.write_text(value, encoding="utf-8")
    return {"schema_version":"1.0", "operation":"redact", "status":"completed", "output":str(output.resolve()), "categories":dict(counts), "coverage":{"formats":["utf-8 text", "markdown", "json"], "mapping_stored":False}, "limitations":["不覆盖图片、PDF、Office、音频和未识别的语义秘密", "已发送到远程服务的原文无法撤回"], "summary":f"已生成脱敏副本，替换 {sum(counts.values())} 个实体"}

