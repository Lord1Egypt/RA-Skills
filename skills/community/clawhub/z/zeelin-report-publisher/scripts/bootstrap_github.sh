#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  bootstrap_github.sh [--name "Your Name"] [--email "you@example.com"] [--repo "/path/to/repo"] [--skip-gh-login] [--skip-ssh]
  bootstrap_github.sh --clone-url "git@github.com:<you>/THU-ZeeLin-Reports.git" [--clone-dir "/path/to/local/repo"] [--upstream-url "git@github.com:thu-nmrc/THU-ZeeLin-Reports.git"]

What it does:
  1) Configures git global identity (user.name, user.email)
  2) Logs in to GitHub CLI with SSH protocol (optional)
  3) Generates and uploads SSH key if needed (optional)
  4) Optionally clones the report repo to local workspace and sets upstream remote
  5) Verifies remote connectivity and push permission via dry-run (optional)
EOF
}

need_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "[ERROR] Missing required command: $1" >&2
    exit 1
  fi
}

info() {
  echo "[INFO] $*"
}

warn() {
  echo "[WARN] $*" >&2
}

die() {
  echo "[ERROR] $*" >&2
  exit 1
}

GIT_NAME="${GIT_NAME:-}"
GIT_EMAIL="${GIT_EMAIL:-}"
REPO_PATH="${REPO_PATH:-}"
CLONE_URL="${CLONE_URL:-}"
CLONE_DIR="${CLONE_DIR:-}"
UPSTREAM_URL="${UPSTREAM_URL:-}"
SKIP_GH_LOGIN=0
SKIP_SSH=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --name)
      [[ $# -ge 2 ]] || die "--name requires a value"
      GIT_NAME="$2"
      shift 2
      ;;
    --email)
      [[ $# -ge 2 ]] || die "--email requires a value"
      GIT_EMAIL="$2"
      shift 2
      ;;
    --repo)
      [[ $# -ge 2 ]] || die "--repo requires a value"
      REPO_PATH="$2"
      shift 2
      ;;
    --clone-url)
      [[ $# -ge 2 ]] || die "--clone-url requires a value"
      CLONE_URL="$2"
      shift 2
      ;;
    --clone-dir)
      [[ $# -ge 2 ]] || die "--clone-dir requires a value"
      CLONE_DIR="$2"
      shift 2
      ;;
    --upstream-url)
      [[ $# -ge 2 ]] || die "--upstream-url requires a value"
      UPSTREAM_URL="$2"
      shift 2
      ;;
    --skip-gh-login)
      SKIP_GH_LOGIN=1
      shift
      ;;
    --skip-ssh)
      SKIP_SSH=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      die "Unknown argument: $1"
      ;;
  esac
done

need_cmd git

if [[ -z "$GIT_NAME" ]]; then
  GIT_NAME="$(git config --global user.name || true)"
fi
if [[ -z "$GIT_EMAIL" ]]; then
  GIT_EMAIL="$(git config --global user.email || true)"
fi

if [[ -z "$GIT_NAME" ]]; then
  read -r -p "Git user.name: " GIT_NAME
fi
if [[ -z "$GIT_EMAIL" ]]; then
  read -r -p "Git user.email: " GIT_EMAIL
fi

[[ -n "$GIT_NAME" ]] || die "Git user.name is empty"
[[ "$GIT_EMAIL" == *"@"* ]] || die "Git user.email looks invalid: $GIT_EMAIL"

git config --global user.name "$GIT_NAME"
git config --global user.email "$GIT_EMAIL"
info "Configured git identity: $GIT_NAME <$GIT_EMAIL>"

HAS_GH=0
if command -v gh >/dev/null 2>&1; then
  HAS_GH=1
else
  warn "gh not found; skipping GitHub CLI login and SSH key upload."
fi

GH_AUTH_OK=0
if [[ $HAS_GH -eq 1 ]]; then
  if gh auth status -h github.com >/dev/null 2>&1; then
    GH_AUTH_OK=1
    info "GitHub CLI already authenticated."
  elif [[ $SKIP_GH_LOGIN -eq 1 ]]; then
    warn "Skipping gh auth login by user request."
  else
    info "Starting GitHub CLI login (browser device flow)..."
    gh auth login -h github.com -p ssh -w
    if gh auth status -h github.com >/dev/null 2>&1; then
      GH_AUTH_OK=1
      info "GitHub CLI login succeeded."
    else
      warn "GitHub CLI login did not complete."
    fi
  fi
fi

if [[ $SKIP_SSH -eq 0 ]]; then
  need_cmd ssh
  need_cmd ssh-keygen
  KEY_PATH="${HOME}/.ssh/id_ed25519"
  PUB_PATH="${KEY_PATH}.pub"

  if [[ ! -f "$KEY_PATH" ]]; then
    info "Generating SSH key: $KEY_PATH"
    mkdir -p "${HOME}/.ssh"
    chmod 700 "${HOME}/.ssh"
    ssh-keygen -t ed25519 -C "$GIT_EMAIL" -f "$KEY_PATH" -N ""
  else
    info "Existing SSH key found: $KEY_PATH"
  fi

  if [[ ! -f "$PUB_PATH" ]]; then
    die "Missing SSH public key: $PUB_PATH"
  fi

  if [[ $HAS_GH -eq 1 && $GH_AUTH_OK -eq 1 ]]; then
    PUB_KEY="$(cat "$PUB_PATH")"
    REMOTE_KEYS="$(gh api user/keys --jq '.[].key' 2>/dev/null || true)"
    if grep -Fxq "$PUB_KEY" <<< "$REMOTE_KEYS"; then
      info "SSH key already uploaded to GitHub."
    else
      KEY_TITLE="$(hostname)-$(date +%F)"
      info "Uploading SSH key to GitHub as: $KEY_TITLE"
      gh ssh-key add "$PUB_PATH" --title "$KEY_TITLE"
    fi
  else
    warn "Skip SSH key upload because gh is unavailable or unauthenticated."
  fi

  SSH_OUTPUT="$(ssh -T -o StrictHostKeyChecking=accept-new git@github.com 2>&1 || true)"
  if grep -qi "successfully authenticated" <<< "$SSH_OUTPUT"; then
    info "SSH auth to GitHub is working."
  else
    warn "SSH auth test did not confirm success. Output:"
    warn "$SSH_OUTPUT"
  fi
fi

if [[ -n "$CLONE_DIR" && -z "$CLONE_URL" ]]; then
  die "--clone-dir requires --clone-url."
fi

if [[ -n "$CLONE_URL" ]]; then
  if [[ -z "$CLONE_DIR" ]]; then
    DEFAULT_REPO_NAME="$(basename "${CLONE_URL%.git}")"
    [[ -n "$DEFAULT_REPO_NAME" ]] || DEFAULT_REPO_NAME="THU-ZeeLin-Reports"
    CLONE_DIR="$PWD/$DEFAULT_REPO_NAME"
    info "No --clone-dir provided. Using workspace default: $CLONE_DIR"
  fi
  CLONE_DIR="${CLONE_DIR/#\~/$HOME}"
  if [[ "$CLONE_DIR" != /* ]]; then
    CLONE_DIR="$PWD/$CLONE_DIR"
  fi
  if [[ -d "$CLONE_DIR/.git" ]]; then
    info "Clone target already exists: $CLONE_DIR"
  else
    if [[ -e "$CLONE_DIR" ]]; then
      die "Clone target exists but is not a git repo: $CLONE_DIR"
    fi
    mkdir -p "$(dirname "$CLONE_DIR")"
    info "Cloning repository: $CLONE_URL -> $CLONE_DIR"
    git clone "$CLONE_URL" "$CLONE_DIR"
  fi
  REPO_PATH="$CLONE_DIR"
fi

if [[ -n "$REPO_PATH" ]]; then
  [[ -d "$REPO_PATH" ]] || die "Repo path not found: $REPO_PATH"
  [[ -d "$REPO_PATH/.git" ]] || die "Not a git repo: $REPO_PATH"

  if [[ -n "$UPSTREAM_URL" ]]; then
    if git -C "$REPO_PATH" remote get-url upstream >/dev/null 2>&1; then
      git -C "$REPO_PATH" remote set-url upstream "$UPSTREAM_URL"
      info "Updated upstream remote: $UPSTREAM_URL"
    else
      git -C "$REPO_PATH" remote add upstream "$UPSTREAM_URL"
      info "Added upstream remote: $UPSTREAM_URL"
    fi
  fi

  REMOTE_URL="$(git -C "$REPO_PATH" config --get remote.origin.url || true)"
  [[ -n "$REMOTE_URL" ]] || die "Repo has no origin remote: $REPO_PATH"
  info "origin remote: $REMOTE_URL"

  if git -C "$REPO_PATH" ls-remote --exit-code origin HEAD >/dev/null 2>&1; then
    info "Remote read access check passed."
  else
    die "Remote read access check failed. Verify auth and remote URL."
  fi

  HEAD_SHA="$(git -C "$REPO_PATH" rev-parse HEAD)"
  PROBE_REF="refs/heads/codex/permission-check-$(date +%Y%m%d%H%M%S)"
  if git -C "$REPO_PATH" push --dry-run origin "${HEAD_SHA}:${PROBE_REF}" >/dev/null 2>&1; then
    info "Remote push permission dry-run passed."
  else
    die "Remote push permission check failed. Ask admin to grant write access."
  fi

  if git -C "$REPO_PATH" remote get-url upstream >/dev/null 2>&1; then
    UPSTREAM_REMOTE_URL="$(git -C "$REPO_PATH" config --get remote.upstream.url || true)"
    info "upstream remote: $UPSTREAM_REMOTE_URL"
    if git -C "$REPO_PATH" ls-remote --exit-code upstream HEAD >/dev/null 2>&1; then
      info "Upstream read access check passed."
    else
      die "Upstream read access check failed. Verify upstream URL and permissions."
    fi
  fi
fi

echo "[OK] GitHub bootstrap completed."
