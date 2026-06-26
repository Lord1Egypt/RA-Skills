#!/usr/bin/env bash
set -euo pipefail

WORKSPACE=${1:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}
CDIR=${WORKSPACE}/eve-work/eve-read-eve-docs
FAILED=0

report() {
  echo "[state-today] $1"
}

have_rg() {
  command -v rg >/dev/null 2>&1
}

assert_no_matches() {
  local pattern=$1
  shift
  local output=""

  if have_rg; then
    if output=$(rg -n "${pattern}" "$@" 2>/dev/null); then
      echo
      echo "[FAIL] Found disallowed content for pattern: ${pattern}"
      printf '%s\n' "${output}"
      FAILED=1
      return
    fi
  else
    local target=$1
    if [ -d "${target}" ]; then
      output=$(find "${target}" -type f -name '*.md' -exec grep -nHE "${pattern}" {} + 2>/dev/null || true)
    else
      output=$(grep -nHE "${pattern}" "$@" 2>/dev/null || true)
    fi
    if [ -n "${output}" ]; then
      echo
      echo "[FAIL] Found disallowed content for pattern: ${pattern}"
      printf '%s\n' "${output}"
      FAILED=1
      return
    fi
  fi

  report "PASS: no matches for ${pattern}"
}

assert_heading() {
  local path=$1
  local heading=$2

  if have_rg; then
    if ! rg -n -F "${heading}" "${path}" >/dev/null 2>&1; then
      echo "[FAIL] Missing heading '${heading}' in ${path}"
      FAILED=1
    else
      report "PASS: ${path} has ${heading}"
    fi
    return
  fi

  if ! grep -nF "${heading}" "${path}" >/dev/null 2>&1; then
    echo "[FAIL] Missing heading '${heading}' in ${path}"
    FAILED=1
  else
    report "PASS: ${path} has ${heading}"
  fi
}

assert_file_exists() {
  local path=$1
  if [ ! -f "${path}" ]; then
    echo "[FAIL] Missing required file: ${path}"
    FAILED=1
  else
    report "PASS: found ${path}"
  fi
}

cd "${WORKSPACE}"

# State-today filtering guard
assert_no_matches "Planned \\(Not Implemented\\)|## Planned|What's next|current vs planned|Planned vs Current" "${CDIR}" -g '*.md'
assert_no_matches "Planned \\(Not Implemented\\)|## Planned|What's next|current vs planned|Planned vs Current" \
  "${CDIR}/references/cli-auth.md" \
  "${CDIR}/references/cli-org-project.md" \
  "${CDIR}/references/cli-jobs.md" \
  "${CDIR}/references/cli-pipelines.md" \
  "${CDIR}/references/cli-deploy-debug.md"

# Progressive-access router checks
assert_heading "${CDIR}/references/overview.md" "## Use When"
assert_heading "${CDIR}/references/jobs.md" "## Load Next"
assert_heading "${WORKSPACE}/eve-work/eve-read-eve-docs/SKILL.md" "## Task Router (Progressive Access)"
assert_heading "${WORKSPACE}/eve-work/eve-read-eve-docs/SKILL.md" "## Intent Coverage Matrix"

# Ensure CLI task modules for split references exist
for module in cli-auth.md cli-org-project.md cli-jobs.md cli-pipelines.md cli-deploy-debug.md; do
  assert_file_exists "${CDIR}/references/${module}"
done

# Ensure every cli task module follows progressive-access entry format
for module in "${CDIR}/references/cli-auth.md" "${CDIR}/references/cli-org-project.md" "${CDIR}/references/cli-jobs.md" "${CDIR}/references/cli-pipelines.md" "${CDIR}/references/cli-deploy-debug.md"; do
  assert_heading "${module}" "## Use When"
  assert_heading "${module}" "## Load Next"
  assert_heading "${module}" "## Ask If Missing"
done

if [ ${FAILED} -ne 0 ]; then
  printf '\n[state-today] Compliance check FAILED\n'
  exit 1
fi

printf '\n[state-today] Compliance check PASSED\n'
