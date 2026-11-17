#!/usr/bin/env python3
"""Assemble ROS template + UserData script. See reference/deploy/07_generate_template.md"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
from pathlib import Path


TPL_DIR = Path(__file__).resolve().parent.parent / "templates"


def load_skeleton(topology: str, with_rds: bool) -> str:
    if with_rds:
        fname = f"ros_{topology}_rds.yaml"
    else:
        fname = f"ros_{topology}.yaml"
    return (TPL_DIR / fname).read_text(encoding="utf-8")


def build_userdata(app_type: str, args) -> str:
    # The bootstrap log records curl commands with OSS signed URLs (expanded by set -x);
    # the default umask yields 644, readable by any local user on the ECS instance ->
    # leaks OSSAccessKeyId/Signature. Symmetric with *_rds.yaml: create the log at 600
    # before exec. All userdata sub-scripts append to the same file, preserving the mode.
    parts = [
        "#!/bin/bash",
        "set -euxo pipefail",
        "install -m 600 /dev/null /var/log/qwencloud-bootstrap.log 2>/dev/null || "
        "{ touch /var/log/qwencloud-bootstrap.log; chmod 600 /var/log/qwencloud-bootstrap.log; }",
        "exec >> /var/log/qwencloud-bootstrap.log 2>&1",
    ]

    nginx_mode = getattr(args, "nginx_mode", "static+app")

    if nginx_mode == "proxy":
        nginx = (TPL_DIR / "userdata" / "nginx_proxy.sh").read_text(encoding="utf-8")
        nginx = nginx.replace("__APP_PORT__", str(args.app_port))
        parts.append("# --- nginx: proxy (server-rendered) ---")
        parts.append(nginx)
    elif nginx_mode == "static":
        nginx = (TPL_DIR / "userdata" / "nginx_static.sh").read_text(encoding="utf-8")
        nginx = nginx.replace("__STATIC_ARTIFACT_URL__", args.static_artifact_url or "")
        parts.append("# --- nginx: static (no app) ---")
        parts.append(nginx)
    else:
        nginx = (TPL_DIR / "userdata" / "nginx_static_proxy.sh").read_text(encoding="utf-8")
        nginx = nginx.replace("__STATIC_ARTIFACT_URL__", args.static_artifact_url or "")
        nginx = nginx.replace("__APP_PORT__", str(args.app_port))
        parts.append("# --- nginx: static+app (static + api) ---")
        parts.append(nginx)


    if app_type == "static-only":
        pass
    elif app_type == "docker":
        app_script = (TPL_DIR / "userdata" / "docker.sh").read_text(encoding="utf-8")
        app_script = app_script.replace("__APP_ARTIFACT_URL__", args.app_artifact_url or "")
        app_script = app_script.replace("__APP_MODE__", args.app_mode or "docker-image")
        app_script = app_script.replace("__APP_PORT__", str(args.app_port))
        app_script = app_script.replace("__APP_IMAGE_NAME__", args.app_image_name or f"{args.app_name}:latest")
        app_script = app_script.replace("__APP_NAME__", args.app_name)
        parts.append("# --- app: docker ---")
        parts.append(app_script)
    elif app_type == "systemd":
        runtime = getattr(args, "runtime", None) or "none"
        app_script = (TPL_DIR / "userdata" / "systemd.sh").read_text(encoding="utf-8")
        app_script = app_script.replace("__APP_ARTIFACT_URL__", args.app_artifact_url or "")
        app_script = app_script.replace("__APP_RUNTIME__", runtime)
        app_script = app_script.replace("__START_COMMAND__", args.start_command or "./server")
        app_script = app_script.replace("__APP_PORT__", str(args.app_port))
        app_script = app_script.replace("__APP_NAME__", args.app_name)
        parts.append(f"# --- app: systemd (runtime={runtime}) ---")
        parts.append(app_script)
    else:
        print(f"unknown app_type: {app_type}", file=sys.stderr)
        sys.exit(2)

    return "\n".join(parts) + "\n"


def inject_userdata_body(template_text: str, userdata_body: str) -> str:
    """Base64-encode userdata_body and inject into template's __USERDATA_BODY__ placeholder.

    Uses base64 encoding: Fn::Sub never sees shell variables. At runtime the encoded
    script is decoded and sourced, inheriting db.env environment variables.
    """
    marker = "__USERDATA_BODY__"
    if marker not in template_text:
        print(f"Cannot find {marker} placeholder in template", file=sys.stderr)
        sys.exit(2)

    encoded = base64.b64encode(userdata_body.encode("utf-8")).decode("ascii")

    loader = (
        f"echo '{encoded}' | base64 -d > /tmp/qwencloud-main.sh\n"
        f"chmod +x /tmp/qwencloud-main.sh\n"
        f". /tmp/qwencloud-main.sh"
    )

    for line in template_text.splitlines():
        if marker in line:
            indent = line[: len(line) - len(line.lstrip())]
            break

    indented_lines = []
    for ln in loader.splitlines():
        if ln.strip():
            indented_lines.append(indent + ln)
        else:
            indented_lines.append("")
    indented_body = "\n".join(indented_lines)

    full_marker_line = indent + marker
    return template_text.replace(full_marker_line, indented_body)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topology", choices=["single"], default="single")
    ap.add_argument("--app-type", required=True,
                    choices=["static-only", "docker", "systemd"])
    ap.add_argument("--app-port", type=int, default=8080)
    ap.add_argument("--runtime", default="none",
                    choices=["none", "java", "node", "python"],
                    help="Runtime installation (systemd only): none=skip (static binary), java/node/python=auto install")
    ap.add_argument("--static-artifact-url", default="")
    ap.add_argument("--app-artifact-url", default="")
    ap.add_argument("--artifacts-json", default=None,
                    help="JSON output from upload_artifacts.py (file path, or - for stdin); "
                         "automatically extracts static_url / app_url, avoiding manual pasting of long signed URLs. "
                         "Explicit --static-artifact-url / --app-artifact-url take priority.")
    ap.add_argument("--app-mode", default="docker-image", choices=["docker-image", "docker-compose"])
    ap.add_argument("--app-image-name", default="")
    ap.add_argument("--app-name", default="qwencloud-app",
                    help="Service name (systemd unit / container name / log file name / default image tag). "
                         "Must match ^[a-z][a-z0-9-]{0,30}$.")
    ap.add_argument("--start-command", default="",
                    help="Full startup command (relative to /opt/qwencloud), e.g. ./server / "
                         "\"python3 app.py\" / \"sh -c 'java -jar /opt/qwencloud/*.jar'\" / \"node server.js\" / "
                         "\"gunicorn -b :8080 app:app\". This is the exact command that will be exec'd.")
    ap.add_argument("--nginx-mode", default="static+app", choices=["static+app", "proxy", "static"],
                    help="static+app: static files + /api/ reverse proxy (default); proxy: full reverse proxy to app (Flask/Django etc); static: pure static hosting")
    ap.add_argument("--output", required=True)
    ap.add_argument("--userdata-output", required=True,
                    help="Write UserData to this file when no RDS; with RDS this path only gets a placeholder comment")
    # RDS-related
    ap.add_argument("--with-rds", action="store_true",
                    help="Use *_rds.yaml template and inline UserData into template (Fn::Sub embeds RDS internal address)")
    args = ap.parse_args()

    if not re.fullmatch(r"[a-z][a-z0-9-]{0,30}", args.app_name):
        print(f"Invalid --app-name: {args.app_name!r}; must match ^[a-z][a-z0-9-]{{0,30}}$ "
              "(lowercase letter first; only lowercase letters/digits/hyphen, length 1-31)", file=sys.stderr)
        sys.exit(64)

    # Validate DB_PASSWORD env var
    if args.with_rds and not os.environ.get("DB_PASSWORD"):
        print("--with-rds requires DB_PASSWORD environment variable", file=sys.stderr)
        sys.exit(64)

    # Consume artifacts-json
    if args.artifacts_json:
        raw = sys.stdin.read() if args.artifacts_json == "-" \
            else Path(args.artifacts_json).read_text(encoding="utf-8")
        try:
            art = json.loads(raw)
        except Exception as e:
            print(f"--artifacts-json parse failed: {e}", file=sys.stderr)
            sys.exit(64)
        if not args.static_artifact_url:
            args.static_artifact_url = art.get("static_url") or ""
        if not args.app_artifact_url:
            args.app_artifact_url = art.get("app_url") or ""

    skeleton = load_skeleton(args.topology, args.with_rds)
    userdata = build_userdata(args.app_type, args)

    if args.with_rds:
        # UserData inlined into template; --userdata-output only writes a reference file (raw, unescaped)
        final_template = inject_userdata_body(skeleton, userdata)
        Path(args.output).write_text(final_template, encoding="utf-8")
        Path(args.userdata_output).write_text(
            "# NOTE: With --with-rds, UserData is inlined into template; not passed as ROS Parameter.\n"
            "# Below is the raw body before escaping (for diff/debug only):\n\n" + userdata,
            encoding="utf-8")
    else:
        # Template written as-is; UserData goes to a standalone file
        Path(args.output).write_text(skeleton, encoding="utf-8")
        Path(args.userdata_output).write_text(userdata, encoding="utf-8")

    print(json.dumps({"template": args.output, "userdata": args.userdata_output, "with_rds": args.with_rds},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
