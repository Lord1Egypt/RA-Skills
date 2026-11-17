#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WenYan - Core Style Engine

Commands:
  prompt    {style_id}    Generate system prompt for the style
  map       {style_id}    Read stdin, map vocabulary
  validate  {style_id}    Read stdin, validate, return JSON
  score     {style_id}    Read stdin, score, return JSON
  all                     List all available style IDs
"""

import json
import os
import sys
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
STYLES_DIR = os.path.join(SKILL_DIR, "references", "styles")
SHARED_DIR = os.path.join(SKILL_DIR, "references", "shared")

MODERN_SYMBOLS = set(
    "\u2605\u2606\u2660\u2665\u2666\u2663"
    "\u266a\u266b\u266c\u2191\u2193\u2190\u2192"
    "\u2196\u2197\u2198\u2199\u221a\u00d7\u00f7"
    "\u00b1\u221e\u2248\u2260\u2264\u2265"
)


def load_style(style_id):
    path = os.path.join(STYLES_DIR, style_id + ".style.json")
    if not os.path.exists(path):
        raise FileNotFoundError("Style config not found: " + path)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_taboo_words():
    path = os.path.join(SHARED_DIR, "taboo-words.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    words = []
    for category in data.get("categories", {}).values():
        if isinstance(category, list):
            words.extend(category)
    return words


def generate_prompt(style_id):
    style = load_style(style_id)
    taboo = load_taboo_words()
    lines = []
    lines.append("## GuFeng Style Instruction -- " + style["name"] + " (" + style["era"] + ")")
    lines.append("")
    lines.append("You MUST reply in the following style. This is mandatory, not optional.")
    lines.append("")

    lines.append("### Core Rules")
    for rule in style.get("rules", []):
        lines.append("- " + rule)
    lines.append("")

    lines.append("### Address System")
    addr = style.get("address_system", {})
    lines.append("- Self: " + ", ".join(addr.get("self", [])))
    lines.append("- Other: " + ", ".join(addr.get("other", [])))
    lines.append("- Authority: " + ", ".join(addr.get("authority", [])))
    lines.append("- Time words: " + ", ".join(addr.get("time_words", [])))
    lines.append("")

    lines.append("### Forbidden Words (usage = FAIL)")
    taboo_sample = taboo[:30] if len(taboo) > 30 else taboo
    lines.append("Absolutely forbidden: " + ", ".join(taboo_sample))
    lines.append("")

    lines.append("### Vocabulary Mapping (modern -> classical)")
    for modern, ancient in style.get("forbidden_replacements", {}).items():
        lines.append("- " + modern + " -> " + ancient)
    lines.append("")

    lines.append("### Sentence Templates (MUST use)")
    for situation, templates in style.get("style_templates", {}).items():
        lines.append("#### " + situation)
        for t in templates:
            lines.append("  - " + t)
        lines.append("")

    rhetoric = style.get("rhetoric", {})
    if rhetoric.get("must_use"):
        lines.append("### Required Rhetoric: " + ", ".join(rhetoric["must_use"]))
    if rhetoric.get("forbidden"):
        lines.append("### Forbidden Rhetoric: " + ", ".join(rhetoric["forbidden"]))
    lines.append("")

    qt = style.get("quality_thresholds", {})
    lines.append("### Quality Standards")
    lines.append("- Max sentence length: " + str(qt.get("max_sentence_length", 15)) + " chars")
    max_modern = qt.get("max_modern_ratio", 0.05)
    lines.append("- Max modern char ratio: " + str(int(max_modern * 100)) + "%")
    lines.append("- Min style score: " + str(qt.get("style_score_min", 70)))
    lines.append("")

    lines.append("### Exceptions")
    lines.append("- Code, commands, file paths, URLs: keep original, do NOT convert")
    lines.append("- User says 'shuohua mode' / 'exit gufeng' / 'normal mode': exit style immediately, use normal language")
    lines.append("- Accuracy always trumps style, never sacrifice accuracy for style")

    return "\n".join(lines)


def count_chinese_chars(text):
    return sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")


def is_modern_char(ch):
    cp = ord(ch)
    if (0x41 <= cp <= 0x5A) or (0x61 <= cp <= 0x7A) or (0x30 <= cp <= 0x39):
        return True
    if (0xFF21 <= cp <= 0xFF3A) or (0xFF41 <= cp <= 0xFF5A) or (0xFF10 <= cp <= 0xFF19):
        return True
    if ch in MODERN_SYMBOLS:
        return True
    return False


def calculate_modern_ratio(text):
    chinese = count_chinese_chars(text)
    if chinese == 0:
        return 0.0
    modern = sum(1 for ch in text if is_modern_char(ch))
    return modern / len(text) if len(text) > 0 else 0.0


def check_forbidden_patterns(text, style):
    found = []
    taboo = load_taboo_words()
    for word in taboo:
        if word in text:
            found.append("Global taboo: " + word)
    for pattern in style.get("forbidden_patterns", []):
        matches = re.findall(pattern, text)
        for m in matches:
            found.append("Forbidden pattern: " + m)
    return found


def check_sentence_length(text, max_len):
    issues = []
    sentences = re.split(r"[\u3002\uff01\uff1f!?]", text)
    for i, sent in enumerate(sentences):
        sent = sent.strip()
        if not sent:
            continue
        chinese_len = count_chinese_chars(sent)
        if chinese_len > max_len:
            issues.append("Sentence " + str(i+1) + " too long: " + str(chinese_len) + " chars (max " + str(max_len) + ")")
    return issues


def check_style_drift(text, style, window=3):
    issues = []
    sentences = re.split(r"[\u3002\uff01\uff1f!?]", text)
    modern_streak = 0
    for i, sent in enumerate(sentences):
        sent = sent.strip()
        if not sent:
            continue
        chinese_len = count_chinese_chars(sent)
        if chinese_len == 0:
            continue
        modern_count = sum(1 for ch in sent if is_modern_char(ch))
        modern_ratio = modern_count / len(sent)
        if modern_ratio > 0.3:
            modern_streak += 1
            if modern_streak >= window:
                issues.append("Style drift: sentences " + str(i-window+2) + "-" + str(i+1) + " are " + str(modern_streak) + " consecutive modern sentences")
        else:
            modern_streak = 0
    return issues


def map_vocabulary(text, style):
    replacements = style.get("forbidden_replacements", {})
    result = text
    for modern, ancient in sorted(replacements.items(), key=lambda x: -len(x[0])):
        result = result.replace(modern, ancient)
    return result


def validate_text(text, style_id):
    style = load_style(style_id)
    qt = style.get("quality_thresholds", {})
    max_len = qt.get("max_sentence_length", 15)
    max_modern = qt.get("max_modern_ratio", 0.05)

    errors = []
    warnings = []

    forbidden = check_forbidden_patterns(text, style)
    if forbidden:
        errors.extend(["Forbidden word: " + w for w in forbidden])

    length_issues = check_sentence_length(text, max_len)
    if length_issues:
        warnings.extend(length_issues)

    modern_ratio = calculate_modern_ratio(text)
    if modern_ratio > max_modern:
        warnings.append("Modern ratio: " + "{:.1%}".format(modern_ratio) + " (max " + "{:.0%}".format(max_modern) + ")")

    drift = check_style_drift(text, style)
    if drift:
        warnings.extend(drift)

    return {
        "style_id": style_id,
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "modern_ratio": modern_ratio,
        "chinese_char_count": count_chinese_chars(text),
        "total_char_count": len(text),
    }


def score_text(text, style_id):
    style = load_style(style_id)
    qt = style.get("quality_thresholds", {})
    validation = validate_text(text, style_id)

    score = 100

    for err in validation["errors"]:
        score -= 15

    max_len = qt.get("max_sentence_length", 15)
    for warn in validation["warnings"]:
        if "too long" in warn:
            score -= 5

    modern_ratio = validation["modern_ratio"]
    max_modern = qt.get("max_modern_ratio", 0.05)
    if modern_ratio > max_modern:
        score -= int((modern_ratio - max_modern) * 200)

    for warn in validation["warnings"]:
        if "drift" in warn:
            score -= 10

    score = max(0, min(100, score))

    return {
        "style_id": style_id,
        "score": score,
        "pass": score >= qt.get("style_score_min", 70),
        "validation": validation,
    }


def list_styles():
    styles = []
    for fname in os.listdir(STYLES_DIR):
        if fname.endswith(".style.json"):
            sid = fname.replace(".style.json", "")
            with open(os.path.join(STYLES_DIR, fname), "r", encoding="utf-8") as f:
                data = json.load(f)
            styles.append({
                "id": sid,
                "name": data.get("name", sid),
                "era": data.get("era", "unknown"),
            })
    return styles


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "all":
        styles = list_styles()
        print(json.dumps(styles, ensure_ascii=False, indent=2))
        return

    if len(sys.argv) < 3:
        print("Usage: " + sys.argv[0] + " " + cmd + " <style_id>", file=sys.stderr)
        sys.exit(1)

    style_id = sys.argv[2]

    if cmd == "prompt":
        print(generate_prompt(style_id))
    elif cmd == "map":
        text = sys.stdin.read()
        style = load_style(style_id)
        result = map_vocabulary(text, style)
        print(result)
    elif cmd == "validate":
        text = sys.stdin.read()
        result = validate_text(text, style_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif cmd == "score":
        text = sys.stdin.read()
        result = score_text(text, style_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("Unknown command: " + cmd, file=sys.stderr)
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
