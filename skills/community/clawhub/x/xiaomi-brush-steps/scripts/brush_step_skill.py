#!/usr/bin/env python3
"""Huami Brush Step Skill for OpenClaw"""
import sys
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
SKILL_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(SCRIPT_DIR))

from manager import BrushStepManager


def check_deps():
    try:
        __import__('requests')
        __import__('Crypto')
        return True
    except ImportError:
        print("[X] Missing deps. Run: pip install requests pycryptodome")
        return False


def check_config():
    config_path = SKILL_DIR / "config.json"
    if not config_path.exists():
        print(f"[X] config.json not found")
        return False
    from config import get_config
    config = get_config(str(config_path))
    accounts = config.get_accounts()
    if not accounts or not all(a.get('username') and a.get('password') for a in accounts):
        print("[!] No valid accounts in config.json")
        return False
    return True


def format_report(results, min_steps, max_steps):
    success = sum(1 for r in results if isinstance(r, dict) and r.get("success"))
    lines = [
        "=== Brush Step Report ===",
        f"Range: {min_steps} - {max_steps}",
        f"Status: {'[OK]' if success == len(results) else '[PARTIAL]'}",
        f"Success: {success}/{len(results)}",
        ""
    ]
    for i, r in enumerate(results):
        if isinstance(r, dict):
            name = r.get("name", r.get("user", "Unknown"))
            step = r.get("step", "-")
            status = "[OK]" if r.get("success") else "[FAIL]"
            lines.append(f"{i+1}. {name}: {step} steps {status}")
    lines.append("=" * 24)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description='Huami Brush Step Skill')
    parser.add_argument('--min-steps', type=int)
    parser.add_argument('--max-steps', type=int)
    parser.add_argument('--account', type=str, help='Specify account name to brush')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()

    print("=" * 60)
    print("[*] Huami Brush Step Skill v1.0.0")
    print("=" * 60)

    if args.check:
        if not check_deps() or not check_config():
            sys.exit(1)
        print("[OK] Environment ready")
        return

    if not check_deps() or not check_config():
        sys.exit(1)

    from config import get_config
    config = get_config(str(SKILL_DIR / "config.json"))
    min_steps = args.min_steps or config.get_min_steps()
    max_steps = args.max_steps or config.get_max_steps()

    print(f"[*] Range: {min_steps} - {max_steps}")
    if args.account:
        print(f"[*] Account: {args.account}")
    print("[*] Starting...")

    try:
        manager = BrushStepManager(str(SKILL_DIR / "config.json"))
        results = manager.run(min_steps, max_steps, args.account)
        print("\n[OK] Done!")
        if results:
            success = sum(1 for r in results if isinstance(r, dict) and r.get("success"))
            print(f"[*] Stats: {success}/{len(results)}")
        print("\n" + format_report(results, min_steps, max_steps))
    except Exception as e:
        print(f"\n[X] Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
