#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

info()  { echo -e "${CYAN}[info]${NC} $*"; }
ok()    { echo -e "${GREEN}[ok]${NC} $*"; }
warn()  { echo -e "${YELLOW}[warn]${NC} $*"; }
err()   { echo -e "${RED}[error]${NC} $*" >&2; }

# Template short-name mapping
declare -A TEMPLATES=(
  ["react-hono"]="cloudflare/templates/react-router-hono-fullstack-template"
  ["next"]="cloudflare/templates/next-starter-template"
  ["remix"]="cloudflare/templates/remix-starter-template"
  ["react-router"]="cloudflare/templates/react-router-starter-template"
  ["astro-blog"]="cloudflare/templates/astro-blog-starter-template"
  ["vite-react"]="cloudflare/templates/vite-react-template"
  ["d1"]="cloudflare/templates/d1-template"
  ["saas-admin"]="cloudflare/templates/saas-admin-template"
  ["r2-explorer"]="cloudflare/templates/r2-explorer-template"
  ["llm-chat"]="cloudflare/templates/llm-chat-app-template"
  ["durable-chat"]="cloudflare/templates/durable-chat-template"
  ["containers"]="cloudflare/templates/containers-template"
  ["openauth"]="cloudflare/templates/openauth-template"
  ["postgres"]="cloudflare/templates/postgres-hyperdrive-template"
  ["mysql"]="cloudflare/templates/mysql-hyperdrive-template"
  ["react-postgres"]="cloudflare/templates/react-postgres-fullstack-template"
  ["text-to-image"]="cloudflare/templates/text-to-image-template"
  ["platforms"]="cloudflare/templates/workers-for-platforms-template"
)

DEFAULT_TEMPLATE="react-hono"

usage() {
  echo "Usage: $(basename "$0") <project-name> [options]"
  echo ""
  echo "Options:"
  echo "  --template <name>       Short name or full template path (default: react-hono)"
  echo "  --template-url <url>    Custom template URL (GitHub repo)"
  echo "  --dir <parent-dir>      Parent directory (default: current directory)"
  echo "  --deploy                Deploy after creation (default: no deploy)"
  echo "  --git                   Initialize git repo (default: no git)"
  echo "  --list                  List available template short names"
  echo ""
  echo "All prompts are auto-accepted. No interactivity required."
  echo ""
  echo "Templates: ${!TEMPLATES[*]}"
}

# Parse args
PROJECT_NAME=""
TEMPLATE="$DEFAULT_TEMPLATE"
TEMPLATE_URL=""
PARENT_DIR="."
LIST_TEMPLATES=false
DO_DEPLOY=false
DO_GIT=false

while [[ $# -gt 0 ]]; do
  case "$1" in
    --template) TEMPLATE="$2"; shift 2 ;;
    --template-url) TEMPLATE_URL="$2"; shift 2 ;;
    --dir) PARENT_DIR="$2"; shift 2 ;;
    --deploy) DO_DEPLOY=true; shift ;;
    --git) DO_GIT=true; shift ;;
    --list) LIST_TEMPLATES=true; shift ;;
    -h|--help) usage; exit 0 ;;
    -*) err "Unknown option: $1"; usage; exit 1 ;;
    *) PROJECT_NAME="$1"; shift ;;
  esac
done

if $LIST_TEMPLATES; then
  echo "Available templates:"
  for key in $(echo "${!TEMPLATES[@]}" | tr ' ' '\n' | sort); do
    printf "  %-20s %s\n" "$key" "${TEMPLATES[$key]}"
  done
  exit 0
fi

if [[ -z "$PROJECT_NAME" ]]; then
  err "Project name is required"
  usage
  exit 1
fi

# Resolve template
if [[ -n "$TEMPLATE_URL" ]]; then
  RESOLVED_TEMPLATE="$TEMPLATE_URL"
  info "Using custom template URL: $RESOLVED_TEMPLATE"
elif [[ -n "${TEMPLATES[$TEMPLATE]+x}" ]]; then
  RESOLVED_TEMPLATE="${TEMPLATES[$TEMPLATE]}"
  info "Using template: $TEMPLATE → $RESOLVED_TEMPLATE"
else
  # Assume it's a full template path
  RESOLVED_TEMPLATE="$TEMPLATE"
  info "Using template path: $RESOLVED_TEMPLATE"
fi

# Build C3 flags as array for safe argument handling
C3_ARGS=("-y")  # Accept all defaults, no prompts

if ! $DO_DEPLOY; then
  C3_ARGS+=("--no-deploy")
fi
if ! $DO_GIT; then
  C3_ARGS+=("--no-git")
fi
C3_ARGS+=("--no-open")

# Create project
info "Creating project '$PROJECT_NAME' in $PARENT_DIR/"
info "Flags: ${C3_ARGS[*]}"

cd "$PARENT_DIR"

npm create cloudflare@latest -- "$PROJECT_NAME" --template="$RESOLVED_TEMPLATE" "${C3_ARGS[@]}"

ok "Project created: $PARENT_DIR/$PROJECT_NAME"
echo ""
echo -e "${CYAN}Next steps:${NC}"
echo "  cd $PROJECT_NAME"
echo "  npm run dev           # Start local dev server"
echo "  npm run build         # Build for production"
echo "  wrangler deploy       # Deploy to Cloudflare"
