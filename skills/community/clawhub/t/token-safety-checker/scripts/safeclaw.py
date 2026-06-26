#!/usr/bin/env python3
"""
safeclaw.py — Token Safety Checker for OpenClaw

Subcommands:

  scan     Detect plaintext secrets in openclaw.json.
           Returns field paths, lengths, and risk levels — never secret values.
           --deep also scans git history for past exposures.

  migrate  Migrate plaintext secrets to env vars + SecretRef.
           Reads actual secret values directly from the config file — never via CLI args.
           Automatically runs verify after a successful migration.

  verify   Post-migration health check:
           - Confirms no plaintext secrets remain in config
           - Checks file permissions on openclaw.json (should be 600)
           - Checks SecretRef env vars are actually set in the current environment
           - Warns if backup .bak file is still on disk

Usage:
  python3 safeclaw.py scan   [--config PATH] [--deep]
  python3 safeclaw.py migrate --findings '[...]' [--config PATH] [--profile PATH] [--dry-run]
  python3 safeclaw.py migrate --restore [--config PATH]
  python3 safeclaw.py verify [--config PATH] [--clean-backup]

Exit codes:
  scan:    0 = no findings, 1 = findings present, 2 = config not found
  migrate: 0 = success, 1 = error
  verify:  0 = all clear, 1 = issues found
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

DEFAULT_CONFIG = Path.home() / ".openclaw" / "openclaw.json"

# ── Constants ──────────────────────────────────────────────────────────────────

SENSITIVE_KEYS = {"token", "apikey", "key", "password", "secret", "credential"}
MIN_SECRET_LEN = 16

ENV_HINTS = {
    "gateway.auth.token":             "OPENCLAW_GATEWAY_TOKEN",
    "gateway.remote.token":           "OPENCLAW_GATEWAY_TOKEN",
    "channels.discord.token":         "OPENCLAW_DISCORD_TOKEN",
    "channels.telegram.token":        "OPENCLAW_TELEGRAM_TOKEN",
    "channels.whatsapp.token":        "OPENCLAW_WHATSAPP_TOKEN",
    "tools.web.search.gemini.apiKey": "OPENCLAW_GEMINI_API_KEY",
    "tools.web.search.openai.apiKey": "OPENCLAW_OPENAI_API_KEY",
    "tools.web.search.brave.apiKey":  "OPENCLAW_BRAVE_API_KEY",
}

# Paths that directly control the agent or expose it to the internet = HIGH
HIGH_RISK_PATHS = {
    "channels.discord.token",
    "channels.telegram.token",
    "channels.whatsapp.token",
    "gateway.auth.token",
    "gateway.remote.token",
}
# API keys for third-party services = MEDIUM
MEDIUM_RISK_PATHS = {
    "tools.web.search.openai.apiKey",
    "tools.web.search.gemini.apiKey",
    "tools.web.search.brave.apiKey",
}

ENV_VAR_RE = re.compile(r'^[A-Z_][A-Z0-9_]*$')

SHELL_PROFILES = {
    "zsh":  ["~/.zshrc", "~/.zprofile"],
    "bash": ["~/.bashrc", "~/.bash_profile", "~/.profile"],
    "fish": ["~/.config/fish/config.fish"],
    "dash": ["~/.profile"],
    "sh":   ["~/.profile"],
}

RISK_ICON = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢"}

# ── Helpers ────────────────────────────────────────────────────────────────────

def detect_shell() -> dict:
    shell_name = Path(os.environ.get("SHELL", "bash")).name
    candidates = SHELL_PROFILES.get(shell_name, SHELL_PROFILES["bash"])
    profile = next((p for p in candidates if Path(p).expanduser().exists()), candidates[0])
    return {
        "name":       shell_name,
        "profile":    profile,
        "source_cmd": f"source {profile}",
    }


def to_env_name(path: str) -> str:
    if path in ENV_HINTS:
        return ENV_HINTS[path]
    parts = path.split(".")
    last   = re.sub(r'(?<!^)(?=[A-Z])', '_', parts[-1]).upper()
    prefix = re.sub(r'[^A-Z0-9]', '_', parts[-2].upper()) if len(parts) >= 2 else parts[0].upper()
    return f"OPENCLAW_{prefix}_{last}".replace("__", "_")


def get_risk_level(path: str) -> str:
    if path in HIGH_RISK_PATHS:
        return "HIGH"
    if path in MEDIUM_RISK_PATHS:
        return "MEDIUM"
    return "LOW"


def is_secretref(value) -> bool:
    return isinstance(value, dict) and value.get("source") in ("env", "file", "exec")


def collect_secretrefs(config: dict, refs: list = None) -> list:
    """Collect all SecretRef env var IDs referenced in the config."""
    if refs is None:
        refs = []
    if isinstance(config, dict):
        if is_secretref(config):
            env_id = config.get("id")
            if env_id:
                refs.append(env_id)
            return refs
        for v in config.values():
            collect_secretrefs(v, refs)
    elif isinstance(config, list):
        for v in config:
            collect_secretrefs(v, refs)
    return refs


def scan_config(config: dict, path: str = "", findings: list = None) -> list:
    """
    Recursively scan config for plaintext secrets.
    Returns list of { path, env_var, length, risk } — NO secret values.
    """
    if findings is None:
        findings = []
    if isinstance(config, dict):
        if is_secretref(config):
            return findings
        for k, v in config.items():
            scan_config(v, f"{path}.{k}" if path else k, findings)
    elif isinstance(config, list):
        for i, v in enumerate(config):
            scan_config(v, f"{path}[{i}]", findings)
    elif isinstance(config, str):
        key = path.split(".")[-1].lower().rstrip("[]0123456789")
        if any(s in key for s in SENSITIVE_KEYS) and len(config) >= MIN_SECRET_LEN:
            findings.append({
                "path":    path,
                "env_var": to_env_name(path),
                "length":  len(config),
                "risk":    get_risk_level(path),
            })
    return findings


def scan_git_history(config_path: Path) -> dict:
    """
    Scan git history of config_path for past plaintext secret exposures.
    Returns { "supported": bool, "commits_scanned": int, "exposed_commits": [...] }
    Never returns secret values — only paths, risk levels, and commit metadata.
    """
    result = {"supported": False, "commits_scanned": 0, "exposed_commits": []}

    # Check git is available
    if not shutil.which("git"):
        result["error"] = "git not found in PATH"
        return result

    # Find git root
    try:
        r = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True, text=True, cwd=config_path.parent
        )
        if r.returncode != 0:
            result["error"] = "Not a git repository"
            return result
        git_root = r.stdout.strip()
    except Exception as e:
        result["error"] = str(e)
        return result

    result["supported"] = True

    # Get relative path from git root
    try:
        rel_path = str(config_path.resolve().relative_to(Path(git_root)))
    except ValueError:
        result["error"] = "Config file is not inside a git repository"
        result["supported"] = False
        return result

    # List all commits that touched this file
    log = subprocess.run(
        ["git", "log", "--all", "--format=%H|%ai|%an", "--", rel_path],
        capture_output=True, text=True, cwd=git_root
    )
    if not log.stdout.strip():
        result["commits_scanned"] = 0
        return result

    commit_lines = [l for l in log.stdout.strip().split("\n") if l]
    result["commits_scanned"] = len(commit_lines)

    for line in commit_lines:
        parts = line.split("|", 2)
        if len(parts) < 3:
            continue
        commit_hash, date, author = parts

        show = subprocess.run(
            ["git", "show", f"{commit_hash}:{rel_path}"],
            capture_output=True, text=True, cwd=git_root
        )
        if show.returncode != 0:
            continue

        try:
            content = json.loads(show.stdout)
        except json.JSONDecodeError:
            continue

        findings = scan_config(content)
        if findings:
            result["exposed_commits"].append({
                "commit":   commit_hash[:8],
                "date":     date,
                "author":   author,
                # Only include path + risk — no values
                "findings": [{"path": f["path"], "risk": f["risk"]} for f in findings],
            })

    return result


def get_nested(d: dict, dot_path: str):
    for key in dot_path.split("."):
        if isinstance(d, dict):
            d = d.get(key)
        else:
            return None
    return d


def set_nested(d: dict, dot_path: str, value):
    keys = dot_path.split(".")
    for k in keys[:-1]:
        d = d.setdefault(k, {})
    d[keys[-1]] = value


def validate_env_var(name: str) -> str:
    if not ENV_VAR_RE.match(name):
        raise ValueError(
            f"Invalid env var name {name!r} — only A-Z, 0-9 and _ allowed, must start with a letter or _"
        )
    return name


def shell_single_quote(value: str) -> str:
    """
    Wrap value in single quotes for safe shell assignment.
    Single quotes prevent ALL interpolation ($, backtick, etc.).
    Literal ' is handled by: 'before'"'"'after' → before'after
    """
    return "'" + value.replace("'", "'\\''") + "'"


def export_line(shell: str, env_var: str, value: str) -> str:
    safe_value = shell_single_quote(value)
    if shell == "fish":
        return f"set -gx {env_var} {safe_value}"
    return f"export {env_var}={safe_value}"


def run_verify(config_path: Path, clean_backup: bool = False) -> int:
    """
    Run post-migration health checks. Returns 0 if all clear, 1 if issues found.
    Checks:
      1. No plaintext secrets remain in config
      2. File permissions are 600
      3. All SecretRef env vars are set in current environment
      4. Backup .bak file cleanup
    """
    bak_path = config_path.with_suffix(".json.bak")
    issues   = []
    ok       = []

    print("\n── SafeClaw Verify ──────────────────────────────────────────")

    if not config_path.exists():
        print(f"[ERROR] Config not found: {config_path}", file=sys.stderr)
        return 1

    with open(config_path) as f:
        config = json.load(f)

    # 1. Remaining plaintext secrets
    findings = scan_config(config)
    if findings:
        for f in findings:
            icon = RISK_ICON.get(f["risk"], "⚪")
            issues.append(f"  {icon} [{f['risk']}] Plaintext secret still present: {f['path']}")
    else:
        ok.append("  ✅ No plaintext secrets in config")

    # 2. File permissions
    mode = oct(config_path.stat().st_mode)[-3:]
    if mode != "600":
        issues.append(
            f"  🟡 [MEDIUM] openclaw.json permissions are {mode} — run: chmod 600 {config_path}"
        )
    else:
        ok.append(f"  ✅ File permissions OK (600)")

    # 3. SecretRef env vars set in current environment
    refs = collect_secretrefs(config)
    missing = [r for r in refs if not os.environ.get(r)]
    if missing:
        for m in missing:
            issues.append(
                f"  🔴 [HIGH] ${m} is referenced in config but NOT set in current environment"
            )
    elif refs:
        ok.append(f"  ✅ All {len(refs)} SecretRef env var(s) are set")
    else:
        ok.append("  ✅ No SecretRefs found (nothing to check)")

    # 4. Backup file
    if bak_path.exists():
        if clean_backup:
            bak_path.unlink()
            ok.append(f"  ✅ Backup removed: {bak_path}")
        else:
            issues.append(
                f"  🟢 [LOW] Backup file still on disk: {bak_path}  "
                f"(run with --clean-backup to delete, or keep it for rollback)"
            )

    for line in ok:
        print(line)
    if issues:
        print(f"\n  ⚠️  {len(issues)} issue(s) found:")
        for line in issues:
            print(line)
        print()
        return 1

    print("\n  🦀 All checks passed — your config looks clean!\n")
    return 0

# ── Subcommands ────────────────────────────────────────────────────────────────

def cmd_scan(args):
    config_path = Path(args.config)
    if not config_path.exists():
        print(json.dumps({"error": f"Config not found: {config_path}"}))
        sys.exit(2)

    with open(config_path) as f:
        config = json.load(f)

    findings = scan_config(config)
    shell    = detect_shell()

    # File permission check
    mode = oct(config_path.stat().st_mode)[-3:]
    perm_ok = (mode == "600")

    output = {
        "findings": findings,
        "shell":    shell,
        "checks": {
            "file_permissions": {
                "ok":   perm_ok,
                "mode": mode,
                "note": None if perm_ok else f"Should be 600 — run: chmod 600 {config_path}",
            }
        }
    }

    # Deep scan: git history
    if args.deep:
        print("[~] Scanning git history...", file=sys.stderr)
        output["git_history"] = scan_git_history(config_path)

    print(json.dumps(output, indent=2))

    # Print human-readable summary to stderr
    if findings:
        print(f"\n[!] {len(findings)} plaintext secret(s) found:", file=sys.stderr)
        for f in findings:
            icon = RISK_ICON.get(f["risk"], "⚪")
            print(f"    {icon} [{f['risk']}] {f['path']}", file=sys.stderr)

    if not perm_ok:
        print(f"\n[!] File permissions: {mode} (should be 600)", file=sys.stderr)

    if args.deep and output.get("git_history", {}).get("exposed_commits"):
        exposed = output["git_history"]["exposed_commits"]
        print(f"\n[!] git history: {len(exposed)} commit(s) contained plaintext secrets:", file=sys.stderr)
        for c in exposed:
            paths = ", ".join(x["path"] for x in c["findings"])
            print(f"    {c['commit']}  {c['date'][:10]}  [{paths}]", file=sys.stderr)
        print("\n    ⚠️  These commits are permanent in git history.", file=sys.stderr)
        print("    Consider rotating the affected tokens.", file=sys.stderr)

    sys.exit(1 if findings else 0)


def cmd_migrate(args):
    config_path = Path(args.config)
    bak_path    = config_path.with_suffix(".json.bak")

    # ── Restore mode ──────────────────────────────────────────────────────────
    if args.restore:
        if not bak_path.exists():
            print(f"[ERROR] No backup found at {bak_path}", file=sys.stderr)
            sys.exit(1)
        shutil.copy2(bak_path, config_path)
        print(f"[OK] Restored {config_path} from {bak_path}")
        return

    if not args.findings:
        print("[ERROR] --findings required", file=sys.stderr)
        sys.exit(1)

    findings = json.loads(args.findings)

    if not config_path.exists():
        print(f"[ERROR] Config not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    with open(config_path) as f:
        config = json.load(f)

    current_findings = {f["path"]: f for f in scan_config(config)}
    to_migrate = [f for f in findings if f["path"] in current_findings]

    if not to_migrate:
        print("[OK] Nothing to migrate — all findings already resolved.")
        return

    # Validate env var names before touching any file
    for f in to_migrate:
        try:
            validate_env_var(f["env_var"])
        except ValueError as e:
            print(f"[ERROR] {e}", file=sys.stderr)
            sys.exit(1)

    profile_path = Path(args.profile or detect_shell()["profile"]).expanduser()
    shell_name   = Path(os.environ.get("SHELL", "bash")).name

    print(f"\n{'[DRY RUN] ' if args.dry_run else ''}Migration plan:")
    print(f"  config  : {config_path}")
    print(f"  backup  : {bak_path}")
    print(f"  profile : {profile_path}")
    print()

    profile_content = profile_path.read_text() if profile_path.exists() else ""
    lines_to_add = []

    for f in to_migrate:
        env_var     = f["env_var"]
        masked_line = export_line(shell_name, env_var, "***")
        if env_var not in profile_content:
            lines_to_add.append(f["path"])
            print(f"  [profile +] {masked_line}")
        else:
            print(f"  [profile =] {env_var} already present, skipping")
        print(f"  [config  →] {f['path']}  →  SecretRef({env_var})")

    if args.dry_run:
        print("\n[DRY RUN] No files modified.")
        return

    # 1. Backup
    shutil.copy2(config_path, bak_path)
    print(f"\n[OK] Backup: {bak_path}")

    # 2. Write shell profile
    if lines_to_add:
        with open(profile_path, "a") as pf:
            pf.write("\n# Added by token-safety-checker\n")
            for finding in to_migrate:
                if finding["path"] in lines_to_add:
                    value = get_nested(config, finding["path"])
                    if value and isinstance(value, str):
                        pf.write(export_line(shell_name, finding["env_var"], value) + "\n")
        print(f"[OK] Wrote {len(lines_to_add)} export(s) to {profile_path}")

    # 3. Update config with SecretRefs
    for finding in to_migrate:
        set_nested(config, finding["path"], {
            "source": "env", "provider": "default", "id": finding["env_var"]
        })

    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)
    print(f"[OK] Updated {config_path} with {len(to_migrate)} SecretRef(s)")

    print(f"""
[!] Next steps — source your profile before restarting:

    source {profile_path}
    openclaw gateway restart

    systemd: add vars to EnvironmentFile= in your unit instead of sourcing profile.
    Docker:  pass via -e or environment: in compose.
""")

    # 4. Auto-verify after successful migration
    print("── Running post-migration verify ──────────────────────────────")
    print("   (env var checks may show NOT SET until you source your profile)")
    run_verify(config_path, clean_backup=False)


def cmd_verify(args):
    config_path = Path(args.config)
    exit_code   = run_verify(config_path, clean_backup=args.clean_backup)
    sys.exit(exit_code)

# ── Entry point ────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="SafeClaw — token safety checker for OpenClaw",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd")

    # scan
    p_scan = sub.add_parser("scan", help="Detect plaintext secrets (returns paths + risk, no values)")
    p_scan.add_argument("--config", default=str(DEFAULT_CONFIG))
    p_scan.add_argument("--deep",   action="store_true",
                        help="Also scan git history for past plaintext secret commits")

    # migrate
    p_mig = sub.add_parser("migrate", help="Migrate secrets to env vars + SecretRef")
    p_mig.add_argument("--findings", help="JSON list from scan output")
    p_mig.add_argument("--config",   default=str(DEFAULT_CONFIG))
    p_mig.add_argument("--profile",  default=None)
    p_mig.add_argument("--dry-run",  action="store_true")
    p_mig.add_argument("--restore",  action="store_true", help="Restore config from .bak")

    # verify
    p_ver = sub.add_parser("verify", help="Post-migration health check")
    p_ver.add_argument("--config",       default=str(DEFAULT_CONFIG))
    p_ver.add_argument("--clean-backup", action="store_true",
                       help="Delete .bak file if found")

    args = parser.parse_args()

    if args.cmd == "scan":
        cmd_scan(args)
    elif args.cmd == "migrate":
        cmd_migrate(args)
    elif args.cmd == "verify":
        cmd_verify(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
