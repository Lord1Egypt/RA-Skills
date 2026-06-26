#!/usr/bin/env python3
"""
generate_template.py — Generate Unraid DockerMan user template XML

Usage:
    python3 generate_template.py --name <name> --image <image> [options]

Examples:
    # OpenCode template
    python3 generate_template.py \
        --name opencode \
        --image ghcr.io/anomalyco/opencode:latest \
        --port 4096 \
        --web-port 4097 \
        --proxy 192.168.8.30:7893 \
        --tz Asia/Shanghai \
        --output /tmp/opencode.xml

    # OpenClaw template
    python3 generate_template.py \
        --name openclaw \
        --image ghcr.io/openclaw/openclaw:latest \
        --port 18789 \
        --output /tmp/openclaw.xml
"""

import argparse
import sys
import textwrap
from pathlib import Path


def build_configs(args) -> list:
    """Build list of Config XML blocks."""
    configs = []

    # Port config
    if args.port:
        configs.append(
            f'  <Config Name="Port" Target="PORT" Default="{args.port}" '
            f'Mode="tcp" Description="Container port" Type="Port" '
            f'Display="always" Required="true" Mask="false">{args.port}</Config>'
        )

    # Web port config
    if args.web_port:
        configs.append(
            f'  <Config Name="Web UI Port" Target="WEB_PORT" Default="{args.web_port}" '
            f'Mode="tcp" Description="Web UI port (if applicable)" Type="Port" '
            f'Display="always" Required="false" Mask="false">{args.web_port}</Config>'
        )

    # Data path config
    if args.name:
        default_path = f"/mnt/user/appdata/{args.name}"
        configs.append(
            f'  <Config Name="Config Path" Target="/config" '
            f'Default="{default_path}" Mode="rw" '
            f'Description="Persistent config/data path" Type="Path" '
            f'Display="always" Required="true" Mask="false">{default_path}</Config>'
        )

    # Proxy configs
    if args.proxy:
        proxy_url = f"http://{args.proxy}"
        configs.append(
            f'  <Config Name="HTTP Proxy" Target="HTTP_PROXY" Default="" '
            f'Type="Variable" Display="advanced" Required="false" Mask="false">'
            f'{proxy_url}</Config>'
        )
        configs.append(
            f'  <Config Name="HTTPS Proxy" Target="HTTPS_PROXY" Default="" '
            f'Type="Variable" Display="advanced" Required="false" Mask="false">'
            f'{proxy_url}</Config>'
        )
        configs.append(
            f'  <Config Name="NO Proxy" Target="NO_PROXY" Default="" '
            f'Type="Variable" Display="advanced" Required="false" Mask="false">'
            f'localhost,127.0.0.1,192.168.0.0/16</Config>'
        )

    # TZ config
    tz = args.tz or "Asia/Shanghai"
    configs.append(
        f'  <Config Name="Timezone" Target="TZ" Default="{tz}" '
        f'Type="Variable" Display="advanced" Required="false" Mask="false">{tz}</Config>'
    )

    # Extra environment variables from CLI
    for env_str in (args.env or []):
        if "=" not in env_str:
            continue
        key, val = env_str.split("=", 1)
        key_upper = key.upper()  # Env vars are conventionally uppercase
        configs.append(
            f'  <Config Name="{key_upper}" Target="{key_upper}" Default="" '
            f'Type="Variable" Display="advanced" Required="false" Mask="false">{val}</Config>'
        )

    return configs


def build_post_args(args) -> str:
    """Build the PostArgs shell command string."""
    if args.post_args:
        # Use exactly what user provided
        return args.post_args

    if args.startup_cmd:
        # Build from user-provided startup command
        env_lines = []
        if args.proxy:
            proxy_url = f"http://{args.proxy}"
            env_lines.append(f'export HTTP_PROXY="{proxy_url}"')
            env_lines.append(f'export HTTPS_PROXY="{proxy_url}"')
            env_lines.append('export NO_PROXY="localhost,127.0.0.1,192.168.0.0/16"')
        if args.tz:
            env_lines.append(f'export TZ="{args.tz}"')
        env_block = " && ".join(env_lines)
        if env_block:
            return f"-ec '{env_block} && {args.startup_cmd}'"
        return f"-ec '{args.startup_cmd}'"

    # Default: just exec the passed command
    return f"-ec 'echo \"No startup command configured\" && exec tail -f /dev/null'"


def generate_template(args) -> str:
    """Generate the complete Unraid XML template."""

    configs = build_configs(args)
    config_xml = "\n".join(configs) if configs else ""

    # ExtraParams
    extra_params = ""
    if args.extra_params:
        extra_params = f"\n  <ExtraParams>{args.extra_params}</ExtraParams>"
    elif args.bypass_entrypoint:
        extra_params = "\n  <ExtraParams>--entrypoint /bin/sh</ExtraParams>"

    # PostArgs
    post_args = build_post_args(args)

    # WebUI
    webui = ""
    if args.web_port:
        webui = f"\n  <WebUI>http://[IP]:[PORT:{args.web_port}]/</WebUI>"

    # Icon
    icon = ""
    if args.icon:
        icon = f"\n  <Icon>{args.icon}</Icon>"

    # Extra volumes from CLI
    extra_volumes = ""
    for vol in (args.volume or []):
        host_path, container_path = vol.split(":")
        extra_volumes += f"\n  <Config Name=\"Volume: {container_path}\" Target=\"{container_path}\" Default=\"{host_path}\" Mode=\"rw\" Type=\"Path\" Display=\"advanced\" Required=\"false\" Mask=\"false\">{host_path}</Config>"

    template = f"""<?xml version="1.0"?>
<Container version="2">
  <Name>{args.name}</Name>
  <Repository>{args.image}</Repository>
  <Network>bridge</Network>{icon}{webui}{extra_params}
  <PostArgs>{post_args}</PostArgs>
{config_xml}{extra_volumes}
</Container>"""

    return template


def main():
    parser = argparse.ArgumentParser(
        description="Generate Unraid DockerMan user template XML"
    )
    parser.add_argument("--name", "-n", required=True, help="Container name (will be prefixed with my-)")
    parser.add_argument("--image", "-i", required=True, help="Docker image (e.g. ghcr.io/anomalyco/opencode:latest)")
    parser.add_argument("--port", "-p", type=int, help="Main port number")
    parser.add_argument("--web-port", help="Web UI port number")
    parser.add_argument("--icon", help="Icon URL")
    parser.add_argument("--category", default="Productivity: Tools: Utilities", help="Unraid category")
    parser.add_argument("--bypass-entrypoint", action="store_true",
                        help="Add --entrypoint /bin/sh to override image ENTRYPOINT")
    parser.add_argument("--startup-cmd", help="Actual startup command (for PostArgs)")
    parser.add_argument("--post-args", help="Full PostArgs string (overrides --startup-cmd)")
    parser.add_argument("--extra-params", help="Extra docker run flags")
    parser.add_argument("--proxy", help="HTTP(S) proxy host:port (e.g. 192.168.8.30:7893)")
    parser.add_argument("--tz", default="Asia/Shanghai", help="Timezone")
    parser.add_argument("--env", action="append",
                        help="Extra env var as KEY=VALUE (can be repeated)")
    parser.add_argument("--volume", action="append",
                        help="Extra volume as /host/path:/container/path (can be repeated)")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    parser.add_argument("--deploy", action="store_true",
                        help="Write directly to Unraid template path (requires confirmation)")

    args = parser.parse_args()

    xml_content = generate_template(args)

    if args.output:
        Path(args.output).write_text(xml_content, encoding="utf-8")
        print(f"Template written to: {args.output}", file=sys.stderr)

    if args.deploy:
        deploy_path = f"/boot/config/plugins/dockerMan/templates-user/my-{args.name}.xml"
        confirm = input(f"Deploy to {deploy_path}? [y/N]: ").strip().lower()
        if confirm == "y":
            Path(deploy_path).write_text(xml_content, encoding="utf-8")
            print(f"Deployed to: {deploy_path}", file=sys.stderr)
        else:
            print("Deploy cancelled.", file=sys.stderr)

    print(xml_content)


if __name__ == "__main__":
    main()
