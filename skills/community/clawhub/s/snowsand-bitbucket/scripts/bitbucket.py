#!/usr/bin/env python3
"""
Bitbucket Cloud CLI - Interact with Bitbucket Cloud REST API v2.

Environment variables required:
  BITBUCKET_WORKSPACE    - Default workspace slug
  BITBUCKET_USERNAME     - Bitbucket username (not email)
  BITBUCKET_APP_PASSWORD - App password from https://bitbucket.org/account/settings/app-passwords/
"""

import argparse
import json
import os
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, quote


API_BASE = "https://api.bitbucket.org/2.0"


def get_config():
    """Get Bitbucket configuration from environment."""
    workspace = os.environ.get("BITBUCKET_WORKSPACE", "")
    username = os.environ.get("BITBUCKET_USERNAME", "")
    app_password = os.environ.get("BITBUCKET_APP_PASSWORD", "")
    
    if not all([username, app_password]):
        missing = []
        if not username: missing.append("BITBUCKET_USERNAME")
        if not app_password: missing.append("BITBUCKET_APP_PASSWORD")
        print(f"Error: Missing environment variables: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)
    
    return workspace, username, app_password


def make_request(method, endpoint, data=None, params=None):
    """Make authenticated request to Bitbucket API."""
    _, username, app_password = get_config()
    
    url = f"{API_BASE}{endpoint}"
    if params:
        url = f"{url}?{urlencode(params)}"
    
    import base64
    auth = base64.b64encode(f"{username}:{app_password}".encode()).decode()
    
    headers = {
        "Authorization": f"Basic {auth}",
        "Accept": "application/json",
    }
    
    body = None
    if data:
        headers["Content-Type"] = "application/json"
        body = json.dumps(data).encode()
    
    req = Request(url, data=body, headers=headers, method=method)
    
    try:
        with urlopen(req) as resp:
            content = resp.read().decode()
            return json.loads(content) if content else {}
    except HTTPError as e:
        error_body = e.read().decode()
        try:
            error_json = json.loads(error_body)
            print(json.dumps(error_json, indent=2), file=sys.stderr)
        except:
            print(f"HTTP {e.code}: {error_body}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"Connection error: {e.reason}", file=sys.stderr)
        sys.exit(1)


def get_workspace(args):
    """Get workspace from args or environment."""
    ws = getattr(args, 'workspace', None) or os.environ.get("BITBUCKET_WORKSPACE", "")
    if not ws:
        print("Error: No workspace specified. Set BITBUCKET_WORKSPACE or use --workspace", file=sys.stderr)
        sys.exit(1)
    return ws


# =============================================================================
# Repository Commands
# =============================================================================

def cmd_repos(args):
    """List repositories in workspace."""
    ws = get_workspace(args)
    params = {"pagelen": args.pagelen}
    if args.page:
        params["page"] = args.page
    
    result = make_request("GET", f"/repositories/{ws}", params=params)
    
    repos = []
    for repo in result.get("values", []):
        repos.append({
            "slug": repo.get("slug"),
            "name": repo.get("name"),
            "full_name": repo.get("full_name"),
            "is_private": repo.get("is_private"),
            "description": repo.get("description"),
            "updated_on": repo.get("updated_on"),
        })
    
    print(json.dumps(repos, indent=2))


def cmd_repo(args):
    """Get repository details."""
    ws = get_workspace(args)
    result = make_request("GET", f"/repositories/{ws}/{args.repo_slug}")
    print(json.dumps(result, indent=2))


def cmd_create_repo(args):
    """Create a new repository."""
    ws = get_workspace(args)
    
    data = {
        "scm": "git",
        "is_private": args.private,
    }
    
    if args.description:
        data["description"] = args.description
    
    if args.project:
        data["project"] = {"key": args.project}
    
    if args.fork_policy:
        data["fork_policy"] = args.fork_policy
    
    result = make_request("POST", f"/repositories/{ws}/{args.repo_slug}", data)
    print(json.dumps(result, indent=2))


# =============================================================================
# Pull Request Commands
# =============================================================================

def cmd_prs(args):
    """List pull requests."""
    ws = get_workspace(args)
    params = {"pagelen": args.pagelen}
    
    if args.state:
        if args.state == "all":
            params["state"] = "OPEN,MERGED,DECLINED,SUPERSEDED"
        else:
            params["state"] = args.state.upper()
    
    result = make_request("GET", f"/repositories/{ws}/{args.repo_slug}/pullrequests", params=params)
    
    prs = []
    for pr in result.get("values", []):
        prs.append({
            "id": pr.get("id"),
            "title": pr.get("title"),
            "state": pr.get("state"),
            "author": pr.get("author", {}).get("display_name"),
            "source_branch": pr.get("source", {}).get("branch", {}).get("name"),
            "destination_branch": pr.get("destination", {}).get("branch", {}).get("name"),
            "created_on": pr.get("created_on"),
            "updated_on": pr.get("updated_on"),
            "comment_count": pr.get("comment_count"),
        })
    
    print(json.dumps(prs, indent=2))


def cmd_pr(args):
    """Get pull request details."""
    ws = get_workspace(args)
    result = make_request("GET", f"/repositories/{ws}/{args.repo_slug}/pullrequests/{args.pr_id}")
    print(json.dumps(result, indent=2))


def cmd_create_pr(args):
    """Create a pull request."""
    ws = get_workspace(args)
    
    data = {
        "title": args.title,
        "source": {
            "branch": {"name": args.source}
        },
    }
    
    if args.destination:
        data["destination"] = {"branch": {"name": args.destination}}
    
    if args.description:
        data["description"] = args.description
    
    if args.close_source_branch:
        data["close_source_branch"] = True
    
    if args.reviewers:
        data["reviewers"] = [{"uuid": r.strip()} for r in args.reviewers.split(",")]
    
    result = make_request("POST", f"/repositories/{ws}/{args.repo_slug}/pullrequests", data)
    print(json.dumps(result, indent=2))


def cmd_pr_comment(args):
    """Add a comment to a pull request."""
    ws = get_workspace(args)
    data = {"content": {"raw": args.text}}
    result = make_request("POST", f"/repositories/{ws}/{args.repo_slug}/pullrequests/{args.pr_id}/comments", data)
    print(json.dumps(result, indent=2))


def cmd_approve(args):
    """Approve a pull request."""
    ws = get_workspace(args)
    result = make_request("POST", f"/repositories/{ws}/{args.repo_slug}/pullrequests/{args.pr_id}/approve")
    print(json.dumps({"status": "approved", "pr_id": args.pr_id}))


def cmd_unapprove(args):
    """Remove approval from a pull request."""
    ws = get_workspace(args)
    make_request("DELETE", f"/repositories/{ws}/{args.repo_slug}/pullrequests/{args.pr_id}/approve")
    print(json.dumps({"status": "unapproved", "pr_id": args.pr_id}))


def cmd_request_changes(args):
    """Request changes on a pull request."""
    ws = get_workspace(args)
    result = make_request("POST", f"/repositories/{ws}/{args.repo_slug}/pullrequests/{args.pr_id}/request-changes")
    print(json.dumps({"status": "changes_requested", "pr_id": args.pr_id}))


def cmd_merge(args):
    """Merge a pull request."""
    ws = get_workspace(args)
    
    data = {}
    if args.strategy:
        data["merge_strategy"] = args.strategy
    if args.message:
        data["message"] = args.message
    if args.close_source_branch:
        data["close_source_branch"] = True
    
    result = make_request("POST", f"/repositories/{ws}/{args.repo_slug}/pullrequests/{args.pr_id}/merge", data if data else None)
    print(json.dumps(result, indent=2))


def cmd_decline(args):
    """Decline a pull request."""
    ws = get_workspace(args)
    result = make_request("POST", f"/repositories/{ws}/{args.repo_slug}/pullrequests/{args.pr_id}/decline")
    print(json.dumps({"status": "declined", "pr_id": args.pr_id}))


# =============================================================================
# Branch Commands
# =============================================================================

def cmd_branches(args):
    """List branches."""
    ws = get_workspace(args)
    params = {"pagelen": args.pagelen}
    if args.sort:
        params["sort"] = args.sort
    
    result = make_request("GET", f"/repositories/{ws}/{args.repo_slug}/refs/branches", params=params)
    
    branches = []
    for branch in result.get("values", []):
        target = branch.get("target", {})
        branches.append({
            "name": branch.get("name"),
            "hash": target.get("hash"),
            "message": target.get("message", "").split("\n")[0] if target.get("message") else None,
            "date": target.get("date"),
            "author": target.get("author", {}).get("raw"),
        })
    
    print(json.dumps(branches, indent=2))


def cmd_branch(args):
    """Get branch details."""
    ws = get_workspace(args)
    # URL encode the branch name for paths with slashes
    branch_name = quote(args.branch_name, safe="")
    result = make_request("GET", f"/repositories/{ws}/{args.repo_slug}/refs/branches/{branch_name}")
    print(json.dumps(result, indent=2))


def cmd_create_branch(args):
    """Create a new branch."""
    ws = get_workspace(args)
    
    data = {
        "name": args.branch_name,
        "target": {"hash": args.from_ref}
    }
    
    result = make_request("POST", f"/repositories/{ws}/{args.repo_slug}/refs/branches", data)
    print(json.dumps(result, indent=2))


def cmd_delete_branch(args):
    """Delete a branch."""
    ws = get_workspace(args)
    branch_name = quote(args.branch_name, safe="")
    make_request("DELETE", f"/repositories/{ws}/{args.repo_slug}/refs/branches/{branch_name}")
    print(json.dumps({"status": "deleted", "branch": args.branch_name}))


# =============================================================================
# Commit Commands
# =============================================================================

def cmd_commits(args):
    """List commits."""
    ws = get_workspace(args)
    params = {"pagelen": args.pagelen}
    
    endpoint = f"/repositories/{ws}/{args.repo_slug}/commits"
    if args.branch:
        endpoint = f"/repositories/{ws}/{args.repo_slug}/commits/{quote(args.branch, safe='')}"
    
    result = make_request("GET", endpoint, params=params)
    
    commits = []
    for commit in result.get("values", []):
        author = commit.get("author", {})
        commits.append({
            "hash": commit.get("hash"),
            "message": commit.get("message", "").split("\n")[0],
            "date": commit.get("date"),
            "author": author.get("user", {}).get("display_name") or author.get("raw"),
        })
    
    print(json.dumps(commits, indent=2))


def cmd_commit(args):
    """Get commit details."""
    ws = get_workspace(args)
    result = make_request("GET", f"/repositories/{ws}/{args.repo_slug}/commit/{args.commit_hash}")
    print(json.dumps(result, indent=2))


# =============================================================================
# Pipeline Commands
# =============================================================================

def cmd_pipelines(args):
    """List pipelines."""
    ws = get_workspace(args)
    params = {"pagelen": args.pagelen, "sort": "-created_on"}
    
    result = make_request("GET", f"/repositories/{ws}/{args.repo_slug}/pipelines", params=params)
    
    pipelines = []
    for pipeline in result.get("values", []):
        state = pipeline.get("state", {})
        state_name = state.get("name")
        if state_name == "COMPLETED":
            state_name = state.get("result", {}).get("name", state_name)
        
        target = pipeline.get("target", {})
        
        # Filter by status if specified
        if args.status and state_name != args.status.upper():
            continue
        
        pipelines.append({
            "uuid": pipeline.get("uuid"),
            "build_number": pipeline.get("build_number"),
            "state": state_name,
            "branch": target.get("ref_name"),
            "commit": target.get("commit", {}).get("hash", "")[:12],
            "created_on": pipeline.get("created_on"),
            "duration_in_seconds": pipeline.get("duration_in_seconds"),
        })
    
    print(json.dumps(pipelines, indent=2))


def cmd_pipeline(args):
    """Get pipeline details."""
    ws = get_workspace(args)
    result = make_request("GET", f"/repositories/{ws}/{args.repo_slug}/pipelines/{args.pipeline_uuid}")
    print(json.dumps(result, indent=2))


def cmd_pipeline_steps(args):
    """List steps in a pipeline."""
    ws = get_workspace(args)
    result = make_request("GET", f"/repositories/{ws}/{args.repo_slug}/pipelines/{args.pipeline_uuid}/steps")
    
    steps = []
    for step in result.get("values", []):
        state = step.get("state", {})
        state_name = state.get("name")
        if state_name == "COMPLETED":
            state_name = state.get("result", {}).get("name", state_name)
        
        steps.append({
            "uuid": step.get("uuid"),
            "name": step.get("name"),
            "state": state_name,
            "duration_in_seconds": step.get("duration_in_seconds"),
        })
    
    print(json.dumps(steps, indent=2))


def cmd_run_pipeline(args):
    """Trigger a pipeline run."""
    ws = get_workspace(args)
    
    data = {
        "target": {
            "type": "pipeline_ref_target",
            "ref_type": "branch",
            "ref_name": args.branch,
        }
    }
    
    if args.selector:
        data["target"]["selector"] = {"type": "custom", "pattern": args.selector}
    
    result = make_request("POST", f"/repositories/{ws}/{args.repo_slug}/pipelines", data)
    print(json.dumps(result, indent=2))


# =============================================================================
# Workspace Commands
# =============================================================================

def cmd_workspaces(args):
    """List accessible workspaces."""
    result = make_request("GET", "/workspaces")
    
    workspaces = []
    for ws in result.get("values", []):
        workspaces.append({
            "slug": ws.get("slug"),
            "name": ws.get("name"),
            "uuid": ws.get("uuid"),
        })
    
    print(json.dumps(workspaces, indent=2))


def cmd_members(args):
    """List workspace members."""
    ws = get_workspace(args)
    params = {"pagelen": args.pagelen}
    
    result = make_request("GET", f"/workspaces/{ws}/members", params=params)
    
    members = []
    for member in result.get("values", []):
        user = member.get("user", {})
        members.append({
            "uuid": user.get("uuid"),
            "display_name": user.get("display_name"),
            "nickname": user.get("nickname"),
            "account_id": user.get("account_id"),
        })
    
    print(json.dumps(members, indent=2))


def cmd_me(args):
    """Get current user info."""
    result = make_request("GET", "/user")
    print(json.dumps(result, indent=2))


# =============================================================================
# Main
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Bitbucket Cloud CLI")
    parser.add_argument("--workspace", "-w", help="Workspace slug (overrides BITBUCKET_WORKSPACE)")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # --- Repositories ---
    p = subparsers.add_parser("repos", help="List repositories")
    p.add_argument("--pagelen", type=int, default=25)
    p.add_argument("--page", type=int)
    p.set_defaults(func=cmd_repos)
    
    p = subparsers.add_parser("repo", help="Get repository details")
    p.add_argument("repo_slug", help="Repository slug")
    p.set_defaults(func=cmd_repo)
    
    p = subparsers.add_parser("create-repo", help="Create repository")
    p.add_argument("repo_slug", help="Repository slug (URL-friendly name)")
    p.add_argument("--private", action="store_true", default=True, help="Private repository (default)")
    p.add_argument("--public", action="store_false", dest="private", help="Public repository")
    p.add_argument("--description", help="Repository description")
    p.add_argument("--project", help="Project key")
    p.add_argument("--fork-policy", choices=["allow_forks", "no_public_forks", "no_forks"])
    p.set_defaults(func=cmd_create_repo)
    
    # --- Pull Requests ---
    p = subparsers.add_parser("prs", help="List pull requests")
    p.add_argument("repo_slug", help="Repository slug")
    p.add_argument("--state", choices=["open", "merged", "declined", "superseded", "all"], default="open")
    p.add_argument("--pagelen", type=int, default=25)
    p.set_defaults(func=cmd_prs)
    
    p = subparsers.add_parser("pr", help="Get pull request details")
    p.add_argument("repo_slug", help="Repository slug")
    p.add_argument("pr_id", type=int, help="Pull request ID")
    p.set_defaults(func=cmd_pr)
    
    p = subparsers.add_parser("create-pr", help="Create pull request")
    p.add_argument("repo_slug", help="Repository slug")
    p.add_argument("--title", required=True, help="PR title")
    p.add_argument("--source", required=True, help="Source branch name")
    p.add_argument("--destination", help="Destination branch (defaults to repo's main branch)")
    p.add_argument("--description", help="PR description")
    p.add_argument("--close-source-branch", action="store_true", help="Close source branch after merge")
    p.add_argument("--reviewers", help="Comma-separated reviewer UUIDs")
    p.set_defaults(func=cmd_create_pr)
    
    p = subparsers.add_parser("pr-comment", help="Comment on pull request")
    p.add_argument("repo_slug", help="Repository slug")
    p.add_argument("pr_id", type=int, help="Pull request ID")
    p.add_argument("text", help="Comment text")
    p.set_defaults(func=cmd_pr_comment)
    
    p = subparsers.add_parser("approve", help="Approve pull request")
    p.add_argument("repo_slug", help="Repository slug")
    p.add_argument("pr_id", type=int, help="Pull request ID")
    p.set_defaults(func=cmd_approve)
    
    p = subparsers.add_parser("unapprove", help="Remove approval from pull request")
    p.add_argument("repo_slug", help="Repository slug")
    p.add_argument("pr_id", type=int, help="Pull request ID")
    p.set_defaults(func=cmd_unapprove)
    
    p = subparsers.add_parser("request-changes", help="Request changes on pull request")
    p.add_argument("repo_slug", help="Repository slug")
    p.add_argument("pr_id", type=int, help="Pull request ID")
    p.set_defaults(func=cmd_request_changes)
    
    p = subparsers.add_parser("merge", help="Merge pull request")
    p.add_argument("repo_slug", help="Repository slug")
    p.add_argument("pr_id", type=int, help="Pull request ID")
    p.add_argument("--strategy", choices=["merge_commit", "squash", "fast_forward"])
    p.add_argument("--message", help="Merge commit message")
    p.add_argument("--close-source-branch", action="store_true")
    p.set_defaults(func=cmd_merge)
    
    p = subparsers.add_parser("decline", help="Decline pull request")
    p.add_argument("repo_slug", help="Repository slug")
    p.add_argument("pr_id", type=int, help="Pull request ID")
    p.set_defaults(func=cmd_decline)
    
    # --- Branches ---
    p = subparsers.add_parser("branches", help="List branches")
    p.add_argument("repo_slug", help="Repository slug")
    p.add_argument("--sort", help="Sort field (e.g., -name)")
    p.add_argument("--pagelen", type=int, default=25)
    p.set_defaults(func=cmd_branches)
    
    p = subparsers.add_parser("branch", help="Get branch details")
    p.add_argument("repo_slug", help="Repository slug")
    p.add_argument("branch_name", help="Branch name")
    p.set_defaults(func=cmd_branch)
    
    p = subparsers.add_parser("create-branch", help="Create branch")
    p.add_argument("repo_slug", help="Repository slug")
    p.add_argument("branch_name", help="New branch name")
    p.add_argument("--from", dest="from_ref", required=True, help="Source branch or commit hash")
    p.set_defaults(func=cmd_create_branch)
    
    p = subparsers.add_parser("delete-branch", help="Delete branch")
    p.add_argument("repo_slug", help="Repository slug")
    p.add_argument("branch_name", help="Branch name to delete")
    p.set_defaults(func=cmd_delete_branch)
    
    # --- Commits ---
    p = subparsers.add_parser("commits", help="List commits")
    p.add_argument("repo_slug", help="Repository slug")
    p.add_argument("--branch", help="Branch name (defaults to main branch)")
    p.add_argument("--pagelen", type=int, default=25)
    p.set_defaults(func=cmd_commits)
    
    p = subparsers.add_parser("commit", help="Get commit details")
    p.add_argument("repo_slug", help="Repository slug")
    p.add_argument("commit_hash", help="Commit hash")
    p.set_defaults(func=cmd_commit)
    
    # --- Pipelines ---
    p = subparsers.add_parser("pipelines", help="List pipelines")
    p.add_argument("repo_slug", help="Repository slug")
    p.add_argument("--status", help="Filter by status (SUCCESSFUL, FAILED, IN_PROGRESS)")
    p.add_argument("--pagelen", type=int, default=25)
    p.set_defaults(func=cmd_pipelines)
    
    p = subparsers.add_parser("pipeline", help="Get pipeline details")
    p.add_argument("repo_slug", help="Repository slug")
    p.add_argument("pipeline_uuid", help="Pipeline UUID")
    p.set_defaults(func=cmd_pipeline)
    
    p = subparsers.add_parser("pipeline-steps", help="List pipeline steps")
    p.add_argument("repo_slug", help="Repository slug")
    p.add_argument("pipeline_uuid", help="Pipeline UUID")
    p.set_defaults(func=cmd_pipeline_steps)
    
    p = subparsers.add_parser("run-pipeline", help="Trigger pipeline")
    p.add_argument("repo_slug", help="Repository slug")
    p.add_argument("--branch", required=True, help="Branch to run pipeline on")
    p.add_argument("--selector", help="Custom pipeline selector pattern")
    p.set_defaults(func=cmd_run_pipeline)
    
    # --- Workspace ---
    p = subparsers.add_parser("workspaces", help="List workspaces")
    p.set_defaults(func=cmd_workspaces)
    
    p = subparsers.add_parser("members", help="List workspace members")
    p.add_argument("--pagelen", type=int, default=50)
    p.set_defaults(func=cmd_members)
    
    p = subparsers.add_parser("me", help="Get current user")
    p.set_defaults(func=cmd_me)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main()
