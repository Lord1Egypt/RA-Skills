#!/usr/bin/env python3
"""Generate sanitized starter templates for a local workspace retrieval setup.

This script is intentionally conservative:
- local file writes only
- no network calls
- no scanning of existing user data
- no automatic indexing
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def corpora_template(workspace_root: str) -> dict:
    return {
        "version": 1,
        "global": {
            "workspaceRoot": workspace_root,
            "defaultDbPath": f"{workspace_root}/retrieval/indexes/workspace_retrieval.sqlite",
            "includeExtensions": [".md", ".txt"],
            "excludeGlobs": [
                "memory/**",
                "my_note/**",
                "my_profile/**",
                ".openclaw/**",
                ".clawhub/**",
                ".git/**",
                "out/**",
                "tmp/**",
                "node_modules/**",
                "retrieval/indexes/**",
            ],
            "chunking": {
                "maxChars": 2800,
                "softBreakChars": 1800,
                "overlapChars": 300,
            },
        },
        "corpora": [
            {
                "id": "workspace-core",
                "description": "Core workspace docs and shared rules.",
                "include": [
                    "AGENTS.md",
                    "USER.md",
                    "TOOLS.md",
                    "SOUL.md",
                    "skills/**",
                    "agents/**",
                ],
            },
            {
                "id": "workspace-specialist",
                "description": "Specialist domain docs.",
                "include": ["specialist/**"],
            },
        ],
    }


def agent_corpora_template() -> dict:
    return {
        "version": 1,
        "defaultPolicy": {"mode": "deny-by-default", "allowedCorpora": []},
        "agents": {
            "main": {"allowedCorpora": ["workspace-core"]},
            "specialist-agent": {"allowedCorpora": ["workspace-specialist"]},
        },
    }


def agent_memory_template() -> dict:
    return {
        "version": 1,
        "agents": {
            "main": {
                "memoryMode": "broad-coordination",
                "memoryRoots": ["MEMORY.md", "memory/"],
                "notes": "Main coordinator can use broad continuity.",
            },
            "specialist-agent": {
                "memoryMode": "domain-scoped",
                "memoryRoots": ["specialist/data/", "specialist-guide.md"],
                "notes": "Specialist stays inside domain memory by default.",
            },
        },
    }


def backend_template(workspace_root: str) -> dict:
    return {
        "version": 1,
        "embeddingProvider": "ollama",
        "embeddingModel": "nomic-embed-text",
        "embeddingEndpoint": "http://127.0.0.1:11434/api/embeddings",
        "sqlite": {
            "dbPath": f"{workspace_root}/retrieval/indexes/workspace_retrieval.sqlite",
            "requireFts5": True,
        },
    }


def write_json(path: Path, payload: dict, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"Refusing to overwrite existing file without --force: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Bootstrap sanitized local retrieval templates.")
    parser.add_argument("--dest", required=True, help="Destination directory for generated retrieval config")
    parser.add_argument("--workspace-root", default="/ABSOLUTE/PATH/TO/WORKSPACE", help="Workspace root placeholder or absolute path")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    dest = Path(args.dest).expanduser().resolve()
    config_dir = dest / "config"

    write_json(config_dir / "corpora.json", corpora_template(args.workspace_root), args.force)
    write_json(config_dir / "agent_corpora.json", agent_corpora_template(), args.force)
    write_json(config_dir / "agent_memory.json", agent_memory_template(), args.force)
    write_json(config_dir / "backend.json", backend_template(args.workspace_root), args.force)

    print(json.dumps({
        "written": [
            str(config_dir / "corpora.json"),
            str(config_dir / "agent_corpora.json"),
            str(config_dir / "agent_memory.json"),
            str(config_dir / "backend.json"),
        ],
        "workspaceRoot": args.workspace_root,
        "note": "Templates generated. Review and customize before indexing.",
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
