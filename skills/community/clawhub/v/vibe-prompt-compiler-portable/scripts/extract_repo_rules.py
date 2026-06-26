#!/usr/bin/env python3
import argparse
import json
import pathlib

RULE_KEYS = ["must_rules", "must_not_rules", "validation_rules", "scope_guardrails"]


def empty_rules() -> dict:
    return {key: [] for key in RULE_KEYS}



def add(rule_map: dict, key: str, value: str):
    if value not in rule_map[key]:
        rule_map[key].append(value)



def scan_text(text: str, rules: dict):
    lower = text.lower()

    if "do not modify unrelated files" in lower or "不要改动无关文件" in text:
        add(rules, "must_not_rules", "Do not modify unrelated files.")
    if "keep changes consistent" in lower or "保持现有" in text:
        add(rules, "must_rules", "Keep changes consistent with the existing codebase.")
    if "update documentation" in lower or "更新文档" in text:
        add(rules, "must_rules", "Update documentation when the change affects usage or behavior.")
    if "do not add dependencies" in lower or "unnecessary dependencies" in lower or "避免引入不必要依赖" in text:
        add(rules, "must_not_rules", "Do not add dependencies unless necessary and justified.")
    if "minimal" in lower or "最小" in text:
        add(rules, "scope_guardrails", "Prefer the smallest change that solves the root problem.")
    if "test" in lower or "验证" in text or "验收" in text:
        add(rules, "validation_rules", "Describe or run the narrowest relevant validation for the change.")
    if "agents.md" in lower or "test agents" in lower:
        add(rules, "must_rules", "Respect AGENTS.md instructions for touched files.")



def scan_package_json(path: pathlib.Path, rules: dict):
    data = json.loads(path.read_text(encoding="utf-8"))
    scripts = data.get("scripts", {})
    if not scripts:
        return
    if any(name in scripts for name in ["test", "test:unit", "check"]):
        add(rules, "validation_rules", "Prefer existing repository test scripts before inventing custom validation commands.")
    if any(name in scripts for name in ["lint", "format", "check"]):
        add(rules, "must_rules", "Prefer existing repository lint/format scripts when validating changes.")



def extract_rules(repo_root: str) -> dict:
    root = pathlib.Path(repo_root)
    rules = empty_rules()
    candidates = [root / "AGENTS.md", root / "README.md", root / "package.json"]

    for candidate in candidates:
        if not candidate.exists():
            continue
        if candidate.name == "package.json":
            scan_package_json(candidate, rules)
        else:
            scan_text(candidate.read_text(encoding="utf-8"), rules)

    return rules



def main():
    parser = argparse.ArgumentParser(description="Extract a small repository-aware rules JSON from common repo files.")
    parser.add_argument("--repo-root", required=True, help="Repository root to inspect")
    parser.add_argument("--output", default="json", choices=["json"], help="Output format")
    args = parser.parse_args()

    rules = extract_rules(args.repo_root)
    print(json.dumps(rules, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
