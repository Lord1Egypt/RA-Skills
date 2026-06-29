#!/usr/bin/env python3
"""Update the GitLab agent profile chart and proof records."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from collections import defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import quote

from profile_chart import MonthStats, ProfileDeliveryChart


DEFAULT_ROOT_GROUP = "xrow-public"
DEFAULT_PROJECTS = "helm-openclaw ci-tools claw-support"
DIRECT_OWNER_COMMIT_POINTS = 0.2


def glab_json(path: str) -> object:
    result = subprocess.run(
        ["glab", "api", path],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return json.loads(result.stdout)


def current_user() -> str:
    result = subprocess.run(
        [
            "glab",
            "api",
            "graphql",
            "-f",
            "query=query { currentUser { username } }",
        ],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    payload = json.loads(result.stdout)
    return payload["data"]["currentUser"]["username"]


def username_display_name(username: str) -> str:
    users = glab_json(f"/users?username={quote(username, safe='')}")
    if isinstance(users, list) and users:
        return users[0].get("name") or username
    return username


def month_keys(months: int) -> list[str]:
    today = date.today()
    year = today.year
    month = today.month
    keys: list[str] = []
    for offset in range(months - 1, -1, -1):
        absolute = year * 12 + month - 1 - offset
        key_year = absolute // 12
        key_month = absolute % 12 + 1
        keys.append(f"{key_year:04d}-{key_month:02d}")
    return keys


def normalize_projects(raw: str, root_group: str) -> list[str]:
    projects: list[str] = []
    for item in raw.replace(",", " ").split():
        if not item:
            continue
        projects.append(item if "/" in item or not root_group else f"{root_group}/{item}")
    return projects


def workspace_path(raw: str, workspace: Path) -> Path:
    path = Path(raw)
    if path.is_absolute():
        return path
    return workspace / path


def month_start_iso(month: str) -> str:
    return f"{month}-01T00:00:00Z"


def size_factor(labels: list[str]) -> int:
    if "size::xlarge" in labels:
        return 5
    if "size::large" in labels:
        return 3
    if "size::medium" in labels:
        return 2
    return 1


def counted_mr_type(labels: list[str], title: str) -> str:
    lowered = title.lower()
    if (
        lowered.startswith("skip:")
        or lowered.startswith("skip(")
        or lowered.startswith("chore:")
        or lowered.startswith("chore(")
        or lowered.startswith("docs:")
        or lowered.startswith("docs(")
        or "type::skip" in labels
        or "type::chore" in labels
        or "type::docs" in labels
    ):
        return ""
    if "type::fix" in labels:
        return "fix"
    if "type::feature" in labels:
        return "feature"

    if lowered.startswith("fix:") or lowered.startswith("fix("):
        return "fix"
    if lowered.startswith("feat:") or lowered.startswith("feat("):
        return "feature"
    return ""


def is_ignored_direct_commit(commit: dict) -> bool:
    title = (commit.get("title") or commit.get("message") or "").strip()
    lowered = title.lower()
    return (
        lowered.startswith("skip:")
        or lowered.startswith("skip(")
        or lowered.startswith("chore:")
        or lowered.startswith("chore(")
        or lowered.startswith("docs:")
        or lowered.startswith("docs(")
        or lowered.startswith("revert")
    )


def paginated(path: str) -> list[dict]:
    page = 1
    records: list[dict] = []
    while True:
        separator = "&" if "?" in path else "?"
        payload = glab_json(f"{path}{separator}per_page=100&page={page}")
        if not isinstance(payload, list) or not payload:
            break
        records.extend(payload)
        page += 1
    return records


def collect_stats(projects: list[str], owner: str, agent: str, months: list[str]) -> tuple[list[MonthStats], list[dict]]:
    owner_counts: dict[str, int] = defaultdict(int)
    with_owner_counts: dict[str, int] = defaultdict(int)
    autonomous_counts: dict[str, int] = defaultdict(int)
    owner_points: dict[str, int] = defaultdict(int)
    with_owner_points: dict[str, int] = defaultdict(int)
    autonomous_points: dict[str, int] = defaultdict(int)
    direct_owner_counts: dict[str, int] = defaultdict(int)
    known_mr_commits: set[str] = set()
    records: list[dict] = []
    month_set = set(months)
    owner_name = username_display_name(owner)
    after = month_start_iso(months[0])

    for project in projects:
        encoded_project = quote(project, safe="")
        merge_requests = paginated(
            f"/projects/{encoded_project}/merge_requests?state=merged&updated_after={quote(after, safe='')}"
        )
        for mr in merge_requests:
            merged_at = mr.get("merged_at")
            if not merged_at:
                continue
            month = merged_at[:7]
            if month not in month_set:
                continue
            labels = mr.get("labels") or []
            title = mr.get("title") or ""
            for field in ("merge_commit_sha", "squash_commit_sha"):
                sha = mr.get(field)
                if sha:
                    known_mr_commits.add(sha)
            counted_type = counted_mr_type(labels, title)
            if not counted_type:
                continue
            points = size_factor(labels)
            author = (mr.get("author") or {}).get("username", "")
            merge_user = (mr.get("merge_user") or {}).get("username", "")
            reviewers = {reviewer.get("username", "") for reviewer in mr.get("reviewers", [])}
            category = ""
            if author == owner:
                category = "owner"
                owner_counts[month] += 1
                owner_points[month] += points
            elif author == agent:
                if merge_user == owner or owner in reviewers:
                    category = "agent_reviewer"
                    with_owner_counts[month] += 1
                    with_owner_points[month] += points
                else:
                    category = "agent_autonomous"
                    autonomous_counts[month] += 1
                    autonomous_points[month] += points
            if category:
                records.append(
                    {
                        "date": merged_at,
                        "month": month,
                        "project": project,
                        "kind": "merge_request",
                        "category": category,
                        "counted_type": counted_type,
                        "title": title,
                        "reference": mr.get("references", {}).get("full") or mr.get("reference") or "",
                        "url": mr.get("web_url") or "",
                        "author": author,
                        "merge_user": merge_user,
                        "reviewers": sorted(filter(None, reviewers)),
                        "labels": labels,
                        "points": points,
                    }
                )

        commits = paginated(
            f"/projects/{encoded_project}/repository/commits?ref_name=main&since={quote(after, safe='')}"
        )
        for commit in commits:
            sha = commit.get("id")
            committed_at = commit.get("committed_date")
            if not sha or not committed_at or sha in known_mr_commits:
                continue
            month = committed_at[:7]
            if month not in month_set:
                continue
            if is_ignored_direct_commit(commit):
                continue
            author_name = commit.get("author_name") or ""
            committer_name = commit.get("committer_name") or ""
            if owner_name in {author_name, committer_name}:
                direct_owner_counts[month] += 1
                records.append(
                    {
                        "date": committed_at,
                        "month": month,
                        "project": project,
                        "kind": "direct_commit",
                        "category": "owner_direct_main",
                        "title": commit.get("title") or "",
                        "reference": sha[:8],
                        "url": commit.get("web_url") or "",
                        "author": author_name,
                        "committer": committer_name,
                        "points": DIRECT_OWNER_COMMIT_POINTS,
                    }
                )

    stats = [
        MonthStats(
            month=month,
            owner_mrs=owner_counts[month],
            agent_with_owner=with_owner_counts[month],
            agent_autonomous=autonomous_counts[month],
            direct_owner_main=direct_owner_counts[month],
            owner_mr_points=owner_points[month],
            agent_with_owner_points=with_owner_points[month],
            agent_autonomous_points=autonomous_points[month],
        )
        for month in months
    ]
    records.sort(key=lambda record: record["date"], reverse=True)
    return stats, records


def write_records(output: Path, records: list[dict], stats: list[MonthStats]) -> None:
    payload = {
        "generated_on": date.today().isoformat(),
        "records": records,
        "months": [
            {
                "month": month.month,
                "owner_mrs": month.owner_mrs,
                "agent_reviewer_mrs": month.agent_with_owner,
                "agent_autonomous_mrs": month.agent_autonomous,
                "direct_owner_main": month.direct_owner_main,
                "contribution_score": month.contribution_score,
            }
            for month in stats
        ],
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_webp(svg_output: Path, webp_output: Path) -> None:
    webp_output.parent.mkdir(parents=True, exist_ok=True)
    magick = shutil.which("magick")
    if magick:
        subprocess.run([magick, str(svg_output), str(webp_output)], check=True)
        return
    convert = shutil.which("convert")
    if convert:
        subprocess.run([convert, str(svg_output), str(webp_output)], check=True)
        return
    npm = shutil.which("npm")
    if npm:
        subprocess.run(
            [
                npm,
                "exec",
                "--yes",
                "sharp-cli",
                "--",
                "--input",
                str(svg_output),
                "--output",
                str(webp_output),
                "--format",
                "webp",
            ],
            check=True,
        )
        return
    try:
        import cairosvg  # type: ignore
        from PIL import Image  # type: ignore
    except (ImportError, OSError) as exc:
        raise SystemExit(
            "WebP output requires ImageMagick, npm sharp-cli, or Python packages cairosvg and Pillow"
        ) from exc
    png_bytes = cairosvg.svg2png(url=str(svg_output))
    from io import BytesIO

    with Image.open(BytesIO(png_bytes)) as image:
        image.save(webp_output, "WEBP")


def main() -> None:
    workspace = Path(os.environ.get("GITLAB_AGENT_PROFILE_WORKSPACE", ".")).resolve()
    chart_output = workspace_path(
        os.environ.get("GITLAB_AGENT_PROFILE_CHART_OUTPUT", "assets/gitlab-agent-profile.svg"),
        workspace,
    )
    webp_output = workspace_path(
        os.environ.get("GITLAB_AGENT_PROFILE_WEBP_OUTPUT", "assets/gitlab-agent-profile.webp"),
        workspace,
    )
    records_output = workspace_path(
        os.environ.get("GITLAB_AGENT_PROFILE_RECORDS_OUTPUT", "assets/gitlab-agent-profile-records.json"),
        workspace,
    )
    root_group = os.environ.get("GITLAB_AGENT_PROFILE_ROOT_GROUP", DEFAULT_ROOT_GROUP)
    projects = normalize_projects(os.environ.get("GITLAB_AGENT_PROFILE_PROJECTS", DEFAULT_PROJECTS), root_group)
    owner = os.environ.get("GITLAB_AGENT_PROFILE_OWNER_USERNAME", "xrow")
    agent = os.environ.get("GITLAB_AGENT_PROFILE_AGENT_USERNAME") or current_user()
    months_raw = os.environ.get("GITLAB_AGENT_PROFILE_MONTHS", "12")

    try:
        months_count = int(months_raw)
    except ValueError as exc:
        raise SystemExit("GITLAB_AGENT_PROFILE_MONTHS must be a positive integer") from exc
    if months_count < 1:
        raise SystemExit("GITLAB_AGENT_PROFILE_MONTHS must be a positive integer")

    stats, records = collect_stats(projects, owner, agent, month_keys(months_count))
    chart_output.parent.mkdir(parents=True, exist_ok=True)
    chart_output.write_text(
        ProfileDeliveryChart(stats, owner=owner, agent=agent).render(),
        encoding="utf-8",
    )
    write_records(records_output, records, stats)
    write_webp(chart_output, webp_output)


if __name__ == "__main__":
    main()
