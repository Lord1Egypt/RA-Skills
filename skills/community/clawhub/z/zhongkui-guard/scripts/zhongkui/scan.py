from __future__ import annotations

import json
import re
import zipfile
from pathlib import Path
from typing import Iterable

from .common import redact_text, safe_path

ROOT = Path(__file__).resolve().parents[2]

def _rules() -> dict:
    return json.loads((ROOT / "rules" / "scan-rules.json").read_text(encoding="utf-8"))

def _finding(rule: dict, file: str, line: int, evidence: str) -> dict:
    return {"rule_id":rule["id"], "severity":rule["severity"], "evidence_strength":"rule_match", "location":{"file":file, "line":line}, "evidence_redacted":redact_text(evidence.strip())[:240], "reason":rule["reason"], "recommendation":rule["recommendation"]}

def _text_findings(text: str, label: str, rules: list[dict]) -> list[dict]:
    findings = []
    for number, line in enumerate(text.splitlines(), 1):
        for rule in rules:
            if re.search(rule["pattern"], line, re.IGNORECASE): findings.append(_finding(rule, label, number, line))
    return findings

def _files(path: Path, limits: dict) -> Iterable[tuple[str, str]]:
    if path.is_file() and path.suffix.lower() == ".zip":
        with zipfile.ZipFile(path) as archive:
            infos = archive.infolist()
            if len(infos) > limits["max_zip_files"]: raise ValueError("ZIP 文件数量超过限制")
            total = sum(i.file_size for i in infos)
            if total > limits["max_zip_uncompressed_bytes"]: raise ValueError("ZIP 解压后大小超过限制")
            for info in infos:
                member = Path(info.filename)
                if member.is_absolute() or ".." in member.parts: raise ValueError("ZIP 含路径穿越成员")
                if (info.external_attr >> 16) & 0o170000 == 0o120000: raise ValueError("ZIP 含符号链接成员")
                if info.is_dir() or info.file_size > limits["max_file_bytes"]: continue
                try: yield info.filename, archive.read(info).decode("utf-8")
                except UnicodeDecodeError: continue
    else:
        candidates = [path] if path.is_file() else (p for p in path.rglob("*") if p.is_file())
        for item in candidates:
            if item.stat().st_size > limits["max_file_bytes"]: continue
            try: yield str(item.relative_to(path.parent if path.is_file() else path)), item.read_text(encoding="utf-8")
            except UnicodeDecodeError: continue

def scan(path: Path, kind: str) -> dict:
    if not path.exists(): raise FileNotFoundError("指定检查路径不存在")
    config = _rules(); findings = []
    for label, content in _files(path, config): findings.extend(_text_findings(content, label, config["rules"]))
    return {"schema_version":"1.0", "operation":"scan", "status":"completed", "target":{"kind":kind, "path":safe_path(path)}, "coverage":{"scope":"selected_files", "execution_interception":False, "rules_version":config["version"]}, "findings":findings, "limitations":["静态检查，未运行目标程序", "未知二进制和超限文件未覆盖", "没有发现不代表绝对安全"], "summary":f"扫描完成：发现 {len(findings)} 项需要复核的线索"}

