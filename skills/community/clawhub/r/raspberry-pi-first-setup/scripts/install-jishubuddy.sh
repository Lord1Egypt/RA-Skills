#!/usr/bin/env bash
set -euo pipefail

readonly REGISTRY="https://registry.npmjs.org/"
readonly PACKAGE="jishubuddy"
readonly VERSION_PATTERN='^[0-9]+\.[0-9]+\.[0-9]+(-[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?(\+[0-9A-Za-z-]+(\.[0-9A-Za-z-]+)*)?$'

fail() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

detect_platform() {
  local os
  local arch
  os="$(uname -s)"
  arch="$(uname -m)"

  case "${os}:${arch}" in
    Linux:x86_64) printf 'linux-x64\n' ;;
    Linux:aarch64|Linux:arm64) printf 'linux-arm64\n' ;;
    Darwin:arm64) printf 'darwin-arm64\n' ;;
    *)
      fail "Unsupported platform ${os}/${arch}. Native Windows, macOS x64, and 32-bit ARM are not supported."
      ;;
  esac
}

require_toolchain() {
  command -v node >/dev/null 2>&1 || fail "Node.js 22 or newer is required."
  command -v npm >/dev/null 2>&1 || fail "npm is required."

  local node_major
  node_major="$(node -p 'Number(process.versions.node.split(".")[0])')"
  [[ "${node_major}" =~ ^[0-9]+$ ]] || fail "Could not determine the Node.js version."
  (( node_major >= 22 )) || fail "Node.js 22 or newer is required; found $(node --version)."
}

validate_version() {
  [[ "${1}" =~ ${VERSION_PATTERN} ]] ||
    fail "Expected an exact package version, found: ${1}"
}

installed_version() {
  if command -v jishubuddy >/dev/null 2>&1; then
    local version
    version="$(jishubuddy --version)" ||
      fail "JishuBuddy is on PATH, but its version command failed. Check the existing installation."
    version="${version//$'\r'/}"
    version="${version#jishubuddy }"
    validate_version "${version}"
    printf '%s\n' "${version}"
  else
    printf 'not installed\n'
  fi
}

latest_version() {
  local version
  version="$(npm view "${PACKAGE}" version --registry="${REGISTRY}")" ||
    fail "Could not query the npm target version."
  validate_version "${version}"
  printf '%s\n' "${version}"
}

main() {
  local action="${1:-check}"
  local target=""
  case "${action}" in
    check)
      (( $# <= 1 )) ||
        fail "Usage: install-jishubuddy.sh check"
      ;;
    install)
      [[ $# -eq 4 && "${2:-}" == "--yes" && "${3:-}" == "--version" ]] ||
        fail "Installation requires approval: install --yes --version <approved-version>"
      target="${4}"
      validate_version "${target}"
      ;;
    *)
      fail "Usage: install-jishubuddy.sh check | install --yes --version <approved-version>"
      ;;
  esac

  local platform
  local current
  local prefix
  platform="$(detect_platform)"
  require_toolchain
  current="$(installed_version)"
  if [[ "${action}" == "check" ]]; then
    target="$(latest_version)"
  fi
  prefix="$(npm prefix --global)"

  printf 'Platform: %s\n' "${platform}"
  printf 'Current version: %s\n' "${current}"
  printf 'Target version: %s\n' "${target}"
  printf 'Registry: %s\n' "${REGISTRY}"
  printf 'Global prefix: %s\n' "${prefix}"
  printf 'Install command: npm install --global %s@%s --registry=%s --ignore-scripts --no-audit --no-fund\n' \
    "${PACKAGE}" "${target}" "${REGISTRY}"

  if [[ "${action}" == "check" ]]; then
    printf 'Reuse a compatible existing installation; a newer target alone does not require an upgrade.\n'
    return 0
  fi

  if [[ "${current}" == "${target}" ]]; then
    printf 'Requested version is already available on PATH; reusing %s.\n' "${current}"
    return 0
  fi

  npm install --global "${PACKAGE}@${target}" \
    --registry="${REGISTRY}" \
    --ignore-scripts \
    --no-audit \
    --no-fund

  command -v jishubuddy >/dev/null 2>&1 ||
    fail "npm completed, but jishubuddy is not on PATH. Check the npm global prefix: ${prefix}"

  current="$(installed_version)"
  [[ "${current}" == "${target}" ]] ||
    fail "Expected ${target}, but PATH resolves to ${current}. Check the npm global prefix: ${prefix}"
  printf 'Installed version: %s\n' "${current}"
  printf 'JishuBuddy was not launched. Run jishubuddy when ready.\n'
}

main "$@"
