#!/usr/bin/env bash
# verify-gate.sh — Safe Change Verify Gate
# Fuhert tsc → lint → test → build in Reihenfolge aus.
# Stoppt beim ersten Fehler. Farbige Ausgabe.
# Read-only: modifiziert keine Quelldateien.
#
# Usage:
#   bash verify-gate.sh [--root <project-root>] [--help]
#
# Exit codes:
#   0 — all checks passed
#   1 — a check failed (details printed above)

set -euo pipefail

# ---- Farben ------------------------------------------------------------
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

# ---- Argumente ---------------------------------------------------------
PROJECT_ROOT="${PWD}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root)
      PROJECT_ROOT="$(realpath "$2")"
      shift 2
      ;;
    --help|-h)
      cat <<EOF
verify-gate.sh — Safe Change Verify Gate

USAGE
  bash verify-gate.sh [options]

OPTIONS
  --root <dir>    Project root (default: current working directory)
  --help          Show this help text

CHECKS (in order)
  1. tsc --noEmit          — TypeScript type-check
  2. npm run lint          — Linter (skipped if script not in package.json)
  3. npm test              — Test suite (skipped if script not in package.json)
  4. npm run build         — Build (skipped if script not in package.json)

EXIT CODES
  0 — all checks passed
  1 — a check failed
EOF
      exit 0
      ;;
    *)
      echo "Unknown argument: $1. Run with --help for usage." >&2
      exit 1
      ;;
  esac
done

# ---- Hilfsfunktionen ---------------------------------------------------

# Prueft ob ein npm-Script in package.json definiert ist
has_npm_script() {
  local script_name="$1"
  local pkg="${PROJECT_ROOT}/package.json"
  if [[ ! -f "$pkg" ]]; then return 1; fi
  # Einfacher grep — kein jq notwendig
  grep -q "\"${script_name}\"" "$pkg"
}

print_header() {
  echo ""
  echo -e "${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${BOLD}${BLUE}  Safe Change — Verify Gate${NC}"
  echo -e "${BOLD}${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "  Root: ${PROJECT_ROOT}"
  echo ""
}

run_check() {
  local label="$1"
  local cmd="$2"
  echo -e "${YELLOW}▶ ${label}${NC}"
  echo -e "  ${cmd}"
  echo ""
  if (cd "${PROJECT_ROOT}" && eval "${cmd}"); then
    echo ""
    echo -e "${GREEN}✓ ${label} passed${NC}"
    echo ""
  else
    echo ""
    echo -e "${RED}✗ ${label} FAILED — stopping gate${NC}"
    echo ""
    exit 1
  fi
}

skip_check() {
  local label="$1"
  local reason="$2"
  echo -e "${YELLOW}○ ${label}${NC} — skipped (${reason})"
  echo ""
}

print_success() {
  echo -e "${BOLD}${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo -e "${BOLD}${GREEN}  All checks passed. Safe to proceed.${NC}"
  echo -e "${BOLD}${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
  echo ""
}

# ---- Gate pruefen ------------------------------------------------------

print_header

# Pruefen ob package.json vorhanden
if [[ ! -f "${PROJECT_ROOT}/package.json" ]]; then
  echo -e "${RED}Error: package.json not found at ${PROJECT_ROOT}${NC}" >&2
  exit 1
fi

# Pruefen ob TypeScript installiert ist
TSC_CMD=""
if [[ -f "${PROJECT_ROOT}/node_modules/.bin/tsc" ]]; then
  TSC_CMD="node_modules/.bin/tsc --noEmit"
elif command -v tsc &>/dev/null; then
  TSC_CMD="tsc --noEmit"
fi

# ---- Check 1: TypeScript -----------------------------------------------
if [[ -n "$TSC_CMD" ]] && [[ -f "${PROJECT_ROOT}/tsconfig.json" ]]; then
  run_check "TypeScript (tsc --noEmit)" "${TSC_CMD}"
else
  skip_check "TypeScript" "tsc or tsconfig.json not found"
fi

# ---- Check 2: Lint ------------------------------------------------------
if has_npm_script "lint"; then
  run_check "Lint (npm run lint)" "npm run lint"
else
  skip_check "Lint" "no 'lint' script in package.json"
fi

# ---- Check 3: Tests -----------------------------------------------------
if has_npm_script "test"; then
  run_check "Tests (npm test)" "npm test"
else
  skip_check "Tests" "no 'test' script in package.json"
fi

# ---- Check 4: Build ----------------------------------------------------
if has_npm_script "build"; then
  run_check "Build (npm run build)" "npm run build"
else
  skip_check "Build" "no 'build' script in package.json"
fi

print_success
