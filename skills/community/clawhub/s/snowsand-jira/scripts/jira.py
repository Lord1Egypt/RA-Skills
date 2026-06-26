#!/usr/bin/env python3
"""
Jira Cloud CLI - Interact with Jira Cloud REST API v3.

Environment variables required:
  JIRA_BASE_URL   - Jira instance URL (e.g., https://yourcompany.atlassian.net)
  JIRA_USER_EMAIL - Atlassian account email
  JIRA_API_TOKEN  - API token from https://id.atlassian.com/manage-profile/security/api-tokens
"""

import argparse
import json
import os
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, quote


def get_config():
    """Get Jira configuration from environment."""
    base_url = os.environ.get("JIRA_BASE_URL", "").rstrip("/")
    email = os.environ.get("JIRA_USER_EMAIL", "")
    token = os.environ.get("JIRA_API_TOKEN", "")
    
    if not all([base_url, email, token]):
        missing = []
        if not base_url: missing.append("JIRA_BASE_URL")
        if not email: missing.append("JIRA_USER_EMAIL")
        if not token: missing.append("JIRA_API_TOKEN")
        print(f"Error: Missing environment variables: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)
    
    return base_url, email, token


def make_request(method, endpoint, data=None):
    """Make authenticated request to Jira API."""
    base_url, email, token = get_config()
    url = f"{base_url}{endpoint}"
    
    import base64
    auth = base64.b64encode(f"{email}:{token}".encode()).decode()
    
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


def format_adf(text):
    """Convert plain text to Atlassian Document Format."""
    return {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": text}]
            }
        ]
    }


def cmd_search(args):
    """Search issues using JQL."""
    params = {
        "jql": args.jql,
        "maxResults": args.max_results,
        "fields": "key,summary,status,assignee,priority,issuetype,created,updated"
    }
    
    result = make_request("GET", f"/rest/api/3/search?{urlencode(params)}")
    
    issues = []
    for issue in result.get("issues", []):
        fields = issue.get("fields", {})
        issues.append({
            "key": issue.get("key"),
            "summary": fields.get("summary"),
            "status": fields.get("status", {}).get("name") if fields.get("status") else None,
            "assignee": fields.get("assignee", {}).get("emailAddress") if fields.get("assignee") else None,
            "priority": fields.get("priority", {}).get("name") if fields.get("priority") else None,
            "type": fields.get("issuetype", {}).get("name") if fields.get("issuetype") else None,
            "created": fields.get("created"),
            "updated": fields.get("updated"),
        })
    
    print(json.dumps(issues, indent=2))


def cmd_get(args):
    """Get issue details."""
    result = make_request("GET", f"/rest/api/3/issue/{args.issue_key}")
    print(json.dumps(result, indent=2))


def cmd_create(args):
    """Create a new issue."""
    fields = {
        "project": {"key": args.project},
        "issuetype": {"name": args.type},
        "summary": args.summary,
    }
    
    if args.description:
        fields["description"] = format_adf(args.description)
    
    if args.priority:
        fields["priority"] = {"name": args.priority}
    
    if args.assignee:
        fields["assignee"] = {"accountId": args.assignee}
    
    if args.labels:
        fields["labels"] = args.labels.split(",")
    
    if args.components:
        fields["components"] = [{"name": c.strip()} for c in args.components.split(",")]
    
    if args.parent:
        fields["parent"] = {"key": args.parent}
    
    result = make_request("POST", "/rest/api/3/issue", {"fields": fields})
    print(json.dumps(result, indent=2))


def cmd_update(args):
    """Update an existing issue."""
    fields = {}
    
    if args.summary:
        fields["summary"] = args.summary
    
    if args.description:
        fields["description"] = format_adf(args.description)
    
    if args.priority:
        fields["priority"] = {"name": args.priority}
    
    if args.assignee:
        # Use accountId for assignment; pass "-1" to unassign
        if args.assignee == "-1":
            fields["assignee"] = None
        else:
            fields["assignee"] = {"accountId": args.assignee}
    
    if args.labels:
        fields["labels"] = args.labels.split(",")
    
    if not fields:
        print("Error: No fields to update", file=sys.stderr)
        sys.exit(1)
    
    make_request("PUT", f"/rest/api/3/issue/{args.issue_key}", {"fields": fields})
    print(json.dumps({"status": "updated", "key": args.issue_key}))


def cmd_comment(args):
    """Add a comment to an issue."""
    data = {"body": format_adf(args.text)}
    result = make_request("POST", f"/rest/api/3/issue/{args.issue_key}/comment", data)
    print(json.dumps(result, indent=2))


def cmd_transitions(args):
    """List available transitions for an issue."""
    result = make_request("GET", f"/rest/api/3/issue/{args.issue_key}/transitions")
    
    transitions = [
        {"id": t["id"], "name": t["name"]}
        for t in result.get("transitions", [])
    ]
    print(json.dumps(transitions, indent=2))


def cmd_transition(args):
    """Transition an issue to a new status."""
    # First get available transitions
    trans_result = make_request("GET", f"/rest/api/3/issue/{args.issue_key}/transitions")
    
    target_name = args.status.lower()
    transition_id = None
    
    for t in trans_result.get("transitions", []):
        if t["name"].lower() == target_name:
            transition_id = t["id"]
            break
    
    if not transition_id:
        available = [t["name"] for t in trans_result.get("transitions", [])]
        print(f"Error: Transition '{args.status}' not available. Available: {available}", file=sys.stderr)
        sys.exit(1)
    
    make_request("POST", f"/rest/api/3/issue/{args.issue_key}/transitions", {"transition": {"id": transition_id}})
    print(json.dumps({"status": "transitioned", "key": args.issue_key, "to": args.status}))


def cmd_boards(args):
    """List all boards."""
    params = {"maxResults": args.max_results}
    if args.project:
        params["projectKeyOrId"] = args.project
    
    result = make_request("GET", f"/rest/agile/1.0/board?{urlencode(params)}")
    
    boards = [
        {"id": b["id"], "name": b["name"], "type": b.get("type")}
        for b in result.get("values", [])
    ]
    print(json.dumps(boards, indent=2))


def cmd_sprints(args):
    """List sprints for a board."""
    params = {"maxResults": args.max_results}
    if args.state:
        params["state"] = args.state
    
    result = make_request("GET", f"/rest/agile/1.0/board/{args.board_id}/sprint?{urlencode(params)}")
    
    sprints = [
        {
            "id": s["id"],
            "name": s["name"],
            "state": s.get("state"),
            "startDate": s.get("startDate"),
            "endDate": s.get("endDate"),
        }
        for s in result.get("values", [])
    ]
    print(json.dumps(sprints, indent=2))


def cmd_sprint_issues(args):
    """List issues in a sprint."""
    params = {
        "maxResults": args.max_results,
        "fields": "key,summary,status,assignee,priority,issuetype"
    }
    
    result = make_request("GET", f"/rest/agile/1.0/sprint/{args.sprint_id}/issue?{urlencode(params)}")
    
    issues = []
    for issue in result.get("issues", []):
        fields = issue.get("fields", {})
        issues.append({
            "key": issue.get("key"),
            "summary": fields.get("summary"),
            "status": fields.get("status", {}).get("name") if fields.get("status") else None,
            "assignee": fields.get("assignee", {}).get("emailAddress") if fields.get("assignee") else None,
            "type": fields.get("issuetype", {}).get("name") if fields.get("issuetype") else None,
        })
    
    print(json.dumps(issues, indent=2))


def cmd_worklog(args):
    """Add a worklog entry to an issue."""
    # Parse time (e.g., "1h 30m", "2h", "45m")
    time_str = args.time.lower().replace(" ", "")
    seconds = 0
    
    import re
    hours = re.search(r"(\d+)h", time_str)
    minutes = re.search(r"(\d+)m", time_str)
    
    if hours:
        seconds += int(hours.group(1)) * 3600
    if minutes:
        seconds += int(minutes.group(1)) * 60
    
    if seconds == 0:
        print("Error: Invalid time format. Use '1h 30m', '2h', or '45m'", file=sys.stderr)
        sys.exit(1)
    
    data = {"timeSpentSeconds": seconds}
    
    if args.comment:
        data["comment"] = format_adf(args.comment)
    
    if args.started:
        data["started"] = args.started
    
    result = make_request("POST", f"/rest/api/3/issue/{args.issue_key}/worklog", data)
    print(json.dumps(result, indent=2))


def cmd_worklogs(args):
    """Get worklogs for an issue."""
    result = make_request("GET", f"/rest/api/3/issue/{args.issue_key}/worklog")
    
    worklogs = [
        {
            "id": w["id"],
            "author": w.get("author", {}).get("emailAddress"),
            "timeSpent": w.get("timeSpent"),
            "started": w.get("started"),
            "comment": w.get("comment", {}).get("content", [{}])[0].get("content", [{}])[0].get("text") if w.get("comment") else None,
        }
        for w in result.get("worklogs", [])
    ]
    print(json.dumps(worklogs, indent=2))


def main():
    parser = argparse.ArgumentParser(description="Jira Cloud CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # search
    p = subparsers.add_parser("search", help="Search issues with JQL")
    p.add_argument("jql", help="JQL query string")
    p.add_argument("--max-results", type=int, default=50)
    p.set_defaults(func=cmd_search)
    
    # get
    p = subparsers.add_parser("get", help="Get issue details")
    p.add_argument("issue_key", help="Issue key (e.g., PROJ-123)")
    p.set_defaults(func=cmd_get)
    
    # create
    p = subparsers.add_parser("create", help="Create issue")
    p.add_argument("project", help="Project key")
    p.add_argument("--type", required=True, help="Issue type (Task, Bug, Story, Epic)")
    p.add_argument("--summary", required=True, help="Issue summary/title")
    p.add_argument("--description", help="Issue description")
    p.add_argument("--priority", help="Priority (Highest, High, Medium, Low, Lowest)")
    p.add_argument("--assignee", help="Assignee account ID")
    p.add_argument("--labels", help="Comma-separated labels")
    p.add_argument("--components", help="Comma-separated component names")
    p.add_argument("--parent", help="Parent issue key (for subtasks)")
    p.set_defaults(func=cmd_create)
    
    # update
    p = subparsers.add_parser("update", help="Update issue")
    p.add_argument("issue_key", help="Issue key")
    p.add_argument("--summary", help="New summary")
    p.add_argument("--description", help="New description")
    p.add_argument("--priority", help="New priority")
    p.add_argument("--assignee", help="New assignee account ID (-1 to unassign)")
    p.add_argument("--labels", help="New labels (comma-separated)")
    p.set_defaults(func=cmd_update)
    
    # comment
    p = subparsers.add_parser("comment", help="Add comment")
    p.add_argument("issue_key", help="Issue key")
    p.add_argument("text", help="Comment text")
    p.set_defaults(func=cmd_comment)
    
    # transitions
    p = subparsers.add_parser("transitions", help="List available transitions")
    p.add_argument("issue_key", help="Issue key")
    p.set_defaults(func=cmd_transitions)
    
    # transition
    p = subparsers.add_parser("transition", help="Transition issue to status")
    p.add_argument("issue_key", help="Issue key")
    p.add_argument("status", help="Target status name")
    p.set_defaults(func=cmd_transition)
    
    # boards
    p = subparsers.add_parser("boards", help="List boards")
    p.add_argument("--project", help="Filter by project key")
    p.add_argument("--max-results", type=int, default=50)
    p.set_defaults(func=cmd_boards)
    
    # sprints
    p = subparsers.add_parser("sprints", help="List sprints for board")
    p.add_argument("board_id", type=int, help="Board ID")
    p.add_argument("--state", choices=["active", "closed", "future"])
    p.add_argument("--max-results", type=int, default=50)
    p.set_defaults(func=cmd_sprints)
    
    # sprint-issues
    p = subparsers.add_parser("sprint-issues", help="List issues in sprint")
    p.add_argument("sprint_id", type=int, help="Sprint ID")
    p.add_argument("--max-results", type=int, default=50)
    p.set_defaults(func=cmd_sprint_issues)
    
    # worklog
    p = subparsers.add_parser("worklog", help="Add worklog entry")
    p.add_argument("issue_key", help="Issue key")
    p.add_argument("--time", required=True, help="Time spent (e.g., '1h 30m', '2h', '45m')")
    p.add_argument("--comment", help="Work description")
    p.add_argument("--started", help="Start time (ISO 8601)")
    p.set_defaults(func=cmd_worklog)
    
    # worklogs
    p = subparsers.add_parser("worklogs", help="Get worklogs for issue")
    p.add_argument("issue_key", help="Issue key")
    p.set_defaults(func=cmd_worklogs)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main()
