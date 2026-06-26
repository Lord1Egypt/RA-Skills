#!/usr/bin/env python3
"""
Strict safety wrapper for ROS 2 introspection commands.
Loads configuration dynamically from config/ and executes safely using subprocess.
"""

import sys
import os
import json
import subprocess
from pathlib import Path

# Allowlist of safe, read-only introspection categories and their subcommands
ALLOWED_COMMANDS = {
    "topic": {"list", "info", "hz", "bw", "echo"},
    "interface": {"show"},
    "node": {"list", "info"},
    "service": {"list", "type", "find"},
    "action": {"list", "info"},
    "param": {"list", "get", "dump"}
}

def main():
    if len(sys.argv) < 2:
        print("Error: No ROS 2 command provided.", file=sys.stderr)
        sys.exit(1)

    category = sys.argv[1]

    # Special case for rqt_graph
    if category == "rqt_graph":
        sys.exit(subprocess.call(["rqt_graph"]))

    if len(sys.argv) < 3:
        # Some commands might just be e.g. "topic list", but if they passed only "topic", it will fail validation below
        subcmd = None
    else:
        subcmd = sys.argv[2]

    # Validate category and subcommand
    valid = False
    if category in ALLOWED_COMMANDS:
        if subcmd in ALLOWED_COMMANDS[category]:
            valid = True

    if not valid:
        print(f"SECURITY BLOCK: Command 'ros2 {category} {subcmd}' is not permitted.", file=sys.stderr)
        print("This wrapper only allows read-only introspection commands.", file=sys.stderr)
        sys.exit(1)

    script_dir = Path(__file__).resolve().parent
    config_file = script_dir.parent / "config" / "config.json"

    # Load configurations
    if not config_file.is_file():
        print(f"Error: {config_file} not found. Run scripts/setup.sh.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(config_file, "r") as f:
            config = json.load(f)
    except json.JSONDecodeError:
        print("Error: Invalid config.json", file=sys.stderr)
        sys.exit(1)

    ros_setup_path = config.get("ros_setup_path")

    if not ros_setup_path or not os.path.isfile(ros_setup_path):
        print("Error: ROS_SETUP_PATH invalid. Run setup.sh.", file=sys.stderr)
        sys.exit(1)

    # Build the environment by sourcing the bash file
    env_command = f"source {ros_setup_path} && env"
    try:
        env_proc = subprocess.run(['bash', '-c', env_command], stdout=subprocess.PIPE, text=True, check=True)
        ros_env = {}
        for line in env_proc.stdout.splitlines():
            if '=' in line:
                key, val = line.split('=', 1)
                ros_env[key] = val
    except subprocess.CalledProcessError:
        print("Error: Failed to source ROS setup file.", file=sys.stderr)
        sys.exit(1)

    # Build the command array safely
    cmd_array = ["ros2"] + sys.argv[1:]

    # Execute safely without shell=True
    sys.exit(subprocess.call(cmd_array, env=ros_env))

if __name__ == "__main__":
    main()
