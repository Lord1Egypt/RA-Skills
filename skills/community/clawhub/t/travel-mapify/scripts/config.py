#!/usr/bin/env python3
"""
Configuration module for flyai-travelmapify skill.
Dynamically determines paths and settings based on environment.
"""

import os
import sys
import subprocess
from pathlib import Path

def get_workspace_dir():
    """
    Determine the OpenClaw workspace directory dynamically.
    Tries multiple methods to find the correct workspace.
    """
    # Method 1: Check if we're running within OpenClaw context
    # Look for common OpenClaw workspace indicators
    possible_paths = []
    
    # Current script directory (should be in skills/flyai-travelmapify/scripts/)
    script_dir = Path(__file__).parent
    skill_dir = script_dir.parent
    workspace_candidate = skill_dir.parent.parent
    
    # Check if this looks like a valid OpenClaw workspace
    if (workspace_candidate / "AGENTS.md").exists() or (workspace_candidate / "SOUL.md").exists():
        return str(workspace_candidate)
    
    # Method 2: Check OPENCLAW_WORKSPACE environment variable
    env_workspace = os.environ.get('OPENCLAW_WORKSPACE')
    if env_workspace and Path(env_workspace).exists():
        return env_workspace
    
    # Method 3: Check typical OpenClaw workspace locations
    home = Path.home()
    typical_workspaces = [
        home / ".openclaw" / "workspace",
        home / "openclaw" / "workspace",
        home / "Documents" / "openclaw" / "workspace"
    ]
    
    for candidate in typical_workspaces:
        if candidate.exists() and (candidate / "AGENTS.md").exists():
            return str(candidate)
    
    # Method 4: Use current working directory as fallback
    return os.getcwd()

def find_flyai_executable():
    """
    Find the flyai executable in the system PATH or common locations.
    """
    # First, try to find it in PATH
    try:
        result = subprocess.run(['which', 'flyai'], capture_output=True, text=True)
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except FileNotFoundError:
        pass
    
    # Try npm global bin directory
    try:
        result = subprocess.run(['npm', 'bin', '-g'], capture_output=True, text=True)
        if result.returncode == 0:
            npm_bin = result.stdout.strip()
            flyai_path = Path(npm_bin) / "flyai"
            if flyai_path.exists():
                return str(flyai_path)
    except FileNotFoundError:
        pass
    
    # Try common Node.js installation paths
    home = Path.home()
    common_paths = [
        home / ".nvm" / "versions" / "node",
        home / ".local" / "share" / "npm" / "bin",
        "/usr/local/bin", "/opt/homebrew/bin"
    ]
    
    for base_path in common_paths:
        if base_path.exists():
            for flyai_path in base_path.rglob("flyai"):
                if flyai_path.is_file():
                    return str(flyai_path)
    
    # If not found, return None - caller should handle this
    return None

def get_skill_dir():
    """Get the skill directory path"""
    return str(Path(__file__).parent.parent)

# Configuration constants
WORKSPACE_DIR = get_workspace_dir()
SKILL_DIR = get_skill_dir()
FLYAI_EXECUTABLE = find_flyai_executable()

# Default ports
DEFAULT_HTTP_PORT = 9000
DEFAULT_HOTEL_PORT = 8770
DEFAULT_PROXY_URL = "http://localhost:8769/api/search"

if __name__ == "__main__":
    print(f"Workspace directory: {WORKSPACE_DIR}")
    print(f"Skill directory: {SKILL_DIR}")
    print(f"FlyAI executable: {FLYAI_EXECUTABLE}")