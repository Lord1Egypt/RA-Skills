#!/usr/bin/env python3
"""Vibe VC API helper.

No dependencies beyond the Python standard library.

Examples:
  python vibevc_api.py register --project-name "My App" --creator-name "Jane" --oneliner "..." \
    --repository-url "https://github.com/org/repo" --email "jane@company.com" \
    --activity-level active --repo-access invite-diff-fund --analytics-connected false --stripe-connected false

  python vibevc_api.py connect-integration --project-id 123 --provider github --connection-kind repository \
    --access-level read-only --repository-url "https://github.com/org/repo"
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request


def _bool(s: str) -> bool:
    v = s.strip().lower()
    if v in {"1", "true", "t", "yes", "y", "on"}:
        return True
    if v in {"0", "false", "f", "no", "n", "off"}:
        return False
    raise argparse.ArgumentTypeError(f"Invalid boolean: {s!r}")


def _post_json(base_url: str, path: str, payload: dict, timeout: float = 30.0) -> dict:
    url = base_url.rstrip("/") + path
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code} from {url}: {body}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Network error calling {url}: {e}") from e

    if not body.strip():
        return {}
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return {"raw": body}


def main(argv: list[str]) -> int:
    base_url = os.environ.get("VIBEVC_BASE_URL", "https://vibevc.md")

    p = argparse.ArgumentParser(description="Vibe VC API helper")
    p.add_argument("--base-url", default=base_url, help="Default: env VIBEVC_BASE_URL or https://vibevc.md")
    p.add_argument("--dry-run", action="store_true", help="Print payload + URL and exit")

    sub = p.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("register", help="POST /api/register")
    r.add_argument("--project-name", required=True)
    r.add_argument("--creator-name", required=True)
    r.add_argument("--oneliner", required=True)
    r.add_argument("--repository-url", required=True)
    r.add_argument("--email", required=True)
    r.add_argument("--telegram")
    r.add_argument("--discord")
    r.add_argument("--mcp-workspace")
    r.add_argument("--activity-level", choices=["active", "steady", "quiet"], required=True)
    r.add_argument("--repo-access", choices=["invite-diff-fund", "guest-repository", "mcp-only"], required=True)
    r.add_argument("--analytics-connected", type=_bool, required=True)
    r.add_argument("--stripe-connected", type=_bool, required=True)

    ci = sub.add_parser("connect-integration", help="POST /api/integrations/connect")
    ci.add_argument("--project-id", type=int)
    ci.add_argument(
        "--provider",
        choices=["github", "gitlab", "bitbucket", "lovable", "mcp", "google-analytics", "stripe", "other"],
        required=True,
    )
    ci.add_argument("--connection-kind", choices=["repository", "workspace", "analytics", "billing"], required=True)
    ci.add_argument("--access-level", choices=["read-only", "guest", "pull-request", "webhook"], required=True)
    ci.add_argument("--repository-url")
    ci.add_argument("--metadata")

    nl = sub.add_parser("subscribe-newsletter", help="POST /api/newsletter")
    nl.add_argument("--email", required=True)
    nl.add_argument("--name")
    nl.add_argument("--source")

    clp = sub.add_parser("contact-limited-partner", help="POST /api/contact")
    clp.add_argument("--name", required=True)
    clp.add_argument("--email", required=True)
    clp.add_argument("--message", required=True)
    clp.add_argument("--firm")
    clp.add_argument("--location")
    clp.add_argument("--check-size")
    clp.add_argument("--thesis")

    args = p.parse_args(argv)

    if args.cmd == "register":
        payload = {
            "projectName": args.project_name,
            "creatorName": args.creator_name,
            "oneliner": args.oneliner,
            "repositoryUrl": args.repository_url,
            "email": args.email,
            "telegram": args.telegram,
            "discord": args.discord,
            "mcpWorkspace": args.mcp_workspace,
            "activityLevel": args.activity_level,
            "repoAccess": args.repo_access,
            "analyticsConnected": args.analytics_connected,
            "stripeConnected": args.stripe_connected,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        path = "/api/register"

    elif args.cmd == "connect-integration":
        payload = {
            "projectId": args.project_id,
            "provider": args.provider,
            "connectionKind": args.connection_kind,
            "accessLevel": args.access_level,
            "repositoryUrl": args.repository_url,
            "metadata": args.metadata,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        path = "/api/integrations/connect"

    elif args.cmd == "subscribe-newsletter":
        payload = {"email": args.email, "name": args.name, "source": args.source}
        payload = {k: v for k, v in payload.items() if v is not None}
        path = "/api/newsletter"

    elif args.cmd == "contact-limited-partner":
        payload = {
            "name": args.name,
            "email": args.email,
            "firm": args.firm,
            "location": args.location,
            "checkSize": args.check_size,
            "thesis": args.thesis,
            "message": args.message,
        }
        payload = {k: v for k, v in payload.items() if v is not None}
        path = "/api/contact"

    else:
        raise AssertionError(args.cmd)

    url = args.base_url.rstrip("/") + path
    if args.dry_run:
        print(json.dumps({"url": url, "payload": payload}, indent=2, sort_keys=True))
        return 0

    out = _post_json(args.base_url, path, payload)
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
