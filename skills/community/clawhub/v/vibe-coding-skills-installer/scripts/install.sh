#!/usr/bin/env bash
set -euo pipefail

# Vibe Coding Skills Installer — helper script
# Called by the agent with structured arguments; outputs machine-readable status lines.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# ── Defaults ──────────────────────────────────────────────────────────────────
HOST="auto"
ACTION=""       # check | install | verify
SKILLSET=""     # openspec | gstack | superpowers
SCOPE="global"  # global | project | team | workflows

GSTACK_REPO="https://github.com/garrytan/gstack.git"
SUPERPOWERS_REPO="https://github.com/obra/superpowers.git"
OPENSPEC_WORKFLOWS_REPO="https://github.com/samotage/cursor-openspec-workflows.git"

# ── Argument parsing ──────────────────────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --host)     HOST="$2"; shift 2 ;;
    --check)    ACTION="check"; shift ;;
    --install)  ACTION="install"; SKILLSET="$2"; shift 2 ;;
    --scope)    SCOPE="$2"; shift 2 ;;
    --verify)   ACTION="verify"; shift ;;
    *)          echo "STATUS: fail | DETAIL: Unknown argument: $1"; exit 1 ;;
  esac
done

# ── Platform resolution ──────────────────────────────────────────────────────
resolve_platform() {
  local host="$1"
  if [[ "$host" == "auto" ]]; then
    # Try to detect from this script's own path
    case "$SCRIPT_DIR" in
      */.cursor/*)   host="cursor" ;;
      */.claude/*)   host="claude" ;;
      */.agents/*)   host="codex" ;;
      */.windsurf/*) host="windsurf" ;;
      */.gemini/*)   host="gemini" ;;
      */.opencode/*) host="opencode" ;;
      *)             host="unknown" ;;
    esac
  fi
  echo "$host"
}

get_global_skills() {
  local host="$1"
  case "$host" in
    cursor)   echo "$HOME/.cursor/skills" ;;
    claude)   echo "$HOME/.claude/skills" ;;
    codex)    echo "$HOME/.agents/skills" ;;
    windsurf) echo "$HOME/.windsurf/skills" ;;
    gemini)   echo "$HOME/.gemini/skills" ;;
    opencode) echo "$HOME/.opencode/skills" ;;
    *)        echo "$HOME/.agents/skills" ;;
  esac
}

get_project_skills() {
  local host="$1"
  case "$host" in
    cursor)   echo ".cursor/skills" ;;
    claude)   echo ".claude/skills" ;;
    codex)    echo ".agents/skills" ;;
    windsurf) echo ".windsurf/skills" ;;
    gemini)   echo ".gemini/skills" ;;
    opencode) echo ".opencode/skills" ;;
    *)        echo ".agents/skills" ;;
  esac
}

get_gstack_host_flag() {
  local host="$1"
  case "$host" in
    cursor)   echo "cursor" ;;
    claude)   echo "claude" ;;
    codex)    echo "codex" ;;
    opencode) echo "opencode" ;;
    *)        echo "claude" ;;
  esac
}

HOST=$(resolve_platform "$HOST")
if [[ "$HOST" == "unknown" ]]; then
  echo "STATUS: warn | DETAIL: Could not auto-detect platform. Defaulting to codex-style paths (~/.agents/skills/). Pass --host explicitly for other platforms."
  HOST="codex"
fi
GLOBAL_SKILLS=$(get_global_skills "$HOST")
PROJECT_SKILLS=$(get_project_skills "$HOST")

# ── Dependency checks ────────────────────────────────────────────────────────
check_cmd() {
  local cmd="$1"
  local label="$2"
  if command -v "$cmd" &>/dev/null; then
    local ver
    ver=$("$cmd" --version 2>/dev/null | head -1)
    echo "STATUS: ok | DEP: $label | VERSION: $ver"
  else
    echo "STATUS: missing | DEP: $label | HINT: Install $label before proceeding"
  fi
}

check_installed() {
  local name="$1"
  local path="$2"
  if [[ -d "$path" ]]; then
    if [[ -f "$path/SKILL.md" ]] || [[ -f "$path/package.json" ]] || [[ -f "$path/setup" ]]; then
      echo "STATUS: installed | SKILLSET: $name | PATH: $path"
    else
      echo "STATUS: partial | SKILLSET: $name | PATH: $path | DETAIL: Directory exists but may be incomplete"
    fi
  else
    echo "STATUS: not_installed | SKILLSET: $name | PATH: $path"
  fi
}

do_check() {
  echo "PLATFORM: $HOST"
  echo "GLOBAL_SKILLS: $GLOBAL_SKILLS"
  echo "PROJECT_SKILLS: $PROJECT_SKILLS"
  echo "---"

  check_cmd "node" "node"
  check_cmd "npm" "npm"
  check_cmd "git" "git"
  check_cmd "bun" "bun"

  if command -v openspec &>/dev/null; then
    local ver
    ver=$(openspec --version 2>/dev/null | head -1 || echo "unknown")
    echo "STATUS: ok | DEP: openspec-cli | VERSION: $ver"
  else
    echo "STATUS: missing | DEP: openspec-cli | HINT: npm install -g @fission-ai/openspec@latest"
  fi
  echo "---"

  check_installed "gstack" "$GLOBAL_SKILLS/gstack"
  check_installed "gstack-project" "$PROJECT_SKILLS/gstack"
  check_installed "superpowers" "$GLOBAL_SKILLS/superpowers"
  check_installed "superpowers-project" "$PROJECT_SKILLS/superpowers"

  # Superpowers may also be a plugin (not in skills dir)
  local plugin_paths=(
    "$HOME/.cursor/plugins/cache/cursor-public/superpowers"
    "$HOME/.claude/plugins/superpowers"
  )
  for pp in "${plugin_paths[@]}"; do
    if [[ -d "$pp" ]]; then
      echo "STATUS: installed | SKILLSET: superpowers-plugin | PATH: $pp"
    fi
  done
}

# ── Install functions ────────────────────────────────────────────────────────
install_openspec() {
  local scope="$1"

  case "$scope" in
    global)
      echo "STEP: Installing OpenSpec CLI globally..."
      npm install -g @fission-ai/openspec@latest
      echo "STATUS: ok | ACTION: openspec-cli-installed"
      ;;
    project)
      echo "STEP: Initializing OpenSpec in current project..."
      openspec init
      echo "STATUS: ok | ACTION: openspec-project-initialized"
      ;;
    workflows)
      echo "STEP: Installing OpenSpec workflow skills to $PROJECT_SKILLS/ ..."
      local tmpdir
      tmpdir=$(mktemp -d)
      git clone --depth 1 "$OPENSPEC_WORKFLOWS_REPO" "$tmpdir/openspec-workflows"
      mkdir -p "$PROJECT_SKILLS"
      # Copy all openspec-* skill directories found in the cloned repo
      local found=0
      for src_dir in "$tmpdir/openspec-workflows/.cursor/skills/openspec-"* \
                     "$tmpdir/openspec-workflows/.claude/skills/openspec-"* \
                     "$tmpdir/openspec-workflows/.agents/skills/openspec-"* \
                     "$tmpdir/openspec-workflows/skills/openspec-"*; do
        if [[ -d "$src_dir" ]]; then
          local basename
          basename=$(basename "$src_dir")
          cp -r "$src_dir" "$PROJECT_SKILLS/$basename"
          found=$((found + 1))
        fi
      done
      rm -rf "$tmpdir"
      if [[ $found -gt 0 ]]; then
        echo "STATUS: ok | ACTION: openspec-workflows-installed | COUNT: $found skills"
      else
        echo "STATUS: fail | ACTION: openspec-workflows-installed | DETAIL: No openspec-* skill dirs found in repo"
      fi
      ;;
    *)
      echo "STATUS: fail | DETAIL: Unknown scope '$scope' for openspec"
      exit 1
      ;;
  esac
}

install_gstack() {
  local scope="$1"
  local host_flag
  host_flag=$(get_gstack_host_flag "$HOST")

  case "$scope" in
    global)
      local gstack_dir="$GLOBAL_SKILLS/gstack"
      echo "STEP: Cloning gstack to $gstack_dir ..."
      mkdir -p "$GLOBAL_SKILLS"
      if [[ -d "$gstack_dir" ]]; then
        echo "STEP: gstack directory already exists, pulling latest..."
        (cd "$gstack_dir" && git pull --ff-only 2>/dev/null || true)
      else
        git clone --single-branch --depth 1 "$GSTACK_REPO" "$gstack_dir"
      fi
      echo "STEP: Running gstack setup --host $host_flag ..."
      (cd "$gstack_dir" && ./setup --host "$host_flag")
      echo "STATUS: ok | ACTION: gstack-global-installed | HOST: $host_flag | PATH: $gstack_dir"
      ;;
    project)
      local gstack_proj="$PROJECT_SKILLS/gstack"
      echo "STEP: Cloning gstack to $gstack_proj ..."
      mkdir -p "$PROJECT_SKILLS"
      if [[ -d "$gstack_proj" ]]; then
        echo "STEP: gstack directory already exists, pulling latest..."
        (cd "$gstack_proj" && git pull --ff-only 2>/dev/null || true)
      else
        git clone --single-branch --depth 1 "$GSTACK_REPO" "$gstack_proj"
      fi
      echo "STEP: Running gstack setup --host $host_flag ..."
      (cd "$gstack_proj" && ./setup --host "$host_flag")
      echo "STATUS: ok | ACTION: gstack-project-installed | HOST: $host_flag | PATH: $gstack_proj"
      ;;
    team)
      local gstack_dir="$GLOBAL_SKILLS/gstack"
      echo "STEP: Configuring gstack team mode for current project..."
      if [[ ! -d "$gstack_dir" ]]; then
        echo "STATUS: fail | DETAIL: gstack not installed globally yet. Run global install first."
        exit 1
      fi
      (cd "$gstack_dir" && ./setup --host "$host_flag" --team)
      echo "STATUS: ok | ACTION: gstack-team-configured | HOST: $host_flag"
      ;;
    *)
      echo "STATUS: fail | DETAIL: Unknown scope '$scope' for gstack"
      exit 1
      ;;
  esac
}

install_superpowers() {
  local scope="$1"

  case "$HOST" in
    cursor)
      if [[ "$scope" == "project" ]]; then
        local sp_proj="$PROJECT_SKILLS/superpowers"
        echo "STEP: Cloning Superpowers to $sp_proj ..."
        mkdir -p "$PROJECT_SKILLS"
        if [[ -d "$sp_proj" ]]; then
          echo "STEP: Superpowers directory already exists, pulling latest..."
          (cd "$sp_proj" && git pull --ff-only 2>/dev/null || true)
        else
          git clone --depth 1 "$SUPERPOWERS_REPO" "$sp_proj"
        fi
        echo "STATUS: ok | ACTION: superpowers-project-installed | PATH: $sp_proj"
      else
        echo "STATUS: agent_action | ACTION: Run /add-plugin superpowers in Cursor agent chat"
      fi
      ;;
    claude)
      if [[ "$scope" == "project" ]]; then
        local sp_proj="$PROJECT_SKILLS/superpowers"
        echo "STEP: Cloning Superpowers to $sp_proj ..."
        mkdir -p "$PROJECT_SKILLS"
        if [[ -d "$sp_proj" ]]; then
          echo "STEP: Superpowers directory already exists, pulling latest..."
          (cd "$sp_proj" && git pull --ff-only 2>/dev/null || true)
        else
          git clone --depth 1 "$SUPERPOWERS_REPO" "$sp_proj"
        fi
        echo "STATUS: ok | ACTION: superpowers-project-installed | PATH: $sp_proj"
      else
        echo "STATUS: agent_action | ACTION: Run /plugin install superpowers@claude-plugins-official in Claude Code"
      fi
      ;;
    *)
      local target_dir
      if [[ "$scope" == "project" ]]; then
        target_dir="$PROJECT_SKILLS/superpowers"
        mkdir -p "$PROJECT_SKILLS"
      else
        target_dir="$GLOBAL_SKILLS/superpowers"
        mkdir -p "$GLOBAL_SKILLS"
      fi
      echo "STEP: Cloning Superpowers to $target_dir ..."
      if [[ -d "$target_dir" ]]; then
        echo "STEP: Superpowers directory already exists, pulling latest..."
        (cd "$target_dir" && git pull --ff-only 2>/dev/null || true)
      else
        git clone --depth 1 "$SUPERPOWERS_REPO" "$target_dir"
      fi
      echo "STATUS: ok | ACTION: superpowers-installed | PATH: $target_dir"
      ;;
  esac
}

# ── Verify ───────────────────────────────────────────────────────────────────
do_verify() {
  echo "PLATFORM: $HOST"
  echo "---"

  # OpenSpec CLI
  if command -v openspec &>/dev/null; then
    echo "VERIFY: ok | COMPONENT: openspec-cli"
  else
    echo "VERIFY: not_found | COMPONENT: openspec-cli"
  fi

  # gstack (global)
  local gstack_dir="$GLOBAL_SKILLS/gstack"
  if [[ -d "$gstack_dir" ]] && [[ -f "$gstack_dir/setup" ]]; then
    echo "VERIFY: ok | COMPONENT: gstack | PATH: $gstack_dir"
  else
    echo "VERIFY: not_found | COMPONENT: gstack | EXPECTED: $gstack_dir"
  fi

  # gstack (project)
  local gstack_proj="$PROJECT_SKILLS/gstack"
  if [[ -d "$gstack_proj" ]] && [[ -f "$gstack_proj/setup" ]]; then
    echo "VERIFY: ok | COMPONENT: gstack-project | PATH: $gstack_proj"
  fi

  # Superpowers (global)
  local sp_dir="$GLOBAL_SKILLS/superpowers"
  if [[ -d "$sp_dir" ]]; then
    echo "VERIFY: ok | COMPONENT: superpowers | PATH: $sp_dir"
  else
    local found=false
    for pp in "$HOME/.cursor/plugins/cache/cursor-public/superpowers" \
              "$HOME/.claude/plugins/superpowers"; do
      if [[ -d "$pp" ]]; then
        echo "VERIFY: ok | COMPONENT: superpowers-plugin | PATH: $pp"
        found=true
        break
      fi
    done
    if [[ "$found" == "false" ]]; then
      echo "VERIFY: not_found | COMPONENT: superpowers | EXPECTED: $sp_dir or plugin"
    fi
  fi

  # Superpowers (project)
  local sp_proj="$PROJECT_SKILLS/superpowers"
  if [[ -d "$sp_proj" ]]; then
    echo "VERIFY: ok | COMPONENT: superpowers-project | PATH: $sp_proj"
  fi
}

# ── Main dispatch ────────────────────────────────────────────────────────────
case "$ACTION" in
  check)
    do_check
    ;;
  install)
    if [[ -z "$SKILLSET" ]]; then
      echo "STATUS: fail | DETAIL: --install requires a skill set name (openspec|gstack|superpowers)"
      exit 1
    fi
    case "$SKILLSET" in
      openspec)     install_openspec "$SCOPE" ;;
      gstack)       install_gstack "$SCOPE" ;;
      superpowers)  install_superpowers "$SCOPE" ;;
      *)            echo "STATUS: fail | DETAIL: Unknown skill set: $SKILLSET"; exit 1 ;;
    esac
    ;;
  verify)
    do_verify
    ;;
  *)
    echo "STATUS: fail | DETAIL: No action specified. Use --check, --install <name>, or --verify"
    exit 1
    ;;
esac
