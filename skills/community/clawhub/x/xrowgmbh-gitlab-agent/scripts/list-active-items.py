#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""List assigned work, collaborator submissions, and adopt unassigned incidents."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys


PER_PAGE = 100
# Only independent reads use this pool. Assignment and label writes stay serial.
READ_WORKERS = 4
GRAPHQL_BATCH_SIZE = 10
NORMAL_ITEM_TYPES = {"issue", "task"}
LOCAL_ATOM = r"[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+"
PRIORITY_ORDER = {
    "priority::blocker": 0,
    "priority::high": 1,
    "priority::medium": 2,
    "priority::low": 3,
}
CONFIG_PATH_ENV = "OPENCLAW_CONFIG_PATH"
INCIDENT_PRIORITY = {
    "CRITICAL": "priority::blocker",
    "HIGH": "priority::high",
    "MEDIUM": "priority::medium",
    "LOW": "priority::low",
}


def api_read(command, **kwargs):
    """Retry one timed-out API read, never a mutation or invalid response."""
    try:
        return subprocess.run(command, timeout=25, **kwargs)
    except subprocess.TimeoutExpired:
        import time

        print("GitLab API read timed out after 25s; retrying once", file=sys.stderr)
        time.sleep(1)
    return subprocess.run(command, timeout=25, **kwargs)


def api_json(endpoint: str) -> object:
    result = api_read(
        ["glab", "api", endpoint],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return json.loads(result.stdout)


def parallel_reads(read, values):
    """Bound network concurrency and preserve input order and read failures."""
    values = list(values)
    if READ_WORKERS == 1 or len(values) < 2:
        return [read(value) for value in values]
    from concurrent.futures import ThreadPoolExecutor

    with ThreadPoolExecutor(max_workers=READ_WORKERS, thread_name_prefix="gitlab-discovery") as pool:
        return list(pool.map(read, values))


def graphql_json(query: str, variables: dict[str, str]) -> object:
    command = ["glab", "api", "graphql", "-f", "query=" + query]
    for name, value in variables.items():
        command.extend(("-f", name + "=" + value))
    result = api_read(command, check=True, text=True, stdout=subprocess.PIPE)
    payload = json.loads(result.stdout)
    if not isinstance(payload, dict) or payload.get("errors") or not isinstance(payload.get("data"), dict):
        raise ValueError("GitLab GraphQL response is incomplete")
    return payload["data"]


def paginated(endpoint: str) -> list[dict[str, object]]:
    from urllib.parse import urlencode

    records: list[dict[str, object]] = []
    page = 1
    while True:
        separator = "&" if "?" in endpoint else "?"
        payload = api_json(
            f"{endpoint}{separator}{urlencode({'per_page': PER_PAGE, 'page': page})}"
        )
        if not isinstance(payload, list):
            raise ValueError(f"GitLab returned a non-list page for {endpoint}")
        for item in payload:
            if not isinstance(item, dict):
                raise ValueError(f"GitLab returned an invalid item for {endpoint}")
            records.append(item)
        if len(payload) < PER_PAGE:
            break
        page += 1
    return records


def configured_owner() -> str:
    """Require the owner in the active OpenClaw skill configuration."""
    from pathlib import Path
    import re

    configured_path = os.environ.get("OPENCLAW_CONFIG_PATH")
    config_path = (Path(configured_path).expanduser() if configured_path
                   else Path.home() / ".openclaw" / "openclaw.json")
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    for key in ("skills", "entries", "gitlab-agent", "config"):
        if not isinstance(payload, dict):
            raise ValueError("GitLab agent owner configuration must contain objects")
        payload = payload.get(key)
    owner = payload.get("owner") if isinstance(payload, dict) else None
    if not isinstance(owner, str) or not re.fullmatch(r"[A-Za-z0-9_][A-Za-z0-9_.-]*", owner.strip()):
        raise ValueError("Set skills.entries.gitlab-agent.config.owner to a GitLab username")
    return owner.strip()


def object_endpoint(item: dict[str, object], kind: str) -> tuple[str, str]:
    """Resolve project identity only from the GitLab item URL."""
    from urllib.parse import quote, unquote, urlsplit

    url = item.get("web_url")
    iid = item.get("iid")
    if not isinstance(url, str) or not url or type(iid) is not int or iid <= 0:
        raise ValueError("GitLab item identity is incomplete")
    path = urlsplit(url).path
    project, separator, tail = path.partition("/-/")
    collection = "merge_requests" if kind == "merge_request" else "issues"
    valid_routes = ("merge_requests",) if kind == "merge_request" else ("issues", "work_items")
    if not separator or not any(tail == f"{route}/{iid}" for route in valid_routes):
        raise ValueError("GitLab item URL does not match its identity")
    project_path = unquote(project.strip("/"))
    if not project_path or any(part in ("", ".", "..") for part in project_path.split("/")):
        raise ValueError("GitLab project path is invalid")
    return project_path, f"projects/{quote(project_path, safe='')}/{collection}/{iid}"


def owner_created_membership(
    project_path: str, agent_id: int, agent_username: str, owner: str
) -> bool:
    from urllib.parse import quote

    try:
        membership = api_json(
            f"projects/{quote(project_path, safe='')}/members/all/{agent_id}"
        )
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError):
        return False
    return (
        isinstance(membership, dict)
        and membership.get("username") == agent_username
        and membership.get("membership_state") == "active"
        and type(membership.get("access_level")) is int
        and membership["access_level"] >= 10
        and isinstance(membership.get("created_by"), dict)
        and membership["created_by"].get("username") == owner
    )


def read_labels(endpoint: str) -> list[str]:
    payload = api_json(endpoint)
    labels = payload.get("labels") if isinstance(payload, dict) else None
    if not isinstance(labels, list) or any(not isinstance(label, str) for label in labels):
        raise ValueError("GitLab object labels are missing or invalid")
    return labels


def forbidden_delta(labels: list[str], *, allowed: bool) -> tuple[list[str], list[str]]:
    current = set(labels)
    forbidden = "workflow::forbidden"
    additions = [] if allowed or forbidden in current else [forbidden]
    removals = sorted(
        label for label in current
        if (label == forbidden if allowed else label.startswith("workflow::") and label != forbidden)
    )
    return additions, removals


def synchronize_forbidden(endpoint: str, *, allowed: bool) -> list[str]:
    """Read current labels, then send only the required delta."""
    current = set(read_labels(endpoint))
    additions, removals = forbidden_delta(list(current), allowed=allowed)
    if additions or removals:
        command = ["glab", "api", "-X", "PUT", endpoint]
        if additions:
            command.extend(("-f", "add_labels=" + ",".join(additions)))
        if removals:
            command.extend(("-f", "remove_labels=" + ",".join(removals)))
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return sorted((current | set(additions)) - set(removals))


def permitted_items(
    items: list[tuple[dict[str, object], str]],
    agent_id: int,
    agent_username: str,
    owner: str,
) -> list[dict[str, object]]:
    """Fail each item closed and quietly omit denied items after label hygiene."""
    records = []
    for item, kind in items:
        try:
            project_path, endpoint = object_endpoint(item, kind)
            records.append((item, kind, project_path, endpoint))
        except ValueError:
            continue
    projects = list(dict.fromkeys(record[2] for record in records))
    access = dict(zip(projects, parallel_reads(
        lambda project: agent_username == owner
        or owner_created_membership(project, agent_id, agent_username, owner), projects,
    )))

    def checked_labels(record):
        try:
            return read_labels(record[3])
        except (OSError, subprocess.SubprocessError, json.JSONDecodeError, ValueError):
            return None

    snapshots = parallel_reads(checked_labels, records)
    result: list[dict[str, object]] = []
    for (item, kind, project_path, endpoint), labels in zip(records, snapshots):
        if labels is None:
            continue
        try:
            allowed = access[project_path]
            additions, removals = forbidden_delta(labels, allowed=allowed)
            if additions or removals:
                # Re-read immediately before each serial mutation, never write a
                # prefetched label snapshot back over a concurrent client.
                labels = synchronize_forbidden(endpoint, allowed=allowed)
            if allowed and "workflow::paused" not in labels:
                safe_item = dict(item)
                safe_item["labels"] = sorted(set(labels))
                result.append(normalized(safe_item, kind))
        except (OSError, subprocess.SubprocessError, json.JSONDecodeError, ValueError):
            continue
    return result


def configured_accept_entries() -> list[str]:
    """Read collaborator selectors from the active OpenClaw configuration."""
    from pathlib import Path

    configured_path = os.environ.get(CONFIG_PATH_ENV)
    config_path = (
        Path(configured_path).expanduser()
        if configured_path
        else Path.home() / ".openclaw" / "openclaw.json"
    )
    if not config_path.exists():
        return []
    payload = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("OpenClaw configuration is not an object")
    skills = payload.get("skills", {})
    if not isinstance(skills, dict):
        raise ValueError("OpenClaw skills configuration is not an object")
    entries = skills.get("entries", {})
    if not isinstance(entries, dict):
        raise ValueError("OpenClaw skill entries configuration is not an object")
    agent = entries.get("gitlab-agent", {})
    if not isinstance(agent, dict):
        raise ValueError("gitlab-agent configuration is not an object")

    # OpenClaw currently reserves arbitrary skill settings below `config`, while
    # accepting the issue-requested direct spelling for forward compatibility.
    collaborators = agent.get("collaborators")
    if collaborators is None:
        skill_config = agent.get("config", {})
        if not isinstance(skill_config, dict):
            raise ValueError("gitlab-agent config is not an object")
        collaborators = skill_config.get("collaborators", {})
    if not isinstance(collaborators, dict):
        raise ValueError("gitlab-agent collaborators configuration is not an object")
    accept = collaborators.get("accept", [])
    if not isinstance(accept, list) or any(
        not isinstance(entry, str) or not entry.strip() for entry in accept
    ):
        raise ValueError("gitlab-agent collaborators.accept must be a list of strings")
    return [entry.strip() for entry in accept]


def valid_domain(domain: str) -> bool:
    return (
        len(domain) <= 253
        and "." in domain
        and all(
            re.fullmatch(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?", label)
            for label in domain.lower().split(".")
        )
    )


def email_domain(address: object) -> str | None:
    """Return an exact, syntactically usable email domain without exposing it."""
    if not isinstance(address, str):
        return None
    local, separator, domain = address.rpartition("@")
    if not separator or not valid_domain(domain):
        return None
    # Accept dot-separated local atoms; reject obvious malformed/quoted values.
    if not re.fullmatch(rf"{LOCAL_ATOM}(?:\.{LOCAL_ATOM})*", local):
        return None
    return domain.casefold()


def user_matches_domain(user: dict[str, object], domain: str) -> bool:
    """Match only authorized account/public address fields, never commit metadata."""
    return any(
        email_domain(user.get(field)) == domain.casefold()
        for field in ("email", "public_email")
    )


def accepted_usernames(selectors: list[str]) -> set[str]:
    """Resolve explicit username/group selectors without domain searching."""
    from urllib.parse import urlencode

    usernames: set[str] = set()
    for selector in selectors:
        if selector.startswith("@"):
            continue
        matching_users = [
            user
            for user in paginated(f"users?{urlencode({'username': selector})}")
            if user.get("username") == selector
        ]
        usernames.update(
            user["username"]
            for user in matching_users
            if isinstance(user.get("username"), str)
        )
        groups = [
            group
            for group in paginated(f"groups?{urlencode({'search': selector})}")
            if group.get("full_path") == selector or group.get("path") == selector
        ]
        for group in groups:
            group_id = group.get("id")
            if type(group_id) is not int or group_id <= 0:
                raise ValueError(f"GitLab group identity is incomplete: {selector}")
            for member in paginated(f"groups/{group_id}/members/all"):
                username = member.get("username")
                if isinstance(username, str):
                    usernames.add(username)
        if not matching_users and not groups:
            raise ValueError(f"unknown collaborator username or group: {selector}")
    return usernames


def assignment_candidates(
    user_id: int, username: str, owner: str, project_cache: dict[int, bool]
) -> list[dict[str, object]]:
    """Enumerate normal unassigned issues only inside allowed active member projects."""
    def read_candidates(project):
        project_id = project.get("id")
        path = project.get("path_with_namespace")
        if not isinstance(path, str) or not path:
            raise ValueError("GitLab member project path is incomplete")
        if username != owner and not owner_created_membership(path, user_id, username, owner):
            return []
        records = []
        for item in paginated(
            f"projects/{project_id}/issues?state=opened&scope=all&assignee_id=None"
        ):
            iid = item.get("iid")
            if type(iid) is not int or iid <= 0:
                raise ValueError("GitLab collaborator issue identity is incomplete")
            if (
                item.get("project_id") != project_id
                or item.get("issue_type") not in NORMAL_ITEM_TYPES
                or item.get("assignees") != []
            ):
                continue
            candidate_path, _ = object_endpoint(item, "issue")
            if candidate_path != path:
                raise ValueError("GitLab collaborator issue project path is inconsistent")
            records.append(item)
        return records

    candidates: dict[tuple[int, int], dict[str, object]] = {}
    for records in parallel_reads(read_candidates, active_member_projects(project_cache)):
        for item in records:
            candidates[(item["project_id"], item["iid"])] = item
    return list(candidates.values())


def assign_unassigned_items(
    user_id: int, username: str, owner: str, project_cache: dict[int, bool]
) -> list[dict[str, object]]:
    """Assign accepted normal collaborator work only after owner and state gates."""
    selectors = configured_accept_entries()
    if not selectors:
        return []
    import fcntl
    import tempfile
    from pathlib import Path

    domains = {selector[1:].lower() for selector in selectors if selector.startswith("@")}
    if any(not valid_domain(domain) for domain in domains):
        raise ValueError("invalid collaborator email domain selector")
    explicit_usernames = accepted_usernames(selectors)
    authors: dict[int, dict[str, object] | None] = {}
    diagnosed_missing_email: set[int] = set()
    assigned: list[dict[str, object]] = []
    lock_path = Path(tempfile.gettempdir()) / f"gitlab-agent-assign-{os.getuid()}.lock"
    lock_fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600)
    try:
        # Coordinate concurrent local cron runs through discovery, recheck, and write.
        # External GitLab clients can still race after the recheck; verify persisted state.
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        for item in assignment_candidates(user_id, username, owner, project_cache):
            try:
                author = item.get("author")
                author_id = author.get("id") if isinstance(author, dict) else None
                author_username = author.get("username") if isinstance(author, dict) else None
                if type(author_id) is not int or not isinstance(author_username, str):
                    raise ValueError("candidate author identity is incomplete")
                accepted = author_username in explicit_usernames
                if not accepted and domains:
                    if author_id not in authors:
                        try:
                            profile = api_json(f"users/{author_id}")
                            if not isinstance(profile, dict) or profile.get("id") != author_id:
                                raise ValueError("author profile identity is incomplete")
                            authors[author_id] = profile
                        except (OSError, subprocess.SubprocessError, json.JSONDecodeError, ValueError):
                            authors[author_id] = None
                            print(f"collaborator author lookup failed for user id {author_id}", file=sys.stderr)
                    profile = authors[author_id]
                    if (
                        profile is not None
                        and author_id not in diagnosed_missing_email
                        and not any(email_domain(profile.get(field)) for field in ("email", "public_email"))
                    ):
                        diagnosed_missing_email.add(author_id)
                        print(
                            f"collaborator author {author_id} has no accessible usable email/public_email; "
                            "use a public verified address or explicit username/group selector",
                            file=sys.stderr,
                        )
                    accepted = profile is not None and any(
                        user_matches_domain(profile, domain) for domain in domains
                    )
                if not accepted:
                    continue
                project_path, endpoint = object_endpoint(item, "issue")
                if username != owner and not owner_created_membership(
                    project_path, user_id, username, owner
                ):
                    continue
                synchronize_forbidden(endpoint, allowed=True)
                current = api_json(endpoint)
                if (
                    not isinstance(current, dict)
                    or current.get("iid") != item.get("iid")
                    or current.get("project_id") != item.get("project_id")
                    or current.get("state") != "opened"
                    or current.get("assignees") != []
                ):
                    continue
                if "workflow::paused" in current.get("labels", []):
                    continue
                if current.get("issue_type") not in NORMAL_ITEM_TYPES:
                    continue
                command = ["glab", "api", "-X", "PUT", "-f", f"assignee_ids={user_id}", endpoint]
                try:
                    write = subprocess.run(command, check=True, text=True, stdout=subprocess.PIPE)
                    result = json.loads(write.stdout)
                except (OSError, subprocess.SubprocessError, json.JSONDecodeError):
                    result = None
                    print(f"collaborator assignment write ambiguous for issue {item.get('iid')}", file=sys.stderr)
                # A failed or ambiguous write gets a fresh state read, never a blind retry.
                persisted = api_json(endpoint)
                assignees = persisted.get("assignees") if isinstance(persisted, dict) else None
                if (
                    isinstance(assignees, list)
                    and username in [a.get("username") for a in assignees if isinstance(a, dict)]
                    and persisted.get("state") == "opened"
                    and persisted.get("iid") == item.get("iid")
                    and persisted.get("project_id") == item.get("project_id")
                    and (result is None or (
                        isinstance(result, dict)
                        and isinstance(result.get("assignees"), list)
                        and username in [a.get("username") for a in result["assignees"] if isinstance(a, dict)]
                    ))
                ):
                    assigned.append(persisted)
                else:
                    print(f"collaborator assignment unconfirmed for issue {item.get('iid')}", file=sys.stderr)
            except (OSError, subprocess.SubprocessError, json.JSONDecodeError, ValueError) as error:
                print(
                    f"collaborator assignment skipped for issue {item.get('iid')}: {type(error).__name__}",
                    file=sys.stderr,
                )
    finally:
        fcntl.flock(lock_fd, fcntl.LOCK_UN)
        os.close(lock_fd)
    return assigned


def project_is_active(project_id: object, cache: dict[int, bool]) -> bool:
    """Exclude archived, deleting, and forked projects before fetching work."""
    if type(project_id) is not int or project_id <= 0:
        raise ValueError("GitLab project identity is incomplete")
    if project_id not in cache:
        project = api_json(f"projects/{project_id}")
        if (
            not isinstance(project, dict)
            or project.get("id") != project_id
            or type(project.get("archived")) is not bool
        ):
            raise ValueError(f"GitLab project metadata is incomplete: {project_id}")
        cache[project_id] = not (
            project["archived"]
            or project.get("marked_for_deletion_at")
            or project.get("pending_delete")
            or project.get("forked_from_project")
        )
    return cache[project_id]


def active_member_projects(project_cache: dict[int, bool]) -> list[dict[str, object]]:
    """Refresh metadata in parallel without sharing mutable caches with workers."""
    projects = paginated("projects?membership=true&simple=true")
    # Give each worker a private cache; publish successful results on this thread.
    states = parallel_reads(
        lambda project: project_is_active(project.get("id"), dict(project_cache)), projects,
    )
    for project, active in zip(projects, states):
        project_cache[project["id"]] = active
    return [project for project, active in zip(projects, states) if active]


def unassigned_incidents(project_cache: dict[int, bool]) -> list[dict[str, object]]:
    """Enumerate incidents only in active non-fork member projects."""
    pages = parallel_reads(
        lambda project: paginated(
            f"projects/{project['id']}/issues?state=opened&issue_type=incident&assignee_id=None"
        ), active_member_projects(project_cache),
    )
    incidents: list[dict[str, object]] = []
    for records in pages:
        for item in records:
            if item.get("issue_type") != "incident":
                raise ValueError("GitLab incident query returned another issue type")
            if item.get("assignees") != []:
                raise ValueError("GitLab unassigned incident query returned an assignee")
            incidents.append(item)
    return incidents


def adopt_incident(
    item: dict[str, object], username: str, user_id: int, owner: str
) -> dict[str, object] | None:
    """Gate, assign, and label an unassigned incident before adding it to the queue."""
    try:
        project_path, endpoint = object_endpoint(item, "incident")
        allowed = username == owner or owner_created_membership(
            project_path, user_id, username, owner
        )
        synchronize_forbidden(endpoint, allowed=allowed)
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError, ValueError):
        return None
    if not allowed:
        return None
    current = api_json(endpoint)
    if not isinstance(current, dict) or current.get("issue_type") != "incident":
        raise ValueError("GitLab incident changed during adoption")
    if current.get("assignees") != [] or current.get("state") != "opened":
        return None
    labels = current.get("labels")
    if not isinstance(labels, list) or any(not isinstance(label, str) for label in labels):
        raise ValueError("GitLab incident labels are incomplete")
    if "workflow::paused" in labels:
        return None
    severity = current.get("severity")
    if not isinstance(severity, str):
        raise ValueError("GitLab incident severity is incomplete")
    desired = {"type::support", "workflow::in-progress"}
    # UNKNOWN is not a priority; retain any existing priority until severity is set.
    priority = INCIDENT_PRIORITY.get(severity.upper())
    if priority:
        desired.add(priority)
    existing = set(labels)
    removals = {
        label for label in existing
        if (label.startswith("workflow::") and label != "workflow::in-progress")
        or (label.startswith("type::") and label != "type::support")
    }
    if priority:
        removals.update(
            label for label in existing
            if label.startswith("priority::") and label != priority
        )
    additions = desired - existing
    command = ["glab", "api", "-X", "PUT", "-f", f"assignee_ids={user_id}"]
    if additions:
        command += ["-f", "add_labels=" + ",".join(sorted(additions))]
    if removals:
        command += ["-f", "remove_labels=" + ",".join(sorted(removals))]
    command.append(endpoint)
    result = subprocess.run(command, check=True, text=True, stdout=subprocess.PIPE)
    adopted = json.loads(result.stdout)
    if not isinstance(adopted, dict) or username not in [
        assignee.get("username") for assignee in adopted.get("assignees", [])
        if isinstance(assignee, dict)
    ]:
        raise ValueError("GitLab did not assign the incident to the agent")
    return adopted


def normalized(item: dict[str, object], kind: str) -> dict[str, object]:
    assignees = item.get("assignees")
    if not isinstance(assignees, list):
        assignees = []
    labels = item.get("labels")
    if not isinstance(labels, list):
        labels = []
    updated_at = item.get("updated_at")
    user_notes_count = item.get("user_notes_count")
    if not isinstance(updated_at, str) or not updated_at:
        raise ValueError("GitLab item activity is missing updated_at")
    if (
        not isinstance(user_notes_count, int)
        or isinstance(user_notes_count, bool)
        or user_notes_count < 0
    ):
        raise ValueError("GitLab item activity has an invalid user_notes_count")
    return {
        "kind": kind,
        "project_id": item.get("project_id"),
        "iid": item.get("iid"),
        "title": item.get("title"),
        "web_url": item.get("web_url"),
        "created_at": item.get("created_at"),
        "updated_at": updated_at,
        "labels": labels,
        "assignees": [
            assignee.get("username")
            for assignee in assignees
            if isinstance(assignee, dict)
        ],
        "activity_cursor": {
            "updated_at": updated_at,
            "user_notes_count": user_notes_count,
        },
    }


def issue_kind(item: dict[str, object]) -> str:
    """Keep incidents visible as incidents while treating other work items as issues."""
    return "incident" if item.get("issue_type") == "incident" else "issue"


def priority_rank(labels: object) -> int:
    if not isinstance(labels, list):
        raise ValueError("GitLab item labels are incomplete")
    return min(
        (PRIORITY_ORDER[label] for label in labels if label in PRIORITY_ORDER),
        default=len(PRIORITY_ORDER),
    )


def root_cause_flags(issues: list[dict[str, object]]) -> list[bool]:
    """Read every GraphQL dependency page for gated issues, failing closed."""
    def read_batch(batch):
        identities = [(object_endpoint(item, "issue")[0], str(item["iid"])) for item in batch]
        pending = {index: None for index in range(len(batch))}
        seen = {index: set() for index in pending}
        flags = [False] * len(batch)
        while pending:
            declarations, fields, variables = [], [], {}
            for index, cursor in pending.items():
                project, iid = identities[index]
                declarations.extend((f"$p{index}: ID!", f"$i{index}: String!", f"$c{index}: String"))
                variables.update({f"p{index}": project, f"i{index}": iid})
                if cursor is not None:
                    variables[f"c{index}"] = cursor
                fields.append(
                    f"p{index}: project(fullPath:$p{index}) {{ fullPath "
                    f"item: issue(iid:$i{index}) {{ iid "
                    f"linkedWorkItems(first:20, filter:BLOCKS, after:$c{index}) {{ "
                    "nodes { linkType workItemState } pageInfo { hasNextPage endCursor } } } }"
                )
            data = graphql_json("query(" + ",".join(declarations) + "){" + " ".join(fields) + "}", variables)
            next_page = {}
            for index in pending:
                project, iid = identities[index]
                try:
                    record = data[f"p{index}"]
                    issue = record["item"]
                    links = issue["linkedWorkItems"]
                    nodes = links["nodes"]
                    info = links["pageInfo"]
                    if (record["fullPath"] != project or issue["iid"] != iid
                            or type(info["hasNextPage"]) is not bool or not isinstance(nodes, list)
                            or any(not isinstance(node, dict) or node.get("linkType") != "blocks"
                                   or node.get("workItemState") not in ("OPEN", "CLOSED") for node in nodes)):
                        raise ValueError("GitLab GraphQL dependency page is incomplete")
                    flags[index] |= any(node["workItemState"] == "OPEN" for node in nodes)
                    if info["hasNextPage"]:
                        cursor = info["endCursor"]
                        if not isinstance(cursor, str) or not cursor or cursor in seen[index]:
                            raise ValueError("GitLab GraphQL dependency cursor did not advance")
                        seen[index].add(cursor)
                        next_page[index] = cursor
                except (KeyError, TypeError) as error:
                    raise ValueError("GitLab GraphQL dependency page is incomplete") from error
            pending = next_page
        return flags

    batches = [issues[index:index + GRAPHQL_BATCH_SIZE] for index in range(0, len(issues), GRAPHQL_BATCH_SIZE)]
    return [flag for batch in parallel_reads(read_batch, batches) for flag in batch]


def order_items(items: list[dict[str, object]]) -> list[dict[str, object]]:
    """Priority first, then least recent GitLab activity across projects.

    Activity is a rotation proxy, not proof of agent effort. Routine no-op
    comments must not refresh it. Read-only reports retain maintainer holds;
    executable discovery excludes them before sorting.
    """
    from datetime import datetime

    issues = [item for item in items if item["kind"] != "merge_request"]
    root_causes = {
        (item["project_id"], item["iid"])
        for item, blocks in zip(issues, root_cause_flags(issues))
        if blocks
    }
    def activity_timestamp(item):
        value = (item.get("updated_at")
                 or (item.get("activity_cursor") or {}).get("updated_at")
                 or item["created_at"])
        return datetime.fromisoformat(str(value).replace("Z", "+00:00")).timestamp()

    return sorted(items, key=lambda item: (
        priority_rank(item["labels"]),
        activity_timestamp(item),
        0 if (item["project_id"], item["iid"]) in root_causes else 1,
        str(item.get("web_url") or ""),
    ))


def main() -> int:
    if shutil.which("glab") is None:
        print("glab is required", file=sys.stderr)
        return 69
    try:
        owner = configured_owner()
        user = api_json("user")
        if not isinstance(user, dict) or not isinstance(user.get("username"), str):
            raise ValueError("GitLab user response is incomplete")
        username = user["username"]
        agent_id = user.get("id")
        if type(agent_id) is not int:
            raise ValueError("GitLab user id is missing")
        project_cache: dict[int, bool] = {}
        adopted_incidents = [
            adopted for incident in unassigned_incidents(project_cache)
            if (adopted := adopt_incident(incident, username, agent_id, owner))
            is not None
        ]
        assigned_issues = [
            item for item in paginated("issues?state=opened&scope=assigned_to_me")
            if project_is_active(item.get("project_id"), project_cache)
        ]
        try:
            collaborator_issues = assign_unassigned_items(agent_id, username, owner, project_cache)
        except (OSError, subprocess.SubprocessError, json.JSONDecodeError, ValueError) as error:
            print(f"collaborator assignment unavailable: {type(error).__name__}: {error}", file=sys.stderr)
            collaborator_issues = []
        issue_items = {
            (item.get("project_id"), item.get("iid")): item
            for item in [*assigned_issues, *collaborator_issues, *adopted_incidents]
        }.values()
        raw_items = [
            *((item, issue_kind(item)) for item in issue_items),
            *((item, "merge_request") for item in paginated(
                "merge_requests?state=opened&scope=assigned_to_me"
            ) if project_is_active(item.get("project_id"), project_cache)),
        ]
        eligible = [
            (item, kind) for item, kind in raw_items
            if any(
                isinstance(assignee, dict) and assignee.get("username") == username
                for assignee in (
                    item.get("assignees") if isinstance(item.get("assignees"), list) else []
                )
            )
        ]
        active = permitted_items(eligible, agent_id, username, owner)
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError, ValueError) as error:
        print(f"unable to list active GitLab items: {error}", file=sys.stderr)
        return 69

    try:
        active = order_items(active)
    except (OSError, subprocess.SubprocessError, json.JSONDecodeError, ValueError) as error:
        print(f"unable to order active GitLab items: {error}", file=sys.stderr)
        return 69
    json.dump(active, sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
