#!/usr/bin/env python3
"""
API密钥泄露扫描工具 v2.0
扫描代码文件中的API密钥和敏感凭证

支持服务商：AWS / GCP / 阿里云 / 腾讯云 / GitHub / Stripe / Slack / 通用数据库连接串 / JWT / 私钥

用法:
  python3 api_leak_scanner.py --path ./src
  python3 api_leak_scanner.py --path ./src --ext .py,.js,.env
  python3 api_leak_scanner.py --path ./config.json --output report.json
"""

import argparse
import json
import re
import sys
from datetime import datetime
from pathlib import Path


# API密钥检测模式
PATTERNS = [
    ("AKIA[0-9A-Z]{16}", "AWS Access Key ID", "critical", "AWS"),
    ("AIza[0-9A-Za-z_-]{35}", "Google API Key", "critical", "GCP"),
    ("LTAI[A-Za-z0-9]{12,20}", "阿里云 AccessKey ID", "critical", "阿里云"),
    ("AKID[A-Za-z0-9]{32}", "腾讯云 SecretId", "critical", "腾讯云"),
    ("ghp_[A-Za-z0-9_]{36}", "GitHub Personal Access Token", "critical", "GitHub"),
    ("gho_[A-Za-z0-9_]{36}", "GitHub OAuth Token", "critical", "GitHub"),
    ("sk_live_[0-9a-zA-Z]{24}", "Stripe Live Secret Key", "critical", "Stripe"),
    ("xox[baprs]-[0-9a-zA-Z-]{10,}", "Slack Token", "high", "Slack"),
    ("(?i)(api[_-]?key|secret[_-]?key|access[_-]?key)[=:]\s*['"]?[A-Za-z0-9_-]{20,}['"]?", "通用API密钥", "high", "通用"),
    ("(?i)(mysql|postgres|mongodb|redis)://[^\s'"]{10,}", "数据库连接串", "critical", "数据库"),
    ("eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+", "JWT Token", "high", "认证"),
    ("-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----", "私钥文件", "critical", "加密"),
]

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}
DEFAULT_EXT = {".py", ".js", ".ts", ".jsx", ".tsx", ".env", ".yaml", ".yml", ".json", ".xml", ".sh", ".bash", ".toml"}

def mask(v):
    if len(v) > 12:
        return v[:8] + "*"*(len(v)-12) + v[-4:]
    return "***"

def scan_file(filepath):
    findings = []
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            for ln, line in enumerate(f, 1):
                s = line.strip()
                if not s or s.startswith("#"):
                    continue
                for pat, name, sev, prov in PATTERNS:
                    if re.search(pat, s):
                        m = re.search(pat, s)
                        findings.append({"file": str(filepath), "line": ln, "type": name, "severity": sev, "provider": prov, "masked": mask(m.group(0))})
    except Exception:
        pass
    return findings

def scan_dir(d, exts):
    all_f, cnt = [], 0
    for root, dirs, files in os.walk(d):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for fn in files:
            if Path(fn).suffix.lower() in exts or fn == ".env":
                all_f.extend(scan_file(os.path.join(root, fn)))
                cnt += 1
    return all_f, cnt

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--path", required=True)
    ap.add_argument("--ext", default="")
    ap.add_argument("--output", default="")
    args = ap.parse_args()

    p = args.path
    exts = set(args.ext.split(",")) if args.ext else DEFAULT_EXT

    if os.path.isfile(p):
        findings, cnt = scan_file(p), 1
    else:
        findings, cnt = scan_dir(p, exts)

    crit = [x for x in findings if x["severity"] == "critical"]
    high = [x for x in findings if x["severity"] == "high"]

    print(f"API密钥泄露扫描报告")
    print("=" * 30)
    print(f"扫描路径: {p}")
    print(f"扫描文件: {cnt}")
    print(f"发现风险: {len(findings)}  (严重{len(crit)} 高危{len(high)})")
    print()
    for f in crit + high:
        print(f"[{f['provider']}] {f['type']}")
        print(f"  {f['file']}:{f['line']}  {f['masked']}")

    if args.output:
        with open(args.output, "w") as fw:
            json.dump({"path": p, "files": cnt, "total": len(findings), "critical": len(crit), "high": len(high), "findings": findings}, fw, ensure_ascii=False)
        print(f"
JSON saved: {args.output}")

if __name__ == "__main__":
    main()
