from __future__ import annotations

import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Result:
    status: str
    message: str
    values: dict[str, Any] | None = None


def command(name: str) -> str | None:
    return shutil.which(name)


def run(args: list[str], cwd: Path, dry_run: bool = False) -> Result:
    if dry_run:
        return Result("planned", "would run: " + " ".join(args))
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)
    if result.returncode:
        detail = (result.stderr or result.stdout).strip()[-1000:]
        return Result("failed", f"{args[0]} failed: {detail}")
    return Result("published", result.stdout.strip()[-1000:] or f"completed: {' '.join(args)}")


def github(info: dict[str, Any], dry_run: bool, yes: bool) -> Result:
    root = Path(info["repoRoot"])
    if not info.get("gitRemote"):
        return Result("blocked", "GitHub requires an origin remote")
    if info.get("unrelatedGitChanges"):
        return Result("blocked", "unrelated working-tree changes: " + ", ".join(info["unrelatedGitChanges"]))
    gh = command("gh")
    if gh and not dry_run:
        auth = run([gh, "auth", "status"], root)
        if auth.status == "failed":
            return Result("blocked", "GitHub login check failed; run gh auth login first")
    elif not dry_run and not gh:
        return Result("blocked", "gh CLI is required for the GitHub login gate")
    if not yes and not dry_run:
        return Result("planned", "confirmation required before git commit/push")
    message = f"feat(skill): publish {info['name']} v{info.get('version', '0.1.0')}"
    if dry_run:
        return Result("planned", f"would commit target skill with: {message}, then push current branch")
    if not info.get("gitStatus"):
        sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, text=True, capture_output=True, check=False).stdout.strip()
        return Result("published", "GitHub source is already clean and current", {"sourceCommit": sha})
    add = run(["git", "add", "--", info["skillDir"]], root)
    if add.status == "failed":
        return add
    commit = run(["git", "commit", "-m", message], root)
    if commit.status == "failed":
        return commit
    push = run(["git", "push", "origin", info["gitBranch"]], root)
    if push.status == "failed":
        return push
    sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, text=True, capture_output=True, check=False).stdout.strip()
    return Result("published", "GitHub source pushed", {"sourceCommit": sha})


def awesome(info: dict[str, Any], dry_run: bool, **kwargs: Any) -> Result:
    if not info.get("pluginManifest"):
        return Result("blocked", "Awesome Codex Plugins requires a valid .codex-plugin/plugin.json; ordinary skills are not auto-wrapped")
    gh = command("gh")
    if not gh:
        return Result("blocked", "gh CLI is required for the Awesome Codex Plugins PR")
    if dry_run or not kwargs.get("yes", False):
        return Result("planned", "fork the curated list, add one README entry, push a branch, and open a PR")
    root = Path(info["repoRoot"])
    auth = run([gh, "auth", "status"], root)
    if auth.status == "failed":
        return Result("blocked", "GitHub login check failed; run gh auth login first")
    repo = "hashgraph-online/awesome-codex-plugins"
    owner = "liuyewang"
    fork = f"{owner}/awesome-codex-plugins"
    view = subprocess.run([gh, "repo", "view", fork], cwd=root, text=True, capture_output=True, check=False)
    if view.returncode:
        created = subprocess.run([gh, "repo", "fork", repo, "--clone=false"], cwd=root, text=True, capture_output=True, check=False)
        if created.returncode:
            return Result("failed", f"could not create Awesome list fork: {(created.stderr or created.stdout).strip()[-1000:]}")
    with tempfile.TemporaryDirectory(prefix="awesome-codex-plugins-") as temp:
        checkout = Path(temp) / "list"
        clone = subprocess.run(["git", "clone", f"https://github.com/{fork}.git", str(checkout)], cwd=root, text=True, capture_output=True, check=False)
        if clone.returncode:
            return Result("failed", f"could not clone Awesome list fork: {(clone.stderr or clone.stdout).strip()[-1000:]}")
        branch = f"codex/{info['name']}-submission"
        checkout_readme = checkout / "README.md"
        content = checkout_readme.read_text(encoding="utf-8")
        source_url = info.get("gitRemote", "")
        if source_url.startswith("git@github.com:"):
            source_url = "https://github.com/" + source_url.split(":", 1)[1]
        source_url = source_url.removesuffix(".git")
        entry = f"- [{info['name']}]({source_url}) - Safely synchronize this Codex skill across public agent-skill registries."
        if source_url in content:
            return Result("indexed", "Awesome Codex Plugins already contains this source URL")
        heading = "### Development & Workflow"
        if heading not in content:
            return Result("blocked", "could not locate the Development & Workflow section in the Awesome list")
        checkout_readme.write_text(content.replace(heading, heading + "\n" + entry, 1), encoding="utf-8")
        for command_args in (
            ["git", "checkout", "-b", branch],
            ["git", "add", "README.md"],
            ["git", "commit", "-m", f"feat: add {info['name']}"],
            ["git", "push", "-u", "origin", branch],
        ):
            result = subprocess.run(command_args, cwd=checkout, text=True, capture_output=True, check=False)
            if result.returncode:
                return Result("failed", f"Awesome list command failed: {(result.stderr or result.stdout).strip()[-1000:]}")
        body = f"Adds [{info['name']}]({source_url}) to the Development & Workflow section.\n\nThe source repository includes the required plugin manifest, security files, and HOL scanner workflow."
        pr = subprocess.run([gh, "pr", "create", "--repo", repo, "--head", f"{owner}:{branch}", "--base", "main", "--title", f"feat: add {info['name']}", "--body", body], cwd=checkout, text=True, capture_output=True, check=False)
        if pr.returncode:
            return Result("failed", f"could not open Awesome list PR: {(pr.stderr or pr.stdout).strip()[-1000:]}")
        return Result("published", "Awesome Codex Plugins PR opened", {"remoteUrl": pr.stdout.strip().splitlines()[-1]})


def hol(info: dict[str, Any], dry_run: bool, **_: Any) -> Result:
    if not dry_run and not command("npx"):
        return Result("blocked", "npx is required for HOL Registry")
    directory = info["skillDir"]
    quote = run(["npx", "--yes", "@hol-org/registry", "skills", "quote", "--dir", directory], Path(info["repoRoot"]), dry_run)
    if quote.status == "failed":
        return quote
    if dry_run or not _.get("yes", False):
        return Result("planned", "HOL quote is ready; user confirmation is required before publish", {"quote": quote.message})
    return run(["npx", "--yes", "@hol-org/registry", "skills", "publish", "--dir", directory], Path(info["repoRoot"]))


def clawhub(info: dict[str, Any], dry_run: bool, **kwargs: Any) -> Result:
    cli = command("clawhub")
    if not cli and not dry_run:
        return Result("blocked", "clawhub CLI is not installed")
    version = info.get("version", "0.1.0")
    if dry_run and not cli:
        return Result("planned", f"would run clawhub skill publish {info['skillDir']} --version {version} --dry-run")
    check = run([cli, "whoami"], Path(info["repoRoot"]), dry_run)
    if check.status == "failed":
        return Result("blocked", "ClawHub login check failed; run clawhub login first")
    publish_dir = Path(info["skillDir"])
    staging = None
    if (publish_dir / ".codex-plugin" / "plugin.json").is_file():
        staging = tempfile.TemporaryDirectory(prefix="skill-sync-clawhub-")
        staged_dir = Path(staging.name) / publish_dir.name
        staged_dir.mkdir(parents=True)
        for name in ("SKILL.md", "agents", "scripts", "references"):
            source = publish_dir / name
            target = staged_dir / name
            if source.is_dir():
                shutil.copytree(source, target)
            elif source.is_file():
                shutil.copy2(source, target)
        publish_dir = staged_dir
    preview = run([cli, "skill", "publish", str(publish_dir), "--version", version, "--dry-run"], Path(info["repoRoot"]), dry_run)
    if preview.status == "failed" or dry_run or not kwargs.get("yes", False):
        result = preview if dry_run or preview.status == "failed" else Result("planned", "ClawHub dry-run is ready; user confirmation is required before publish", {"preview": preview.message})
    else:
        result = run([cli, "skill", "publish", str(publish_dir), "--version", version], Path(info["repoRoot"]))
    if staging is not None:
        staging.cleanup()
    return result


def directory(info: dict[str, Any], platform: str, **_: Any) -> Result:
    remote = info.get("gitRemote", "")
    if not remote.startswith(("http://", "https://", "git@")):
        return Result("blocked", f"{platform} requires a public GitHub source URL")
    normalized = remote
    if normalized.startswith("git@github.com:"):
        normalized = "https://github.com/" + normalized.split(":", 1)[1]
    normalized = normalized.removesuffix(".git")
    urls = {
        "skills.sh": "https://skills.sh/",
        "skillsmp": "https://skillsmp.com/",
        "lobehub": "https://lobehub.com/skills",
        "cursor-directory": "https://cursor.directory/",
    }
    return Result(
        "planned",
        f"open {urls[platform]}, submit or verify source {normalized}; no stable publisher CLI is assumed",
        {"sourceUrl": normalized, "handoffUrl": urls[platform]},
    )


ADAPTERS = {
    "github": github,
    "awesome-codex-plugins": awesome,
    "hol": hol,
    "clawhub": clawhub,
    "skills.sh": lambda info, **kwargs: directory(info, "skills.sh", **kwargs),
    "skillsmp": lambda info, **kwargs: directory(info, "skillsmp", **kwargs),
    "lobehub": lambda info, **kwargs: directory(info, "lobehub", **kwargs),
    "cursor-directory": lambda info, **kwargs: directory(info, "cursor-directory", **kwargs),
}
