#!/usr/bin/env bash
set -euo pipefail

repo_dir=${1:-}
if [[ -z "${repo_dir}" || ! -d "${repo_dir}" ]]; then
  echo "Usage: $0 <repoDir>" >&2
  exit 2
fi

cd "${repo_dir}"
if [[ ! -f package.json ]]; then
  echo "No package.json found" >&2
  exit 3
fi

pm="npm"
install_cmd="npm install"
run_prefix="npm run"

if [[ -f pnpm-lock.yaml ]]; then
  pm="pnpm"
  install_cmd="pnpm install --frozen-lockfile"
  run_prefix="pnpm"
elif [[ -f yarn.lock ]]; then
  pm="yarn"
  install_cmd="yarn install --frozen-lockfile"
  run_prefix="yarn"
elif [[ -f package-lock.json ]]; then
  pm="npm"
  install_cmd="npm ci"
  run_prefix="npm run"
elif [[ -f bun.lockb ]]; then
  pm="bun"
  install_cmd="bun install"
  run_prefix="bun run"
fi

echo "pm=${pm}"
echo "install=${install_cmd}"

auto=""
if command -v node >/dev/null 2>&1; then
  auto=$(node -e '
    const fs = require("fs");
    const pkg = JSON.parse(fs.readFileSync("package.json","utf8"));
    const s = pkg.scripts || {};
    if (s.dev) return console.log("dev");
    if (s.start) return console.log("start");
    if (s.serve) return console.log("serve");
    return console.log("");
  ')
fi

if [[ -n "${auto}" ]]; then
  echo "run=${run_prefix} ${auto}"
else
  echo "run=${run_prefix} <script>  # (no obvious dev/start script)"
fi

if [[ -f .env.example && ! -f .env ]]; then
  echo "env_hint=.env.example exists; consider copying to .env (ask user for values)"
fi
