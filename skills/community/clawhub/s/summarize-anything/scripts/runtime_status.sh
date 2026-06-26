#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
RUNTIME_DIR="${SKILL_DIR}/runtime"

human_size() {
  local path="$1"
  if [[ ! -e "${path}" ]]; then
    echo "0B"
    return
  fi
  du -sh "${path}" 2>/dev/null | awk '{print $1}'
}

entry_count() {
  local path="$1"
  if [[ ! -d "${path}" ]]; then
    echo "0"
    return
  fi
  find "${path}" -mindepth 1 ! -name '.gitkeep' | wc -l | tr -d ' '
}

printf 'runtime: %s\n' "${RUNTIME_DIR}"
printf 'total:   %s\n' "$(human_size "${RUNTIME_DIR}")"
printf '\n'
printf '%-10s %-8s %s\n' "section" "size" "entries"

for section in bin models cache src work; do
  section_path="${RUNTIME_DIR}/${section}"
  printf '%-10s %-8s %s\n' "${section}" "$(human_size "${section_path}")" "$(entry_count "${section_path}")"
done

if find "${RUNTIME_DIR}/models" -maxdepth 1 -type f -name 'ggml-*.bin' | grep -q .; then
  printf '\nmodels:\n'
  while IFS= read -r model_path; do
    printf -- '- %s (%s)\n' "$(basename "${model_path}")" "$(human_size "${model_path}")"
  done < <(find "${RUNTIME_DIR}/models" -maxdepth 1 -type f -name 'ggml-*.bin' | sort)
fi
