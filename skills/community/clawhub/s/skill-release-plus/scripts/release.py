#!/usr/bin/env python3
"""
skill-release-plus — publish a skill to multiple hubs.

Usage:
  python3 release.py --slug my-skill --changelog "..." [--target clawhub]
  python3 release.py --slug my-skill --changelog "..." --target clawhub,skillhub-cn
  python3 release.py --slug my-skill --changelog "..." --target all
  python3 release.py --slug my-skill --changelog "..." --target user-hook:./my-hook.sh
  python3 release.py --slug my-skill --changelog "..." --dry-run

Targets (auto-detected from env):
  clawhub          ClawHub.com (default; cn.clawhub-mirror.com auto-syncs)
  skillhub-cn      SkillHub.cn (Tencent Cloud)
  github-release   GitHub Releases (git tag + gh release)
  user-hook:<path> Custom hook script for future hubs
  all              All registered targets that have tokens ready

Exit codes:
  0  all targets succeeded
  1  business failure (one or more targets failed; see report)
  2  config missing (no targets ready / required token absent in non-TTY)
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Optional

# Ensure local scripts/ is importable
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

from _lib_config import (
    resolve_config, parse_targets, check_targets_ready,
    is_tty, onboard_token, emit_missing_token_hint,
    VALID_TARGETS, TARGET_TOKEN_ENV,
)
from _lib_package import package_skill, try_sign_skill
from _lib_adapters_base import PublishResult


# ── Adapter registry ──────────────────────────────────────────────────────

def _load_adapter(target: str, cfg: dict):
    """Lazy-load adapter class for a target. Returns instance or None+error_msg."""
    if target.startswith("user-hook:"):
        from _adapter_user_hook import UserHookAdapter  # P5
        return UserHookAdapter(cfg, hook_path=target.split(":", 1)[1]), None
    if target == "clawhub":
        from _adapter_clawhub import ClawhubAdapter
        return ClawhubAdapter(cfg), None
    if target == "skillhub-cn":
        try:
            from _adapter_skillhub_cn import SkillhubCnAdapter  # P4
            return SkillhubCnAdapter(cfg), None
        except ImportError:
            return None, "skillhub-cn adapter not implemented yet"
    if target == "github-release":
        try:
            from _adapter_github_release import GitHubReleaseAdapter  # P3
            return GitHubReleaseAdapter(cfg), None
        except ImportError:
            return None, "github-release adapter not implemented yet"
    return None, f"unknown target: {target}"


# ── Slug + version helpers ────────────────────────────────────────────────

_SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")


def validate_slug(slug: str) -> Optional[str]:
    """Return error message if invalid, else None."""
    if not slug:
        return "--slug is required"
    if not _SLUG_RE.match(slug):
        return (f"slug '{slug}' invalid; must match {_SLUG_RE.pattern}"
                " (lowercase letters, digits, hyphens; start & end alphanumeric)")
    return None


def read_skill_version_from_md(skill_dir: str) -> str:
    """Best-effort read SKILL.md frontmatter for `version` field (may not exist)."""
    md_path = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(md_path):
        return ""
    try:
        with open(md_path, encoding="utf-8") as f:
            content = f.read()
        m = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
        if not m:
            return ""
        # Simple grep for version: line; avoid yaml dep
        for line in m.group(1).splitlines():
            if line.strip().startswith("version:"):
                return line.split(":", 1)[1].strip().strip('"').strip("'")
    except Exception:
        return ""
    return ""


# ── Main pipeline ─────────────────────────────────────────────────────────

def cmd_publish(args, cfg: dict) -> int:
    # 1. Parse + validate targets
    targets_str = args.target or cfg.get("SRP_DEFAULT_TARGETS", "clawhub")
    try:
        targets = parse_targets(targets_str)
    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 2

    # 2. Validate slug + skill_dir
    err = validate_slug(args.slug)
    if err:
        print(f"❌ {err}", file=sys.stderr)
        return 2

    skill_dir = os.path.abspath(args.skill_dir)
    if not os.path.isdir(skill_dir):
        print(f"❌ skill directory not found: {skill_dir}", file=sys.stderr)
        return 2
    if not os.path.isfile(os.path.join(skill_dir, "SKILL.md")):
        print(f"❌ SKILL.md not found in {skill_dir}", file=sys.stderr)
        return 2

    # 3. Token readiness check (per target)
    ready = check_targets_ready(targets, cfg)
    unready = [(t, info["missing_env"]) for t, info in ready.items() if not info["ready"]]

    if unready:
        for target, env_key in unready:
            if is_tty():
                token = onboard_token(target)
                if token:
                    cfg[env_key] = token
                    os.environ[env_key] = token
                    # Re-check
                    ready[target]["ready"] = True
                    continue
            # Non-TTY or skipped → hint and fail
            emit_missing_token_hint(target, env_key)

        # Re-evaluate after onboarding attempts
        still_unready = [t for t, info in ready.items() if not info["ready"]]
        if still_unready:
            print(f"\n❌ Cannot proceed: {len(still_unready)} target(s) missing token: "
                  f"{', '.join(still_unready)}", file=sys.stderr)
            return 2

    # 4. Sign (optional; auto-skip if skill-sign not installed; skip in dry-run)
    if args.dry_run:
        print(f"📦 [1/4] Signing skipped (dry-run mode).", file=sys.stderr)
        sign_result = {"ok": True, "skipped": True, "reason": "dry-run mode"}
    else:
        print(f"📦 [1/4] Signing skill at {skill_dir} ...", file=sys.stderr)
        sign_optional = cfg.get("SRP_SIGN_OPTIONAL", "true").lower() == "true"
        sign_result = try_sign_skill(skill_dir, optional=sign_optional)
        if not sign_result["ok"]:
            print(f"❌ sign failed: {sign_result['error']}", file=sys.stderr)
            return 1
        if sign_result.get("skipped"):
            print(f"   ⚠️  {sign_result['reason']}", file=sys.stderr)
        else:
            print(f"   ✓ signed; content_hash={sign_result.get('hash', '')[:16]}...",
                  file=sys.stderr)

    # 5. Package (tar.gz, applies exclude rules)
    out_dir = cfg.get("SRP_OUTPUT_DIR") or os.path.join(os.getcwd(), "output", "skill-release")
    out_dir = os.path.expanduser(out_dir)
    print(f"📦 [2/4] Packaging into {out_dir}/{args.slug}.tar.gz ...", file=sys.stderr)
    pkg_result = package_skill(args.slug, skill_dir, out_dir,
                               skill_root_for_config=Path(_SCRIPT_DIR).parent)
    if not pkg_result["ok"]:
        msg = pkg_result.get("error", "unknown")
        if pkg_result.get("oversize_files"):
            print(f"❌ packaging skipped: {msg}", file=sys.stderr)
            for f in pkg_result["oversize_files"]:
                print(f"     - {f['path']} ({f['size_mb']} MB)", file=sys.stderr)
        else:
            print(f"❌ packaging failed: {msg}", file=sys.stderr)
        return 1
    tar_path = pkg_result["path"]
    print(f"   ✓ packaged {pkg_result['file_count']} files → {tar_path}",
          file=sys.stderr)

    # 6. Dry-run: stop here, just report what would happen
    if args.dry_run:
        print(f"\n🔍 [DRY-RUN] would publish to: {', '.join(targets)}", file=sys.stderr)
        print(f"   slug={args.slug} version={args.version or '(auto)'}", file=sys.stderr)
        report = {
            "dry_run": True,
            "slug": args.slug,
            "version": args.version,
            "targets": targets,
            "package": {"path": tar_path, "file_count": pkg_result["file_count"]},
        }
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    # 7. Dispatch to each target
    print(f"📦 [3/4] Publishing to {len(targets)} target(s): {', '.join(targets)} ...",
          file=sys.stderr)
    extra = {
        "display_name": args.display_name or args.slug,
    }
    results = []
    for target in targets:
        adapter, err = _load_adapter(target, cfg)
        if adapter is None:
            print(f"   ⏸ {target}: {err}", file=sys.stderr)
            results.append({"target": target, "ok": False, "error": err})
            continue
        print(f"   → {target} ...", file=sys.stderr)
        res = adapter.publish(
            slug=args.slug,
            version=args.version,
            changelog=args.changelog,
            tar_path=tar_path,
            skill_dir=skill_dir,
            extra=extra,
        )
        flag = "✅" if res.ok else "❌"
        msg = res.url if res.ok else res.error
        print(f"     {flag} {target}: {msg}", file=sys.stderr)
        results.append({
            "target": res.target,
            "ok": res.ok,
            "url": res.url,
            "version": res.version,
            "action": res.action,
            "error": res.error,
        })

    # 8. Report
    print(f"📦 [4/4] Done.", file=sys.stderr)
    success = sum(1 for r in results if r["ok"])
    total = len(results)
    print(f"   Result: {success}/{total} target(s) succeeded.", file=sys.stderr)

    summary = {
        "slug": args.slug,
        "version": args.version or "(auto)",
        "results": results,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    return 0 if success == total else 1


def cmd_show_exclude(args, cfg: dict) -> int:
    from _lib_package import load_exclude_config
    skill_root = Path(_SCRIPT_DIR).parent
    dirs, files, exts, patterns = load_exclude_config(skill_root)
    print(f"Exclude rules (from {skill_root}/config/exclude.json):")
    print(f"\nDirectories ({len(dirs)}):")
    for d in sorted(dirs):
        print(f"  {d}/")
    print(f"\nFilenames ({len(files)}):")
    for f in sorted(files):
        print(f"  {f}")
    print(f"\nExtensions ({len(exts)}):")
    for e in sorted(exts):
        print(f"  *{e}")
    if patterns:
        print(f"\nPatterns ({len(patterns)}):")
        for p in sorted(patterns):
            print(f"  {p}")
    return 0


def cmd_check(args, cfg: dict) -> int:
    """Check token readiness without publishing."""
    targets_str = args.target or cfg.get("SRP_DEFAULT_TARGETS", "clawhub")
    try:
        targets = parse_targets(targets_str)
    except ValueError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 2

    ready = check_targets_ready(targets, cfg)
    print("Target readiness check:")
    all_ok = True
    for t, info in ready.items():
        flag = "✅" if info["ready"] else "❌"
        if info["ready"]:
            print(f"  {flag} {t}: token present")
        else:
            print(f"  {flag} {t}: missing {info['missing_env']}")
            all_ok = False
    return 0 if all_ok else 2


# ── argparse ──────────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="skill-release-plus: publish a skill to multiple hubs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  release.py --slug my-skill --changelog 'first release' --skill-dir ./my-skill\n"
            "  release.py --slug my-skill -m 'fix bug' --target clawhub,skillhub-cn\n"
            "  release.py --slug my-skill -m 'test' --target user-hook:./my-hook.sh\n"
            "  release.py --slug my-skill -m 'check' --dry-run\n"
            "  release.py --show-exclude\n"
            "  release.py --check --target all\n"
        ),
    )
    p.add_argument("--slug", help="skill slug (lowercase, digits, hyphens)")
    p.add_argument("--changelog", "-m", default="", help="release changelog")
    p.add_argument("--version", default="", help="explicit version (semver); default: auto-bump or read from SKILL.md")
    p.add_argument("--display-name", default="", help="display name (default: slug)")
    p.add_argument("--skill-dir", default=".",
                   help="path to the skill folder (default: CWD)")
    p.add_argument("--target", default="",
                   help="comma-separated targets; default: SRP_DEFAULT_TARGETS or 'clawhub'")
    p.add_argument("--dry-run", action="store_true",
                   help="package only; do not publish")
    p.add_argument("--show-exclude", action="store_true",
                   help="print current exclude rules and exit")
    p.add_argument("--check", action="store_true",
                   help="check target token readiness and exit")
    return p


def main():
    parser = build_parser()
    args = parser.parse_args()

    cfg = resolve_config(cli_overrides={
        "SRP_DEFAULT_TARGETS": args.target or None,
    })

    if args.show_exclude:
        return cmd_show_exclude(args, cfg)
    if args.check:
        return cmd_check(args, cfg)
    if not args.slug:
        parser.error("--slug is required (or use --show-exclude / --check)")
    return cmd_publish(args, cfg)


if __name__ == "__main__":
    sys.exit(main())
