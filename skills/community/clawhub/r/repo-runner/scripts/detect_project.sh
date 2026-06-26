#!/usr/bin/env bash
set -euo pipefail

repo_dir=${1:-}
if [[ -z "${repo_dir}" || ! -d "${repo_dir}" ]]; then
  echo "Usage: $0 <repoDir>" >&2
  exit 2
fi

cd "${repo_dir}"

has_file() { [[ -f "$1" ]]; }
has_dir() { [[ -d "$1" ]]; }

say() { printf '%s\n' "$*"; }

say "repo_dir=${repo_dir}"

# Docs
if has_file README.md; then say "docs=README.md"; fi
if has_file readme.md; then say "docs=readme.md"; fi
if has_dir docs; then say "docs_dir=docs/"; fi

# Node/TS
if has_file package.json; then
  say "type=node"

  pm="npm"
  if has_file pnpm-lock.yaml; then pm="pnpm"; fi
  if has_file yarn.lock; then pm="yarn"; fi
  if has_file bun.lockb; then pm="bun"; fi
  say "node.package_manager=${pm}"

  if command -v node >/dev/null 2>&1; then
    node -e '
      const fs = require("fs");
      const pkg = JSON.parse(fs.readFileSync("package.json","utf8"));
      const scripts = pkg.scripts || {};
      const keys = ["dev","start","build","test","typecheck","lint"]; 
      for (const k of keys) {
        if (scripts[k]) console.log(`node.script.${k}=${scripts[k]}`);
      }
      const engines = pkg.engines || {};
      if (engines.node) console.log(`node.engine.node=${engines.node}`);
    '
  else
    say "warn=node_not_found"
  fi
fi

# Python
if has_file pyproject.toml || has_file requirements.txt || has_file setup.py; then
  say "type=python"
  if has_file pyproject.toml; then say "python=pyproject.toml"; fi
  if has_file requirements.txt; then say "python=requirements.txt"; fi
fi

# Docker
if has_file docker-compose.yml || has_file docker-compose.yaml || has_file Dockerfile; then
  say "type=docker"
  if has_file docker-compose.yml; then say "docker=compose"; fi
  if has_file docker-compose.yaml; then say "docker=compose"; fi
  if has_file Dockerfile; then say "docker=dockerfile"; fi
fi

# Go
if has_file go.mod; then
  say "type=go"
  say "go=go.mod"
fi

# Rust
if has_file Cargo.toml; then
  say "type=rust"
  say "rust=Cargo.toml"
fi
