#!/usr/bin/env python3
"""
Strict safety wrapper for ROS 2 Control Execution commands.
Loads configuration dynamically and executes safely using subprocess.
"""

import sys
import os
import json
import subprocess
import argparse
from pathlib import Path

ALLOWED_SUBCMDS = {
    "load_controller",
    "reload_controller_libraries",
    "set_controller_state",
    "set_hardware_component_state",
    "switch_controllers",
    "unload_controller",
    "cleanup_controller"
}

def main():
    parser = argparse.ArgumentParser(description="Strict ROS 2 Control Execution wrapper.")
    parser.add_argument("subcommand", choices=list(ALLOWED_SUBCMDS))
    parser.add_argument("--profile", help="Load parameters from ~/.openclaw/workspace/ros_profiles/<profile>.yaml")
    parser.add_argument("--params-file", help="Load parameters from a specific YAML file path")

    args, extra = parser.parse_known_args()

    script_dir = Path(__file__).resolve().parent
    config_file = script_dir.parent / "config" / "config.json"

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

    # Build the environment
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

    cmd_array = ["ros2", "control", args.subcommand]
    
    ros_args = []
    if args.profile:
        profile_path = os.path.expanduser(f"~/.openclaw/workspace/ros_profiles/{args.profile}.yaml")
        if not os.path.isfile(profile_path):
            print(f"Error: Profile file not found at {profile_path}", file=sys.stderr)
            sys.exit(1)
        ros_args.extend(["--params-file", profile_path])
    elif args.params_file:
        if not os.path.isfile(args.params_file):
            print(f"Error: Params file not found at {args.params_file}", file=sys.stderr)
            sys.exit(1)
        ros_args.extend(["--params-file", args.params_file])

    if extra and extra[0] == '--':
        extra = extra[1:]
        
    if ros_args:
        if "--ros-args" not in extra:
            cmd_array.extend(["--ros-args"] + ros_args)
        else:
            idx = extra.index("--ros-args")
            extra = extra[:idx+1] + ros_args + extra[idx+1:]
            
    cmd_array.extend(extra)

    # Execute safely without shell=True
    sys.exit(subprocess.call(cmd_array, env=ros_env))

if __name__ == "__main__":
    main()
