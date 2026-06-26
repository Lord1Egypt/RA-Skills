#!/usr/bin/env python3
"""
OpenClaw Agent Creator - Helper Script
Automates directory creation, config update, and file scaffolding for new OpenClaw agents.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

OPENCLAW_DIR = Path.home() / ".openclaw"
OPENCLAW_JSON = OPENCLAW_DIR / "openclaw.json"
MAIN_AGENT_DIR = OPENCLAW_DIR / "agents" / "main" / "agent"


def load_config():
    if not OPENCLAW_JSON.exists():
        print(f"Error: {OPENCLAW_JSON} not found")
        sys.exit(1)
    with open(OPENCLAW_JSON, "r") as f:
        return json.load(f)


def save_config(config):
    # Back up before writing
    backup = OPENCLAW_JSON.with_suffix(".json.bak")
    shutil.copy2(OPENCLAW_JSON, backup)
    print(f"Backed up config to {backup}")

    with open(OPENCLAW_JSON, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    print(f"Saved config to {OPENCLAW_JSON}")


def write_file(path: Path, content: str):
    path.write_text(content, encoding="utf-8")
    print(f"  Created {path.name}")


def create_workspace(agent_id: str):
    """Create workspace directory with all required files."""
    workspace_dir = OPENCLAW_DIR / f"workspace-{agent_id}"
    workspace_dir.mkdir(parents=True, exist_ok=True)
    (workspace_dir / "memory").mkdir(exist_ok=True)
    (workspace_dir / "skills").mkdir(exist_ok=True)

    # AGENTS.md
    write_file(
        workspace_dir / "AGENTS.md",
        """# AGENTS.md - Your Workspace

If `BOOTSTRAP.md` exists, that's your birth certificate. Follow it, figure out who you are, then delete it.

## Every Session

Before doing anything else:

1. Read `SOUL.md` — this is who you are
2. Read `USER.md` — this is who you're helping
3. Read `memory/YYYY-MM-DD.md` (today + yesterday) for recent context
4. **If in MAIN SESSION** (direct chat with your human): Also read `MEMORY.md`

## Memory

You wake up fresh each session. These files are your continuity:

- **Daily notes:** `memory/YYYY-MM-DD.md` — raw logs of what happened
- **Long-term:** `MEMORY.md` — your curated memories

## Safety

- Don't exfiltrate private data
- When in doubt, ask.
""",
    )

    # HEARTBEAT.md
    write_file(
        workspace_dir / "HEARTBEAT.md",
        "# HEARTBEAT.md\n\n# Keep this file empty to skip heartbeat API calls.\n",
    )

    # TOOLS.md
    write_file(
        workspace_dir / "TOOLS.md",
        "# TOOLS.md - Local Notes\n\nNotes specific to this agent's setup.\n",
    )

    # USER.md (empty template)
    write_file(
        workspace_dir / "USER.md",
        "# USER.md\n\nInformation about the user this agent is helping.\n",
    )

    # SOUL.md placeholder — user should customize this
    write_file(
        workspace_dir / "SOUL.md",
        f"# SOUL.md - {agent_id}\n\n_Define this agent's persona here._\n",
    )

    print(f"Created workspace: {workspace_dir}")
    return workspace_dir


def create_agent_dir(agent_id: str):
    """Create agent runtime directory and copy configs from main."""
    agent_dir = OPENCLAW_DIR / "agents" / agent_id / "agent"
    sessions_dir = OPENCLAW_DIR / "agents" / agent_id / "sessions"
    agent_dir.mkdir(parents=True, exist_ok=True)
    sessions_dir.mkdir(parents=True, exist_ok=True)

    # Copy config files from main agent
    for filename in ("models.json", "auth-profiles.json"):
        src = MAIN_AGENT_DIR / filename
        dst = agent_dir / filename
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  Copied {filename} from main agent")
        else:
            print(f"  Warning: {src} not found — you need to provide {filename} manually")

    print(f"Created agent dir: {agent_dir}")
    return agent_dir


def update_config(agent_id: str, agent_name: str, group_id: str = None, user_id: str = None):
    """Add agent entry and optional bindings to openclaw.json."""
    config = load_config()

    # Check for duplicates
    for agent in config.get("agents", {}).get("list", []):
        if agent["id"] == agent_id:
            print(f"Error: Agent '{agent_id}' already exists in config")
            return False

    # Add agent to list
    new_agent = {
        "id": agent_id,
        "name": agent_name,
        "workspace": str(OPENCLAW_DIR / f"workspace-{agent_id}"),
        "agentDir": str(OPENCLAW_DIR / "agents" / agent_id / "agent"),
    }

    if "agents" not in config:
        config["agents"] = {"list": []}
    if "list" not in config["agents"]:
        config["agents"]["list"] = []

    config["agents"]["list"].append(new_agent)
    print(f"Added agent: {agent_id}")

    # Add bindings
    if "bindings" not in config:
        config["bindings"] = []

    if group_id:
        binding = {
            "agentId": agent_id,
            "match": {
                "channel": "feishu",
                "peer": {"kind": "group", "id": group_id},
            },
        }
        config["bindings"].append(binding)
        print(f"Added group binding: {group_id}")

    if user_id:
        binding = {
            "agentId": agent_id,
            "match": {
                "channel": "feishu",
                "peer": {"kind": "direct", "id": user_id},
            },
        }
        config["bindings"].append(binding)
        print(f"Added direct binding: {user_id}")

    save_config(config)
    return True


def restart_gateway():
    """Restart the OpenClaw gateway."""
    print("\nRestarting gateway...")
    result = subprocess.run(["openclaw", "gateway", "restart"], capture_output=True, text=True)
    if result.returncode == 0:
        print("Gateway restarted successfully")
    else:
        print(f"Warning: Gateway restart failed (exit code {result.returncode})")
        if result.stderr:
            print(f"  stderr: {result.stderr.strip()}")
        print("  You may need to restart it manually: openclaw gateway restart")


def create_agent(agent_id: str, agent_name: str, group_id: str = None, user_id: str = None):
    """Full agent creation flow."""
    print(f"\n{'='*50}")
    print(f"Creating agent: {agent_id} ({agent_name})")
    print(f"{'='*50}\n")

    # 1. Create workspace with all files
    print("[1/4] Creating workspace...")
    create_workspace(agent_id)

    # 2. Create agent runtime dir + copy configs
    print("\n[2/4] Creating agent directory...")
    create_agent_dir(agent_id)

    # 3. Update openclaw.json
    print("\n[3/4] Updating config...")
    if not update_config(agent_id, agent_name, group_id, user_id):
        return False

    # 4. Restart gateway
    print("\n[4/4] Restarting gateway...")
    restart_gateway()

    print(f"\n{'='*50}")
    print(f"Agent '{agent_id}' created successfully!")
    print(f"  Workspace: ~/.openclaw/workspace-{agent_id}/")
    print(f"  Agent dir: ~/.openclaw/agents/{agent_id}/")
    print(f"\nNext steps:")
    print(f"  1. Edit ~/.openclaw/workspace-{agent_id}/SOUL.md to define the persona")
    print(f"  2. Add skills to ~/.openclaw/workspace-{agent_id}/skills/ if needed")
    if group_id:
        print(f"  3. Make sure the bot is added to the group chat")
    print(f"{'='*50}")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 agent_creator.py <agent_id> <agent_name> [--group oc_xxx] [--user ou_xxx]")
        print()
        print("Examples:")
        print("  python3 agent_creator.py brainstorm 'Brainstorm Buddy'")
        print("  python3 agent_creator.py reviewer 'Code Reviewer' --group oc_abc123")
        print("  python3 agent_creator.py assistant 'My Assistant' --user ou_xyz789")
        print("  python3 agent_creator.py helper 'Team Helper' --group oc_abc --user ou_xyz")
        sys.exit(1)

    agent_id = sys.argv[1]
    agent_name = sys.argv[2]
    group_id = None
    user_id = None

    # Parse optional flags
    args = sys.argv[3:]
    i = 0
    while i < len(args):
        if args[i] == "--group" and i + 1 < len(args):
            group_id = args[i + 1]
            i += 2
        elif args[i] == "--user" and i + 1 < len(args):
            user_id = args[i + 1]
            i += 2
        else:
            print(f"Unknown argument: {args[i]}")
            sys.exit(1)

    create_agent(agent_id, agent_name, group_id, user_id)
