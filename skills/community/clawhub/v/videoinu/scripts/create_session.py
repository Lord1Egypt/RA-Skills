#!/usr/bin/env python3
"""
Create an agent session for a graph, or list existing sessions.

Usage:
    python3 create_session.py GRAPH_ID
    python3 create_session.py GRAPH_ID --list

Output (JSON):
    {
      "project_id": "...",
      "session_id": "...",
      "graph_url": "..."
    }
"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from _common import require_access_key, api_get, api_post, build_graph_url, AGENT_API_PREFIX


def get_or_create_project(graph_id: str) -> dict:
    """Get existing agent project for a graph, or create one."""
    try:
        project = api_get(f"/projects/by-graph/{graph_id}", base=AGENT_API_PREFIX)
        if project:
            return project
    except SystemExit:
        pass  # Not found, create new

    project = api_post("/projects/", body={
        "name": f"canvas:{graph_id}",
        "graph_id": graph_id,
    }, base=AGENT_API_PREFIX)
    return project


def list_sessions(project_id: str) -> list:
    sessions = api_get(f"/sessions/by-project/{project_id}", base=AGENT_API_PREFIX)
    return sessions if isinstance(sessions, list) else []


def create_session(project_id: str) -> dict:
    return api_post("/sessions/", body={
        "project_id": project_id,
    }, base=AGENT_API_PREFIX)


def main():
    parser = argparse.ArgumentParser(description="Create or list agent sessions")
    parser.add_argument("graph_id", help="Graph ID")
    parser.add_argument("--list", action="store_true", help="List existing sessions instead of creating")
    args = parser.parse_args()

    require_access_key()

    project = get_or_create_project(args.graph_id)
    project_id = project.get("id", "")

    if args.list:
        sessions = list_sessions(project_id)
        result = {
            "project_id": project_id,
            "graph_url": build_graph_url(args.graph_id),
            "sessions": [
                {
                    "session_id": s.get("session_id", s.get("id", "")),
                    "last_updated": s.get("last_updated", ""),
                }
                for s in sessions
            ],
        }
        print(json.dumps(result, indent=2))
        return

    session = create_session(project_id)
    session_id = session.get("session_id", session.get("id", ""))

    result = {
        "project_id": project_id,
        "session_id": session_id,
        "graph_url": build_graph_url(args.graph_id),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
