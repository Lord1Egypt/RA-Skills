#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import shutil
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from lib.approval import derive_secret, hash_skill_dir, verify_token
from lib.telegram_config import discover_telegram_config


def manifest_path(target_root: Path) -> Path:
    return target_root / ".skill-forge-installs.json"


def load_manifest(target_root: Path) -> dict:
    path = manifest_path(target_root)
    if not path.exists():
        return {"installs": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def save_manifest(target_root: Path, manifest: dict) -> None:
    target_root.mkdir(parents=True, exist_ok=True)
    path = manifest_path(target_root)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(tmp, path)


class _ManifestLock:
    def __init__(self, target_root: Path):
        self.target_root = target_root
        self.handle = None

    def __enter__(self):
        self.target_root.mkdir(parents=True, exist_ok=True)
        lock_path = self.target_root / ".skill-forge-installs.lock"
        self.handle = lock_path.open("w")
        try:
            import fcntl
            fcntl.flock(self.handle.fileno(), fcntl.LOCK_EX)
        except Exception:
            pass
        return self

    def __exit__(self, *exc):
        try:
            import fcntl
            if self.handle is not None:
                fcntl.flock(self.handle.fileno(), fcntl.LOCK_UN)
        except Exception:
            pass
        if self.handle is not None:
            self.handle.close()


def timestamp() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def install_plan(skill_dir: Path, target_root: Path, method: str) -> dict:
    target = target_root / skill_dir.name
    return {
        "skill": skill_dir.name,
        "source": str(skill_dir),
        "target": str(target),
        "method": method,
        "commands": [
            f"mkdir -p {target_root}",
            f"ln -sfn {skill_dir} {target}" if method == "symlink" else f"cp -R {skill_dir} {target}",
        ],
        "notes": [
            "Review the generated skill before installing it.",
            "Add the skill name to specific agent configs only after it passes real tasks.",
            "Existing targets are backed up before replacement.",
        ],
    }


def validate_skill_source(skill_dir: Path) -> Optional[str]:
    if not skill_dir.is_dir():
        return "candidate skill directory must exist"
    if not (skill_dir / "SKILL.md").is_file():
        return "candidate skill directory must contain SKILL.md"
    return None


def backup_existing(target: Path, target_root: Path) -> Optional[str]:
    if not target.exists() and not target.is_symlink():
        return None
    backup_root = target_root / ".skill-forge-backups"
    backup_root.mkdir(parents=True, exist_ok=True)
    backup = backup_root / f"{target.name}-{timestamp()}"
    target.rename(backup)
    return str(backup)


def apply_install(
    skill_dir: Path,
    target_root: Path,
    method: str,
    approved_by: str,
    approval_request_id: str,
) -> tuple:
    with _ManifestLock(target_root):
        target = target_root / skill_dir.name
        backup = backup_existing(target, target_root)
        if method == "symlink":
            target.symlink_to(skill_dir, target_is_directory=True)
        else:
            shutil.copytree(skill_dir, target)
        manifest = load_manifest(target_root)
        previous = manifest.setdefault("installs", {}).get(skill_dir.name, {})
        history = list(previous.get("versions", []))
        revision = len(history) + 1
        record = {
            "skill": skill_dir.name,
            "source": str(skill_dir),
            "target": str(target),
            "method": method,
            "installed_at": timestamp(),
            "previous_backup": backup,
            "approved_by": approved_by or None,
            "approval_request_id": approval_request_id or None,
            "revision": revision,
        }
        history.append({k: v for k, v in record.items() if k != "skill"})
        record["versions"] = history
        manifest["installs"][skill_dir.name] = record
        save_manifest(target_root, manifest)
        return target, backup


def remove_target(target: Path) -> None:
    if target.is_symlink() or target.is_file():
        target.unlink()
    elif target.exists():
        shutil.rmtree(target)


def uninstall_skill(skill_name: str, target_root: Path, restore_backup: bool) -> dict:
    with _ManifestLock(target_root):
        manifest = load_manifest(target_root)
        installs = manifest.setdefault("installs", {})
        record = installs.get(skill_name, {})
        target = Path(record.get("target", str(target_root / skill_name)))
        removed = target.exists() or target.is_symlink()
        if removed:
            remove_target(target)

        restored_backup = None
        backup = record.get("previous_backup")
        if restore_backup and backup:
            backup_path = Path(backup)
            if backup_path.exists() or backup_path.is_symlink():
                backup_path.rename(target)
                restored_backup = str(target)

        history = list(record.get("versions", []))
        history.append(
            {
                "uninstalled_at": timestamp(),
                "target": str(target),
                "removed": removed,
                "restored_backup": restored_backup,
            }
        )
        installs[skill_name] = {
            "skill": skill_name,
            "uninstalled_at": timestamp(),
            "target": str(target),
            "versions": history,
            "active": False,
        }
        save_manifest(target_root, manifest)
        return {
            "skill": skill_name,
            "target": str(target),
            "removed": removed,
            "restored_backup": restored_backup,
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Create or apply an OpenClaw skill install proposal.")
    parser.add_argument("skill_dir", help="Candidate skill directory, or skill name when uninstalling.")
    parser.add_argument(
        "--target-root",
        default=str(Path.home() / ".openclaw" / "workspace" / "skills"),
        help="OpenClaw skills root.",
    )
    parser.add_argument("--method", choices=["symlink", "copy"], default="symlink")
    parser.add_argument("--apply", action="store_true", help="Actually install the skill candidate.")
    parser.add_argument(
        "--approval-token",
        default="",
        help="Signed approval token issued by telegram_approval.py. Required for --apply.",
    )
    parser.add_argument(
        "--allow-dry-run-install",
        action="store_true",
        help="Permit a dry-run-mode token to mutate state. Audit will record approved_by=dry-run.",
    )
    parser.add_argument(
        "--bot-token-env",
        default="TELEGRAM_BOT_TOKEN",
        help="Bot token env var used to derive the HMAC secret when SKILL_FORGE_APPROVAL_SECRET is unset.",
    )
    parser.add_argument("--env-file", default="")
    parser.add_argument("--no-default-env-files", action="store_true")
    parser.add_argument("--uninstall", action="store_true", help="Uninstall a skill by name or path.")
    parser.add_argument("--restore-backup", action="store_true", help="Restore the previous target backup when uninstalling.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    target_root = Path(args.target_root).expanduser().resolve()

    def emit_blocked(reason: str, extra: Optional[dict] = None) -> int:
        payload = {
            "status": "blocked",
            "reason": reason,
            "installed": False,
            "target_root": str(target_root),
        }
        if extra:
            payload.update(extra)
        print(json.dumps(payload, ensure_ascii=False, indent=2) if args.json else payload["reason"])
        return 1

    approval_claims: dict = {}
    approved_by_label = ""
    if args.apply:
        if not args.approval_token:
            return emit_blocked("approval token required (run telegram_approval.py first)")
        config = discover_telegram_config(
            args.bot_token_env,
            args.bot_token_env,
            args.env_file,
            load_defaults=not args.no_default_env_files,
        )
        bot_token = os.getenv(config["token_env"] or args.bot_token_env)
        try:
            secret = derive_secret(bot_token)
        except RuntimeError as exc:
            return emit_blocked(f"approval secret unavailable: {exc}")

    if args.uninstall:
        skill_name = Path(args.skill_dir).name
        if args.apply:
            target = str(target_root / skill_name)
            ok, reason, claims = verify_token(
                args.approval_token,
                secret,
                expected={"skill": skill_name, "target": target, "method": args.method},
            )
            if not ok:
                return emit_blocked(f"approval token rejected: {reason}", {"claims": claims})
            mode = claims.get("mode", "telegram")
            if mode == "dry-run" and not args.allow_dry_run_install:
                return emit_blocked("dry-run approval cannot mutate state", {"claims": claims})
            approved_by_label = "dry-run" if mode == "dry-run" else "telegram"
            approval_claims = claims
        if args.apply:
            plan = uninstall_skill(skill_name, target_root, args.restore_backup)
            plan["approved_by"] = approved_by_label
            plan["approval_request_id"] = approval_claims.get("request_id")
        else:
            plan = {
                "skill": skill_name,
                "target": str(target_root / skill_name),
                "uninstall": True,
                "restore_backup": args.restore_backup,
                "installed": False,
            }
        if args.json:
            print(json.dumps(plan, ensure_ascii=False, indent=2))
        else:
            print(f"skill={plan['skill']}")
            print(f"target={plan['target']}")
            print(f"uninstall={plan.get('uninstall', True)}")
            print(f"restore_backup={args.restore_backup}")
        return 0

    skill_dir = Path(args.skill_dir).expanduser().resolve()
    plan = install_plan(skill_dir, target_root, args.method)

    if args.apply:
        source_error = validate_skill_source(skill_dir)
        if source_error:
            return emit_blocked(source_error)
        expected_target = str(target_root / skill_dir.name)
        expected_source = str(skill_dir)
        expected_hash = hash_skill_dir(skill_dir)
        ok, reason, claims = verify_token(
            args.approval_token,
            secret,
            expected={
                "skill": skill_dir.name,
                "target": expected_target,
                "method": args.method,
                "source_dir": expected_source,
                "source_hash": expected_hash,
            },
        )
        if not ok:
            return emit_blocked(f"approval token rejected: {reason}", {"claims": claims})
        mode = claims.get("mode", "telegram")
        if mode == "dry-run" and not args.allow_dry_run_install:
            return emit_blocked("dry-run approval cannot mutate state", {"claims": claims})
        approved_by_label = "dry-run" if mode == "dry-run" else "telegram"
        target, backup = apply_install(
            skill_dir,
            target_root,
            args.method,
            approved_by_label,
            claims.get("request_id", ""),
        )
        plan["installed"] = True
        plan["installed_target"] = str(target)
        plan["backup"] = backup
        plan["approved_by"] = approved_by_label
        plan["approval_request_id"] = claims.get("request_id")
    else:
        plan["installed"] = False

    if args.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    else:
        print(f"skill={plan['skill']}")
        print(f"source={plan['source']}")
        print(f"target={plan['target']}")
        print(f"method={plan['method']}")
        print(f"installed={plan['installed']}")
        print("commands:")
        for command in plan["commands"]:
            print(f"- {command}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
