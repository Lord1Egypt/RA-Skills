#!/usr/bin/env bash
# deploy.sh: Deploy hosted MCP server + nginx config to wip.computer.
#
# Writes a JSON provenance manifest to
#   /var/www/wip.computer/deploy-manifests/hosted-mcp/<timestamp>.json
# on the VPS per F-009 of the VPS hosted-mcp audit
# (ai/product/bugs/security/2026-04-28--cc-mini--vps-hosted-mcp-audit.md).
#
# Manifest fields:
#   deployedAt, deployedBy, git (remote + branch + commit + dirty),
#   files[] (source, destination, sha256),
#   nginx (test_pass, test_output) when nginx is deployed,
#   pm2 (pid, status, restart_time, exec_path) when app is deployed.
#
# Usage:
#   bash deploy.sh                       # deploy app + nginx + manifest
#   bash deploy.sh --dry-run             # preview, no scp/reload/restart
#   bash deploy.sh --allow-dirty         # allow uncommitted changes
#   bash deploy.sh --skip-nginx          # only deploy Node app
#   bash deploy.sh --skip-app            # only deploy nginx config
#   bash deploy.sh --remote host         # override SSH host (default: wip.computer)
#
# Prerequisites:
#   - SSH config has Host wip.computer with key auth
#   - VPS user has passwordless sudo for nginx + systemctl reload
#   - pm2 installed on the server
#   - python3 and shasum/sha256sum available locally

set -euo pipefail

# ── Args ────────────────────────────────────────────────────────────

DRY_RUN=0
ALLOW_DIRTY=0
SKIP_NGINX=0
SKIP_APP=0
REMOTE="wip.computer"

while [ $# -gt 0 ]; do
  case "$1" in
    --dry-run)     DRY_RUN=1; shift ;;
    --allow-dirty) ALLOW_DIRTY=1; shift ;;
    --skip-nginx)  SKIP_NGINX=1; shift ;;
    --skip-app)    SKIP_APP=1; shift ;;
    --remote)      REMOTE=$2; shift 2 ;;
    -h|--help)     sed -n '2,30p' "$0"; exit 0 ;;
    *) echo "unknown arg: $1" >&2; exit 2 ;;
  esac
done

APP_REMOTE_DIR="/var/www/wip.computer/app/mcp-server"
NGINX_SNIPPETS_DIR="/etc/nginx/snippets"
NGINX_CONFD_DIR="/etc/nginx/conf.d"
MANIFEST_DIR="/var/www/wip.computer/deploy-manifests/hosted-mcp"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Pick whichever sha256 tool is available locally (macOS vs Linux).
if command -v sha256sum >/dev/null 2>&1; then
  SHA256_CMD="sha256sum"
elif command -v shasum >/dev/null 2>&1; then
  SHA256_CMD="shasum -a 256"
else
  echo "FATAL: neither sha256sum nor shasum found locally" >&2
  exit 1
fi

# Pick python3 for JSON-escape helpers; fall back to node if absent.
if command -v python3 >/dev/null 2>&1; then
  json_escape() { python3 -c 'import sys,json;print(json.dumps(sys.stdin.read()),end="")'; }
elif command -v node >/dev/null 2>&1; then
  json_escape() { node -e 'let d="";process.stdin.on("data",c=>d+=c);process.stdin.on("end",()=>process.stdout.write(JSON.stringify(d)));'; }
else
  echo "FATAL: neither python3 nor node found locally for JSON escaping" >&2
  exit 1
fi

# ── Pre-deploy: git state ───────────────────────────────────────────

REPO_ROOT="$(cd "${SCRIPT_DIR}" && git rev-parse --show-toplevel)"
cd "${REPO_ROOT}"
GIT_REMOTE_URL="$(git config --get remote.origin.url || echo 'unknown')"
GIT_COMMIT="$(git rev-parse HEAD)"
GIT_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
GIT_DIRTY_LIST="$(git status --porcelain)"
if [ -n "$GIT_DIRTY_LIST" ] && [ "$ALLOW_DIRTY" -ne 1 ]; then
  echo "FATAL: working tree has uncommitted changes:" >&2
  echo "$GIT_DIRTY_LIST" >&2
  echo "Pass --allow-dirty to deploy anyway (dev only)." >&2
  exit 1
fi
GIT_DIRTY=false
[ -n "$GIT_DIRTY_LIST" ] && GIT_DIRTY=true

# ── File inventory ──────────────────────────────────────────────────
#
# Two parallel arrays: SRC_FILES (relative to SCRIPT_DIR) and DST_FILES
# (absolute path on remote). Plain bash arrays for macOS bash 3.2
# compatibility.

SRC_FILES=()
DST_FILES=()
SHA_FILES=()

add_file() {
  local src=$1 dst=$2
  if [ ! -f "${SCRIPT_DIR}/${src}" ]; then
    echo "WARN: ${src} not found locally; skipping" >&2
    return
  fi
  SRC_FILES+=("$src")
  DST_FILES+=("$dst")
  SHA_FILES+=("$(${SHA256_CMD} "${SCRIPT_DIR}/${src}" | awk '{print $1}')")
}

if [ "$SKIP_APP" -ne 1 ]; then
  add_file "server.mjs"   "${APP_REMOTE_DIR}/server.mjs"
  add_file "inbox.mjs"    "${APP_REMOTE_DIR}/inbox.mjs"
  add_file "tools.mjs"    "${APP_REMOTE_DIR}/tools.mjs"
  add_file "codex-relay-e2ee-registry.mjs" "${APP_REMOTE_DIR}/codex-relay-e2ee-registry.mjs"
  add_file "codex-relay-ws-abuse-limits.mjs" "${APP_REMOTE_DIR}/codex-relay-ws-abuse-limits.mjs"
  add_file "package.json" "${APP_REMOTE_DIR}/package.json"
  # Phone app static files (codex-remote-control, login).
  if [ -d "${SCRIPT_DIR}/app" ]; then
    while IFS= read -r f; do
      rel=${f#${SCRIPT_DIR}/}
      add_file "$rel" "${APP_REMOTE_DIR}/${rel}"
    done < <(find "${SCRIPT_DIR}/app" -type f | sort)
  fi
  # Kaleidoscope demo files (login.html, index.html, agent.html, etc.).
  if [ -d "${SCRIPT_DIR}/demo" ]; then
    while IFS= read -r f; do
      rel=${f#${SCRIPT_DIR}/}
      add_file "$rel" "${APP_REMOTE_DIR}/${rel}"
    done < <(find "${SCRIPT_DIR}/demo" -type f | sort)
  fi
fi

if [ "$SKIP_NGINX" -ne 1 ]; then
  # Snippets included from the site config.
  if [ -d "${SCRIPT_DIR}/nginx" ]; then
    while IFS= read -r f; do
      rel=${f#${SCRIPT_DIR}/nginx/}
      base=$(basename "$f")
      case "$rel" in
        conf.d/*) add_file "nginx/${rel}" "${NGINX_CONFD_DIR}/${base}" ;;
        wip.computer.conf) ;;  # site config: deploy manually, has carry-over
        *) add_file "nginx/${rel}" "${NGINX_SNIPPETS_DIR}/${base}" ;;
      esac
    done < <(find "${SCRIPT_DIR}/nginx" -maxdepth 2 -type f -name '*.conf' | sort)
  fi
fi

# ── Dry-run preview ─────────────────────────────────────────────────

if [ "$DRY_RUN" -eq 1 ]; then
  echo "DRY RUN. Git: ${GIT_BRANCH} @ ${GIT_COMMIT} (dirty=${GIT_DIRTY})"
  echo "Remote: ${REMOTE}"
  echo "Files (${#SRC_FILES[@]}):"
  for ((i=0; i<${#SRC_FILES[@]}; i++)); do
    printf "  %-40s -> %s  [%s]\n" "${SRC_FILES[$i]}" "${DST_FILES[$i]}" "${SHA_FILES[$i]:0:12}"
  done
  echo ""
  echo "Would write manifest to: ${MANIFEST_DIR}/$(date -u +%Y-%m-%dT%H-%M-%SZ).json"
  exit 0
fi

if [ ${#SRC_FILES[@]} -eq 0 ]; then
  echo "Nothing to deploy (both --skip-app and --skip-nginx, or no files matched)." >&2
  exit 1
fi

# ── Deploy app files ────────────────────────────────────────────────

# /var/www/wip.computer/ is root-owned; the manifest dir must be
# created with sudo on first deploy. After creation, parker:parker
# ownership lets subsequent deploys write the manifest without sudo.
ssh "${REMOTE}" "sudo install -d -o parker -g parker -m 0755 ${MANIFEST_DIR}"

if [ "$SKIP_APP" -ne 1 ]; then
  ssh "${REMOTE}" "mkdir -p ${APP_REMOTE_DIR}/inbox"
fi

# scp each file. Pre-create destination dir on the remote so app/foo/bar.html
# does not fail on missing parent.
for ((i=0; i<${#SRC_FILES[@]}; i++)); do
  src=${SRC_FILES[$i]}
  dst=${DST_FILES[$i]}
  case "$dst" in
    /etc/nginx/*) need_sudo=1 ;;
    *)            need_sudo=0 ;;
  esac
  remote_parent=$(dirname "$dst")
  if [ "$need_sudo" -eq 1 ]; then
    # Stage to a temp dir on remote, then sudo mv into place.
    tmp="/tmp/deploy-staging-$$/$(basename "$src")"
    ssh "${REMOTE}" "mkdir -p $(dirname "$tmp")"
    scp "${SCRIPT_DIR}/${src}" "${REMOTE}:${tmp}"
    ssh "${REMOTE}" "sudo install -m 0644 ${tmp} ${dst}"
  else
    ssh "${REMOTE}" "mkdir -p ${remote_parent}"
    scp "${SCRIPT_DIR}/${src}" "${REMOTE}:${dst}"
  fi
done

# Cleanup staging dir if it exists.
ssh "${REMOTE}" "rm -rf /tmp/deploy-staging-$$" || true

# ── Verify post-deploy hashes (transfer integrity) ──────────────────

for ((i=0; i<${#SRC_FILES[@]}; i++)); do
  remote_sha=$(ssh "${REMOTE}" "sudo sha256sum ${DST_FILES[$i]}" 2>/dev/null | awk '{print $1}' || echo "")
  if [ "${SHA_FILES[$i]}" != "$remote_sha" ]; then
    echo "FATAL: post-deploy hash mismatch for ${SRC_FILES[$i]}" >&2
    echo "  local : ${SHA_FILES[$i]}" >&2
    echo "  remote: ${remote_sha}" >&2
    exit 1
  fi
done

# ── npm install (app only) ──────────────────────────────────────────

if [ "$SKIP_APP" -ne 1 ]; then
  ssh "${REMOTE}" "cd ${APP_REMOTE_DIR} && npm install --omit=dev"
fi

# ── nginx test + reload (nginx only) ────────────────────────────────

NGINX_TEST_PASS=null
NGINX_TEST_OUTPUT_JSON='""'
if [ "$SKIP_NGINX" -ne 1 ]; then
  set +e
  NGINX_TEST_OUTPUT=$(ssh "${REMOTE}" "sudo nginx -t" 2>&1)
  NGINX_TEST_RC=$?
  set -e
  if [ "$NGINX_TEST_RC" -eq 0 ]; then
    NGINX_TEST_PASS=true
    ssh "${REMOTE}" "sudo systemctl reload nginx"
  else
    NGINX_TEST_PASS=false
    echo "FATAL: nginx -t failed; not reloading." >&2
    echo "$NGINX_TEST_OUTPUT" >&2
  fi
  NGINX_TEST_OUTPUT_JSON=$(printf '%s' "$NGINX_TEST_OUTPUT" | json_escape)
fi

# ── PM2 reload ──────────────────────────────────────────────────────

PM2_INFO_JSON=null
if [ "$SKIP_APP" -ne 1 ]; then
  ssh "${REMOTE}" "cd ${APP_REMOTE_DIR} && (pm2 reload mcp-server || (pm2 start server.mjs --name mcp-server && pm2 save))"

  # Capture pm2 status for the manifest.
  PM2_RAW=$(ssh "${REMOTE}" "pm2 jlist" 2>/dev/null || echo "[]")
  PM2_INFO_JSON=$(printf '%s' "$PM2_RAW" | python3 -c '
import json,sys
data=json.load(sys.stdin)
target="mcp-server"
for p in data:
    if p.get("name")==target:
        env=p.get("pm2_env",{})
        print(json.dumps({
            "name": p.get("name"),
            "pid": p.get("pid"),
            "status": env.get("status"),
            "restart_time": env.get("restart_time"),
            "uptime": env.get("pm_uptime"),
            "exec_path": env.get("pm_exec_path"),
            "node_version": env.get("node_version"),
        }))
        break
else:
    print("null")
')
fi

# ── Build manifest ──────────────────────────────────────────────────

DEPLOYED_AT=$(date -u +%Y-%m-%dT%H:%M:%SZ)
TIMESTAMP_SLUG=$(date -u +%Y-%m-%dT%H-%M-%SZ)
DEPLOYED_BY="$(whoami)@$(hostname)"

# files[] JSON
FILES_JSON=""
for ((i=0; i<${#SRC_FILES[@]}; i++)); do
  [ "$i" -eq 0 ] || FILES_JSON+=","
  FILES_JSON+=$(printf '{"source":"%s","destination":"%s","sha256":"%s"}' \
    "${SRC_FILES[$i]}" "${DST_FILES[$i]}" "${SHA_FILES[$i]}")
done

MANIFEST=$(cat <<JSON
{
  "deployedAt": "${DEPLOYED_AT}",
  "deployedBy": "${DEPLOYED_BY}",
  "git": {
    "remote": "${GIT_REMOTE_URL}",
    "branch": "${GIT_BRANCH}",
    "commit": "${GIT_COMMIT}",
    "dirty": ${GIT_DIRTY}
  },
  "files": [${FILES_JSON}],
  "nginx": {
    "skipped": $([ "$SKIP_NGINX" -eq 1 ] && echo true || echo false),
    "test_pass": ${NGINX_TEST_PASS},
    "test_output": ${NGINX_TEST_OUTPUT_JSON}
  },
  "pm2": ${PM2_INFO_JSON}
}
JSON
)

# ── Write manifest to VPS ───────────────────────────────────────────

MANIFEST_PATH="${MANIFEST_DIR}/${TIMESTAMP_SLUG}.json"
printf '%s\n' "$MANIFEST" | ssh "${REMOTE}" "sudo install -d -m 0755 ${MANIFEST_DIR} && sudo tee ${MANIFEST_PATH} > /dev/null && sudo chmod 0644 ${MANIFEST_PATH}"

echo ""
echo "Deploy complete."
echo "Manifest: ${REMOTE}:${MANIFEST_PATH}"
echo ""
echo "Verify:"
echo "  curl -fsS https://wip.computer/health"
echo "  bash ${SCRIPT_DIR}/scripts/verify-deploy.sh ${MANIFEST_PATH}"
