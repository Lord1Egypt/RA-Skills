#!/usr/bin/env python3
"""
Dokploy API MCP Skill — Interactive Setup

Configures:
1. MCP server in ~/.claude/mcp.json (auto-installs @sattva/dokploy-mcp)
2. Validates connection to Dokploy instance
3. Lists available projects/apps for verification

Usage:
  python3 ~/.claude/skills/dokploy-api-mcp/scripts/setup.py
  python3 ~/.claude/skills/dokploy-api-mcp/scripts/setup.py --url https://dokploy.example.com --key YOUR_KEY
"""

import json
import os
import sys
import platform
import urllib.request
import urllib.error
import ssl

CLAUDE_DIR = os.path.expanduser("~/.claude")
MCP_JSON = os.path.join(CLAUDE_DIR, "mcp.json")
LOCAL_MCP_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "MCP", "dokploy-mcp", "dist", "index.js"))


def get_input(prompt, default=None):
    """Get user input with optional default."""
    if default:
        prompt = f"{prompt} [{default}]: "
    else:
        prompt = f"{prompt}: "
    value = input(prompt).strip()
    return value if value else default


def parse_args():
    """Parse --url and --key from command line."""
    url = None
    key = None
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--url" and i + 1 < len(args):
            url = args[i + 1]
            i += 2
        elif args[i] == "--key" and i + 1 < len(args):
            key = args[i + 1]
            i += 2
        else:
            i += 1
    return url, key


def validate_connection(url, key):
    """Test connection to Dokploy by calling settings.health."""
    api_url = url.rstrip("/")
    if not api_url.endswith("/api"):
        api_url += "/api"

    health_url = f"{api_url}/settings.health"
    req = urllib.request.Request(health_url, headers={"x-api-key": key})

    # Allow self-signed certs
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = json.loads(resp.read())
            return True, data
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}: {e.reason}"
    except Exception as e:
        return False, str(e)


def list_projects(url, key):
    """Fetch project list to verify full API access."""
    api_url = url.rstrip("/")
    if not api_url.endswith("/api"):
        api_url += "/api"

    projects_url = f"{api_url}/trpc/project.all"
    req = urllib.request.Request(projects_url, headers={"x-api-key": key})

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            data = json.loads(resp.read())
            projects = data.get("result", {}).get("data", {}).get("json", [])
            return projects
    except Exception:
        return []


def read_mcp_json():
    """Read existing mcp.json or return empty structure."""
    if os.path.exists(MCP_JSON):
        with open(MCP_JSON, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"mcpServers": {}}
    return {"mcpServers": {}}


def write_mcp_json(data):
    """Write mcp.json with proper formatting."""
    os.makedirs(CLAUDE_DIR, exist_ok=True)
    with open(MCP_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def configure_mcp(url, key):
    """Add or update dokploy MCP server in mcp.json."""
    api_url = url.rstrip("/")
    if not api_url.endswith("/api"):
        api_url += "/api"

    mcp = read_mcp_json()

    # Prefer local development build if available
    if os.path.exists(LOCAL_MCP_PATH):
        server_config = {
            "command": "node",
            "args": [LOCAL_MCP_PATH.replace("\\", "/")],
            "env": {
                "DOKPLOY_URL": api_url,
                "DOKPLOY_API_KEY": key
            }
        }
    elif platform.system() == "Windows":
        server_config = {
            "command": "cmd",
            "args": ["/c", "npx", "-y", "@sattva/dokploy-mcp"],
            "env": {
                "DOKPLOY_URL": api_url,
                "DOKPLOY_API_KEY": key
            }
        }
    else:
        server_config = {
            "command": "npx",
            "args": ["-y", "@sattva/dokploy-mcp"],
            "env": {
                "DOKPLOY_URL": api_url,
                "DOKPLOY_API_KEY": key
            }
        }

    existing = "dokploy" in mcp.get("mcpServers", {})
    mcp.setdefault("mcpServers", {})["dokploy"] = server_config
    write_mcp_json(mcp)

    return existing


def main():
    print("=" * 50)
    print("  Dokploy API MCP Skill — Setup")
    print("=" * 50)
    print()

    # Parse CLI args or ask interactively
    arg_url, arg_key = parse_args()

    # Step 1: Get Dokploy URL
    if arg_url:
        dokploy_url = arg_url
    else:
        print("Step 1/3: Dokploy URL")
        print("  Enter your Dokploy dashboard URL.")
        print("  Example: https://dokploy.example.com")
        print()
        dokploy_url = get_input("  Dokploy URL")

    if not dokploy_url:
        print("\n  ERROR: URL is required.")
        sys.exit(1)

    # Normalize URL
    dokploy_url = dokploy_url.rstrip("/")
    if dokploy_url.endswith("/api"):
        dokploy_url = dokploy_url[:-4]

    print()

    # Step 2: Get API key
    if arg_key:
        api_key = arg_key
    else:
        print("Step 2/3: API Key")
        print("  Generate at: Dashboard -> Settings -> Profile -> API/CLI -> Generate")
        print()
        api_key = get_input("  API Key")

    if not api_key:
        print("\n  ERROR: API key is required.")
        sys.exit(1)

    print()

    # Step 3: Validate connection
    print("Step 3/3: Validating connection...")
    ok, result = validate_connection(dokploy_url, api_key)

    if not ok:
        print(f"\n  ERROR: Cannot connect to Dokploy: {result}")
        print(f"  URL tried: {dokploy_url}/api/settings.health")
        print()
        proceed = get_input("  Save config anyway? (y/N)", "N")
        if proceed.lower() != "y":
            sys.exit(1)
    else:
        print(f"  OK — Dokploy is reachable")

        # Show projects
        projects = list_projects(dokploy_url, api_key)
        if projects:
            print(f"\n  Found {len(projects)} project(s):")
            for p in projects[:5]:
                name = p.get("name", "?")
                pid = p.get("projectId", "?")
                print(f"    - {name} (id: {pid[:20]}...)")
            if len(projects) > 5:
                print(f"    ... and {len(projects) - 5} more")

    print()

    # Configure MCP
    was_existing = configure_mcp(dokploy_url, api_key)
    action = "Updated" if was_existing else "Added"
    print(f"  {action} 'dokploy' MCP server in {MCP_JSON}")

    print()
    print("=" * 50)
    print("  Setup complete!")
    print()
    if os.path.exists(LOCAL_MCP_PATH):
        print(f"  MCP server: local ({LOCAL_MCP_PATH})")
    else:
        print("  MCP server: @sattva/dokploy-mcp (449 tools)")
    print(f"  Dokploy:    {dokploy_url}")
    print(f"  Config:     {MCP_JSON}")
    print()
    print("  Restart Claude Code to activate MCP server.")
    print("  Then use /dokploy-api-mcp to deploy your apps.")
    print("=" * 50)


if __name__ == "__main__":
    main()
