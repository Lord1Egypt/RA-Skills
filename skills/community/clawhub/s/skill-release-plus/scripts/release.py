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
from _lib_package import (
    package_skill, try_sign_skill,
    build_clean_stage, detect_private_key, init_private_key,
    do_package_only, read_skill_md_version,
)
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

    # 4. Resolve sign mode (v1.1.0: auto-detect, ported from the internal edition)
    #    --no-sign > --sign > auto-detect (private key present → sign; absent → unsigned)
    if args.no_sign:
        sign_mode = False
        sign_reason = "--no-sign"
    elif args.sign:
        key_status, key_path = detect_private_key()
        if key_status != "ok":
            why = "no private key found" if key_status == "missing" else "private key file unreadable"
            print(f"❌ --sign requested but {why}: {key_path}", file=sys.stderr)
            print("   → enable signing: python3 scripts/release.py --init-sign-key, then retry",
                  file=sys.stderr)
            print("   → publish unsigned: drop --sign (auto-unsigned when no key exists)",
                  file=sys.stderr)
            return 1
        sign_mode, sign_reason = True, "--sign"
    else:
        key_status, key_path = detect_private_key()
        if key_status == "corrupt":
            print(f"❌ Signing private key exists but is unreadable: {key_path}", file=sys.stderr)
            print("   → fix or delete the file, or pass --no-sign to publish unsigned",
                  file=sys.stderr)
            return 1
        sign_mode = (key_status == "ok")
        sign_reason = (f"private key detected ({key_path})" if sign_mode
                       else "no private key — auto-unsigned")

    if sign_mode:
        print(f"📦 [1/4] Signing enabled ({sign_reason}).", file=sys.stderr)
    else:
        print(f"📦 [1/4] Unsigned mode ({sign_reason}; --init-sign-key enables signing).",
              file=sys.stderr)

    # 5. Build clean stage: signing & packaging share ONE file-set baseline, so
    #    sign.key's content_hash always matches the shipped files (no drift).
    #    keep_sign_key=False in unsigned mode drops any stale sign.key from source
    #    (an old signature covers old content → false tampering reports downstream).
    out_dir = (os.path.expanduser(args.output_dir) if args.output_dir else "") or \
        cfg.get("SRP_OUTPUT_DIR") or os.path.join(os.getcwd(), "output", "skill-release")
    out_dir = os.path.expanduser(out_dir)
    stage_root = os.path.join(out_dir, ".stage")
    try:
        os.makedirs(stage_root, exist_ok=True)
        stage_skill = build_clean_stage(args.slug, skill_dir, stage_root,
                                         keep_sign_key=sign_mode,
                                         skill_root_for_config=Path(_SCRIPT_DIR).parent)
    except Exception as e:
        print(f"❌ failed to build clean staging dir: {e}", file=sys.stderr)
        return 1

    # 6. Sign the staged copy (dry-run keeps legacy behavior: no signing side effects)
    if args.dry_run:
        print("📦 [1/4] Signing skipped (dry-run mode).", file=sys.stderr)
    elif sign_mode:
        sign_optional = cfg.get("SRP_SIGN_OPTIONAL", "true").lower() == "true"
        print("📦 [1/4] Signing staged copy ...", file=sys.stderr)
        sign_result = try_sign_skill(stage_skill, optional=sign_optional)
        if not sign_result["ok"]:
            shutil.rmtree(stage_root, ignore_errors=True)
            print(f"❌ sign failed: {sign_result['error']}", file=sys.stderr)
            return 1
        if sign_result.get("skipped"):
            print(f"   ⚠️  {sign_result['reason']}", file=sys.stderr)
            # Degraded to unsigned: rebuild stage without the stale sign.key
            # copied from source (it would ship an outdated signature).
            stage_skill = build_clean_stage(args.slug, skill_dir, stage_root,
                                             keep_sign_key=False,
                                             skill_root_for_config=Path(_SCRIPT_DIR).parent)
        else:
            print(f"   ✓ signed; content_hash={sign_result.get('hash', '')[:16]}...",
                  file=sys.stderr)
            # Best-effort: re-sign the source dir too so local verify() works there.
            # The two sign.key files describe two different file sets; both verify.
            try:
                local_sign = try_sign_skill(skill_dir, optional=True)
                if local_sign.get("ok") and not local_sign.get("skipped"):
                    print("   ✓ source dir re-signed (local verify works)", file=sys.stderr)
            except Exception:
                pass
    else:
        print("📦 [1/4] Unsigned mode: package will contain no sign.key.", file=sys.stderr)

    # 7. Package the staged copy (the exact baseline the signature covers)
    print(f"📦 [2/4] Packaging into {out_dir}/{args.slug}.tar.gz ...", file=sys.stderr)
    pkg_result = package_skill(args.slug, stage_skill, out_dir,
                               skill_root_for_config=Path(_SCRIPT_DIR).parent)
    shutil.rmtree(stage_root, ignore_errors=True)
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

    # 安全网报告：如实告知哪些敏感内容被拦截、未随包发布
    sensitive = pkg_result.get("sensitive_excluded") or []
    if sensitive:
        print("   🔒 安全网拦截 — 以下敏感内容未随包发布：", file=sys.stderr)
        for f in sensitive:
            print(f"     - {f}", file=sys.stderr)
    skipped_links = pkg_result.get("symlinks_skipped") or []
    if skipped_links:
        print("   🔗 以下符号链接已跳过（不跟随进包）：", file=sys.stderr)
        for f in skipped_links:
            print(f"     - {f}", file=sys.stderr)
    if sign_mode:
        print("   ℹ️  v1.1.1 起 sign.key 不再随包发布（避免 hub 侧扫描误报）",
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
            "sensitive_excluded": pkg_result.get("sensitive_excluded") or [],
            "symlinks_skipped": pkg_result.get("symlinks_skipped") or [],
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


def cmd_package_only(args, cfg: dict) -> int:
    """Deterministic unsigned ZIP: no credentials, no network, no source mutation.

    Ported from the internal edition's v1.4.x governance flow: the caller
    resolves the target version upstream, this mode only accepts an exact
    --expected-version that must equal the SKILL.md frontmatter value.
    """
    skill_dir = os.path.abspath(args.skill_dir)
    out_dir = os.path.expanduser(args.output_dir) if args.output_dir else \
        os.path.join(os.getcwd(), "output", "skill-release")

    if not os.path.isdir(skill_dir):
        result = {"ok": False, "mode": "package-only", "slug": args.slug,
                  "code": "SKILL_NOT_FOUND", "error": f"skill directory not found: {skill_dir}"}
    elif not os.path.isfile(os.path.join(skill_dir, "SKILL.md")):
        result = {"ok": False, "mode": "package-only", "slug": args.slug,
                  "code": "SKILL_MD_MISSING", "error": f"SKILL.md not found in {skill_dir}"}
    else:
        result = do_package_only(args.slug, skill_dir, out_dir,
                                 args.expected_version,
                                 skill_root_for_config=Path(_SCRIPT_DIR).parent,
                                 tool_version=read_skill_md_version(Path(_SCRIPT_DIR).parent))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result.get("ok"):
        return 0
    return 2 if result.get("skipped") else 1


def cmd_init_sign_key(args, cfg: dict) -> int:
    """One-shot generation of the signing private key, then exit."""
    result = init_private_key()
    if not result["ok"]:
        print(f"❌ {result['error']}: {result['path']}", file=sys.stderr)
        print("   Fix or delete the file, then re-run --init-sign-key.", file=sys.stderr)
        return 1
    if result["existed"]:
        print(f"ℹ️  Signing private key already exists: {result['path']} — nothing to do.",
              file=sys.stderr)
        print("   Resetting it would break identity checks of historical signatures;",
              file=sys.stderr)
        print("   delete the file manually first if you really mean to reset.", file=sys.stderr)
        return 0
    print(f"✅ Signing private key generated: {result['path']}", file=sys.stderr)
    print("   Future publishes will sign automatically (key presence = sign mode).",
          file=sys.stderr)
    return 0


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
    # ── Sign mode controls (ported from internal v1.3.0) ──────────────────────
    p.add_argument("--sign", action="store_true",
                   help="force signing (requires an existing private key; "
                        "run --init-sign-key first)")
    p.add_argument("--no-sign", action="store_true",
                   help="force unsigned publish (skip signing; package has no sign.key)")
    p.add_argument("--init-sign-key", action="store_true",
                   help="generate the signing private key (~/.openclaw/workspace/.sign-key) "
                        "and exit")
    # ── Package-only mode (ported from internal v1.4.x) ──────────────────────
    p.add_argument("--package-only", action="store_true",
                   help="build a deterministic unsigned ZIP only; no credentials, "
                        "no network, no source mutation")
    p.add_argument("--expected-version", default="",
                   help="required by --package-only; must exactly match the "
                        "SKILL.md frontmatter version")
    p.add_argument("--output-dir", default="",
                   help="package output directory (default: ./output/skill-release)")
    return p


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.sign and args.no_sign:
        parser.error("--sign and --no-sign are mutually exclusive")

    cfg = resolve_config(cli_overrides={
        "SRP_DEFAULT_TARGETS": args.target or None,
    })

    if args.init_sign_key:
        return cmd_init_sign_key(args, cfg)
    if args.show_exclude:
        return cmd_show_exclude(args, cfg)
    if args.check:
        return cmd_check(args, cfg)
    if args.package_only:
        incompatible = []
        for enabled, name in (
            (args.sign, "--sign"), (args.no_sign, "--no-sign"),
            (args.init_sign_key, "--init-sign-key"),
            (args.dry_run, "--dry-run"),
        ):
            if enabled:
                incompatible.append(name)
        if incompatible:
            parser.error("--package-only cannot combine with: " + ", ".join(incompatible))
        if args.version:
            parser.error("--package-only uses --expected-version, not --version")
        if not args.slug:
            parser.error("--package-only requires --slug")
        if not args.expected_version:
            parser.error("--package-only requires --expected-version")
        return cmd_package_only(args, cfg)
    if not args.slug:
        parser.error("--slug is required (or use --show-exclude / --check / "
                     "--package-only / --init-sign-key)")
    return cmd_publish(args, cfg)


if __name__ == "__main__":
    sys.exit(main())
