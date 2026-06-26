#!/usr/bin/env python3
"""Batch install curated skill packs for OpenClaw."""

import subprocess
import sys
import shutil
import time

PACKS = {
    "essential": [
        "agent-memory-architect",
        "self-improving",
        "find-skills",
        "quick-note",
        "weather",
        "summarize",
        "multi-search-engine",
    ],
    "developer": [
        # includes essential
        "agent-memory-architect",
        "self-improving",
        "find-skills",
        "quick-note",
        "weather",
        "summarize",
        "multi-search-engine",
        # developer extras
        "git-workflows",
        "browser-use",
        "image-analyzer",
        "github",
    ],
    "full": [
        # includes developer
        "agent-memory-architect",
        "self-improving",
        "find-skills",
        "quick-note",
        "weather",
        "summarize",
        "multi-search-engine",
        "git-workflows",
        "browser-use",
        "image-analyzer",
        "github",
        # full extras
        "agent-team-monitor",
        "decide",
        "proactive-agent",
    ],
}


def find_clawhub():
    """Find clawhub or npx clawhub."""
    clawhub = shutil.which("clawhub")
    if clawhub:
        return [clawhub]
    npx = shutil.which("npx")
    if npx:
        return [npx, "clawhub"]
    return None


def install_skill(cmd_base, skill_name):
    """Install a single skill. Returns (name, success, message)."""
    cmd = cmd_base + ["install", skill_name]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
        )
        output = (result.stdout + result.stderr).strip()
        if result.returncode == 0:
            return (skill_name, True, output or "installed")
        else:
            return (skill_name, False, output or f"exit code {result.returncode}")
    except subprocess.TimeoutExpired:
        return (skill_name, False, "timeout (120s)")
    except Exception as e:
        return (skill_name, False, str(e))


def main():
    if len(sys.argv) < 2:
        print("Usage: install_pack.py <essential|developer|full> [extra-skill ...]")
        print()
        print("Packs:")
        for name, skills in PACKS.items():
            print(f"  {name}: {len(skills)} skills")
        sys.exit(1)

    pack_name = sys.argv[1].lower()
    extra_skills = sys.argv[2:]

    if pack_name not in PACKS:
        print(f"Unknown pack: {pack_name}")
        print(f"Available: {', '.join(PACKS.keys())}")
        sys.exit(1)

    skills = list(PACKS[pack_name])
    for s in extra_skills:
        if s not in skills:
            skills.append(s)

    cmd_base = find_clawhub()
    if not cmd_base:
        print("Error: clawhub not found. Install with: npm i -g clawhub")
        sys.exit(1)

    print(f"📦 Installing {pack_name} pack ({len(skills)} skills)...")
    print()

    succeeded = []
    failed = []

    for i, skill in enumerate(skills, 1):
        print(f"[{i}/{len(skills)}] Installing {skill}...", end=" ", flush=True)
        name, ok, msg = install_skill(cmd_base, skill)
        if ok:
            print("✅")
            succeeded.append(name)
        else:
            print(f"❌ {msg}")
            failed.append((name, msg))
        # Small delay to respect rate limits
        if i < len(skills):
            time.sleep(1)

    print()
    print("=" * 50)
    print(f"✅ Installed: {len(succeeded)}/{len(skills)}")
    if failed:
        print(f"❌ Failed: {len(failed)}")
        for name, msg in failed:
            print(f"   - {name}: {msg}")
        print()
        print("Retry failed skills manually:")
        for name, _ in failed:
            print(f"  clawhub install {name}")
    else:
        print("🎉 All skills installed successfully!")

    print()
    print("💡 Restart your session for new skills to take effect.")


if __name__ == "__main__":
    main()
