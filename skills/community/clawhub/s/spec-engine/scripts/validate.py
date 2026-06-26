#!/usr/bin/env python3
"""
spec-engine validate v2.0 — 可配置的 spec 完整性验证器。

用法:
    python validate.py <spec文件> [--rules rules.json] [--strict] [--json]

v2.0 升级:
    - 支持 --rules 参数加载自定义验证规则
    - 评分系统：100分制，输出得分+等级（A/B/C/D）
    - 支持 --strict 模式（WARN 也当作 FAIL）
    - 检查项：required_sections, min_content_length, required_keywords, custom_checks
    - 向后兼容 v1 用法

Exit code: 0=PASS, 1=FAIL, 2=WARN
"""

import argparse
import json
import os
import re
import sys


# ─── 默认规则（v1 兼容） ─────────────────────────────────────────
DEFAULT_RULES = {
    "required_sections": [
        {
            "name": "项目名称",
            "patterns": [r"^#\s+项目名称[：:]", r"^#\s+.+"],
            "deduct": 25,
        },
        {
            "name": "目标",
            "patterns": [r"##\s*\d*[.、]?\s*目标", r"##\s*目标"],
            "deduct": 20,
        },
        {
            "name": "验收标准",
            "patterns": [r"##\s*\d*[.、]?\s*验收标准", r"##\s*验收标准"],
            "deduct": 20,
        },
        {
            "name": "时间规划",
            "patterns": [r"##\s*\d*[.、]?\s*时间规划", r"##\s*时间规划", r"##\s*排期", r"##\s*计划"],
            "deduct": 15,
        },
    ],
    "recommended_sections": [
        {
            "name": "项目背景",
            "patterns": [r"##\s*\d*[.、]?\s*项目背景", r"##\s*背景"],
            "deduct": 5,
        },
        {
            "name": "技术方案",
            "patterns": [r"##\s*\d*[.、]?\s*技术方案", r"##\s*技术栈"],
            "deduct": 5,
        },
        {
            "name": "风险评估",
            "patterns": [r"##\s*\d*[.、]?\s*风险评估", r"##\s*风险"],
            "deduct": 5,
        },
        {
            "name": "依赖项",
            "patterns": [r"##\s*\d*[.、]?\s*依赖项", r"##\s*依赖"],
            "deduct": 5,
        },
    ],
    "min_content_length": {
        "目标": 20,
        "验收标准": 20,
        "时间规划": 15,
        "技术方案": 10,
    },
    "required_keywords": [
        {"keyword": "验收", "section_hint": "验收标准", "deduct": 5},
        {"keyword": "测试", "section_hint": "", "deduct": 3},
    ],
    "custom_checks": [],
}

# 评分等级
GRADE_THRESHOLDS = [
    (90, "A"),
    (80, "B"),
    (70, "C"),
    (0, "D"),
]

# ANSI 颜色
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
RESET = "\033[0m"


def read_file(filepath, encoding="utf-8-sig"):
    """安全读取文件，自动去除 BOM。"""
    try:
        with open(filepath, "r", encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        print(f"[ERROR] 文件不存在: {filepath}", file=sys.stderr)
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"[ERROR] 文件编码错误: {filepath}", file=sys.stderr)
        sys.exit(1)


def load_rules(rules_path):
    """加载自定义验证规则。"""
    try:
        with open(rules_path, "r", encoding="utf-8-sig") as f:
            rules = json.load(f)
        # 合并默认规则（自定义规则覆盖默认）
        merged = dict(DEFAULT_RULES)
        for key, value in rules.items():
            if key in merged and isinstance(merged[key], list) and isinstance(value, list):
                # 列表类型：如果自定义规则非空则替换
                if value:
                    merged[key] = value
            else:
                merged[key] = value
        return merged
    except FileNotFoundError:
        print(f"[ERROR] 规则文件不存在: {rules_path}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[ERROR] 规则文件 JSON 格式错误: {e}", file=sys.stderr)
        sys.exit(1)


def extract_sections(text):
    """从 markdown 文本中提取所有 section。"""
    sections = {}
    pattern = r"^##\s+(.+?)\s*\n(.*?)(?=\n##\s|\Z)"
    matches = re.findall(pattern, text, re.MULTILINE | re.DOTALL)

    for title, content in matches:
        clean_title = re.sub(r"^\d+[.、]?\s*", "", title).strip()
        sections[clean_title] = content.strip()

    h1_match = re.match(r"^#\s+(.+)", text)
    if h1_match:
        raw_name = h1_match.group(1).strip()
        clean_name = re.sub(r"^项目名称[：:]\s*", "", raw_name).strip()
        sections["__project_name__"] = clean_name

    return sections


def has_substantial_content(content, min_length=2):
    """检查内容是否有实质（非空占位符）。"""
    if not content:
        return False
    cleaned = content.strip()
    without_todos = re.sub(r"<!--.*?-->", "", cleaned, flags=re.DOTALL).strip()
    if not without_todos:
        return False
    meaningful = re.sub(r"[\s\n\r]", "", without_todos)
    return len(meaningful) >= min_length


def check_section_exists(sections, section_name, patterns):
    """检查 section 是否存在。返回 (found, content)。"""
    if section_name == "项目名称":
        name = sections.get("__project_name__", "")
        return (bool(name) and name != "未命名项目", name)

    for key in sections:
        if key.startswith("__"):
            continue
        for pattern in patterns:
            if re.search(pattern, f"## {key}", re.IGNORECASE):
                return (True, sections[key])
    return (False, "")


def validate_spec(text, rules, strict=False):
    """
    v2.0: 可配置验证规则 + 评分系统。
    返回: (score, grade, status, issues)
    """
    sections = extract_sections(text)
    score = 100
    issues = []

    # 1. 检查 required_sections
    for section_rule in rules.get("required_sections", []):
        name = section_rule["name"]
        patterns = section_rule["patterns"]
        deduct = section_rule.get("deduct", 15)

        found, content = check_section_exists(sections, name, patterns)
        if not found:
            score -= deduct
            issues.append(("fail", f"缺少必要 section: {name}（扣{deduct}分）"))
        elif not has_substantial_content(content):
            score -= deduct // 2
            issues.append(("warn", f"{name}: 存在但内容为空或仅占位符（扣{deduct//2}分）"))
        else:
            issues.append(("pass", f"{name}: 内容完整"))

    # 2. 检查 recommended_sections
    for section_rule in rules.get("recommended_sections", []):
        name = section_rule["name"]
        patterns = section_rule["patterns"]
        deduct = section_rule.get("deduct", 5)

        found, content = check_section_exists(sections, name, patterns)
        if not found:
            score -= deduct
            issues.append(("warn", f"建议补充: {name}（扣{deduct}分）"))
        elif not has_substantial_content(content):
            score -= deduct // 2
            issues.append(("warn", f"{name}: 存在但内容较少（扣{deduct//2}分）"))
        else:
            issues.append(("pass", f"{name}: 内容完整"))

    # 3. 检查 min_content_length
    for section_name, min_len in rules.get("min_content_length", {}).items():
        # 在 sections 中查找
        found_key = None
        for key in sections:
            if key.startswith("__"):
                continue
            if section_name in key or key in section_name:
                found_key = key
                break

        if found_key:
            content = sections[found_key]
            clean_content = re.sub(r"[\s\n\r<>/!-]", "", content)
            if len(clean_content) < min_len:
                deduct = 3
                score -= deduct
                issues.append(("warn", f"{section_name}: 内容过少（{len(clean_content)}字 < {min_len}字要求，扣{deduct}分）"))

    # 4. 检查 required_keywords
    full_text = text
    for kw_rule in rules.get("required_keywords", []):
        keyword = kw_rule["keyword"]
        section_hint = kw_rule.get("section_hint", "")
        deduct = kw_rule.get("deduct", 3)

        if section_hint:
            # 只在指定 section 中搜索
            search_text = ""
            for key in sections:
                if section_hint in key or key in section_hint:
                    search_text = sections[key]
                    break
            if keyword not in search_text:
                score -= deduct
                issues.append(("warn", f"关键词 \"{keyword}\" 未在 {section_hint} 中出现（扣{deduct}分）"))
        else:
            if keyword not in full_text:
                score -= deduct
                issues.append(("warn", f"关键词 \"{keyword}\" 未出现（扣{deduct}分）"))

    # 5. 自定义检查
    for check in rules.get("custom_checks", []):
        check_name = check.get("name", "自定义检查")
        check_type = check.get("type", "contains")
        check_target = check.get("target", "")
        check_value = check.get("value", "")
        deduct = check.get("deduct", 5)

        target_text = ""
        if check_target:
            for key in sections:
                if check_target in key or key in check_target:
                    target_text = sections[key]
                    break
        else:
            target_text = full_text

        passed = True
        if check_type == "contains":
            passed = check_value in target_text
        elif check_type == "regex":
            passed = bool(re.search(check_value, target_text))
        elif check_type == "min_length":
            clean = re.sub(r"[\s\n\r]", "", target_text)
            passed = len(clean) >= int(check_value)
        elif check_type == "date_format":
            passed = bool(re.search(r"\d{1,2}[/.-]\d{1,2}|\d{4}[/.-]\d{1,2}", target_text))

        if not passed:
            score -= deduct
            issues.append(("warn", f"{check_name}: 未通过（扣{deduct}分）"))

    # 确保分数不低于 0
    score = max(0, score)

    # 评定等级
    grade = "D"
    for threshold, g in GRADE_THRESHOLDS:
        if score >= threshold:
            grade = g
            break

    # 综合状态
    has_fail = any(level == "fail" for level, _ in issues)
    has_warn = any(level == "warn" for level, _ in issues)

    if has_fail:
        status = "fail"
    elif has_warn:
        status = "warn"
    else:
        status = "pass"

    # strict 模式：WARN 也当 FAIL
    if strict and status == "warn":
        status = "fail"

    return score, grade, status, issues


def print_report(filepath, score, grade, status, issues, strict=False):
    """打印验证报告。"""
    color = {"pass": GREEN, "warn": YELLOW, "fail": RED}[status]
    label = {"pass": "PASS", "warn": "WARN", "fail": "FAIL"}[status]

    print(f"\n{'='*50}")
    print(f"Spec 验证报告 v2.0: {filepath}")
    if strict:
        print(f"（严格模式：WARN 视为 FAIL）")
    print(f"{'='*50}")
    print(f"得分: {CYAN}{score}/100{RESET}  等级: {CYAN}{grade}{RESET}")
    print(f"状态: {color}{label}{RESET}\n")

    icon_map = {"pass": "[OK]", "warn": "[WARN]", "fail": "[FAIL]"}
    for level, msg in issues:
        icon = icon_map[level]
        print(f"  {icon} {msg}")

    print()


def print_json_report(filepath, score, grade, status, issues, strict=False):
    """以 JSON 格式输出报告。"""
    report = {
        "file": filepath,
        "score": score,
        "grade": grade,
        "status": status,
        "strict": strict,
        "issues": [{"level": level, "message": msg} for level, msg in issues],
    }
    print(json.dumps(report, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="spec-engine validate v2.0 — 可配置的 spec 完整性验证器"
    )
    parser.add_argument("spec_file", help="spec 文件路径")
    parser.add_argument("--rules", "-r", default=None,
                        help="自定义验证规则 JSON 文件路径（可选）")
    parser.add_argument("--strict", "-s", action="store_true",
                        help="严格模式：WARN 也当作 FAIL")
    parser.add_argument("--json", "-j", action="store_true",
                        help="JSON 格式输出")
    args = parser.parse_args()

    if not os.path.isfile(args.spec_file):
        print(f"[ERROR] 文件不存在: {args.spec_file}", file=sys.stderr)
        sys.exit(1)

    # 加载规则
    if args.rules:
        rules = load_rules(args.rules)
    else:
        rules = DEFAULT_RULES

    # 读取并验证
    text = read_file(args.spec_file)
    score, grade, status, issues = validate_spec(text, rules, strict=args.strict)

    # 输出
    if args.json:
        print_json_report(args.spec_file, score, grade, status, issues, args.strict)
    else:
        print_report(args.spec_file, score, grade, status, issues, args.strict)

    # Exit code
    if status == "fail":
        sys.exit(1)
    elif status == "warn":
        sys.exit(2)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
