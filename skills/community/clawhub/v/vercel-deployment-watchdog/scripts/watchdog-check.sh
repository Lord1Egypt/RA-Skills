#!/bin/bash

# Deployment Watchdog - Vercel API Enhanced
# Checks deployment health with accurate Vercel API detection (no false positives)
# Falls back to cache-header detection when Vercel token not available
#
# Usage: ./watchdog-check.sh [--homepage URL] [--api URL] [--vercel-token TOKEN] [--project-id ID] [--team-id ID] [--state-file PATH] [--verbose] [--help]
# Defaults: homepage=https://your-site.com/, api=https://your-site.com/api/feed
# Vercel token can also be set via VERCEL_TOKEN environment variable

set -euo pipefail

# Detect if terminal supports colors
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

# Default URLs (should be provided via --homepage and --api arguments)
HOMEPAGE_URL=""
API_URL=""
# Allow internal URL monitoring only when explicitly permitted via environment variable
if [[ -n "${ALLOW_INTERNAL:-}" ]]; then
    SKIP_VALIDATION=true
    echo "Warning: Internal URL validation disabled via ALLOW_INTERNAL environment variable"
else
    SKIP_VALIDATION=false
fi
VERBOSE=false
JSON_OUTPUT=false

# Vercel API settings (optional)
VERCEL_TOKEN_ENV="${VERCEL_TOKEN:-}"  # Capture environment variable before we overwrite it
VERCEL_TOKEN=""
VERCEL_PROJECT_ID="${VERCEL_PROJECT_ID:-}"
VERCEL_TEAM_ID="${VERCEL_TEAM_ID:-}"
STATE_FILE="${WATCHDOG_STATE_FILE:-$HOME/.openclaw/workspace/state/watchdog-state.json}"
NEW_DEPLOYMENT=false
DEPLOYMENT_DETECTION_METHOD="none"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --homepage)
      HOMEPAGE_URL="$2"
      shift 2
      ;;
    --api)
      API_URL="$2"
      shift 2
      ;;
    --vercel-token)
      VERCEL_TOKEN="$2"
      shift 2
      ;;
    --project-id)
      VERCEL_PROJECT_ID="$2"
      shift 2
      ;;
    --team-id)
      VERCEL_TEAM_ID="$2"
      shift 2
      ;;
    --state-file)
      STATE_FILE="$2"
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
      echo "Usage: $0 [OPTIONS]"
      echo ""
      echo "Monitor deployment health with accurate Vercel API detection (no false positives)"
      echo "Falls back to cache-header detection when Vercel token not available"
      echo ""
      echo "Required:"
      echo "  --homepage URL    Homepage URL to check"
      echo "  --api URL         API feed URL to check"
      echo ""
      echo "Optional Vercel API (recommended for accurate detection):"
      echo "  --vercel-token TOKEN   Vercel API token (or set VERCEL_TOKEN env var)"
      echo "  --project-id ID        Vercel project ID (or set VERCEL_PROJECT_ID env var)"
      echo "  --team-id ID           Team ID for organization accounts"
      echo "  --state-file PATH      Path to store deployment state (default: ~/.openclaw/workspace/state/watchdog-state.json)"
      echo ""
      echo "Other options:"
      echo "  --verbose              Enable verbose output"
      echo "  --json                 Output results as JSON"
      echo "  --help                 Show this help message"
      echo ""
      echo "Security note: Only monitor sites you own. Internal/private URL checks are enabled by default."
      echo "To bypass security checks for internal resources, set ALLOW_INTERNAL=true env var."
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      echo "Use --help for usage information"
      exit 1
      ;;
  esac
done

# Validate required URLs
if [[ -z "$HOMEPAGE_URL" ]]; then
    echo "Error: --homepage URL is required"
    echo "Use --help for usage information"
    exit 1
fi

if [[ -z "$API_URL" ]]; then
    echo "Error: --api URL is required"
    echo "Use --help for usage information"
    exit 1
fi

# Use environment variable token if not provided via CLI
if [[ -z "$VERCEL_TOKEN" ]] && [[ -n "${VERCEL_TOKEN_ENV:-}" ]]; then
    VERCEL_TOKEN="$VERCEL_TOKEN_ENV"
fi

# URL Validation (Security Check)
validate_url() {
    local url="$1"
    local type="$2"
    
    if [[ "$SKIP_VALIDATION" == "true" ]]; then
        return 0
    fi
    
    # Ensure URL starts with http:// or https://
    if [[ ! "$url" =~ ^https?:// ]]; then
        echo -e "${RED}Error: ${type} URL must start with http:// or https://${NC}"
        exit 1
    fi
    
    # Extract hostname from URL
    local hostname
    hostname=$(echo "$url" | sed -E 's|^https?://([^:/]+).*$|\1|')
    
    # DNS resolution check (optional, can be slow)
    # local ip
    # ip=$(dig +short "$hostname" 2>/dev/null | head -1)
    
    # Block localhost and private IP patterns in hostname
    if [[ "$hostname" =~ localhost|127\.0\.0\.1|0\.0\.0\.0 ]]; then
        echo -e "${YELLOW}Warning: Local address detected in ${type} URL. Use ALLOW_INTERNAL=true if this is intentional.${NC}"
        if [[ "$VERBOSE" == "true" ]]; then
            echo "URL: $url"
        else
            exit 1
        fi
    fi
    
    # Block private IP ranges (RFC 1918) in hostname
    # 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
    if [[ "$hostname" =~ ^10\. ]] ||
       [[ "$hostname" =~ ^172\.(1[6-9]|2[0-9]|3[0-1])\. ]] ||
       [[ "$hostname" =~ ^192\.168\. ]]; then
        echo -e "${RED}Error: Private IP address detected in ${type} URL. Use ALLOW_INTERNAL=true only if you have permission.${NC}"
        if [[ "$VERBOSE" == "true" ]]; then
            echo "URL: $url"
        else
            exit 1
        fi
    fi
    
    # Additional security: Check for common internal domains
    if [[ "$hostname" =~ \.local$|\.internal$|\.lan$|\.home$ ]]; then
        echo -e "${YELLOW}Warning: Internal domain detected in ${type} URL. Use ALLOW_INTERNAL=true if this is intentional.${NC}"
        if [[ "$VERBOSE" == "true" ]]; then
            echo "URL: $url"
        fi
    fi
}

validate_url "$HOMEPAGE_URL" "Homepage"
validate_url "$API_URL" "API"

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

# Function to load state from file
load_state() {
    local state_file="$1"
    
    if [[ -f "$state_file" ]]; then
        cat "$state_file" 2>/dev/null || echo '{}'
    else
        echo '{}'
    fi
}

# Function to save state to file
save_state() {
    local state_file="$1"
    local state_json="$2"
    
    # Create directory if it doesn't exist
    mkdir -p "$(dirname "$state_file")"
    echo "$state_json" > "$state_file"
}

# Function to check for new deployment via Vercel API
check_vercel_deployment() {
    local token="$1"
    local project_id="$2"
    local team_id="$3"
    local state_file="$4"
    
    if [[ -z "$token" ]]; then
        log "INFO" "No Vercel token provided, skipping API detection"
        DEPLOYMENT_DETECTION_METHOD="cache"
        return 2
    fi
    
    log "INFO" "Checking Vercel API for new deployments..."
    
    # Load current state
    local current_state
    current_state=$(load_state "$state_file")
    local last_timestamp
    last_timestamp=$(echo "$current_state" | jq -r '.lastDeploymentTimestamp // 0')
    
    # Build API query
    local api_url="https://api.vercel.com/v6/deployments"
    local query_params="limit=1&state=READY"
    
    if [[ -n "$project_id" ]]; then
        query_params="${query_params}&projectId=${project_id}"
    fi
    
    if [[ -n "$team_id" ]]; then
        query_params="${query_params}&teamId=${team_id}"
    fi
    
    # Make API call
    local response
    response=$(curl -s -H "Authorization: Bearer $token" "${api_url}?${query_params}" 2>/dev/null || true)
    
    # Check for API errors
    if echo "$response" | jq -e '.error' >/dev/null 2>&1; then
        local error_msg
        error_msg=$(echo "$response" | jq -r '.error.message // "Unknown error"')
        log "ERROR" "Vercel API error: $error_msg"
        DEPLOYMENT_DETECTION_METHOD="cache"
        return 1
    fi
    
    # Parse deployments
    local deployment_count
    deployment_count=$(echo "$response" | jq '.deployments | length' 2>/dev/null || echo "0")
    
    if [[ "$deployment_count" -eq 0 ]]; then
        log "INFO" "No READY deployments found via Vercel API"
        DEPLOYMENT_DETECTION_METHOD="cache"
        return 2
    fi
    
    # Get latest deployment
    local latest_deployment
    latest_deployment=$(echo "$response" | jq -c '.deployments[0]' 2>/dev/null)
    
    if [[ -z "$latest_deployment" ]]; then
        log "WARNING" "Failed to parse Vercel API response"
        DEPLOYMENT_DETECTION_METHOD="cache"
        return 1
    fi
    
    local deployment_timestamp
    local deployment_state
    local deployment_url
    local deployment_name
    
    deployment_timestamp=$(echo "$latest_deployment" | jq -r '.created // 0')
    deployment_state=$(echo "$latest_deployment" | jq -r '.state // ""')
    deployment_url=$(echo "$latest_deployment" | jq -r '.url // ""')
    deployment_name=$(echo "$latest_deployment" | jq -r '.name // ""')
    
    if [[ "$deployment_state" != "READY" ]]; then
        log "INFO" "Latest deployment is not READY (state: $deployment_state)"
        DEPLOYMENT_DETECTION_METHOD="cache"
        return 2
    fi
    
    # Compare timestamps
    if [[ "$deployment_timestamp" -gt "$last_timestamp" ]]; then
        log "SUCCESS" "✅ New deployment detected via Vercel API: $deployment_name ($deployment_url)"
        log "INFO" "Deployment timestamp: $deployment_timestamp (previous: $last_timestamp)"
        
        # Update state
        local new_state
        new_state=$(echo "$current_state" | jq --arg ts "$deployment_timestamp" '.lastDeploymentTimestamp = ($ts | tonumber)')
        save_state "$state_file" "$new_state"
        
        NEW_DEPLOYMENT=true
        DEPLOYMENT_DETECTION_METHOD="vercel_api"
        return 0
    else
        log "INFO" "No new deployment via Vercel API (latest: $deployment_timestamp, stored: $last_timestamp)"
        DEPLOYMENT_DETECTION_METHOD="vercel_api"
        return 2
    fi
}

# Function to check for deployment via cache headers (fallback)
check_cache_deployment() {
    local homepage_url="$1"
    local state_file="$2"
    
    log "INFO" "Checking cache headers for deployment indicators..."
    
    # Load current state
    local current_state
    current_state=$(load_state "$state_file")
    local last_cache_status
    last_cache_status=$(echo "$current_state" | jq -r '.lastCacheStatus // "{}"')
    
    # Get headers
    local headers
    headers=$(curl -s -I "$homepage_url" 2>/dev/null || true)
    
    # Check for cache freshness indicators
    local cache_miss
    local age_zero
    
    cache_miss=$(echo "$headers" | grep -i "x-vercel-cache: MISS" || true)
    age_zero=$(echo "$headers" | grep -i "age: 0" || true)
    
    # Determine current cache status
    local current_cache_status="HIT"
    if [[ -n "$cache_miss" ]] && [[ -n "$age_zero" ]]; then
        current_cache_status="MISS_AND_ZERO"
    elif [[ -n "$cache_miss" ]]; then
        current_cache_status="MISS"
    elif [[ -n "$age_zero" ]]; then
        current_cache_status="ZERO"
    fi
    
    # Compare with previous status
    if [[ "$current_cache_status" != "$last_cache_status" ]]; then
        log "WARNING" "Cache status changed: $last_cache_status → $current_cache_status"
        log "WARNING" "⚠️  Cache-header detection can produce false positives (CDN rotation, visitor traffic)"
        
        # Update state
        local new_state
        new_state=$(echo "$current_state" | jq --arg status "$current_cache_status" '.lastCacheStatus = $status')
        save_state "$state_file" "$new_state"
        
        # Only consider it a deployment if we have strong indicators
        if [[ "$current_cache_status" == "MISS_AND_ZERO" ]]; then
            NEW_DEPLOYMENT=true
            log "WARNING" "Possible new deployment detected via cache headers (less accurate)"
        fi
    else
        log "INFO" "Cache status unchanged: $current_cache_status"
    fi
    
    DEPLOYMENT_DETECTION_METHOD="cache"
}

# Function to log success
log_success() {
  echo -e "${GREEN}✅ $1${NC}"
}

# Function to log warning
log_warning() {
  echo -e "${YELLOW}⚠️  $1${NC}"
}

# Function to log error
log_error() {
  echo -e "${RED}❌ $1${NC}"
}

# Function to check HTTP response
check_http_response() {
  local url="$1"
  local description="$2"
  
  echo -e "${BLUE}Checking: ${description}${NC}"
  
  # Get HTTP status code
  local status_code
  status_code=$(curl -s -o /dev/null -w "%{http_code}" "$url")
  
  if [[ "$status_code" == "200" ]]; then
    log_success "HTTP $status_code OK"
    return 0
  else
    log_error "HTTP $status_code (expected 200)"
    return 1
  fi
}

# Check 1: Homepage cache freshness (for informational purposes)
check_homepage_cache() {
  echo -e "${BLUE}Checking: Homepage cache freshness${NC}"
  
  local headers
  headers=$(curl -s -I "$HOMEPAGE_URL")
  
  # Check for cache freshness indicators
  local cache_miss
  local age_zero
  
  cache_miss=$(echo "$headers" | grep -i "x-vercel-cache: MISS" || true)
  age_zero=$(echo "$headers" | grep -i "age: 0" || true)
  
  if [[ -n "$cache_miss" ]]; then
    log_success "Cache: MISS"
  else
    log_warning "Cache: HIT"
  fi
  
  if [[ -n "$age_zero" ]]; then
    log_success "Age: 0"
  else
    log_warning "Age: >0"
  fi
}

# Check 2: Homepage title
check_homepage_title() {
  echo -e "${BLUE}Checking: Homepage title${NC}"
  
  local html
  html=$(curl -s "$HOMEPAGE_URL")
  
  # Extract title tag content
  local title
  title=$(echo "$html" | grep -o '<title>[^<]*</title>' | sed 's/<title>\(.*\)<\/title>/\1/')
  
  if [[ -n "$title" ]]; then
    log_success "Title found: \"$title\""
    return 0
  else
    log_error "No title tag found"
    return 1
  fi
}

# Check 3: API feed validation
check_api_feed() {
  echo -e "${BLUE}Checking: API feed validation${NC}"
  
  local response
  response=$(curl -s "$API_URL")
  
  # Check if response is valid JSON
  if echo "$response" | jq empty 2>/dev/null; then
    log_success "Valid JSON response"
    
    # Check if response has items array
    local item_count
    item_count=$(echo "$response" | jq '.items | length' 2>/dev/null || echo "0")
    
    if [[ "$item_count" -gt 0 ]]; then
      log_success "Feed contains $item_count items"
      
      # Optional: Check first item structure
      local first_item_type
      first_item_type=$(echo "$response" | jq -r '.items[0].type // "unknown"' 2>/dev/null)
      log_success "First item type: $first_item_type"
    else
      log_warning "Feed contains 0 items (might be empty)"
    fi
    
    # Check for common error fields
    if echo "$response" | jq 'has("error")' 2>/dev/null | grep -q "true"; then
      local error_msg
      error_msg=$(echo "$response" | jq -r '.error // "Unknown error"' 2>/dev/null)
      log_error "API returned error: $error_msg"
      return 1
    fi
    
    return 0
  else
    log_error "Invalid JSON response from API"
    return 1
  fi
}

# Track overall success
ALL_CHECKS_PASSED=true
FAILED_CHECKS=()

# Main execution
if [[ "$JSON_OUTPUT" != "true" ]]; then
  echo -e "${BLUE}🚀 Deployment Watchdog Check${NC}"
  echo -e "${BLUE}==========================${NC}"
  echo -e "Homepage: ${HOMEPAGE_URL}"
  echo -e "API Feed: ${API_URL}"
  echo -e "Detection Method: ${VERCEL_TOKEN:+Vercel API (recommended)}${VERCEL_TOKEN:-Cache headers (fallback)}"
  echo ""
fi

# First: Check for new deployment using Vercel API (accurate) or cache headers (fallback)
if [[ -n "$VERCEL_TOKEN" ]]; then
  check_vercel_deployment "$VERCEL_TOKEN" "$VERCEL_PROJECT_ID" "$VERCEL_TEAM_ID" "$STATE_FILE"
  vercel_result=$?
  
  if [[ $vercel_result -eq 1 ]]; then
    log "WARNING" "Vercel API failed, falling back to cache-header detection"
    check_cache_deployment "$HOMEPAGE_URL" "$STATE_FILE"
  fi
else
  check_cache_deployment "$HOMEPAGE_URL" "$STATE_FILE"
fi

# Second: Run health checks (always run these)
if [[ "$JSON_OUTPUT" != "true" ]]; then
  echo -e "${BLUE}🏁 Starting health checks...${NC}"
  echo ""
fi

check_http_response "$HOMEPAGE_URL" "Homepage HTTP status"
http_homepage=$?
if [[ $http_homepage -ne 0 ]]; then
  ALL_CHECKS_PASSED=false
  FAILED_CHECKS+=("Homepage HTTP status")
fi

check_homepage_cache

check_homepage_title
title_result=$?
if [[ $title_result -ne 0 ]]; then
  ALL_CHECKS_PASSED=false
  FAILED_CHECKS+=("Homepage title")
fi

check_http_response "$API_URL" "API feed HTTP status"
http_api=$?
if [[ $http_api -ne 0 ]]; then
  ALL_CHECKS_PASSED=false
  FAILED_CHECKS+=("API HTTP status")
fi

check_api_feed
api_feed_result=$?
if [[ $api_feed_result -ne 0 ]]; then
  ALL_CHECKS_PASSED=false
  FAILED_CHECKS+=("API feed validation")
fi

# Summary
if [[ "$JSON_OUTPUT" == "true" ]]; then
  # JSON output for programmatic use
  local summary_json="{
    \"deployment\": {
      \"new_detected\": $([[ \"$NEW_DEPLOYMENT\" == \"true\" ]] && echo true || echo false),
      \"detection_method\": \"$DEPLOYMENT_DETECTION_METHOD\"
    },
    \"health\": {
      \"all_passed\": $([[ \"$ALL_CHECKS_PASSED\" == \"true\" ]] && echo true || echo false),
      \"failed_checks\": ["
  
  for check in "${FAILED_CHECKS[@]}"; do
    summary_json="${summary_json}\"$check\","
  done
  
  summary_json="${summary_json%,}]},"
  summary_json="${summary_json}\"urls\": {"
  summary_json="${summary_json}\"homepage\": \"$HOMEPAGE_URL\","
  summary_json="${summary_json}\"api\": \"$API_URL\""
  summary_json="${summary_json}}}"
  
  echo "$summary_json"
  
  if $ALL_CHECKS_PASSED && [[ "$NEW_DEPLOYMENT" == "true" ]]; then
    exit 0
  elif $ALL_CHECKS_PASSED; then
    exit 2  # No new deployment but healthy
  else
    exit 1  # Health checks failed
  fi
else
  # Human-readable output
  echo ""
  echo -e "${BLUE}📊 Summary${NC}"
  echo -e "${BLUE}=========${NC}"
  
  echo -e "Deployment Detection: ${DEPLOYMENT_DETECTION_METHOD^^}"
  if [[ "$NEW_DEPLOYMENT" == "true" ]]; then
    echo -e "New Deployment: ${GREEN}✅ YES${NC}"
  else
    echo -e "New Deployment: ${YELLOW}⚠️  NO${NC}"
  fi
  
  if $ALL_CHECKS_PASSED; then
    echo -e "Health Checks: ${GREEN}✅ ALL PASSED${NC}"
    if [[ "$NEW_DEPLOYMENT" == "true" ]]; then
      echo -e "${GREEN}🎉 New deployment detected and all health checks passed!${NC}"
      exit 0
    else
      echo -e "${GREEN}✅ Site is healthy (no new deployment detected)${NC}"
      exit 2
    fi
  else
    echo -e "Health Checks: ${RED}❌ SOME FAILED${NC}"
    echo -e "${RED}⚠️  The following checks failed:${NC}"
    for check in "${FAILED_CHECKS[@]}"; do
      echo -e "  ${RED}• $check${NC}"
    done
    echo ""
    echo -e "${YELLOW}💡 Recommendation: Investigate the failed checks above.${NC}"
    exit 1
  fi
fi