#!/usr/bin/env python3
"""
analyze_skill.py — Load TEST.md or generate test cases via LLM.

Open-source version: uses OpenAI-compatible LLM (via _lib_llm) instead of `openclaw ask`.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

# Local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _lib_config import resolve_config, require_config_ready  # noqa: E402
from _lib_llm import infer_test_cases  # noqa: E402

try:
    import yaml  # type: ignore
except ImportError:
    print("❌ pyyaml not installed. Run: pip install pyyaml --break-system-packages", file=sys.stderr)
    sys.exit(1)


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--skill-dir", required=True)
    p.add_argument("--output", required=True)
    p.add_argument("--cases", type=int, default=3)
    p.add_argument("--error-cases", type=int, default=2)
    p.add_argument("--no-llm", action="store_true",
                   help="Skip LLM inference; only emit fallback placeholders if no TEST.md")
    return p.parse_args()


def load_tests_md(skill_dir):
    """Parse TEST.md (or legacy Test.md/TESTS.md) into structured case list."""
    for fname in ["TEST.md", "Test.md", "TESTS.md"]:
        tests_path = os.path.join(skill_dir, fname)
        if os.path.exists(tests_path):
            break
    else:
        return None

    print(f"  → Found {os.path.basename(tests_path)}, parsing test cases...")
    with open(tests_path, "r", encoding="utf-8") as f:
        content = f.read()

    cases = []
    yaml_blocks = re.findall(r"```yaml\n(.*?)```", content, re.DOTALL)
    for block in yaml_blocks:
        try:
            data = yaml.safe_load(block)
            if data and "trigger" in data:
                cases.append({
                    "id": data.get("id", f"case_{len(cases)+1:03d}"),
                    "name": data.get("name", f"Case {len(cases)+1}"),
                    "type": data.get("type", "normal"),
                    "trigger": data.get("trigger", ""),
                    "script_cmd": data.get("script_cmd", ""),
                    "expected_output": data.get("expected_output", ""),
                    "expected_output_mode": data.get("expected_output_mode", "contains"),
                    "expected_agent_response": data.get("expected_agent_response", ""),
                    "skip_agent": data.get("skip_agent", False),
                })
        except yaml.YAMLError:
            continue

    return cases if cases else None


def read_skill_docs(skill_dir):
    """Read SKILL.md and README.md content."""
    docs = {}
    for fname in ["SKILL.md", "README.md"]:
        fpath = os.path.join(skill_dir, fname)
        if os.path.exists(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                docs[fname] = f.read()
    return docs


def generate_default_cases(skill_name, normal_count, error_count):
    """Fallback placeholder cases when LLM inference fails or is disabled.

    These have generic triggers — AI layer would almost always pass them, producing
    false positives. So we set skip_agent=True to limit them to script-layer only.
    Users should fill in real TEST.md ASAP.
    """
    cases = []
    seq = 1
    for i in range(1, normal_count + 1):
        cases.append({
            "id": f"case_{seq:03d}",
            "name": f"Normal flow {i} (auto-generated placeholder)",
            "type": "normal",
            "trigger": f"Please use {skill_name} skill for a basic operation",
            "script_cmd": "",
            "expected_output": "",
            "expected_output_mode": "contains",
            "expected_agent_response": f"Successfully execute {skill_name} core functionality",
            "skip_agent": True,
        })
        seq += 1
    for i in range(1, error_count + 1):
        cases.append({
            "id": f"case_{seq:03d}",
            "name": f"Error handling {i} (auto-generated placeholder)",
            "type": "error",
            "trigger": f"Please use {skill_name} skill with invalid input",
            "script_cmd": "",
            "expected_output": "",
            "expected_output_mode": "contains",
            "expected_agent_response": "Recognize the error and give friendly guidance",
            "skip_agent": True,
        })
        seq += 1
    return cases


def main():
    args = parse_args()
    skill_dir = os.path.realpath(args.skill_dir)

    if not os.path.exists(skill_dir):
        print(f"Error: skill directory does not exist: {skill_dir}", file=sys.stderr)
        sys.exit(1)

    # Try TEST.md first
    cases = load_tests_md(skill_dir)
    source = "TEST.md"

    if cases is None:
        source = "LLM-generated"
        print(f"  → No TEST.md found, inferring cases from docs (normal: {args.cases}, error: {args.error_cases})...")
        docs = read_skill_docs(skill_dir)
        if not docs:
            print("  ⚠️  No SKILL.md / README.md found, using default placeholders")
            cases = generate_default_cases(os.path.basename(skill_dir), args.cases, args.error_cases)
            source = "default-placeholders"
        elif args.no_llm:
            print("  ℹ️  --no-llm set, using default placeholders")
            cases = generate_default_cases(os.path.basename(skill_dir), args.cases, args.error_cases)
            source = "default-placeholders"
        else:
            # LLM inference needs config
            cfg = resolve_config(project_dir=Path(skill_dir).parent)
            cfg = require_config_ready(cfg)
            llm_cases = infer_test_cases(
                skill_md=docs.get("SKILL.md", ""),
                readme_md=docs.get("README.md", ""),
                normal_count=args.cases,
                error_count=args.error_cases,
                cfg=cfg,
            )
            if llm_cases:
                cases = llm_cases
                # Normalize: ensure required fields exist
                for c in cases:
                    c.setdefault("id", f"case_{cases.index(c)+1:03d}")
                    c.setdefault("type", "error" if c.get("is_error_case") else "normal")
                    c.setdefault("expected_output_mode", "contains")
                    c.setdefault("skip_agent", False)
            else:
                print("  ⚠️  LLM inference failed, falling back to placeholders")
                cases = generate_default_cases(os.path.basename(skill_dir), args.cases, args.error_cases)
                source = "default-placeholders"

    output = {
        "skill_name": os.path.basename(skill_dir),
        "skill_dir": skill_dir,
        "source": source,
        "cases": cases,
    }
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"  → Cases saved: {args.output}")


if __name__ == "__main__":
    main()
