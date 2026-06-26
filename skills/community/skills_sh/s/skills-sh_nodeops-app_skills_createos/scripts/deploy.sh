#!/bin/bash
#
# CreateOS Deployment Script
# Usage: ./deploy.sh <command> [options]
#
# Commands:
#   create-project    Create a new project
#   deploy            Trigger deployment
#   upload            Upload files to deploy
#   status            Check deployment status
#   logs              View deployment logs
#   env-vars          Update environment variables
#   list-projects     List all projects
#   list-deployments  List deployments for a project
#

set -euo pipefail

# Configuration
API_BASE="${CREATEOS_API_URL:-https://api-createos.nodeops.network}"
API_KEY="${CREATEOS_API_KEY}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

check_api_key() {
    if [ -z "$API_KEY" ]; then
        log_error "CREATEOS_API_KEY environment variable is not set"
    fi
}

api_call() {
    local method=$1
    local endpoint=$2
    local data=$3
    
    local url="${API_BASE}${endpoint}"
    local curl_args=(-sS -X "$method" -H "X-Api-Key: $API_KEY" -H "Content-Type: application/json")
    
    if [ -n "$data" ]; then
        curl_args+=(-d "$data")
    fi
    
    curl "${curl_args[@]}" "$url"
}

api_jq() {
    # Print jq output and fail fast if API returned status=fail.
    # Many CreateOS endpoints return HTTP 200 even for application-level failures.
    local response
    response=$(api_call "$1" "$2" "${3:-}")
    local ok
    ok=$(echo "$response" | jq -r 'if type=="object" and has("status") then .status else "success" end')
    if [ "$ok" != "success" ]; then
        local msg
        msg=$(echo "$response" | jq -r '.data // .error.message // .error // .')
        log_error "CreateOS API error: ${msg}"
    fi
    echo "$response"
}

# Commands

cmd_create_project() {
    local name=$1
    local display_name=$2
    local type=${3:-upload}
    local runtime=${4:-node:20}
    local port=${5:-3000}
    
    if [ -z "$name" ] || [ -z "$display_name" ]; then
        echo "Usage: $0 create-project <unique_name> <display_name> [type] [runtime] [port]"
        echo "  type: vcs, image, upload (default: upload)"
        echo "  runtime: node:20, python:3.12, etc (default: node:20)"
        echo "  port: application port (default: 3000)"
        exit 1
    fi
    
    log_info "Creating project: $name"
    
    local payload=$(cat <<EOF
{
    "uniqueName": "$name",
    "displayName": "$display_name",
    "type": "$type",
    "source": {},
    "settings": {
        "runtime": "$runtime",
        "port": $port
    }
}
EOF
)
    
    local response
    response=$(api_jq POST "/v1/projects" "$payload")
    echo "$response" | jq .
    
    local project_id
    project_id=$(echo "$response" | jq -r '.data.id // empty')
    if [ -n "$project_id" ]; then
        log_success "Project created: $project_id"
    else
        log_error "Failed to create project"
    fi
}

cmd_deploy() {
    local project_id=$1
    local branch=${2:-main}
    
    if [ -z "$project_id" ]; then
        echo "Usage: $0 deploy <project_id> [branch]"
        exit 1
    fi
    
    log_info "Triggering deployment for project: $project_id (branch: $branch)"
    
    local response
    response=$(api_jq POST "/v1/projects/$project_id/deployments/trigger" "{\"branch\": \"$branch\"}")
    echo "$response" | jq .
    
    local deployment_id
    deployment_id=$(echo "$response" | jq -r '.data.id // empty')
    if [ -n "$deployment_id" ]; then
        log_success "Deployment triggered: $deployment_id"
    fi
}

cmd_deploy_image() {
    local project_id=$1
    local image=$2
    
    if [ -z "$project_id" ] || [ -z "$image" ]; then
        echo "Usage: $0 deploy-image <project_id> <image>"
        echo "  image: Docker image reference (e.g., nginx:latest, myapp:v1.0.0)"
        exit 1
    fi
    
    log_info "Deploying image: $image to project: $project_id"
    
    local response
    response=$(api_jq POST "/v1/projects/$project_id/deployments" "{\"image\": \"$image\"}")
    echo "$response" | jq .
}

cmd_upload() {
    local project_id=$1
    local file_path=$2
    local mode=${3:-base64}
    
    if [ -z "$project_id" ] || [ -z "$file_path" ]; then
        echo "Usage: $0 upload <project_id> <file_or_directory> [base64|text]"
        echo "  base64 (default): PUT /deployments/files/base64 (supports binaries)"
        echo "  text:             PUT /deployments/files (UTF-8 text only)"
        exit 1
    fi

    if [ "$mode" != "base64" ] && [ "$mode" != "text" ]; then
        log_error "Invalid upload mode: $mode (use base64 or text)"
    fi

    local endpoint
    if [ "$mode" = "base64" ]; then
        endpoint="/v1/projects/$project_id/deployments/files/base64"
    else
        endpoint="/v1/projects/$project_id/deployments/files"
    fi
    
    if [ -d "$file_path" ]; then
        log_info "Uploading directory ($mode): $file_path"
    elif [ -f "$file_path" ]; then
        log_info "Uploading file ($mode): $file_path"
    else
        log_error "Path not found: $file_path"
    fi

    # Build payload using python to avoid shell quoting issues.
    # Default ignore patterns are tuned for typical JS/Python repos.
    local payload
    payload=$(python3 - "$file_path" "$mode" <<'PY'
import base64
import json
import os
import sys
from pathlib import Path

root = Path(sys.argv[1])
mode = sys.argv[2]

IGNORE_DIRS = {'.git', 'node_modules', '.next', '.turbo', '.cache', '__pycache__', '.venv', '.agents', '.claude'}
IGNORE_FILES = {'.DS_Store'}

def iter_files(p: Path):
    if p.is_file():
        yield p, Path(p.name)
        return

    for fp in p.rglob('*'):
        if fp.is_dir():
            continue
        rel = fp.relative_to(p)
        parts = rel.parts
        if any(part in IGNORE_DIRS for part in parts):
            continue
        if fp.name in IGNORE_FILES:
            continue
        yield fp, rel

files = []
for fp, rel in iter_files(root):
    if mode == 'base64':
        content = base64.b64encode(fp.read_bytes()).decode('ascii')
    else:
        content = fp.read_text(encoding='utf-8')
    files.append({'path': rel.as_posix(), 'content': content})

if len(files) == 0:
    print(json.dumps({'files': []}))
    sys.exit(0)

if len(files) > 100:
    raise SystemExit(f"Too many files ({len(files)}). CreateOS upload endpoints accept max 100 files per request. Use a VCS project or reduce the upload set.")

print(json.dumps({'files': files}))
PY
)

if [ -z "$payload" ]; then
    log_error "Failed to build upload payload"
fi

log_info "Uploading to CreateOS endpoint: $endpoint"
local response
response=$(api_jq PUT "$endpoint" "$payload")
echo "$response" | jq .
}

cmd_status() {
    local project_id=$1
    local deployment_id=$2
    
    if [ -z "$project_id" ]; then
        echo "Usage: $0 status <project_id> [deployment_id]"
        exit 1
    fi
    
    if [ -n "$deployment_id" ]; then
        log_info "Getting deployment status: $deployment_id"
        api_jq GET "/v1/projects/$project_id/deployments/$deployment_id" | jq .
    else
        log_info "Getting latest deployments for project: $project_id"
        api_jq GET "/v1/projects/$project_id/deployments?limit=5" | jq .
    fi
}

cmd_logs() {
    local project_id=$1
    local deployment_id=$2
    local log_type=${3:-runtime}
    
    if [ -z "$project_id" ] || [ -z "$deployment_id" ]; then
        echo "Usage: $0 logs <project_id> <deployment_id> [build|runtime]"
        exit 1
    fi
    
    log_info "Getting $log_type logs for deployment: $deployment_id"
    
    if [ "$log_type" == "build" ]; then
        api_jq GET "/v1/projects/$project_id/deployments/$deployment_id/logs/build" | jq -r '.data.logs // .data // .'
    else
        api_jq GET "/v1/projects/$project_id/deployments/$deployment_id/logs/runtime?since-seconds=300" | jq -r '.data.logs // .data // .'
    fi
}

cmd_env_vars() {
    local project_id=$1
    local environment_id=$2
    shift 2
    
    if [ -z "$project_id" ] || [ -z "$environment_id" ]; then
        echo "Usage: $0 env-vars <project_id> <environment_id> KEY1=value1 KEY2=value2 ..."
        exit 1
    fi
    
    # Build JSON object from KEY=value pairs
    local env_json="{"
    local first=true
    for pair in "$@"; do
        local key="${pair%%=*}"
        local value="${pair#*=}"
        if [ "$first" = true ]; then
            first=false
        else
            env_json+=","
        fi
        env_json+="\"$key\":\"$value\""
    done
    env_json+="}"
    
    log_info "Updating environment variables for environment: $environment_id"

    # CreateOS currently updates environment settings via PUT /environments/{environment_id}
    # (no dedicated /variables endpoint).
    local current
    current=$(api_jq GET "/v1/projects/$project_id/environments" | jq -c --arg id "$environment_id" '.data[] | select(.id==$id)')
    if [ -z "$current" ]; then
        log_error "Environment not found: $environment_id"
    fi

    local payload
    payload=$(python3 - "$current" "$env_json" <<'PY'
import json
import sys

env_obj = json.loads(sys.argv[1])
new_pairs = json.loads(sys.argv[2])

run_envs = (env_obj.get('settings') or {}).get('runEnvs') or {}
run_envs.update(new_pairs)

payload = {
  'displayName': env_obj.get('displayName'),
  'uniqueName': env_obj.get('uniqueName'),
  'description': env_obj.get('description') or '',
  'branch': env_obj.get('branch'),
  'isAutoPromoteEnabled': bool(env_obj.get('isAutoPromoteEnabled')),
  'resources': env_obj.get('resources') or {'cpu': 200, 'memory': 500, 'replicas': 1},
  'settings': {'runEnvs': run_envs},
}

print(json.dumps(payload))
PY
)

    api_jq PUT "/v1/projects/$project_id/environments/$environment_id" "$payload" | jq .
}

cmd_list_projects() {
    local limit=${1:-10}
    log_info "Listing projects (limit: $limit)"
    api_jq GET "/v1/projects?limit=$limit" | jq .
}

cmd_list_deployments() {
    local project_id=$1
    local limit=${2:-10}
    
    if [ -z "$project_id" ]; then
        echo "Usage: $0 list-deployments <project_id> [limit]"
        exit 1
    fi
    
    log_info "Listing deployments for project: $project_id"
    api_jq GET "/v1/projects/$project_id/deployments?limit=$limit" | jq .
}

cmd_rollback() {
    local project_id=$1
    local environment_id=$2
    local deployment_id=$3
    
    if [ -z "$project_id" ] || [ -z "$environment_id" ] || [ -z "$deployment_id" ]; then
        echo "Usage: $0 rollback <project_id> <environment_id> <deployment_id>"
        exit 1
    fi
    
    log_info "Rolling back environment $environment_id to deployment $deployment_id"
    log_warn "Note: CreateOS may not support pinning deployments on all project types."

    local current
    current=$(api_jq GET "/v1/projects/$project_id/environments" | jq -c --arg id "$environment_id" '.data[] | select(.id==$id)')
    if [ -z "$current" ]; then
        log_error "Environment not found: $environment_id"
    fi

    # Best-effort: update the environment object with a deployment pointer if the API honors it.
    local payload
    payload=$(python3 - "$current" "$deployment_id" <<'PY'
import json
import sys
env_obj = json.loads(sys.argv[1])
dep = sys.argv[2]

payload = {
  'displayName': env_obj.get('displayName'),
  'uniqueName': env_obj.get('uniqueName'),
  'description': env_obj.get('description') or '',
  'branch': env_obj.get('branch'),
  'isAutoPromoteEnabled': bool(env_obj.get('isAutoPromoteEnabled')),
  'resources': env_obj.get('resources') or {'cpu': 200, 'memory': 500, 'replicas': 1},
  'settings': env_obj.get('settings') or {'runEnvs': {}},
  # Include both keys because API variants differ.
  'deploymentId': dep,
  'projectDeploymentId': dep,
}
print(json.dumps(payload))
PY
)

    api_jq PUT "/v1/projects/$project_id/environments/$environment_id" "$payload" | jq .
    log_success "Rollback request submitted"
}

cmd_wake() {
    local project_id=$1
    local deployment_id=$2
    
    if [ -z "$project_id" ] || [ -z "$deployment_id" ]; then
        echo "Usage: $0 wake <project_id> <deployment_id>"
        exit 1
    fi
    
    log_info "Waking deployment: $deployment_id"
    api_jq POST "/v1/projects/$project_id/deployments/$deployment_id/wake" | jq .
}

cmd_analytics() {
    local project_id=$1
    local environment_id=$2
    
    if [ -z "$project_id" ] || [ -z "$environment_id" ]; then
        echo "Usage: $0 analytics <project_id> <environment_id>"
        exit 1
    fi
    
    log_info "Getting analytics for environment: $environment_id"
    api_jq GET "/v1/projects/$project_id/environments/$environment_id/analytics" | jq .
}

# Main
check_api_key

case "${1:-help}" in
    create-project)
        shift
        cmd_create_project "$@"
        ;;
    deploy)
        shift
        cmd_deploy "$@"
        ;;
    deploy-image)
        shift
        cmd_deploy_image "$@"
        ;;
    upload)
        shift
        cmd_upload "$@"
        ;;
    status)
        shift
        cmd_status "$@"
        ;;
    logs)
        shift
        cmd_logs "$@"
        ;;
    env-vars)
        shift
        cmd_env_vars "$@"
        ;;
    list-projects)
        shift
        cmd_list_projects "$@"
        ;;
    list-deployments)
        shift
        cmd_list_deployments "$@"
        ;;
    rollback)
        shift
        cmd_rollback "$@"
        ;;
    wake)
        shift
        cmd_wake "$@"
        ;;
    analytics)
        shift
        cmd_analytics "$@"
        ;;
    help|--help|-h)
        echo "CreateOS Deployment Script"
        echo ""
        echo "Environment Variables:"
        echo "  CREATEOS_API_KEY    Your CreateOS API key (required)"
        echo "  CREATEOS_API_URL    API base URL (default: https://api-createos.nodeops.network)"
        echo ""
        echo "Commands:"
        echo "  create-project <name> <display_name> [type] [runtime] [port]"
        echo "  deploy <project_id> [branch]"
        echo "  deploy-image <project_id> <image>"
        echo "  upload <project_id> <file_or_directory> [base64|text]"
        echo "  status <project_id> [deployment_id]"
        echo "  logs <project_id> <deployment_id> [build|runtime]"
        echo "  env-vars <project_id> <environment_id> KEY=value ..."
        echo "  list-projects [limit]"
        echo "  list-deployments <project_id> [limit]"
        echo "  rollback <project_id> <environment_id> <deployment_id>"
        echo "  wake <project_id> <deployment_id>"
        echo "  analytics <project_id> <environment_id>"
        echo ""
        echo "Examples:"
        echo "  $0 create-project my-app \"My Application\" upload node:20 3000"
        echo "  $0 upload abc123 ./dist base64"
        echo "  $0 deploy abc123 main"
        echo "  $0 logs abc123 def456 build"
        echo "  $0 env-vars abc123 env789 API_KEY=secret DEBUG=true"
        ;;
    *)
        log_error "Unknown command: $1. Use '$0 help' for usage."
        ;;
esac
