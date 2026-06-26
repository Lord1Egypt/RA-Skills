#!/usr/bin/env python3
"""
GH Script Generator & Deployer — Creates Grasshopper definitions via RhinoClaw
and optionally deploys them to the Rhino Compute Platform.

Usage:
    # Build a GH definition with Python code
    python3 ghscript.py build --name "MyBox" --script code.py --inputs inputs.json --output /path/to/output.gh

    # Build and deploy to Rhino Compute Platform
    python3 ghscript.py deploy --name "MyBox" --script code.py --inputs inputs.json

    # Execute Python code directly in Rhino (quick test, no GH definition)
    python3 ghscript.py exec --code "import Rhino; print(Rhino.RhinoApp.Version)"

    # Execute from file
    python3 ghscript.py exec --file script.py
"""

import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
from pathlib import Path

from rhino_client import RhinoClient

logger = logging.getLogger("rhinoclaw.ghscript")

# Rhino Compute Platform definitions directory
COMPUTE_PLATFORM_DEFS = Path.home() / "projects" / "rhino-compute-platform" / "definitions"
META_GEN_TOOL = Path.home() / "projects" / "rhino-compute-platform" / "tools" / "meta_gen.py"


def build_definition(client: RhinoClient, name: str, script: str, inputs: list, 
                     outputs: list = None, file_path: str = None, 
                     description: str = None) -> dict:
    """Build a .gh definition via RhinoClaw plugin."""
    if file_path is None:
        file_path = f"C:/temp/gh_definitions/{name}.gh"

    params = {
        "file_path": file_path,
        "script": script,
        "inputs": inputs,
        "name": name,
    }
    if outputs:
        params["outputs"] = outputs
    if description:
        params["description"] = description

    result = client.send_command("build_gh_definition", params)
    return result


def deploy_to_compute_platform(gh_file_path_windows: str, name: str) -> dict:
    """
    Deploy a .gh definition to the Rhino Compute Platform.
    
    1. Copy .gh from Windows path to definitions/
    2. Run meta_gen.py to auto-generate .meta.json
    3. Return the deployment info
    """
    # Convert Windows path to WSL path
    if gh_file_path_windows.startswith("C:"):
        wsl_path = gh_file_path_windows.replace("C:", "/mnt/c").replace("\\", "/")
    elif gh_file_path_windows.startswith("/"):
        wsl_path = gh_file_path_windows
    else:
        wsl_path = gh_file_path_windows

    dest_dir = COMPUTE_PLATFORM_DEFS
    dest_file = dest_dir / f"{name}.gh"
    
    if not dest_dir.exists():
        raise FileNotFoundError(f"Compute Platform definitions dir not found: {dest_dir}")

    # Copy the file
    if os.path.exists(wsl_path):
        shutil.copy2(wsl_path, dest_file)
    else:
        # Try UNC path for WSL access to Windows files
        unc_path = wsl_path
        if not os.path.exists(unc_path):
            raise FileNotFoundError(
                f"Cannot find .gh file at {wsl_path} or {unc_path}. "
                f"Windows path was: {gh_file_path_windows}"
            )
        shutil.copy2(unc_path, dest_file)

    # Run meta_gen.py
    meta_result = None
    if META_GEN_TOOL.exists():
        try:
            result = subprocess.run(
                [sys.executable, str(META_GEN_TOOL), str(dest_file), "--force"],
                capture_output=True, text=True, timeout=30
            )
            meta_result = result.stdout.strip()
            if result.returncode != 0:
                meta_result = f"meta_gen warning: {result.stderr.strip()}"
        except Exception as e:
            meta_result = f"meta_gen error: {e}"

    meta_path = dest_file.with_suffix(".meta.json")
    
    return {
        "status": "deployed",
        "definition": str(dest_file),
        "meta_json": str(meta_path) if meta_path.exists() else None,
        "meta_gen_output": meta_result,
        "solve_url": f"POST /solve {{ definition: '{name}.gh', inputs: {{...}} }}",
    }


def execute_code(client: RhinoClient, code: str) -> dict:
    """Execute Python code directly in Rhino."""
    result = client.send_command("execute_rhinoscript_python_code", {"code": code})
    return result


def write_meta_json(name: str, inputs: list, outputs: list = None, description: str = None):
    """Write a .meta.json file directly (for when meta_gen can't parse the GH binary)."""
    params = {}
    for inp in inputs:
        param_name = inp["name"]
        param_type = inp.get("type", "number")
        
        meta = {"type": param_type}
        if "default" in inp:
            meta["default"] = inp["default"]
        if "min" in inp:
            meta["min"] = inp["min"]
        if "max" in inp:
            meta["max"] = inp["max"]
        if param_type in ("number", "float", "double"):
            step = inp.get("step")
            if step is None and "max" in inp and "min" in inp:
                step = round((inp["max"] - inp["min"]) / 100, 2)
            if step:
                meta["step"] = step
        
        params[param_name] = meta

    meta_json = {
        "$schema": "meta-json-schema",
        "name": name,
        "description": description or f"Generated by RhinoClaw: {name}",
        "author": "RhinoClaw",
        "version": "1.0.0",
        "params": params
    }

    meta_path = COMPUTE_PLATFORM_DEFS / f"{name}.meta.json"
    with open(meta_path, "w") as f:
        json.dump(meta_json, f, indent=2)
    
    return str(meta_path)


def main():
    parser = argparse.ArgumentParser(description="GH Script Generator & Deployer")
    subparsers = parser.add_subparsers(dest="action", required=True)

    # Build action
    build_parser = subparsers.add_parser("build", help="Build a .gh definition")
    build_parser.add_argument("--name", required=True, help="Definition name")
    build_parser.add_argument("--script", required=True, help="Python script file")
    build_parser.add_argument("--inputs", required=True, help="JSON file with input specs")
    build_parser.add_argument("--outputs", help="Comma-separated output names")
    build_parser.add_argument("--output", help="Output .gh file path (Windows)")
    build_parser.add_argument("--description", help="Description")

    # Deploy action
    deploy_parser = subparsers.add_parser("deploy", help="Build + deploy to Compute Platform")
    deploy_parser.add_argument("--name", required=True, help="Definition name")
    deploy_parser.add_argument("--script", required=True, help="Python script file")
    deploy_parser.add_argument("--inputs", required=True, help="JSON file with input specs")
    deploy_parser.add_argument("--outputs", help="Comma-separated output names")
    deploy_parser.add_argument("--description", help="Description")

    # Exec action
    exec_parser = subparsers.add_parser("exec", help="Execute Python code in Rhino")
    exec_parser.add_argument("--code", help="Python code string")
    exec_parser.add_argument("--file", help="Python script file to execute")

    # Common args
    for p in [build_parser, deploy_parser, exec_parser]:
        p.add_argument("--host", help="RhinoClaw host")
        p.add_argument("--port", type=int, help="RhinoClaw port")

    args = parser.parse_args()
    
    # Create client
    client = RhinoClient(
        host=args.host if hasattr(args, 'host') and args.host else None,
        port=args.port if hasattr(args, 'port') and args.port else None,
    )
    client.connect()

    if args.action == "exec":
        if args.code:
            code = args.code
        elif args.file:
            with open(args.file) as f:
                code = f.read()
        else:
            print("Error: --code or --file required")
            sys.exit(1)
        
        result = execute_code(client, code)
        print(json.dumps(result, indent=2))
        return

    # Build or deploy
    with open(args.script) as f:
        script = f.read()
    
    with open(args.inputs) as f:
        inputs = json.load(f)
    
    outputs = args.outputs.split(",") if args.outputs else None

    if args.action == "build":
        result = build_definition(
            client, args.name, script, inputs,
            outputs=outputs,
            file_path=args.output,
            description=getattr(args, 'description', None),
        )
        print(json.dumps(result, indent=2))

    elif args.action == "deploy":
        # Build on Windows via RhinoClaw
        win_path = f"C:/temp/gh_definitions/{args.name}.gh"
        build_result = build_definition(
            client, args.name, script, inputs,
            outputs=outputs,
            file_path=win_path,
            description=getattr(args, 'description', None),
        )
        print("Build result:", json.dumps(build_result, indent=2))

        # Write meta.json directly (more reliable than parsing binary .gh)
        meta_path = write_meta_json(
            args.name, inputs, outputs,
            description=getattr(args, 'description', None)
        )
        print(f"Meta JSON written: {meta_path}")

        # Deploy
        deploy_result = deploy_to_compute_platform(win_path, args.name)
        print("Deploy result:", json.dumps(deploy_result, indent=2))


if __name__ == "__main__":
    main()
