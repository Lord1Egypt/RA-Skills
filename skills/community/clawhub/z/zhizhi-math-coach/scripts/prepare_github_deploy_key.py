#!/usr/bin/env python3
"""Prepare a repository-scoped GitHub deploy key for OpenClaw sync."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path


MANAGED_START = "# zhizhi-math-coach deploy key start:"
MANAGED_END = "# zhizhi-math-coach deploy key end:"


def run(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        args,
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def fail(message: str) -> None:
    raise RuntimeError(message)


def git(args: list[str], workspace: Path) -> subprocess.CompletedProcess[str]:
    return run(["git", *args], cwd=workspace)


def parse_remote_url(url: str) -> tuple[str, str] | None:
    patterns = [
        r"^git@github\.com:([^/]+)/(.+?)(?:\.git)?$",
        r"^git@([^:]+):([^/]+)/(.+?)(?:\.git)?$",
        r"^https://github\.com/([^/]+)/(.+?)(?:\.git)?$",
    ]
    for pattern in patterns:
        match = re.match(pattern, url.strip())
        if not match:
            continue
        groups = match.groups()
        if len(groups) == 2:
            return groups[0], groups[1]
        return groups[1], groups[2]
    return None


def sanitize(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-") or "repo"


def default_key_path(owner: str, repo: str) -> Path:
    name = f"zhizhi_math_{sanitize(owner)}_{sanitize(repo)}_deploy"
    return Path.home() / ".ssh" / name


def ensure_key(key_path: Path, comment: str) -> None:
    if shutil.which("ssh-keygen") is None:
        fail("ssh-keygen is not installed on this OpenClaw machine")

    key_path = key_path.expanduser()
    key_path.parent.mkdir(parents=True, exist_ok=True)
    key_path.parent.chmod(0o700)

    if key_path.exists():
        return

    result = run(["ssh-keygen", "-t", "ed25519", "-C", comment, "-f", str(key_path), "-N", ""])
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        fail(f"failed to generate deploy key: {detail}")
    key_path.chmod(0o600)


def public_key_for(key_path: Path) -> str:
    public_path = Path(f"{key_path}.pub")
    if public_path.exists():
        return public_path.read_text(encoding="utf-8").strip()

    result = run(["ssh-keygen", "-y", "-f", str(key_path)])
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        fail(f"failed to derive public key: {detail}")
    public_key = result.stdout.strip()
    public_path.write_text(public_key + "\n", encoding="utf-8")
    return public_key


def update_ssh_config(config_path: Path, host_alias: str, key_path: Path, owner: str, repo: str) -> None:
    config_path = config_path.expanduser()
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.parent.chmod(0o700)

    start = f"{MANAGED_START} {owner}/{repo}"
    end = f"{MANAGED_END} {owner}/{repo}"
    block = "\n".join(
        [
            start,
            f"Host {host_alias}",
            "    HostName github.com",
            "    User git",
            f"    IdentityFile {key_path}",
            "    IdentitiesOnly yes",
            end,
            "",
        ]
    )

    old = config_path.read_text(encoding="utf-8") if config_path.exists() else ""
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end) + r"\n?", re.DOTALL)
    if pattern.search(old):
        new = pattern.sub(block, old)
    else:
        new = old.rstrip() + "\n\n" + block if old.strip() else block
    config_path.write_text(new, encoding="utf-8")
    config_path.chmod(0o600)


def infer_owner_repo(workspace: Path, remote: str) -> tuple[str, str]:
    remote_url = git(["remote", "get-url", remote], workspace)
    if remote_url.returncode != 0:
        fail(f"cannot infer repository because remote {remote!r} is not configured; pass --github-owner and --repo")
    parsed = parse_remote_url(remote_url.stdout.strip())
    if parsed is None:
        fail(f"cannot parse GitHub remote URL: {remote_url.stdout.strip()}")
    return parsed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a repository-scoped SSH deploy key for GitHub sync.")
    parser.add_argument("--workspace", type=Path, default=Path("."), help="Personal learning repository root.")
    parser.add_argument("--remote", default="origin", help="Git remote name. Defaults to origin.")
    parser.add_argument("--github-owner", help="GitHub owner. Inferred from the remote when omitted.")
    parser.add_argument("--repo", help="GitHub repository name. Inferred from the remote when omitted.")
    parser.add_argument("--key-path", type=Path, help="Private key path. Defaults to ~/.ssh/zhizhi_math_<owner>_<repo>_deploy.")
    parser.add_argument("--host-alias", help="SSH host alias. Defaults to github.com-zhizhi-<owner>-<repo>.")
    parser.add_argument("--configure-remote", action="store_true", help="Set the git remote to use the generated SSH host alias.")
    parser.add_argument("--no-ssh-config", action="store_true", help="Do not update ~/.ssh/config.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workspace = args.workspace.resolve()

    if shutil.which("git") is None:
        fail("git is not installed on this OpenClaw machine")
    if not workspace.exists():
        fail(f"workspace does not exist: {workspace}")

    if args.github_owner and args.repo:
        owner, repo = args.github_owner, args.repo
    else:
        owner, repo = infer_owner_repo(workspace, args.remote)

    key_path = (args.key_path or default_key_path(owner, repo)).expanduser()
    host_alias = args.host_alias or f"github.com-zhizhi-{sanitize(owner)}-{sanitize(repo)}"
    comment = f"openclaw-zhizhi-math-coach-{owner}/{repo}"

    ensure_key(key_path, comment)
    public_key = public_key_for(key_path)

    if not args.no_ssh_config:
        update_ssh_config(Path.home() / ".ssh" / "config", host_alias, key_path, owner, repo)

    remote_url = f"git@{host_alias}:{owner}/{repo}.git"
    if args.configure_remote:
        existing_remote = git(["remote", "get-url", args.remote], workspace)
        if existing_remote.returncode == 0:
            result = git(["remote", "set-url", args.remote, remote_url], workspace)
        else:
            result = git(["remote", "add", args.remote, remote_url], workspace)
        if result.returncode != 0:
            detail = result.stderr.strip() or result.stdout.strip()
            fail(f"failed to set git remote: {detail}")

    print(f"ok: deploy key private path: {key_path}")
    print(f"ok: deploy key public path: {key_path}.pub")
    if not args.no_ssh_config:
        print(f"ok: ssh host alias: {host_alias}")
    if args.configure_remote:
        print(f"ok: remote {args.remote}: {remote_url}")
    else:
        print(f"next: after adding the deploy key, set remote with: git remote set-url {args.remote} {remote_url}")
    print()
    print("public-key-start")
    print(public_key)
    print("public-key-end")
    print()
    print("next: send only the public key text to the parent, for example through Lark/Feishu.")
    print("next: parent adds it in GitHub repository Settings -> Deploy keys -> Add deploy key, with Allow write access enabled.")
    print("next: then run check_git_sync.py --check-push from the personal learning workspace.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}")
        raise SystemExit(1)
