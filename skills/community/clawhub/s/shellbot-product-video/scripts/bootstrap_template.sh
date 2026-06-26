#!/usr/bin/env bash
set -euo pipefail

# Copy a bundled Remotion template into a target directory.
# Usage:
#   ./scripts/bootstrap_template.sh --list
#   ./scripts/bootstrap_template.sh ./my-product-video
#   ./scripts/bootstrap_template.sh --template mobile-ugc-9x16 ./my-product-video
#   ./scripts/bootstrap_template.sh --template saas-metrics-16x9 --include-rule-assets ./my-product-video

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
ASSETS_DIR="${SKILL_DIR}/assets"

DEFAULT_TEMPLATE="aida-classic-16x9"
TEMPLATE_KEY="${DEFAULT_TEMPLATE}"
TARGET_DIR=""
INCLUDE_RULE_ASSETS=false

print_templates() {
  cat <<'EOF'
Available templates:
  - aida-classic-16x9 (default)     -> assets/remotion-product-template
  - cinematic-product-16x9          -> assets/templates/cinematic-product-16x9
  - saas-metrics-16x9               -> assets/templates/saas-metrics-16x9
  - mobile-ugc-9x16                 -> assets/templates/mobile-ugc-9x16
EOF
}

resolve_template_dir() {
  case "$1" in
    aida-classic-16x9)
      echo "${ASSETS_DIR}/remotion-product-template"
      ;;
    cinematic-product-16x9)
      echo "${ASSETS_DIR}/templates/cinematic-product-16x9"
      ;;
    saas-metrics-16x9)
      echo "${ASSETS_DIR}/templates/saas-metrics-16x9"
      ;;
    mobile-ugc-9x16)
      echo "${ASSETS_DIR}/templates/mobile-ugc-9x16"
      ;;
    *)
      echo "Unknown template: $1" >&2
      print_templates >&2
      exit 1
      ;;
  esac
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --list)
      print_templates
      exit 0
      ;;
    --template)
      if [[ $# -lt 2 ]]; then
        echo "--template requires a value" >&2
        exit 1
      fi
      TEMPLATE_KEY="$2"
      shift 2
      ;;
    --include-rule-assets)
      INCLUDE_RULE_ASSETS=true
      shift
      ;;
    -*)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
    *)
      if [[ -n "${TARGET_DIR}" ]]; then
        echo "Unexpected extra argument: $1" >&2
        exit 1
      fi
      TARGET_DIR="$1"
      shift
      ;;
  esac
done

if [[ -z "${TARGET_DIR}" ]]; then
  TARGET_DIR="./product-video-template"
fi

TEMPLATE_DIR="$(resolve_template_dir "${TEMPLATE_KEY}")"

if [[ ! -d "${TEMPLATE_DIR}" ]]; then
  echo "Template directory not found: ${TEMPLATE_DIR}" >&2
  exit 1
fi

if [[ -e "${TARGET_DIR}" ]] && [[ -n "$(ls -A "${TARGET_DIR}" 2>/dev/null || true)" ]]; then
  echo "Target directory exists and is not empty: ${TARGET_DIR}" >&2
  echo "Choose an empty directory or remove existing files." >&2
  exit 1
fi

mkdir -p "${TARGET_DIR}"
cp -R "${TEMPLATE_DIR}/." "${TARGET_DIR}/"

if [[ "${INCLUDE_RULE_ASSETS}" == true ]]; then
  RULE_ASSETS_DIR="${SKILL_DIR}/references/remotion-rules/assets"
  if [[ ! -d "${RULE_ASSETS_DIR}" ]]; then
    echo "Rule assets folder not found: ${RULE_ASSETS_DIR}" >&2
    exit 1
  fi
  mkdir -p "${TARGET_DIR}/src/rule-assets"
  cp -R "${RULE_ASSETS_DIR}/." "${TARGET_DIR}/src/rule-assets/"
  echo "Included rule assets in: ${TARGET_DIR}/src/rule-assets"
fi

echo "Template (${TEMPLATE_KEY}) copied to: ${TARGET_DIR}"
echo "Next:"
echo "  cd ${TARGET_DIR}"
echo "  npm install"
echo "  npm run start"
