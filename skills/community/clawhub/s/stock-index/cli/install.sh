#!/usr/bin/env bash
set -euo pipefail

MODE="all"
RESTART_GATEWAY=0
SKILLS_PREF="default"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --cli-only)
      MODE="cli"
      shift
      ;;
    --skill-only)
      MODE="skill"
      shift
      ;;
    --plugin-only)
      MODE="plugin"
      shift
      ;;
    --restart-gateway)
      RESTART_GATEWAY=1
      shift
      ;;
    --no-skills)
      SKILLS_PREF="off"
      shift
      ;;
    --with-skills)
      SKILLS_PREF="on"
      shift
      ;;
    -h|--help)
      cat <<'USAGE'
Usage: install.sh [--cli-only|--skill-only|--plugin-only] [--no-skills|--with-skills] [--restart-gateway]

Installs the skillhub CLI.
Default mode installs CLI + workspace skill (find-skill style).
Use --plugin-only only when you explicitly want legacy plugin injection.
Use --no-skills to skip installing workspace skills and persist this preference
for OTA self-upgrade migrations.
USAGE
      exit 0
      ;;
    *)
      echo "Error: unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Supports two archive layouts:
# 1) install.sh at kit root: ./install.sh + ./cli + ./plugin + ./skill
# 2) install.sh inside cli folder: ./cli/install.sh + ./cli/plugin + ./cli/skill + cli files
if [[ -d "${SCRIPT_DIR}/cli" ]]; then
  CLI_SRC_DIR="${SCRIPT_DIR}/cli"
  PLUGIN_SRC_DIR="${SCRIPT_DIR}/plugin"
  SKILL_SRC_DIR="${SCRIPT_DIR}/skill"
else
  CLI_SRC_DIR="${SCRIPT_DIR}"
  PLUGIN_SRC_DIR="${SCRIPT_DIR}/plugin"
  SKILL_SRC_DIR="${SCRIPT_DIR}/skill"
fi

INSTALL_BASE="${HOME}/.skillhub"
BIN_DIR="${HOME}/.local/bin"
CLI_TARGET="${INSTALL_BASE}/skills_store_cli.py"
UPGRADE_MODULE_TARGET="${INSTALL_BASE}/skills_upgrade.py"
VERSION_TARGET="${INSTALL_BASE}/version.json"
METADATA_TARGET="${INSTALL_BASE}/metadata.json"
INDEX_TARGET="${INSTALL_BASE}/skills_index.local.json"
CONFIG_TARGET="${INSTALL_BASE}/config.json"
WRAPPER_TARGET="${BIN_DIR}/skillhub"
LEGACY_WRAPPER_TARGET="${BIN_DIR}/oc-skills"

PLUGIN_TARGET_DIR="${HOME}/.openclaw/extensions/skillhub"
FIND_SKILL_TARGET_DIR="${HOME}/.openclaw/workspace/skills/find-skills"
PREFERENCE_SKILL_TARGET_DIR="${HOME}/.openclaw/workspace/skills/skillhub-preference"

find_openclaw_bin() {
  if command -v openclaw >/dev/null 2>&1; then
    command -v openclaw
    return 0
  fi
  if [[ -x "${HOME}/.local/share/pnpm/openclaw" ]]; then
    echo "${HOME}/.local/share/pnpm/openclaw"
    return 0
  fi
  return 1
}

install_cli() {
  if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: python3 is required for skillhub." >&2
    exit 1
  fi

  mkdir -p "${INSTALL_BASE}" "${BIN_DIR}"
  cp "${CLI_SRC_DIR}/skills_store_cli.py" "${CLI_TARGET}"
  cp "${CLI_SRC_DIR}/skills_upgrade.py" "${UPGRADE_MODULE_TARGET}"
  cp "${CLI_SRC_DIR}/version.json" "${VERSION_TARGET}"
  cp "${CLI_SRC_DIR}/metadata.json" "${METADATA_TARGET}"
  if [[ -f "${CLI_SRC_DIR}/skills_index.local.json" ]]; then
    cp "${CLI_SRC_DIR}/skills_index.local.json" "${INDEX_TARGET}"
  fi
  chmod +x "${CLI_TARGET}"

  if [[ ! -f "${CONFIG_TARGET}" ]]; then
    cat > "${CONFIG_TARGET}" <<'JSON'
{
  "self_update_url": "https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/version.json"
}
JSON
  fi

  cat > "${WRAPPER_TARGET}" <<'WRAPPER'
#!/usr/bin/env bash
set -euo pipefail

BASE="${HOME}/.skillhub"
CLI="${BASE}/skills_store_cli.py"

if [[ ! -f "${CLI}" ]]; then
  echo "Error: CLI not found at ${CLI}" >&2
  exit 1
fi

exec python3 "${CLI}" "$@"
WRAPPER

  chmod +x "${WRAPPER_TARGET}"

  cat > "${LEGACY_WRAPPER_TARGET}" <<'WRAPPER'
#!/usr/bin/env bash
set -euo pipefail
exec "${HOME}/.local/bin/skillhub" "$@"
WRAPPER

  chmod +x "${LEGACY_WRAPPER_TARGET}"
}

set_workspace_skills_preference() {
  local enabled="$1"
  if ! command -v python3 >/dev/null 2>&1; then
    echo "Warn: python3 not found; cannot persist skills preference." >&2
    return 0
  fi

  python3 - "$CONFIG_TARGET" "$enabled" <<'PY'
import json
import sys
from pathlib import Path

config_path = Path(sys.argv[1]).expanduser()
enabled = sys.argv[2].strip().lower() == "true"
default_update_url = "https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/version.json"

raw = {}
if config_path.exists():
    try:
        loaded = json.loads(config_path.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            raw = loaded
    except Exception:
        raw = {}

if not isinstance(raw.get("self_update_url"), str) or not raw["self_update_url"].strip():
    raw["self_update_url"] = default_update_url
raw["install_workspace_skills"] = enabled

config_path.parent.mkdir(parents=True, exist_ok=True)
config_path.write_text(json.dumps(raw, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY
}

install_plugin() {
  mkdir -p "${PLUGIN_TARGET_DIR}"
  cp "${PLUGIN_SRC_DIR}/index.ts" "${PLUGIN_TARGET_DIR}/index.ts"
  cp "${PLUGIN_SRC_DIR}/openclaw.plugin.json" "${PLUGIN_TARGET_DIR}/openclaw.plugin.json"
}

install_skill() {
  local find_skill_src="${SKILL_SRC_DIR}/SKILL.md"
  local preference_skill_src="${SKILL_SRC_DIR}/SKILL.skillhub-preference.md"
  local installed=0

  if [[ -f "${find_skill_src}" ]]; then
    mkdir -p "${FIND_SKILL_TARGET_DIR}"
    cp "${find_skill_src}" "${FIND_SKILL_TARGET_DIR}/SKILL.md"
    installed=1
  else
    echo "Warn: find-skills source not found at ${find_skill_src}; skipped." >&2
  fi

  if [[ -f "${preference_skill_src}" ]]; then
    mkdir -p "${PREFERENCE_SKILL_TARGET_DIR}"
    cp "${preference_skill_src}" "${PREFERENCE_SKILL_TARGET_DIR}/SKILL.md"
    installed=1
  else
    echo "Warn: skillhub-preference source not found at ${preference_skill_src}; skipped." >&2
  fi

  if [[ "${installed}" -ne 1 ]]; then
    echo "Warn: no skill templates installed." >&2
  fi
}

configure_plugin() {
  local openclaw_bin
  if ! openclaw_bin="$(find_openclaw_bin)"; then
    echo "Warn: openclaw not found on PATH; skipped plugin config." >&2
    return 0
  fi

  "${openclaw_bin}" config set plugins.entries.skillhub.enabled true
  "${openclaw_bin}" config set plugins.entries.skillhub.config.primaryCli 'skillhub'
  "${openclaw_bin}" config set plugins.entries.skillhub.config.fallbackCli 'clawhub'
  "${openclaw_bin}" config set plugins.entries.skillhub.config.primaryLabel 'cn-optimized'
  "${openclaw_bin}" config set plugins.entries.skillhub.config.fallbackLabel 'public-registry'
}

disable_plugin_if_present() {
  local openclaw_bin
  if ! openclaw_bin="$(find_openclaw_bin)"; then
    echo "Warn: openclaw not found on PATH; skipped plugin disable." >&2
    return 0
  fi

  # Remove the whole config entry to avoid OpenClaw warning:
  # "plugin disabled (not in allowlist) but config is present".
  if ! "${openclaw_bin}" config unset plugins.entries.skillhub >/dev/null 2>&1; then
    echo "Info: skillhub plugin config entry not found or already removed; skip disable."
  fi
}

restart_gateway_if_needed() {
  if [[ "${RESTART_GATEWAY}" -ne 1 ]]; then
    return 0
  fi

  local openclaw_bin
  if ! openclaw_bin="$(find_openclaw_bin)"; then
    echo "Warn: openclaw not found on PATH; skipped gateway restart." >&2
    return 0
  fi

  nohup "${openclaw_bin}" gateway run --bind loopback --port 18789 --force >/tmp/openclaw-gateway.log 2>&1 &
}

if [[ "${MODE}" == "all" || "${MODE}" == "cli" ]]; then
  install_cli
fi

if [[ "${SKILLS_PREF}" == "off" ]]; then
  set_workspace_skills_preference false
elif [[ "${SKILLS_PREF}" == "on" ]]; then
  set_workspace_skills_preference true
fi

if [[ "${MODE}" == "all" || "${MODE}" == "skill" ]]; then
  if [[ "${SKILLS_PREF}" != "off" ]]; then
    install_skill
  else
    echo "Info: skipped workspace skills installation by --no-skills."
  fi
  disable_plugin_if_present
fi

if [[ "${MODE}" == "plugin" ]]; then
  install_plugin
  configure_plugin
fi

restart_gateway_if_needed

echo "Install complete."
echo "  mode: ${MODE}"
if [[ "${MODE}" == "all" || "${MODE}" == "cli" ]]; then
  echo "  cli: ${WRAPPER_TARGET}"
  if [[ -f "${INDEX_TARGET}" ]]; then
    echo "  index: ${INDEX_TARGET}"
  fi
fi
if [[ "${MODE}" == "all" || "${MODE}" == "skill" ]]; then
  if [[ "${SKILLS_PREF}" != "off" ]]; then
    echo "  skill: ${FIND_SKILL_TARGET_DIR}/SKILL.md"
    echo "  skill: ${PREFERENCE_SKILL_TARGET_DIR}/SKILL.md"
  else
    echo "  skill: skipped (--no-skills)"
  fi
fi
if [[ "${MODE}" == "plugin" ]]; then
  echo "  plugin: ${PLUGIN_TARGET_DIR}"
fi
echo
echo "Quick check:"
if [[ "${MODE}" == "all" || "${MODE}" == "cli" ]]; then
  echo "  skillhub search calendar"
fi
if [[ "${MODE}" == "all" || "${MODE}" == "skill" ]]; then
  if [[ "${SKILLS_PREF}" != "off" ]]; then
    echo "  test -f ${FIND_SKILL_TARGET_DIR}/SKILL.md && echo find-skills-installed"
    echo "  test -f ${PREFERENCE_SKILL_TARGET_DIR}/SKILL.md && echo skillhub-preference-installed"
  else
    echo "  skills install skipped by --no-skills"
  fi
fi
if [[ "${MODE}" == "plugin" ]]; then
  echo "  If you use OpenClaw: openclaw plugins list | grep skillhub"
fi
