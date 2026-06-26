#!/usr/bin/env python3
"""
Publish a report asset into a ZeeLin-style reports site and open a PR workflow.

Features:
- Copy report file into public/<category_dir>/
- Insert a new report entry at the top of public/reports_config.json
- Optionally run npm build verification
- Create a feature branch, commit, push, and open PR (if gh CLI is available)
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
import sys
import urllib.parse
from pathlib import Path
from typing import Any, Tuple


ALLOWED_EXTENSIONS = {".pdf", ".ppt", ".pptx"}


class PublishError(RuntimeError):
    pass


def run_cmd(cmd: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        cmd,
        cwd=str(cwd),
        text=True,
        capture_output=True,
    )
    if check and result.returncode != 0:
        stderr = result.stderr.strip()
        stdout = result.stdout.strip()
        details = stderr or stdout or f"exit code {result.returncode}"
        raise PublishError(f"Command failed: {' '.join(cmd)}\n{details}")
    return result


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sanitize_path_segment(value: str) -> str:
    s = value.strip()
    s = re.sub(r"[\\/]+", "-", s)
    s = re.sub(r"[\x00-\x1f\x7f]", "", s)
    s = re.sub(r"\s+", " ", s).strip()
    s = s.strip(".")
    if not s:
        raise PublishError("Category directory name is empty after sanitization.")
    return s


def infer_date_label(*candidates: str) -> str:
    patterns = [
        re.compile(r"((?:19|20)\d{2})[-_/\.](0?[1-9]|1[0-2])"),
        re.compile(r"((?:19|20)\d{2})(0[1-9]|1[0-2])"),
        re.compile(r"((?:19|20)\d{2})年(0?[1-9]|1[0-2])月?"),
    ]
    year_only = re.compile(r"((?:19|20)\d{2})")

    for text in candidates:
        s = (text or "").strip()
        if not s:
            continue
        for p in patterns:
            m = p.search(s)
            if m:
                year = m.group(1)
                month = int(m.group(2))
                return f"{year}-{month:02d}"
        y = year_only.search(s)
        if y:
            return y.group(1)

    return dt.datetime.now().strftime("%Y")


def build_default_abstract(title: str, category: str) -> str:
    return (
        f"本报告围绕《{title}》展开，聚焦{category}相关议题，"
        "系统梳理核心进展、关键问题与落地路径，供研究与决策参考。"
    )


def slug_for_id(value: str) -> str:
    s = value.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    s = re.sub(r"-{2,}", "-", s)
    return s


def ensure_clean_worktree(repo_dir: Path) -> None:
    status = run_cmd(["git", "status", "--porcelain"], cwd=repo_dir)
    if status.stdout.strip():
        raise PublishError(
            "Working tree is not clean. Commit/stash changes first, or rerun with --allow-dirty."
        )


def ensure_git_identity(repo_dir: Path) -> None:
    name = run_cmd(["git", "config", "--get", "user.name"], cwd=repo_dir, check=False).stdout.strip()
    email = run_cmd(["git", "config", "--get", "user.email"], cwd=repo_dir, check=False).stdout.strip()
    if not name or not email:
        raise PublishError(
            "Git identity is not configured (user.name/user.email). "
            "Run scripts/bootstrap_github.sh first."
        )
    if "@" not in email:
        raise PublishError(f"Git user.email looks invalid: {email}")


def remote_exists(repo_dir: Path, remote_name: str) -> bool:
    result = run_cmd(["git", "remote", "get-url", remote_name], cwd=repo_dir, check=False)
    return result.returncode == 0


def get_remote_url(repo_dir: Path, remote_name: str) -> str:
    remote_url = run_cmd(["git", "remote", "get-url", remote_name], cwd=repo_dir, check=False).stdout.strip()
    if not remote_url:
        raise PublishError(f"Remote '{remote_name}' is not configured.")
    return remote_url


def ensure_remote_read_access(repo_dir: Path, remote_name: str) -> str:
    remote_url = get_remote_url(repo_dir, remote_name)
    readable = run_cmd(["git", "ls-remote", "--exit-code", remote_name, "HEAD"], cwd=repo_dir, check=False)
    if readable.returncode != 0:
        details = readable.stderr.strip() or readable.stdout.strip() or "cannot read remote"
        raise PublishError(
            f"Remote read check failed for '{remote_name}'. Verify authentication and URL.\n{details}"
        )
    return remote_url


def ensure_remote_push_access(repo_dir: Path, remote_name: str) -> str:
    remote_url = ensure_remote_read_access(repo_dir, remote_name)
    head_sha = run_cmd(["git", "rev-parse", "HEAD"], cwd=repo_dir).stdout.strip()
    probe_ref = f"refs/heads/codex/permission-check-{dt.datetime.now().strftime('%Y%m%d%H%M%S')}"
    writable = run_cmd(
        ["git", "push", "--dry-run", remote_name, f"{head_sha}:{probe_ref}"],
        cwd=repo_dir,
        check=False,
    )
    if writable.returncode != 0:
        details = writable.stderr.strip() or writable.stdout.strip() or "cannot push to remote"
        raise PublishError(
            f"Remote push permission check failed for '{remote_name}'. "
            "Ask repo admin to grant write access.\n"
            f"{details}"
        )
    return remote_url


def resolve_base_remote(repo_dir: Path, push_remote: str, base_remote: str | None) -> str:
    if base_remote:
        return base_remote
    if push_remote == "origin" and remote_exists(repo_dir, "upstream"):
        return "upstream"
    return push_remote


def load_reports_config(path: Path) -> list[dict[str, Any]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise PublishError(f"Missing config file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise PublishError(f"Invalid JSON in {path}: {exc}") from exc

    if not isinstance(data, list):
        raise PublishError(f"Expected top-level JSON array in {path}.")
    return data


def write_reports_config(path: Path, records: list[dict[str, Any]]) -> None:
    path.write_text(
        json.dumps(records, ensure_ascii=False, indent=4) + "\n",
        encoding="utf-8",
    )


def build_cover_url(category: str, version: str) -> str:
    text = f"{category} {version}".strip()
    encoded = urllib.parse.quote_plus(text)
    return f"https://placehold.co/800x600/660874/FFFFFF/png?text={encoded}"


def generate_entry_id(
    given_id: str | None,
    title: str,
    category: str,
    date_text: str,
    existing_ids: set[str],
) -> str:
    if given_id:
        base = slug_for_id(given_id)
        if not base:
            raise PublishError("Provided --id is invalid after normalization.")
    else:
        title_slug = slug_for_id(title) or "report"
        category_slug = slug_for_id(category) or "category"
        date_slug = slug_for_id(date_text) or dt.datetime.now().strftime("%Y")
        base = f"{title_slug}-{category_slug}-{date_slug}"
        if len(base) > 64:
            base = base[:64].rstrip("-")

    candidate = base
    index = 2
    while candidate in existing_ids:
        suffix = f"-{index}"
        candidate = (base[: max(1, 64 - len(suffix))].rstrip("-") or "report") + suffix
        index += 1
    return candidate


def pick_unique_destination(dest_dir: Path, source_file: Path, overwrite: bool) -> Path:
    candidate = dest_dir / source_file.name
    if not candidate.exists():
        return candidate

    if overwrite:
        return candidate

    # If same content exists, keep original file path.
    if file_sha256(candidate) == file_sha256(source_file):
        return candidate

    stamp = dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    stem = source_file.stem
    suffix = source_file.suffix
    renamed = f"{stem}-{stamp}{suffix}"
    return dest_dir / renamed


def parse_owner_repo_from_remote(remote_url: str) -> Tuple[str, str]:
    # Supports:
    # - git@github.com:owner/repo.git
    # - https://github.com/owner/repo.git
    # - ssh://git@github.com/owner/repo.git
    patterns = [
        r"^git@github\.com:([^/]+)/(.+?)(?:\.git)?$",
        r"^https://github\.com/([^/]+)/(.+?)(?:\.git)?$",
        r"^ssh://git@github\.com/([^/]+)/(.+?)(?:\.git)?$",
    ]
    for pattern in patterns:
        m = re.match(pattern, remote_url)
        if m:
            return m.group(1), m.group(2)
    raise PublishError(f"Cannot parse GitHub owner/repo from remote URL: {remote_url}")


def ensure_branch_available(repo_dir: Path, branch_name: str) -> str:
    check = run_cmd(
        ["git", "show-ref", "--verify", "--quiet", f"refs/heads/{branch_name}"],
        cwd=repo_dir,
        check=False,
    )
    if check.returncode != 0:
        return branch_name
    stamp = dt.datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{branch_name}-{stamp}"


def maybe_open_pr_with_gh(
    repo_dir: Path,
    base_repo: str,
    base_branch: str,
    head_ref: str,
    title: str,
    body: str,
) -> str | None:
    has_gh = shutil.which("gh") is not None
    if not has_gh:
        return None

    auth = run_cmd(["gh", "auth", "status"], cwd=repo_dir, check=False)
    if auth.returncode != 0:
        return None

    pr = run_cmd(
        [
            "gh",
            "pr",
            "create",
            "--repo",
            base_repo,
            "--base",
            base_branch,
            "--head",
            head_ref,
            "--title",
            title,
            "--body",
            body,
        ],
        cwd=repo_dir,
        check=False,
    )
    if pr.returncode == 0:
        return pr.stdout.strip() or None
    return None


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Publish a report to the 智灵报告网站 repository with PR workflow."
    )
    parser.add_argument("--repo", default=".", help="Repository root path.")
    parser.add_argument("--report-file", required=True, help="Path to source report file.")
    parser.add_argument("--title", required=True, help="Report title.")
    parser.add_argument("--category", required=True, help="Report category text shown on site.")
    parser.add_argument(
        "--date",
        default=None,
        help="Report date label (e.g. 2026 or 2026-03). If omitted, infer from file name/title or fallback to current year.",
    )
    parser.add_argument("--version", default="1.0", help="Version label shown on site.")
    parser.add_argument(
        "--abstract",
        default=None,
        help="Report abstract text. If omitted, auto-generate a concise abstract.",
    )
    parser.add_argument("--id", default=None, help="Optional report id; normalized to hyphen-case.")
    parser.add_argument("--cover-url", default=None, help="Optional explicit cover URL.")
    parser.add_argument(
        "--category-dir",
        default=None,
        help="Optional directory name under public/. Defaults to sanitized category text.",
    )
    parser.add_argument(
        "--config-path",
        default="public/reports_config.json",
        help="Path to reports config, relative to repo root.",
    )
    parser.add_argument(
        "--push-remote",
        default="origin",
        help="Git remote used for pushing the feature branch. Default: origin (fork).",
    )
    parser.add_argument(
        "--base-remote",
        default=None,
        help="Git remote used as PR base. Default: auto (upstream when exists, else same as push-remote).",
    )
    parser.add_argument("--base-branch", default="main", help="Base branch for PR.")
    parser.add_argument(
        "--branch-prefix",
        default="codex/report",
        help="Feature branch prefix. Example: codex/report",
    )
    parser.add_argument("--commit-message", default=None, help="Optional custom commit message.")
    parser.add_argument("--pr-title", default=None, help="Optional custom PR title.")
    parser.add_argument("--skip-build", action="store_true", help="Skip npm run build check.")
    parser.add_argument("--allow-dirty", action="store_true", help="Allow dirty git worktree.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing target file name.")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without mutating files.")
    args = parser.parse_args()

    repo_dir = Path(args.repo).resolve()
    source_file = Path(args.report_file).expanduser().resolve()
    config_path = (repo_dir / args.config_path).resolve()
    public_dir = config_path.parent

    if not source_file.exists():
        raise PublishError(f"Report file does not exist: {source_file}")
    if source_file.suffix.lower() not in ALLOWED_EXTENSIONS:
        raise PublishError(
            f"Unsupported extension {source_file.suffix}. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        )
    if not (repo_dir / ".git").exists():
        raise PublishError(f"Not a git repository: {repo_dir}")
    if not config_path.exists():
        raise PublishError(f"Config file not found: {config_path}")

    push_remote = args.push_remote.strip()
    if not push_remote:
        raise PublishError("--push-remote cannot be empty.")
    base_remote = resolve_base_remote(repo_dir, push_remote, (args.base_remote or "").strip() or None)

    push_remote_url = ""
    base_remote_url = ""
    if not args.allow_dirty and not args.dry_run:
        ensure_clean_worktree(repo_dir)
        ensure_git_identity(repo_dir)
        push_remote_url = ensure_remote_push_access(repo_dir, push_remote)
        base_remote_url = (
            push_remote_url
            if base_remote == push_remote
            else ensure_remote_read_access(repo_dir, base_remote)
        )
    elif not args.dry_run:
        # Even when allowing dirty state, keep identity/remote checks for deterministic failure.
        ensure_git_identity(repo_dir)
        push_remote_url = ensure_remote_push_access(repo_dir, push_remote)
        base_remote_url = (
            push_remote_url
            if base_remote == push_remote
            else ensure_remote_read_access(repo_dir, base_remote)
        )

    records = load_reports_config(config_path)
    existing_ids = {str(item.get("id", "")).strip() for item in records if isinstance(item, dict)}

    category_dir_name = sanitize_path_segment(args.category_dir or args.category)
    dest_dir = public_dir / category_dir_name
    target_path = pick_unique_destination(dest_dir, source_file, overwrite=args.overwrite)
    rel_asset = target_path.relative_to(public_dir).as_posix()

    # Duplicate guard by exact asset path.
    for item in records:
        if not isinstance(item, dict):
            continue
        if str(item.get("pdfUrl", "")).strip() == f"./{rel_asset}":
            raise PublishError(
                f"Target asset path already exists in config: ./{rel_asset}. "
                "Choose a different file name or use --overwrite intentionally."
            )

    resolved_date = (args.date or "").strip() or infer_date_label(source_file.name, args.title)
    resolved_abstract = (args.abstract or "").strip() or build_default_abstract(args.title, args.category)

    entry_id = generate_entry_id(args.id, args.title, args.category, resolved_date, existing_ids)
    cover_url = args.cover_url or build_cover_url(args.category, args.version)
    entry = {
        "id": entry_id,
        "title": args.title,
        "version": args.version,
        "date": resolved_date,
        "category": args.category,
        "abstract": resolved_abstract,
        "coverUrl": cover_url,
        "pdfUrl": f"./{rel_asset}",
    }

    if args.dry_run:
        if not push_remote_url:
            push_remote_url = get_remote_url(repo_dir, push_remote)
        if not base_remote_url:
            base_remote_url = (
                push_remote_url if base_remote == push_remote else get_remote_url(repo_dir, base_remote)
            )
        if not args.date:
            print(f"[DRY RUN] Auto date: {resolved_date}")
        if not args.abstract:
            print(f"[DRY RUN] Auto abstract: {resolved_abstract}")
        print(f"[DRY RUN] Push remote: {push_remote} ({push_remote_url})")
        print(f"[DRY RUN] Base remote: {base_remote} ({base_remote_url})")
        print("[DRY RUN] Planned entry:")
        print(json.dumps(entry, ensure_ascii=False, indent=2))
        print(f"[DRY RUN] Copy: {source_file} -> {target_path}")
        print(f"[DRY RUN] Update config: {config_path}")
        return 0

    dest_dir.mkdir(parents=True, exist_ok=True)
    if not target_path.exists() or file_sha256(target_path) != file_sha256(source_file):
        shutil.copy2(source_file, target_path)

    records.insert(0, entry)
    write_reports_config(config_path, records)

    if not args.skip_build:
        print("[INFO] Running npm run build ...")
        run_cmd(["npm", "run", "build"], cwd=repo_dir)

    if not args.date:
        print(f"[INFO] Auto date: {resolved_date}")
    if not args.abstract:
        print(f"[INFO] Auto abstract: {resolved_abstract}")

    current_branch = run_cmd(["git", "branch", "--show-current"], cwd=repo_dir).stdout.strip()
    if current_branch != args.base_branch:
        raise PublishError(
            f"Current branch is '{current_branch}', expected '{args.base_branch}'. "
            "Switch to base branch before publishing."
        )

    branch_base = f"{args.branch_prefix}-{entry_id}"
    branch_name = ensure_branch_available(repo_dir, branch_base)
    run_cmd(["git", "checkout", "-b", branch_name], cwd=repo_dir)

    rel_config = config_path.relative_to(repo_dir).as_posix()
    rel_target = target_path.relative_to(repo_dir).as_posix()
    run_cmd(["git", "add", rel_config, rel_target], cwd=repo_dir)

    commit_message = args.commit_message or f"feat(reports): publish {entry_id} ({args.category})"
    run_cmd(["git", "commit", "-m", commit_message], cwd=repo_dir)
    run_cmd(["git", "push", "-u", push_remote, branch_name], cwd=repo_dir)

    if not push_remote_url:
        push_remote_url = get_remote_url(repo_dir, push_remote)
    if not base_remote_url:
        base_remote_url = push_remote_url if base_remote == push_remote else get_remote_url(repo_dir, base_remote)

    base_owner, base_repo = parse_owner_repo_from_remote(base_remote_url)
    push_owner, push_repo = parse_owner_repo_from_remote(push_remote_url)
    same_repo = (base_owner, base_repo) == (push_owner, push_repo)
    head_ref = branch_name if same_repo else f"{push_owner}:{branch_name}"
    base_repo_slug = f"{base_owner}/{base_repo}"

    pr_title = args.pr_title or f"Publish report: {args.title}"
    pr_body = (
        f"### Report Publish Request\n\n"
        f"- Title: {args.title}\n"
        f"- Category: {args.category}\n"
        f"- Date: {resolved_date}\n"
        f"- Version: {args.version}\n"
        f"- Push remote: `{push_remote}` ({push_owner}/{push_repo})\n"
        f"- Base remote: `{base_remote}` ({base_owner}/{base_repo})\n"
        f"- Config path: `{rel_config}`\n"
        f"- Asset path: `{rel_target}`\n"
    )

    pr_url = maybe_open_pr_with_gh(
        repo_dir,
        base_repo_slug,
        args.base_branch,
        head_ref,
        pr_title,
        pr_body,
    )
    if pr_url:
        print(f"[OK] PR created: {pr_url}")
    else:
        compare_head = branch_name if same_repo else f"{push_owner}:{branch_name}"
        compare_url = f"https://github.com/{base_owner}/{base_repo}/compare/{args.base_branch}...{compare_head}?expand=1"
        print("[INFO] gh CLI unavailable or not authenticated; open PR manually:")
        print(compare_url)

    print("[OK] Report publishing branch is ready.")
    print(f"[INFO] Branch: {branch_name}")
    print(f"[INFO] Entry id: {entry_id}")
    print(f"[INFO] Push remote: {push_remote}")
    print(f"[INFO] Base remote: {base_remote}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except PublishError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        raise SystemExit(1)
