#!/usr/bin/env python3
"""Create the GitHub Actions workflow that deploys the public site/ folder."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from learning_workspace_config import (  # noqa: E402
    default_base_url,
    infer_owner_repo,
    update_config,
)


WORKFLOW = """name: Deploy GitHub Pages

on:
  push:
    branches: ["main"]
    paths:
      - "site/**"
      - ".github/workflows/pages.yml"
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Setup Pages
        uses: actions/configure-pages@v5
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: "site"
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Install .github/workflows/pages.yml for publishing site/ with GitHub Actions.")
    parser.add_argument("--workspace", type=Path, default=Path("."), help="Personal learning repository root.")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing workflow file.")
    parser.add_argument("--remote", default="origin", help="Git remote name used to infer the Pages URL.")
    parser.add_argument("--base-url", help="GitHub Pages base URL. Defaults to https://<owner>.github.io/<repo>.")
    parser.add_argument("--no-auto-publish", action="store_true", help="Do not mark generated worksheets for automatic Pages publishing.")
    parser.add_argument("--public-repository-accepted", action="store_true", help="Record that the parent accepts public repository visibility.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workspace = args.workspace.resolve()
    target = workspace / ".github" / "workflows" / "pages.yml"

    if target.exists() and not args.force:
        print(f"skipped: {target} already exists; use --force to overwrite")
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(WORKFLOW, encoding="utf-8")
        print(f"written: {target}")

    inferred = infer_owner_repo(workspace, args.remote)
    owner = inferred[0] if inferred else ""
    repo = inferred[1] if inferred else workspace.name
    base_url = (args.base_url or default_base_url(owner, repo)).rstrip("/")
    update_config(
        workspace,
        {
            "github": {
                "owner": owner,
                "repo": repo,
            },
            "git_sync": {
                "public_repository_accepted": args.public_repository_accepted,
            },
            "pages": {
                "enabled": True,
                "source": "github-actions",
                "auto_publish_worksheets": not args.no_auto_publish,
                "base_url": base_url,
            },
        },
        owner=owner,
        repo=repo,
        remote=args.remote,
    )
    print(f"updated: {workspace / '.zhizhi-math-coach' / 'config.json'}")
    print("next: in GitHub repository Settings -> Pages -> Build and deployment -> Source, choose GitHub Actions")
    print("next: commit and push .github/workflows/pages.yml, .zhizhi-math-coach/config.json, and site/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
