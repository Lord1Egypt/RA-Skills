#!/usr/bin/env python3
"""发布前安检 —— 自包含 PII / 密钥扫描（仅标准库，离线可用，免积分）。

模式：
  --mode pii      扫描个人敏感信息（身份证/手机/邮箱/银行卡/地址片段）
  --mode secret   扫描密钥形态（API Key/Token/PAT/私钥/密码赋值）
  --mode all      两者都扫

用法：
  python secret_scan.py --path ./to_publish --mode all
退出码：0=无风险可放行，1=发现风险(阻断)，2=参数/IO 错误
"""
import argparse
import os
import re
import sys

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".vault", "venv"}
# 扫描器自身的源文件不参与自审（避免模式字符串自指命中）
SELF_SKIP = {"secret_scan.py", "desens_check.py"}
SCAN_EXT = {".md", ".py", ".js", ".ts", ".json", ".txt", ".yaml", ".yml", ".toml", ".sh", ".bat"}

# PII = 真实个人身份数据；路径/环境名词不在此列（交由 desens_check 专项复核）
PII_PATTERNS = {
    "身份证": re.compile(r"\b[1-9]\d{5}(18|19|20)\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])\d{3}[\dXx]\b"),
    "手机号": re.compile(r"\b1[3-9]\d{9}\b"),
    "邮箱": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"),
    "银行卡": re.compile(r"\b(?:62\d{14,17}|4\d{12,15}|5[1-5]\d{14})\b"),
}
SECRET_PATTERNS = {
    "AWS_KEY": re.compile(r"AKIA[0-9A-Z]{16}"),
    "GitHub_PAT": re.compile(r"gh[pousr]_[A-Za-z0-9]{36,}"),
    "通用APIKey": re.compile(r"(?i)(api[_-]?key|secret|token|password|passwd)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}"),
    "私钥块": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "Bearer": re.compile(r"(?i)bearer\s+[A-Za-z0-9._-]{20,}"),
    "SK密钥": re.compile(r"sk[_-](?:live|test)[_-]?[A-Za-z0-9]{10,}|sk-[A-Za-z0-9]{20,}"),
}


def mask(snippet, label):
    """输出脱敏：绝不把命中的密钥/PII 原值打印到日志或终端。

    只保留前 3 位作为定位线索，尾部一律隐去——保留末位会泄露可用于爆破的字符信息。
    """
    s = snippet
    if label in ("私钥块",):
        return s
    if len(s) <= 3:
        return "*" * len(s)
    return s[:3] + "*" * 8


def scan_text(text):
    hits = []
    for label, pat in {**PII_PATTERNS, **SECRET_PATTERNS}.items():
        for m in pat.finditer(text):
            snippet = m.group(0)
            if len(snippet) > 60:
                snippet = snippet[:57] + "..."
            hits.append((label, snippet))
    return hits


def contained(path, root):
    """符号链接/相对路径越界检查：解析后的真实路径必须仍在 root 内。"""
    try:
        rp = os.path.realpath(path)
        rr = os.path.realpath(root)
        return os.path.commonpath([rp, rr]) == rr
    except (ValueError, OSError):
        return False


def scan_path(path, mode):
    results = []
    errors = []
    if not os.path.exists(path):
        raise FileNotFoundError("扫描目标不存在：%s" % path)
    root = path if os.path.isdir(path) else os.path.dirname(os.path.abspath(path))
    if os.path.isfile(path):
        targets = [path]
    else:
        targets = []
        for r, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for f in files:
                fp_full = os.path.join(r, f)
                if os.path.basename(fp_full) in SELF_SKIP:
                    continue
                if os.path.islink(fp_full):
                    # 不跟随符号链接，避免借链接读到扫描目标之外的凭据
                    errors.append((fp_full, "跳过符号链接"))
                    continue
                if not contained(fp_full, root):
                    errors.append((fp_full, "越出扫描根目录"))
                    continue
                if os.path.splitext(f)[1].lower() in SCAN_EXT:
                    targets.append(fp_full)
    for fp in targets:
        try:
            with open(fp, "r", encoding="utf-8", errors="ignore") as fh:
                content = fh.read()
        except OSError as e:
            # 读不到不等于干净：记入 errors，由 main 按 fail-closed 处理
            errors.append((fp, "读取失败：%s" % e))
            continue
        for label, snip in scan_text(content):
            if mode == "pii" and label in SECRET_PATTERNS:
                continue
            if mode == "secret" and label in PII_PATTERNS:
                continue
            results.append((fp, label, snip))
    return results, errors, len(targets)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--path", required=True)
    p.add_argument("--mode", choices=["pii", "secret", "all"], default="all")
    a = p.parse_args()
    try:
        res, errs, n = scan_path(a.path, a.mode)
    except OSError as e:
        print(f"[IO错误] {e}", file=sys.stderr)
        sys.exit(2)
    if not n:
        print("[BLOCK] 未枚举到任何可扫描文件（路径不存在或无可扫描扩展名），按 fail-closed 处理。")
        sys.exit(2)
    if errs:
        print(f"[WARN] {len(errs)} 个文件未能检查，本次结论不完整：")
        for fp, why in errs[:10]:
            print(f"  - {fp}  [{why}]")
    if not res:
        if errs:
            print(f"[BLOCK] 模式={a.mode}：已扫描文件未发现风险，但存在未检查文件，不能判定为可放行。")
            sys.exit(1)
        print(f"[PASS] 模式={a.mode}：未发现 PII/密钥风险，可放行。")
        sys.exit(0)
    print(f"[BLOCK] 模式={a.mode}：发现 {len(res)} 处风险，阻断发布：")
    for fp, label, snip in res:
        print(f"  - {fp}  [{label}]  {mask(snip, label)}")
    sys.exit(1)


if __name__ == "__main__":
    main()
