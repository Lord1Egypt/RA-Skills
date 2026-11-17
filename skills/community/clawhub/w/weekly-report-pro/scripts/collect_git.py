#!/usr/bin/env python3
"""周报素材收集:扫描目录下的 Git 仓库,汇总最近 N 天的提交记录。

只读操作(git log),不修改任何仓库。输出 JSON 到 stdout。
用法:python3 collect_git.py --dirs ~/code ~/work --days 7 [--author 名字或邮箱] [--include-merges] [--mode weekly|monthly]
"""
import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys

MAX_DEPTH = 3          # 目录扫描深度上限
MAX_REPOS = 30         # 仓库数量上限,防失控
MAX_COMMITS_PER_REPO = 200
GIT_TIMEOUT_SECONDS = 15
SKIP_DIRS = {"node_modules", ".venv", "venv", "Library", ".Trash", ".cache", "__pycache__", ".git"}
CODE_EXTENSIONS = {".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".go", ".rs", ".cpp", ".c", ".swift"}


def detect_role(commits, extensions, override=None):
    """根据显式覆盖、提交关键词和文件类型推断角色。"""
    if override and override != "auto":
        return override
    text = " ".join(str(commit.get("msg", "")) for commit in commits).lower()
    if any(word in text for word in ("运营", "转化", "增长", "活动", "运营数据", "运营") ):
        return "ops"
    if any(word in text for word in ("销售", "客户", "商机", "成交", "pipeline")):
        return "sales"
    if any(word in text for word in ("管理", "团队", "招聘", "绩效", "lead")):
        return "manager"
    if any(str(ext).lower() in CODE_EXTENSIONS for ext in extensions):
        return "developer"
    if any(word in text for word in ("fix", "feat", "refactor", "bug", "api", "deploy")):
        return "developer"
    return "unknown"


def parse_plan_file(path):
    """读取 Markdown 复选框,返回计划完成统计;文件只读。"""
    result = {"total": 0, "completed": 0, "pending": 0, "completion_rate": 0.0, "items": []}
    if not path:
        return result
    try:
        with open(os.path.expanduser(path), "r", encoding="utf-8") as handle:
            content = handle.read()
    except (OSError, UnicodeError) as exc:
        result["error"] = f"plan_file: {type(exc).__name__}"
        return result
    pattern = re.compile(r"^\s*[-*]\s+\[([ xX])\]\s+(.+?)\s*$")
    for line in content.splitlines():
        match = pattern.match(line)
        if not match:
            continue
        completed = match.group(1).lower() == "x"
        result["items"].append({"text": match.group(2), "completed": completed})
    result["total"] = len(result["items"])
    result["completed"] = sum(1 for item in result["items"] if item["completed"])
    result["pending"] = result["total"] - result["completed"]
    result["completion_rate"] = round(result["completed"] / result["total"] * 100, 2) if result["total"] else 0.0
    return result


def build_dashboard(result):
    """聚合跨仓库的提交和代码统计,缺失统计按 0 处理。"""
    dashboard = {
        "repo_count": len(result.get("repos", [])),
        "total_commits": int(result.get("total_commits", 0)),
        "lines_added": 0,
        "lines_deleted": 0,
        "files_changed": 0,
    }
    for repo in result.get("repos", []):
        stats = repo.get("stats") or {}
        dashboard["lines_added"] += int(stats.get("lines_added", 0) or 0)
        dashboard["lines_deleted"] += int(stats.get("lines_deleted", 0) or 0)
        dashboard["files_changed"] += int(stats.get("files_changed", 0) or 0)
    return dashboard


def repo_file_extensions(repo):
    """返回仓库受 Git 管理文件的后缀集合。"""
    cmd = ["git", "-C", repo, "ls-files"]
    try:
        output = subprocess.run(cmd, capture_output=True, text=True,
                                timeout=GIT_TIMEOUT_SECONDS).stdout
    except (subprocess.TimeoutExpired, OSError):
        return []
    extensions = set()
    for path in output.splitlines():
        suffix = os.path.splitext(path)[1].lower()
        if suffix:
            extensions.add(suffix)
    return sorted(extensions)


def resolve_language(commits, requested):
    """决定模板语言; auto 根据提交信息是否含中文选择。"""
    if requested != "auto":
        return requested
    text = " ".join(str(commit.get("msg", "")) for commit in commits)
    if not text.strip():
        return "zh"
    return "zh" if re.search(r"[\u4e00-\u9fff]", text) else "en"


def find_repos(roots):
    """在给定根目录内(限深)查找 git 仓库。"""
    repos = []
    for root in roots:
        root = os.path.abspath(os.path.expanduser(root))
        if not os.path.isdir(root):
            continue
        base_depth = root.rstrip(os.sep).count(os.sep)
        for dirpath, dirnames, _ in os.walk(root):
            if dirpath.rstrip(os.sep).count(os.sep) - base_depth >= MAX_DEPTH:
                dirnames[:] = []
                continue
            dirnames[:] = [d for d in dirnames
                           if d not in SKIP_DIRS and not (d.startswith(".") and d != ".git")]
            entries = os.listdir(dirpath) if os.path.isdir(dirpath) else []
            if ".git" in entries:
                repos.append(dirpath)
                dirnames[:] = []
            if len(repos) >= MAX_REPOS:
                return repos
    return repos


def repo_commits(repo, days, author, include_merges=False):
    cmd = ["git", "-C", repo, "log", f"--since={days} days ago",
           "--pretty=format:%ad|%s", "--date=format:%Y-%m-%d"]
    if not include_merges:
        cmd.append("--no-merges")
    if author:
        cmd += ["--author", author]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True,
                             timeout=GIT_TIMEOUT_SECONDS).stdout.strip()
    except (subprocess.TimeoutExpired, OSError):
        return []
    commits = []
    for line in out.splitlines()[:MAX_COMMITS_PER_REPO]:
        if "|" in line:
            date, msg = line.split("|", 1)
            commits.append({"date": date, "msg": msg.strip()})
    return commits


def repo_stats(repo, days, author):
    """获取仓库统计:文件数、增删行数。只读,不修改。"""
    cmd = ["git", "-C", repo, "log", f"--since={days} days ago",
           "--pretty=tformat:", "--numstat", "--no-merges"]
    if author:
        cmd += ["--author", author]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True,
                             timeout=GIT_TIMEOUT_SECONDS).stdout.strip()
    except (subprocess.TimeoutExpired, OSError):
        return {"files_changed": 0, "lines_added": 0, "lines_deleted": 0}
    lines_added, lines_deleted = 0, 0
    files = set()
    for line in out.splitlines():
        parts = line.split("\t")
        if len(parts) >= 3:
            try:
                lines_added += int(parts[0]) if parts[0] != "-" else 0
                lines_deleted += int(parts[1]) if parts[1] != "-" else 0
                files.add(parts[2])
            except ValueError:
                continue
    return {"files_changed": len(files), "lines_added": lines_added, "lines_deleted": lines_deleted}


def main():
    parser = argparse.ArgumentParser(description="周报 Git 素材收集(只读)")
    parser.add_argument("--dirs", nargs="+", default=["."], help="要扫描的目录,可多个")
    parser.add_argument("--days", type=int, default=7, help="回溯天数,默认7")
    parser.add_argument("--author", default=None, help="按作者过滤(名字或邮箱片段)")
    parser.add_argument("--include-merges", action="store_true", help="包含 merge commits")
    parser.add_argument("--mode", default="weekly", choices=["weekly", "monthly"],
                        help="周报/月报模式,影响默认天数(weekly=7, monthly=30)")
    parser.add_argument("--with-stats", action="store_true", help="附带每个仓库的增删行数统计")
    parser.add_argument("--role", default="auto",
                        choices=["auto", "developer", "ops", "sales", "manager"],
                        help="角色,默认根据提交和文件类型自动识别")
    parser.add_argument("--plan-file", default=None,
                        help="只读解析 Markdown 计划文件中的复选框")
    parser.add_argument("--language", default="auto", choices=["auto", "zh", "en"],
                        help="报告模板语言元数据,默认自动识别")
    args = parser.parse_args()

    days = args.days
    if args.mode == "monthly" and days == 7:
        days = 30  # 月报默认30天

    repos = find_repos(args.dirs)
    result = {
        "generated_at": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        "since_days": days,
        "mode": args.mode,
        "author_filter": args.author,
        "include_merges": args.include_merges,
        "repos": [],
    }
    all_commits = []
    all_extensions = []
    for repo in repos:
        commits = repo_commits(repo, days, args.author, args.include_merges)
        if commits:
            all_commits.extend(commits)
            all_extensions.extend(repo_file_extensions(repo))
            entry = {
                "path": repo,
                "name": os.path.basename(repo),
                "commit_count": len(commits),
                "commits": commits,
            }
            if args.with_stats:
                entry["stats"] = repo_stats(repo, days, args.author)
            result["repos"].append(entry)
    result["total_commits"] = sum(r["commit_count"] for r in result["repos"])
    result["role"] = detect_role(all_commits, all_extensions, args.role)
    result["language"] = resolve_language(all_commits, args.language)
    result["dashboard"] = build_dashboard(result)
    if args.plan_file:
        result["goal_tracking"] = parse_plan_file(args.plan_file)
    print(json.dumps(result, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
