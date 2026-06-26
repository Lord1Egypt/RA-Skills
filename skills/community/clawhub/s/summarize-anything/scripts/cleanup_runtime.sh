#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
RUNTIME_DIR="${SKILL_DIR}/runtime"

DRY_RUN=0
INCLUDE_SRC=0
PRUNE_MODELS=0
REMOVE_ALL_MODELS=0
KEEP_MODEL="small"

usage() {
  cat <<'EOF'
Usage: cleanup_runtime.sh [options]

Default behavior:
- remove runtime/cache contents
- remove runtime/work contents
- keep runtime/bin intact
- keep runtime/models intact
- keep runtime/src intact

Options:
  --dry-run          Show what would be removed without deleting it
  --include-src      Also remove runtime/src contents
  --prune-models     Remove model files except the one named by --keep-model
  --all-models       Remove all model files in runtime/models
  --keep-model NAME  Model to preserve when using --prune-models (default: small)
  --help             Show this message
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --include-src)
      INCLUDE_SRC=1
      shift
      ;;
    --prune-models)
      PRUNE_MODELS=1
      shift
      ;;
    --all-models)
      REMOVE_ALL_MODELS=1
      shift
      ;;
    --keep-model)
      KEEP_MODEL="${2:-}"
      if [[ -z "${KEEP_MODEL}" ]]; then
        echo "--keep-model requires a model name" >&2
        exit 1
      fi
      shift 2
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ "${PRUNE_MODELS}" -eq 1 && "${REMOVE_ALL_MODELS}" -eq 1 ]]; then
  echo "Use either --prune-models or --all-models, not both" >&2
  exit 1
fi

list_entries() {
  local path="$1"
  if [[ ! -d "${path}" ]]; then
    return
  fi
  find "${path}" -mindepth 1 ! -name '.gitkeep' | sort
}

clear_dir() {
  local path="$1"
  if [[ ! -d "${path}" ]]; then
    return
  fi
  if [[ "${DRY_RUN}" -eq 1 ]]; then
    list_entries "${path}"
    return
  fi
  find "${path}" -mindepth 1 ! -name '.gitkeep' -exec rm -rf {} +
}

remove_models() {
  local mode="$1"
  local model_dir="${RUNTIME_DIR}/models"
  if [[ ! -d "${model_dir}" ]]; then
    return
  fi

  local keep_path="${model_dir}/ggml-${KEEP_MODEL}.bin"
  local removed_any=0

  while IFS= read -r model_path; do
    if [[ "${mode}" == "prune" && "${model_path}" == "${keep_path}" ]]; then
      continue
    fi
    removed_any=1
    if [[ "${DRY_RUN}" -eq 1 ]]; then
      printf '%s\n' "${model_path}"
    else
      rm -f "${model_path}"
    fi
  done < <(find "${model_dir}" -maxdepth 1 -type f -name 'ggml-*.bin' | sort)

  if [[ "${removed_any}" -eq 0 && "${DRY_RUN}" -eq 1 ]]; then
    :
  fi
}

printf 'runtime: %s\n' "${RUNTIME_DIR}"

printf '\n[cache]\n'
clear_dir "${RUNTIME_DIR}/cache"

printf '\n[work]\n'
clear_dir "${RUNTIME_DIR}/work"

if [[ "${INCLUDE_SRC}" -eq 1 ]]; then
  printf '\n[src]\n'
  clear_dir "${RUNTIME_DIR}/src"
fi

if [[ "${PRUNE_MODELS}" -eq 1 ]]; then
  printf '\n[models]\n'
  printf 'keeping: ggml-%s.bin\n' "${KEEP_MODEL}"
  remove_models "prune"
fi

if [[ "${REMOVE_ALL_MODELS}" -eq 1 ]]; then
  printf '\n[models]\n'
  remove_models "all"
fi

if [[ "${DRY_RUN}" -eq 1 ]]; then
  printf '\nNo files were deleted.\n'
else
  printf '\nCleanup finished.\n'
fi
