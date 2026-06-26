#!/bin/bash

# Vercel Deployment Monitor
# Checks for new deployments and triggers health checks
#
# Usage: ./vercel-monitor.sh --token TOKEN [--project NAME] [--since MINUTES] [--team-id ID]
#
# SECURITY NOTE:
# This script requires a Vercel API token with 'deployment:read' scope.
# Only use tokens from your own Vercel account. Do not use this script
# to access deployments you do not own or have permission to monitor.
#
# By using this script, you agree to Vercel's Terms of Service and
# Acceptable Use Policy: https://vercel.com/legal/terms

set -euo pipefail

# Default values
VERCEL_TOKEN_ENV="${VERCEL_TOKEN:-}"  # Capture environment variable before we overwrite it
VERCEL_TOKEN=""
PROJECT_NAME=""
SINCE_MINUTES=5
TEAM_ID=""
API_BASE="https://api.vercel.com"
VERBOSE=false
JSON_OUTPUT=false

# Colors for output (detect terminal support)
if [[ -t 1 ]] && [[ "$(tput colors)" -ge 8 ]]; then
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  YELLOW='\033[1;33m'
  BLUE='\033[0;34m'
  NC='\033[0m' # No Color
else
  RED=''
  GREEN=''
  YELLOW=''
  BLUE=''
  NC=''
fi

# Function to print usage
usage() {
  echo -e "${BLUE}Vercel Deployment Monitor${NC}"
  echo -e "${BLUE}========================${NC}"
  echo "Usage: $0 [OPTIONS]"
  echo ""
  echo "Options:"
  echo "  --token TOKEN      Vercel API token (required, can also be set via VERCEL_TOKEN environment variable)"
  echo "  --project NAME     Project name to monitor (default: auto-detect)"
  echo "  --since MINUTES    Check deployments from last N minutes (default: 5)"
  echo "  --team-id ID       Team ID for organization accounts"
  echo "  --verbose          Enable verbose output"
  echo "  --json             Output results as JSON"
  echo "  --help             Show this help message"
  echo ""
  echo "Example:"
  echo "  $0 --token vcp_abc123 --project your-project --since 10"
  echo ""
}

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --token)
      VERCEL_TOKEN="$2"
      shift 2
      ;;
    --project)
      PROJECT_NAME="$2"
      shift 2
      ;;
    --since)
      SINCE_MINUTES="$2"
      shift 2
      ;;
    --team-id)
      TEAM_ID="$2"
      shift 2
      ;;
    --verbose)
      VERBOSE=true
      shift
      ;;
    --json)
      JSON_OUTPUT=true
      shift
      ;;
    --help)
      usage
      exit 0
      ;;
    *)
      echo -e "${RED}Unknown option: $1${NC}"
      usage
      exit 1
      ;;
  esac
done

# Validate required arguments
if [[ -z "$VERCEL_TOKEN" ]]; then
  # Check environment variable as fallback
  if [[ -n "${VERCEL_TOKEN_ENV:-}" ]]; then
    VERCEL_TOKEN="$VERCEL_TOKEN_ENV"
    echo -e "${YELLOW}Using Vercel token from environment variable${NC}"
  else
    echo -e "${RED}Error: --token is required (or set VERCEL_TOKEN environment variable)${NC}"
    usage
    exit 1
  fi
fi

# Function to log messages
log() {
  if [[ "$VERBOSE" == "true" ]] || [[ "$1" == "ERROR" ]]; then
    local level="$1"
    local message="$2"
    
    case "$level" in
      INFO)
        echo -e "${BLUE}[INFO]${NC} $message"
        ;;
      SUCCESS)
        echo -e "${GREEN}[SUCCESS]${NC} $message"
        ;;
      WARNING)
        echo -e "${YELLOW}[WARNING]${NC} $message"
        ;;
      ERROR)
        echo -e "${RED}[ERROR]${NC} $message" >&2
        ;;
    esac
  fi
}

# Function to make API calls
api_call() {
  local endpoint="$1"
  local query_params="$2"
  
  local url="${API_BASE}${endpoint}"
  if [[ -n "$query_params" ]]; then
    url="${url}?${query_params}"
  fi
  
  if [[ "$VERBOSE" == "true" ]]; then
    log "INFO" "API call: curl -s -H 'Authorization: Bearer ***' '$url'"
  fi
  
  curl -s -H "Authorization: Bearer $VERCEL_TOKEN" "$url"
}

# Calculate timestamp for --since parameter
calculate_since_timestamp() {
  local minutes="$1"
  local now_ms
  now_ms=$(date +%s%3N)  # Milliseconds since epoch
  local since_ms=$((now_ms - (minutes * 60 * 1000)))
  echo "$since_ms"
}

# Main monitoring function
monitor_deployments() {
  log "INFO" "Checking for deployments in the last $SINCE_MINUTES minutes..."
  
  # Build query parameters
  local query_params="limit=10"
  local since_timestamp
  since_timestamp=$(calculate_since_timestamp "$SINCE_MINUTES")
  query_params="${query_params}&since=${since_timestamp}"
  
  if [[ -n "$TEAM_ID" ]]; then
    query_params="${query_params}&teamId=${TEAM_ID}"
  fi
  
  if [[ -n "$PROJECT_NAME" ]]; then
    query_params="${query_params}&app=${PROJECT_NAME}"
  fi
  
  # Get deployments
  local response
  response=$(api_call "/v6/deployments" "$query_params")
  
  # Check for API errors
  if echo "$response" | jq -e '.error' >/dev/null 2>&1; then
    local error_msg
    error_msg=$(echo "$response" | jq -r '.error.message // "Unknown error"')
    log "ERROR" "Vercel API error: $error_msg"
    return 1
  fi
  
  # Parse deployments
  local deployment_count
  deployment_count=$(echo "$response" | jq '.deployments | length' 2>/dev/null || echo "0")
  
  if [[ "$deployment_count" -eq 0 ]]; then
    log "INFO" "No deployments found in the last $SINCE_MINUTES minutes"
    
    if [[ "$JSON_OUTPUT" == "true" ]]; then
      echo '{"deployments": [], "count": 0, "new_deployments": 0}'
    fi
    
    return 0
  fi
  
  log "INFO" "Found $deployment_count deployment(s)"
  
  # Filter for READY deployments (successfully deployed)
  local ready_deployments=0
  local new_deployments=()
  
  for i in $(seq 0 $((deployment_count - 1))); do
    local deployment
    deployment=$(echo "$response" | jq -c ".deployments[$i]" 2>/dev/null)
    
    if [[ -n "$deployment" ]]; then
      local state
      local name
      local url
      local created
      
      state=$(echo "$deployment" | jq -r '.state // ""')
      name=$(echo "$deployment" | jq -r '.name // ""')
      url=$(echo "$deployment" | jq -r '.url // ""')
      created=$(echo "$deployment" | jq -r '.created // ""')
      
      if [[ "$VERBOSE" == "true" ]]; then
        log "INFO" "Deployment: $name (state: $state, url: $url, created: $created)"
      fi
      
      if [[ "$state" == "READY" ]] && [[ -n "$url" ]]; then
        ((ready_deployments++))
        new_deployments+=("$url")
        
        log "SUCCESS" "✅ Ready deployment: $name ($url)"
      elif [[ "$state" == "ERROR" ]]; then
        log "ERROR" "❌ Failed deployment: $name"
      elif [[ "$state" == "BUILDING" ]] || [[ "$state" == "INITIALIZING" ]]; then
        log "INFO" "⏳ In-progress deployment: $name (state: $state)"
      fi
    fi
  done
  
  # Output results
  if [[ "$JSON_OUTPUT" == "true" ]]; then
    local json_result="{\"deployments\": $deployment_count, \"ready_deployments\": $ready_deployments, \"urls\": ["
    
    for url in "${new_deployments[@]}"; do
      json_result="${json_result}\"$url\","
    done
    
    # Remove trailing comma
    json_result="${json_result%,}]}"
    echo "$json_result"
  else
    echo -e "${BLUE}📊 Monitoring Results${NC}"
    echo -e "${BLUE}===================${NC}"
    echo -e "Total deployments found: $deployment_count"
    echo -e "Ready deployments: $ready_deployments"
    
    if [[ "$ready_deployments" -gt 0 ]]; then
      echo -e "${GREEN}✅ New deployments ready for health checks:${NC}"
      for url in "${new_deployments[@]}"; do
        echo "  - $url"
      done
    fi
  fi
  
  # Return success if we found any ready deployments
  if [[ "$ready_deployments" -gt 0 ]]; then
    return 0
  else
    return 2  # No new ready deployments (not an error, just nothing new)
  fi
}

# Main execution
if [[ "$JSON_OUTPUT" != "true" ]]; then
  echo -e "${BLUE}🚀 Vercel Deployment Monitor${NC}"
  echo -e "${BLUE}==========================${NC}"
  echo -e "Project: ${PROJECT_NAME:-auto-detect}"
  echo -e "Time window: last $SINCE_MINUTES minutes"
  echo ""
fi

# Run monitoring
if monitor_deployments; then
  if [[ "$JSON_OUTPUT" != "true" ]]; then
    echo ""
    echo -e "${GREEN}✅ Monitoring completed successfully${NC}"
  fi
  exit 0
else
  exit_code=$?
  if [[ "$JSON_OUTPUT" != "true" ]]; then
    echo ""
    if [[ $exit_code -eq 2 ]]; then
      echo -e "${YELLOW}⚠️  No new ready deployments found${NC}"
    else
      echo -e "${RED}❌ Monitoring failed${NC}"
    fi
  fi
  exit $exit_code
fi