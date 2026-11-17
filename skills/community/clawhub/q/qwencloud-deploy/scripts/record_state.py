#!/usr/bin/env python3
"""Write .qwencloud-deploy state file. See reference/deploy/13_record_state.md"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path


# State file and password sidecar produced by the deploy scripts, always ignored
# to avoid committing state and signed URLs.
DEPLOY_LEAK_PATHS = (
    ".qwencloud-deploy",
    ".qwencloud-deploy.local",
)

# Host AI-agent workspaces persist approved commands and history, which can
# capture AK/SK, passwords, or signed URLs. Add them to .gitignore only when the
# directory actually exists in the current directory.
AGENT_DIRS = (
    ".claude", ".qoder", ".cursor", ".windsurf", ".codex", ".gemini",
    ".continue", ".roo", ".cline", ".trae", ".aider",
)


def _ensure_gitignore(root: Path, *entries: str) -> None:
    """Ensure .gitignore contains the given entries (idempotent)."""
    gi = root / ".gitignore"
    existing = gi.read_text(encoding="utf-8") if gi.exists() else ""
    lines = existing.splitlines()
    changed = False
    for entry in entries:
        if entry not in lines:
            lines.append(entry)
            changed = True
    if changed:
        content = "\n".join(lines)
        if not content.endswith("\n"):
            content += "\n"
        gi.write_text(content, encoding="utf-8")


def _ignore_agent_dirs(root: Path) -> None:
    """Add host AI-agent workspaces that actually exist in the directory to .gitignore."""
    found = [name + "/" for name in AGENT_DIRS if (root / name).is_dir()]
    if found:
        _ensure_gitignore(root, *found)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stack-id", required=True,
                    help="ROS Stack ID")
    ap.add_argument("--stack-name", required=True,
                    help="ROS Stack Name")
    ap.add_argument("--region", required=True)
    ap.add_argument("--topology", default="single", choices=["single"])
    ap.add_argument("--app-type", required=True)
    ap.add_argument("--app-name", default="qwencloud-app",
                    help="Service name (systemd unit / container name / log file name); observe/operate use it to locate the service")
    ap.add_argument("--runtime", default=None,
                    help="Runtime type (none/java/node/python), used for hot update dependency installation")
    ap.add_argument("--app-mode", default=None, choices=["docker-image", "docker-compose"],
                    help="Docker deployment mode (docker-image/docker-compose); hot update uses it to pick docker load vs compose up")
    ap.add_argument("--app-image-name", default=None,
                    help="Image name:tag after docker load in docker-image mode; used when rebuilding the container on hot update")
    ap.add_argument("--app-port", type=int, default=None,
                    help="App listening port (reverse-proxied by Nginx); used by hot update health check and docker run port mapping")
    ap.add_argument("--outputs-json", required=True,
                    help='ROS GetStack Outputs serialized as {"Key": "Value"} JSON')
    ap.add_argument("--artifact-bucket", default=None)
    ap.add_argument("--static-dir", default=None)
    ap.add_argument("--app-dir", default=None)
    ap.add_argument("--nginx-mode", default=None, choices=["static+app", "proxy", "static"])
    ap.add_argument("--with-rds", action="store_true")
    ap.add_argument("--db-engine", default=None, choices=["mysql"])
    ap.add_argument("--artifact-urls-json", default=None,
                    help='Artifact signed URLs (output JSON from upload_artifacts.py), stored as current_artifact_urls')
    ap.add_argument("--notes", default="")
    ap.add_argument("--project-root", default=".")
    args = ap.parse_args()

    deploy_mode = "full-stack"

    # Read passwords from environment variables, not command line (to avoid ps leaks)
    ecs_password = os.environ.get("PASSWORD") or None
    db_password = os.environ.get("DB_PASSWORD") or None

    outputs = json.loads(args.outputs_json)
    public_ip = outputs.get("PublicIp") or outputs.get("public_ip")
    ecs_ids_raw = outputs.get("EcsInstanceIds") or outputs.get("ecs_instance_ids") or ""
    if isinstance(ecs_ids_raw, list):
        ecs_ids = [str(x) for x in ecs_ids_raw]
    else:
        ecs_ids = [x.strip() for x in str(ecs_ids_raw).split(",") if x.strip()]
    security_group_id = outputs.get("SecurityGroupId") or outputs.get("security_group_id")
    eip_allocation_id = outputs.get("EipAllocationId") or outputs.get("eip_allocation_id")
    db_instance_id = outputs.get("DbInstanceId") or outputs.get("db_instance_id")
    db_conn = outputs.get("DbConnectionAddress") or outputs.get("db_connection_address")
    db_port_raw = outputs.get("DbPort") or outputs.get("db_port")
    db_port = int(db_port_raw) if db_port_raw not in (None, "") else None
    db_account = outputs.get("DbAccount") or outputs.get("db_account")

    state = {
        "version": 1,
        "deploy_mode": deploy_mode,
        "region_id": args.region,
        "topology": args.topology,
        "app_type": args.app_type,
        "service_name": args.app_name,
        "runtime": args.runtime,
        "static_dir": args.static_dir,
        "app_dir": args.app_dir,
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "tags": [{"Key": "from", "Value": "qwencloud"}],
        "outputs": {
            "public_ip": public_ip,
            "ecs_instance_ids": ecs_ids,
            "security_group_id": security_group_id,
            "eip_allocation_id": eip_allocation_id,
            "db_instance_id": db_instance_id,
            "db_connection_address": db_conn,
            "db_port": db_port,
            "db_account": db_account,
        },
        "nginx_mode": args.nginx_mode,
        "artifact_bucket": args.artifact_bucket,
        "notes": args.notes,
    }
    # Fields required for Docker hot update: only meaningful for docker deployments,
    # so avoid polluting state files of other app_types.
    if args.app_type == "docker":
        state["app_mode"] = args.app_mode or "docker-image"
        state["app_image_name"] = args.app_image_name or f"{args.app_name}:latest"
    if args.app_port is not None:
        state["app_port"] = args.app_port
    if args.stack_id:
        state["stack_id"] = args.stack_id
    if args.stack_name:
        state["stack_name"] = args.stack_name
    if args.with_rds or db_instance_id:
        state["db_engine"] = args.db_engine or "mysql"

    if args.artifact_urls_json:
        urls = json.loads(args.artifact_urls_json)
        current = {k: v for k, v in urls.items() if v and k.endswith("_url") and k not in ("template_url",)}
        if current:
            state["current_artifact_urls"] = current

    root = Path(args.project_root).resolve()
    state_path = root / ".qwencloud-deploy"
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    # State file holds current_artifact_urls (OSS signed URLs == download creds); 0600.
    os.chmod(state_path, 0o600)
    # Ignore deploy artifacts and the password sidecar.
    _ensure_gitignore(root, *DEPLOY_LEAK_PATHS)

    if ecs_password or db_password:
        local_path = root / ".qwencloud-deploy.local"
        local_data = {"stack_id": args.stack_id,
                      "warning": "This file contains passwords, do not commit to version control"}
        if ecs_password:
            local_data["ecs_password"] = ecs_password
        if db_password:
            local_data["db_password"] = db_password
        local_path.write_text(json.dumps(local_data, ensure_ascii=False, indent=2),
                              encoding="utf-8")
        os.chmod(local_path, 0o600)

    # Ignore host AI-agent workspaces that actually exist in the current directory.
    _ignore_agent_dirs(root)

    print(str(state_path))


if __name__ == "__main__":
    main()
