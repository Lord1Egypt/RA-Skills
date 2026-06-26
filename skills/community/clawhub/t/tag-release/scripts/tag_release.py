#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
按日期规则批量给微服务打远程 release tag。

安全约束：
- 本脚本内置 GitHub API allowlist，只允许 tag-release 所需的固定接口
- 允许的能力仅包括：查询分支 commit、查询 commit 关联 PR、查询/创建 tag
- 禁止扩展成通用 GitHub 工具；如果需求超出打 tag 范围，应改走其他 skill/凭据

规则：
- tag 格式：release-{year_index}.{month}.{day:02d}
- 其中 year_index = year - base_year
- 默认 base_year=2024，因此：
  - 2025 => release-1.M.DD
  - 2026 => release-2.M.DD
  - 2027 => release-3.M.DD

默认行为：
- 读取同目录 config.json
- 默认对 config.json 里的所有 repos 生效
- 默认基于远程 master 分支 tip 打 tag
- 创建 annotated tag，并 push 到 origin
- 如果远程 tag 已存在：
  - 指向同一 commit => skip
  - 指向不同 commit => fail

示例：
  python tag_release.py
  python tag_release.py --branch test
  python tag_release.py --services cloud-device cloud-data
  python tag_release.py --date 2026-05-18 --branch master
  python tag_release.py --tag release-2.5.18 --services cloud-device
  python tag_release.py --dry-run
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = SCRIPT_DIR.parent / "assets" / "config.json"
ALLOWED_GITHUB_GET_PREFIXES = (
    "/repos/{org}/{repo}/git/ref/heads/",
    "/repos/{org}/{repo}/git/ref/tags/",
    "/repos/{org}/{repo}/git/tags/",
    "/repos/{org}/{repo}/commits/{commit}/pulls",
    "/repos/{org}/{repo}/releases/tags/",
)
ALLOWED_GITHUB_POST_PATHS = (
    "/repos/{org}/{repo}/git/tags",
    "/repos/{org}/{repo}/git/refs",
    "/repos/{org}/{repo}/releases",
)


@dataclass
class RepoTarget:
    name: str
    github_repo: str


@dataclass
class TagResult:
    name: str
    ok: bool
    action: str
    detail: str
    tag: str = ""
    branch: str = ""
    target_commit: str = ""
    tag_url: str = ""
    release_url: str = ""
    tag_message: str = ""
    latest_pr_number: str = ""
    latest_pr_title: str = ""
    latest_pr_url: str = ""
    latest_pr_author: str = ""


def load_config() -> dict:
    with CONFIG_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def run_git(repo_dir: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=repo_dir,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if check and result.returncode != 0:
        stderr = (result.stderr or "").strip()
        stdout = (result.stdout or "").strip()
        msg = stderr or stdout or f"git exited with code {result.returncode}"
        raise RuntimeError(f"git {' '.join(args)} failed: {msg}")
    return result


def git_output(repo_dir: Path, *args: str, check: bool = True) -> str:
    return run_git(repo_dir, *args, check=check).stdout.strip()


def _normalize_allowed_path(template: str, **kwargs) -> str:
    normalized = template
    for key, value in kwargs.items():
        normalized = normalized.replace("{" + key + "}", str(value))
    return normalized


def assert_allowed_github_get(path: str, org: str, repo: str, commit: str = "") -> None:
    allowed = [
        _normalize_allowed_path(item, org=org, repo=repo, commit=commit)
        for item in ALLOWED_GITHUB_GET_PREFIXES
    ]
    if not any(path.startswith(prefix) for prefix in allowed):
        raise RuntimeError("禁止访问未授权的 GitHub GET 接口: {}".format(path))


def assert_allowed_github_post(path: str, org: str, repo: str) -> None:
    allowed = [
        _normalize_allowed_path(item, org=org, repo=repo)
        for item in ALLOWED_GITHUB_POST_PATHS
    ]
    if path not in allowed:
        raise RuntimeError("禁止访问未授权的 GitHub POST 接口: {}".format(path))


def github_api_get(cfg: dict, path: str, params: dict | None = None, *, org: str = "", repo: str = "", commit: str = "") -> dict | list:
    token = str(cfg.get("github_token") or "").strip()
    if not token:
        raise RuntimeError("config.json 缺少 github_token")
    if any(ch in token for ch in ("…", "***")):
        raise RuntimeError("config.json 中 github_token 看起来已脱敏，无法查询 GitHub API")
    if org and repo:
        assert_allowed_github_get(path, org=org, repo=repo, commit=commit)
    url = "https://api.github.com{}".format(path)
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer {}".format(token),
        "X-GitHub-Api-Version": "2022-11-28",
    }
    resp = requests.get(url, headers=headers, params=params, timeout=20)
    if resp.status_code >= 400:
        raise RuntimeError("GitHub API {} 失败: HTTP {} {}".format(path, resp.status_code, resp.text[:200]))
    return resp.json()


def github_api_post(cfg: dict, path: str, payload: dict, *, org: str = "", repo: str = "") -> dict:
    token = str(cfg.get("github_token") or "").strip()
    if not token:
        raise RuntimeError("config.json 缺少 github_token")
    if any(ch in token for ch in ("…", "***")):
        raise RuntimeError("config.json 中 github_token 看起来已脱敏，无法调用 GitHub 写接口")
    if org and repo:
        assert_allowed_github_post(path, org=org, repo=repo)
    url = "https://api.github.com{}".format(path)
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer {}".format(token),
        "X-GitHub-Api-Version": "2022-11-28",
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=20)
    if resp.status_code >= 400:
        raise RuntimeError("GitHub API {} 失败: HTTP {} {}".format(path, resp.status_code, resp.text[:200]))
    return resp.json()


def build_tag_url(cfg: dict, github_repo: str, tag: str) -> str:
    org = str(cfg.get("github_org") or "").strip()
    if not org:
        return ""
    return "https://github.com/{}/{}/tree/{}".format(org, github_repo, tag)


def build_release_url(cfg: dict, github_repo: str, tag: str) -> str:
    org = str(cfg.get("github_org") or "").strip()
    if not org:
        return ""
    return "https://github.com/{}/{}/releases/tag/{}".format(org, github_repo, tag)


def get_latest_merged_pr_for_commit(cfg: dict, github_repo: str, commit: str) -> dict:
    org = str(cfg.get("github_org") or "").strip()
    if not org or not commit:
        return {}
    pulls = github_api_get(
        cfg,
        "/repos/{}/{}/commits/{}/pulls".format(org, github_repo, commit),
        org=org,
        repo=github_repo,
        commit=commit,
    )
    if not isinstance(pulls, list) or not pulls:
        return {}

    merged_pulls = [p for p in pulls if p.get("merged_at")]
    if not merged_pulls:
        return {}
    merged_pulls.sort(key=lambda item: item.get("merged_at") or "", reverse=True)
    pr = merged_pulls[0]
    user = pr.get("user") or {}
    return {
        "number": pr.get("number"),
        "title": pr.get("title") or "",
        "url": pr.get("html_url") or "",
        "author": user.get("login") or user.get("name") or "",
    }


def dedupe_keep_order(items: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        key = item.strip()
        if not key or key in seen:
            continue
        seen.add(key)
        result.append(key)
    return result


def normalize_service_key(value: str) -> str:
    return (value or "").strip().lower().replace("_", "-")


def resolve_services(cfg: dict, names: list[str] | None, workspace_override: str | None = None) -> list[RepoTarget]:
    repos_cfg = cfg.get("repos", {})
    aliases_cfg = cfg.get("service_aliases", {})

    normalized_repo_names = {
        normalize_service_key(repo_name): repo_name for repo_name in repos_cfg.keys()
    }
    normalized_aliases = {
        normalize_service_key(alias): target for alias, target in aliases_cfg.items()
    }

    if not names:
        selected = list(repos_cfg.keys())
    else:
        selected = []
        for raw in names:
            name = raw.strip()
            normalized = normalize_service_key(name)
            if not normalized:
                continue

            alias_target = normalized_aliases.get(normalized)
            if alias_target and alias_target in repos_cfg:
                selected.append(alias_target)
                continue

            exact_match = normalized_repo_names.get(normalized)
            if exact_match:
                selected.append(exact_match)
                continue

            matches = [
                repo_name
                for repo_name in repos_cfg
                if normalized in normalize_service_key(repo_name)
            ]
            if len(matches) == 1:
                selected.append(matches[0])
            elif len(matches) > 1:
                print(f"[WARN] '{name}' 匹配到多个服务 {matches}，已跳过")
            else:
                print(f"[WARN] 未找到服务 '{name}'，已跳过")

    result: list[RepoTarget] = []
    for name in dedupe_keep_order(selected):
        info = repos_cfg[name]
        result.append(RepoTarget(name=name, github_repo=info.get("repo", name)))
    return result


def parse_date(date_str: str | None) -> datetime:
    if not date_str:
        return datetime.now()
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError("--date 格式必须是 YYYY-MM-DD") from exc


def build_tag_name(target_date: datetime, prefix: str, base_year: int) -> str:
    year_index = target_date.year - base_year
    if year_index <= 0:
        raise ValueError(
            f"根据 base_year={base_year} 计算得到的 year_index={year_index} 非法，请检查年份规则"
        )
    return f"{prefix}{year_index}.{target_date.month}.{target_date.day:02d}"


def get_remote_branch_commit(cfg: dict, github_repo: str, branch: str) -> str:
    org = str(cfg.get("github_org") or "").strip()
    ref = github_api_get(
        cfg,
        "/repos/{}/{}/git/ref/heads/{}".format(org, github_repo, branch),
        org=org,
        repo=github_repo,
    )
    return ((ref.get("object") or {}).get("sha") or "").strip()


def github_ref_exists(cfg: dict, github_repo: str, ref_type: str, ref_name: str) -> bool:
    org = str(cfg.get("github_org") or "").strip()
    try:
        github_api_get(
            cfg,
            "/repos/{}/{}/git/ref/{}/{}".format(org, github_repo, ref_type, ref_name),
            org=org,
            repo=github_repo,
        )
        return True
    except Exception:
        return False


def get_commit_short(commit: str) -> str:
    return commit[:7] if commit else ""


def get_remote_tag_commit(cfg: dict, github_repo: str, tag: str) -> str:
    org = str(cfg.get("github_org") or "").strip()
    try:
        ref = github_api_get(
            cfg,
            "/repos/{}/{}/git/ref/tags/{}".format(org, github_repo, tag),
            org=org,
            repo=github_repo,
        )
    except Exception:
        return ""
    obj = ref.get("object") or {}
    sha = (obj.get("sha") or "").strip()
    obj_type = (obj.get("type") or "").strip()
    if obj_type == "commit":
        return sha
    if obj_type == "tag" and sha:
        tag_obj = github_api_get(
            cfg,
            "/repos/{}/{}/git/tags/{}".format(org, github_repo, sha),
            org=org,
            repo=github_repo,
        )
        return (((tag_obj.get("object") or {}).get("sha")) or "").strip()
    return ""


def create_remote_annotated_tag(cfg: dict, github_repo: str, tag: str, commit: str, message: str) -> None:
    org = str(cfg.get("github_org") or "").strip()
    tag_obj = github_api_post(
        cfg,
        "/repos/{}/{}/git/tags".format(org, github_repo),
        {
            "tag": tag,
            "message": message,
            "object": commit,
            "type": "commit",
        },
        org=org,
        repo=github_repo,
    )
    tag_sha = (tag_obj.get("sha") or "").strip()
    if not tag_sha:
        raise RuntimeError("创建 annotated tag 失败：未返回 tag sha")
    github_api_post(
        cfg,
        "/repos/{}/{}/git/refs".format(org, github_repo),
        {
            "ref": "refs/tags/{}".format(tag),
            "sha": tag_sha,
        },
        org=org,
        repo=github_repo,
    )


def build_default_tag_message(tag: str, branch: str, latest_pr: dict | None) -> str:
    latest_pr = latest_pr or {}
    pr_title = str(latest_pr.get("title") or "").strip()
    pr_number = str(latest_pr.get("number") or "").strip()
    pr_author = str(latest_pr.get("author") or "").strip()
    parts = [tag]
    if pr_number:
        parts.append(f"PR #{pr_number}")
    if pr_title:
        parts.append(pr_title)
    if pr_author:
        parts.append(f"by {pr_author}")
    if len(parts) > 1:
        return " | ".join(parts)
    return f"{tag} from origin/{branch}"


def get_release_by_tag(cfg: dict, github_repo: str, tag: str) -> dict:
    org = str(cfg.get("github_org") or "").strip()
    if not org or not tag:
        return {}
    try:
        data = github_api_get(
            cfg,
            "/repos/{}/{}/releases/tags/{}".format(org, github_repo, tag),
            org=org,
            repo=github_repo,
        )
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def create_github_release(cfg: dict, github_repo: str, tag: str, branch: str, message: str, latest_pr: dict | None) -> dict:
    org = str(cfg.get("github_org") or "").strip()
    latest_pr = latest_pr or {}
    pr_title = str(latest_pr.get("title") or "").strip()
    pr_number = str(latest_pr.get("number") or "").strip()
    pr_url = str(latest_pr.get("url") or "").strip()
    body_lines = [message.strip() or tag]
    if pr_number or pr_title:
        body_lines.append("")
        body_lines.append("Latest merged PR: #{} {}".format(pr_number, pr_title).rstrip())
    if pr_url:
        body_lines.append(pr_url)
    body_lines.append("")
    body_lines.append("Source branch: origin/{}".format(branch))
    payload = {
        "tag_name": tag,
        "target_commitish": branch,
        "name": tag,
        "body": "\n".join(body_lines).strip(),
        "draft": False,
        "prerelease": False,
    }
    return github_api_post(
        cfg,
        "/repos/{}/{}/releases".format(org, github_repo),
        payload,
        org=org,
        repo=github_repo,
    )


def process_repo(
    cfg: dict,
    repo: RepoTarget,
    branch: str,
    tag: str,
    tag_message: str | None,
    dry_run: bool,
) -> TagResult:
    try:
        target_commit = get_remote_branch_commit(cfg, repo.github_repo, branch)
        if not target_commit:
            return TagResult(repo.name, False, "fail", f"远程分支不存在: origin/{branch}")
        target_short = get_commit_short(target_commit)

        tag_url = build_tag_url(cfg, repo.github_repo, tag)
        release_url = build_release_url(cfg, repo.github_repo, tag)
        latest_pr = {}
        try:
            latest_pr = get_latest_merged_pr_for_commit(cfg, repo.github_repo, target_commit)
        except Exception as exc:
            latest_pr = {"title": "[获取失败] {}".format(exc)}

        existing_commit = ""
        try:
            existing_commit = get_remote_tag_commit(cfg, repo.github_repo, tag)
        except Exception:
            existing_commit = ""

        existing_release = get_release_by_tag(cfg, repo.github_repo, tag)
        effective_tag_message = (tag_message or "").strip() or build_default_tag_message(tag, branch, latest_pr)

        if existing_commit:
            existing_short = get_commit_short(existing_commit)
            if existing_commit == target_commit:
                if existing_release:
                    return TagResult(
                        repo.name, True, "skip", f"远程 tag / release 已存在且指向同一 commit ({existing_short})",
                        tag=tag, branch=branch, target_commit=target_commit, tag_url=tag_url, release_url=release_url, tag_message=effective_tag_message,
                        latest_pr_number=str(latest_pr.get("number") or ""),
                        latest_pr_title=str(latest_pr.get("title") or ""),
                        latest_pr_url=str(latest_pr.get("url") or ""),
                        latest_pr_author=str(latest_pr.get("author") or ""),
                    )
                if dry_run:
                    return TagResult(
                        repo.name, True, "dry-run", f"将为已存在 tag 补建 release {tag} ({existing_short})",
                        tag=tag, branch=branch, target_commit=target_commit, tag_url=tag_url, release_url=release_url, tag_message=effective_tag_message,
                        latest_pr_number=str(latest_pr.get("number") or ""),
                        latest_pr_title=str(latest_pr.get("title") or ""),
                        latest_pr_url=str(latest_pr.get("url") or ""),
                        latest_pr_author=str(latest_pr.get("author") or ""),
                    )
                create_github_release(cfg, repo.github_repo, tag, branch, effective_tag_message, latest_pr)
                return TagResult(
                    repo.name, True, "release-created", f"远程 tag 已存在，已补建 release {tag} ({existing_short})",
                    tag=tag, branch=branch, target_commit=target_commit, tag_url=tag_url, release_url=release_url, tag_message=effective_tag_message,
                    latest_pr_number=str(latest_pr.get("number") or ""),
                    latest_pr_title=str(latest_pr.get("title") or ""),
                    latest_pr_url=str(latest_pr.get("url") or ""),
                    latest_pr_author=str(latest_pr.get("author") or ""),
                )
            return TagResult(
                repo.name,
                False,
                "fail",
                f"远程 tag 已存在，且不是目标 commit: existing={existing_short}, target={target_short}",
            )

        if dry_run:
            branch_exists = github_ref_exists(cfg, repo.github_repo, "heads", branch)
            if not branch_exists:
                return TagResult(repo.name, False, "fail", f"远程分支不存在: origin/{branch}")
            return TagResult(
                repo.name, True, "dry-run", f"将创建并推送 {tag}，并创建同名 release -> origin/{branch} ({target_short})",
                tag=tag, branch=branch, target_commit=target_commit, tag_url=tag_url, release_url=release_url, tag_message=effective_tag_message,
                latest_pr_number=str(latest_pr.get("number") or ""),
                latest_pr_title=str(latest_pr.get("title") or ""),
                latest_pr_url=str(latest_pr.get("url") or ""),
                latest_pr_author=str(latest_pr.get("author") or ""),
            )

        create_remote_annotated_tag(cfg, repo.github_repo, tag, target_commit, effective_tag_message)
        create_github_release(cfg, repo.github_repo, tag, branch, effective_tag_message, latest_pr)
        return TagResult(
            repo.name, True, "created", f"已创建远程 tag + release {tag} -> origin/{branch} ({target_short})",
            tag=tag, branch=branch, target_commit=target_commit, tag_url=tag_url, release_url=release_url, tag_message=effective_tag_message,
            latest_pr_number=str(latest_pr.get("number") or ""),
            latest_pr_title=str(latest_pr.get("title") or ""),
            latest_pr_url=str(latest_pr.get("url") or ""),
            latest_pr_author=str(latest_pr.get("author") or ""),
        )
    except Exception as exc:
        return TagResult(repo.name, False, "fail", str(exc))


def print_summary(results: list[TagResult]) -> int:
    success = [r for r in results if r.ok]
    failed = [r for r in results if not r.ok]

    print("\n" + "=" * 72)
    print(f"完成：成功 {len(success)}，失败 {len(failed)}")
    if success:
        print("成功明细:")
        for item in success:
            print(f"  - {item.name}: [{item.action}] {item.detail}")
            if item.branch:
                print(f"    branch: origin/{item.branch}")
            if item.tag:
                print(f"    tag: {item.tag}")
            if item.tag_url:
                print(f"    tag_url: {item.tag_url}")
            if item.release_url:
                print(f"    release_url: {item.release_url}")
            if item.tag_message:
                print(f"    tag_message: {item.tag_message}")
            if item.latest_pr_number or item.latest_pr_title:
                print(f"    latest_pr: #{item.latest_pr_number} {item.latest_pr_title}".rstrip())
            if item.latest_pr_author:
                print(f"    latest_pr_author: {item.latest_pr_author}")
            if item.latest_pr_url:
                print(f"    latest_pr_url: {item.latest_pr_url}")
    if failed:
        print("失败明细:")
        for item in failed:
            print(f"  - {item.name}: [{item.action}] {item.detail}")
    return 0 if not failed else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="按日期规则批量给微服务打远程 release tag")
    parser.add_argument(
        "--services",
        nargs="*",
        default=None,
        help="服务名列表；不传默认使用 config.json 里的全部 repos",
    )
    parser.add_argument(
        "--workspace",
        default=None,
        help="覆盖 config.json 里的 workspace；适合单独测试某个不在默认目录下的仓库",
    )
    parser.add_argument(
        "--branch",
        default=None,
        help="基于哪个远程分支打 tag；不传时固定使用 master",
    )
    parser.add_argument(
        "--date",
        default=None,
        help="目标日期，格式 YYYY-MM-DD；默认今天",
    )
    parser.add_argument(
        "--tag",
        default=None,
        help="直接指定完整 tag；传了就不按日期规则生成",
    )
    parser.add_argument(
        "--prefix",
        default=None,
        help="tag 前缀；默认优先取 config.tagging.prefix，否则 release-",
    )
    parser.add_argument(
        "--base-year",
        type=int,
        default=None,
        help="year_index 的基准年；默认优先取 config.tagging.base_year，否则 2024",
    )
    parser.add_argument(
        "--message",
        default=None,
        help="annotated tag message；传了就按用户输入；不传则自动使用最新 PR 信息作为描述，拿不到 PR 时回退为 tag/branch 信息",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只打印计划，不真正创建/推送 tag",
    )
    args = parser.parse_args()

    try:
        cfg = load_config()
    except Exception as exc:
        print(f"[ERROR] 读取 config.json 失败: {exc}", file=sys.stderr)
        return 1

    tagging_cfg = cfg.get("tagging", {}) if isinstance(cfg.get("tagging"), dict) else {}
    branch = args.branch or "master"
    prefix = args.prefix or tagging_cfg.get("prefix") or "release-"
    base_year = args.base_year or tagging_cfg.get("base_year") or 2024

    try:
        repos = resolve_services(cfg, args.services, workspace_override=args.workspace)
        if not repos:
            print("[ERROR] 没有解析到任何有效服务", file=sys.stderr)
            return 1

        target_date = parse_date(args.date)
        tag = args.tag or build_tag_name(target_date, prefix, base_year)
        tag_message = (args.message or "").strip() or None
    except Exception as exc:
        print(f"[ERROR] 参数解析失败: {exc}", file=sys.stderr)
        return 1

    print(f"[INFO] Services: {', '.join(repo.name for repo in repos)}")
    print(f"[INFO] Branch: origin/{branch}")
    print(f"[INFO] Tag: {tag}")
    print(f"[INFO] Dry-run: {'YES' if args.dry_run else 'NO'}")

    results: list[TagResult] = []
    for repo in repos:
        print(f"[{repo.name}] processing...", end=" ")
        result = process_repo(
            cfg=cfg,
            repo=repo,
            branch=branch,
            tag=tag,
            tag_message=tag_message,
            dry_run=args.dry_run,
        )
        results.append(result)
        status = "OK" if result.ok else "FAIL"
        print(f"[{status}] {result.detail}")

    return print_summary(results)


if __name__ == "__main__":
    raise SystemExit(main())
