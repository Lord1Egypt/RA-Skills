#!/usr/bin/env bash
# shellbot-creative-studio — Remotion project bootstrap
# Usage: remotion_init --template <name> [--name <composition-id>] [--output <dir>]
#                      [--include-rule-assets] [--no-install] [--no-verify]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/lib/config.sh"
source "${SCRIPT_DIR}/lib/output.sh"

TEMPLATE=""
COMP_NAME=""
OUTPUT_DIR=""
INCLUDE_RULES=false
DO_INSTALL=true
DO_VERIFY=true

AVAILABLE_TEMPLATES=(
  "aida-classic-16x9"
  "cinematic-product-16x9"
  "saas-metrics-16x9"
  "mobile-ugc-9x16"
  "blank-16x9"
  "explainer-16x9"
)

usage() {
  cat >&2 <<EOF
Usage: remotion_init --template <name> [options]

Templates:
  aida-classic-16x9       AIDA product marketing (default, 1920x1080)
  cinematic-product-16x9   Dramatic product launch (1920x1080)
  saas-metrics-16x9        B2B dashboard metrics (1920x1080)
  mobile-ugc-9x16          Vertical social / Reels (1080x1920)
  blank-16x9               Minimal starter (1920x1080)
  explainer-16x9           How-it-works 5-scene (1920x1080)

Options:
  --template            Template name (required)
  --name                Custom composition ID (default: from template)
  --output              Target directory (default: ./remotion-project)
  --include-rule-assets Copy Remotion rule code snippets to src/rule-assets/
  --no-install          Skip npm install
  --no-verify           Skip Remotion composition verify
  --list                List available templates and exit
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --template)            TEMPLATE="$2"; shift 2 ;;
    --name)                COMP_NAME="$2"; shift 2 ;;
    --output)              OUTPUT_DIR="$2"; shift 2 ;;
    --include-rule-assets) INCLUDE_RULES=true; shift ;;
    --no-install)          DO_INSTALL=false; shift ;;
    --no-verify)           DO_VERIFY=false; shift ;;
    --list)
      echo "Available templates:"
      for t in "${AVAILABLE_TEMPLATES[@]}"; do
        echo "  - $t"
      done
      exit 0
      ;;
    -h|--help) usage; exit 0 ;;
    *)         log_error "Unknown option: $1"; usage; exit 1 ;;
  esac
done

if [[ -z "$TEMPLATE" ]]; then
  log_error "--template is required"
  usage
  exit 1
fi

# Validate template
TEMPLATE_DIR="${TEMPLATES_DIR}/${TEMPLATE}"
if [[ ! -d "$TEMPLATE_DIR" ]]; then
  log_error "Template '${TEMPLATE}' not found at ${TEMPLATE_DIR}"
  log_error "Available templates:"
  for t in "${AVAILABLE_TEMPLATES[@]}"; do
    log_error "  - $t"
  done
  exit 1
fi

OUTPUT_DIR="${OUTPUT_DIR:-./remotion-project}"

if [[ -d "$OUTPUT_DIR" && "$(ls -A "$OUTPUT_DIR" 2>/dev/null)" ]]; then
  log_warn "Target directory ${OUTPUT_DIR} already exists and is not empty"
fi

# Copy template
log_info "Bootstrapping from template: ${TEMPLATE}"
mkdir -p "$OUTPUT_DIR"
cp -R "${TEMPLATE_DIR}/"* "$OUTPUT_DIR/"
cp -R "${TEMPLATE_DIR}/".[!.]* "$OUTPUT_DIR/" 2>/dev/null || true

log_ok "Template copied to ${OUTPUT_DIR}"

# Rename composition ID if requested
if [[ -n "$COMP_NAME" ]]; then
  log_info "Renaming composition to: ${COMP_NAME}"

  # Update Root.tsx composition id
  if [[ -f "${OUTPUT_DIR}/src/Root.tsx" ]]; then
    sed -i '' "s/id=\"[^\"]*\"/id=\"${COMP_NAME}\"/" "${OUTPUT_DIR}/src/Root.tsx" 2>/dev/null || true
  fi

  # Update package.json render script
  if [[ -f "${OUTPUT_DIR}/package.json" ]]; then
    # Update render command to use new composition name
    sed -i '' "s/remotion render src\/index.ts [^ ]*/remotion render src\/index.ts ${COMP_NAME}/" "${OUTPUT_DIR}/package.json" 2>/dev/null || true
  fi
fi

# Copy rule assets if requested
if [[ "$INCLUDE_RULES" == "true" ]]; then
  local rules_assets="${SKILL_DIR}/references/remotion-rules/assets"
  if [[ -d "$rules_assets" ]]; then
    log_info "Copying Remotion rule assets..."
    mkdir -p "${OUTPUT_DIR}/src/rule-assets"
    cp -R "${rules_assets}/"* "${OUTPUT_DIR}/src/rule-assets/" 2>/dev/null || true
    log_ok "Rule assets copied to src/rule-assets/"
  fi
fi

# Install dependencies
if [[ "$DO_INSTALL" == "true" ]]; then
  log_info "Installing dependencies..."
  (cd "$OUTPUT_DIR" && npm install --loglevel=error)
  log_ok "Dependencies installed"
fi

# Verify compositions
if [[ "$DO_VERIFY" == "true" && "$DO_INSTALL" == "true" ]]; then
  log_info "Verifying Remotion compositions..."
  if (cd "$OUTPUT_DIR" && npm run verify 2>/dev/null); then
    log_ok "Compositions verified"
  else
    log_warn "Composition verification failed — check your template"
  fi
fi

json_output "$(json_build status=completed template="$TEMPLATE" output_dir="$OUTPUT_DIR" composition="${COMP_NAME:-default}")"
