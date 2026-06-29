#!/usr/bin/env bash
set -euo pipefail

PROJECT_ID="${PROJECT_ID:-${SAGE_ROUTER_GCP_PROJECT_ID:-sage-router-demo-20260428}}"
REGION="${REGION:-us-central1}"
SERVICE_NAME="${SERVICE_NAME:-sage-router}"
TERMS_URL="${SAGEROUTER_PROVIDER_RESALE_TERMS_URL:-https://sagerouter.dev/provider-resale-terms}"
MARGIN_POLICY_URL="${SAGEROUTER_PROVIDER_RESALE_MARGIN_POLICY_URL:-https://sagerouter.dev/margin-policy}"
TERMS_ACKNOWLEDGED="${SAGEROUTER_PROVIDER_RESALE_TERMS_ACKNOWLEDGED:-0}"
AUTHORIZATION_REF="${SAGEROUTER_PROVIDER_RESALE_AUTHORIZATION_REF:-}"
ALLOWED_PROVIDERS="${SAGEROUTER_PROVIDER_RESALE_ALLOWED_PROVIDERS:-}"
COST_CENTS_PER_1K="${SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS:-}"
MIN_MARGIN="${SAGEROUTER_PROVIDER_RESALE_MIN_GROSS_MARGIN_PERCENT:-35}"
ENABLE_PUBLIC="${SAGEROUTER_MANAGED_PROVIDER_RESALE_ENABLE_PUBLIC:-0}"
RUN_READINESS="${SAGEROUTER_RUN_READINESS:-1}"
MODE="apply"
RESALE_ELIGIBLE_PROVIDER_FAMILIES="ollama openai anthropic"
BYOK_ONLY_PROVIDER_FAMILIES="openrouter"

usage() {
  cat >&2 <<'EOF'
Usage: scripts/configure_managed_provider_resale_readiness.sh [--check|--stage-public-controls|--unit-economics]

Stage Sage Router managed provider-access readiness on Cloud Run.

Required environment:
  SAGEROUTER_PROVIDER_RESALE_ALLOWED_PROVIDERS="ollama,openai,anthropic"
  SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS="reviewed private cost"

Optional:
  SAGEROUTER_PROVIDER_RESALE_TERMS_URL="https://sagerouter.dev/provider-resale-terms"
  SAGEROUTER_PROVIDER_RESALE_MARGIN_POLICY_URL="https://sagerouter.dev/margin-policy"
  SAGEROUTER_PROVIDER_RESALE_TERMS_ACKNOWLEDGED=0
  SAGEROUTER_PROVIDER_RESALE_AUTHORIZATION_REF="private provider authorization evidence reference"
  SAGEROUTER_PROVIDER_RESALE_MIN_GROSS_MARGIN_PERCENT=35
  SAGEROUTER_MANAGED_PROVIDER_RESALE_ENABLE_PUBLIC=0
  PROJECT_ID=sage-router-demo-20260428
  REGION=us-central1
  SERVICE_NAME=sage-router
  SAGEROUTER_RUN_READINESS=0

Options:
  --check                  Report public readiness, Cloud Run bindings, and local
                           input presence without writing secrets or printing
                           the cost model.
  --stage-public-controls  Bind non-secret terms, margin-policy, allowlist, and
                           disabled public-enable env without requiring or
                           writing the private cost model.
  --unit-economics         Validate the private provider-cost candidate against
                           public plan revenue and minimum-margin thresholds
                           without printing the private cost value.

The provider cost model is stored in Secret Manager and is not printed.
Managed public resale remains disabled unless
SAGEROUTER_MANAGED_PROVIDER_RESALE_ENABLE_PUBLIC=1 is explicitly set.
The helper also rejects managed-resale provider allowlists with BYOK-only
families and rejects minimum gross-margin thresholds below the launch floor.
Terms acknowledgment or public enablement also requires
SAGEROUTER_PROVIDER_RESALE_AUTHORIZATION_REF; the helper prints only presence,
never the reference value.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --check)
      MODE="check"
      shift
      ;;
    --stage-public-controls)
      MODE="stage-public-controls"
      shift
      ;;
    --unit-economics)
      MODE="unit-economics"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      usage
      exit 2
      ;;
  esac
done

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    printf 'Missing required command: %s\n' "$1" >&2
    exit 2
  fi
}

require_value() {
  local name="$1"
  local value="$2"
  if [[ -z "$value" ]]; then
    printf 'Missing required env: %s\n\n' "$name" >&2
    usage
    exit 2
  fi
}

truthy() {
  case "${1,,}" in
    1|true|yes|on) return 0 ;;
    *) return 1 ;;
  esac
}

presence() {
  if [[ -n "${1:-}" ]]; then
    printf 'present'
  else
    printf 'missing'
  fi
}

contains_word() {
  local needle="$1"
  shift
  local item
  for item in "$@"; do
    if [[ "$item" == "$needle" ]]; then
      return 0
    fi
  done
  return 1
}

normalize_provider_list() {
  printf '%s' "$1" \
    | tr '[:upper:]' '[:lower:]' \
    | tr ',' '\n' \
    | sed 's/^[[:space:]]*//;s/[[:space:]]*$//' \
    | awk 'NF && !seen[$0]++ {print}'
}

validate_allowed_providers() {
  local raw="$1"
  local failures=0 family
  local eligible_count=0 byok_count=0 unknown_count=0
  local -a eligible=($RESALE_ELIGIBLE_PROVIDER_FAMILIES)
  local -a byok=($BYOK_ONLY_PROVIDER_FAMILIES)

  while IFS= read -r family; do
    [[ -n "$family" ]] || continue
    if contains_word "$family" "${eligible[@]}"; then
      eligible_count=$((eligible_count + 1))
      continue
    fi
    if contains_word "$family" "${byok[@]}"; then
      byok_count=$((byok_count + 1))
      printf 'Provider allowlist includes BYOK-only family %s; do not include it in managed resale.\n' "$family" >&2
      failures=1
      continue
    fi
    unknown_count=$((unknown_count + 1))
    printf 'Provider allowlist includes unknown/non-resale family %s.\n' "$family" >&2
    failures=1
  done < <(normalize_provider_list "$raw")

  printf 'Provider allowlist preflight: resaleEligible=%s byokOnlyRejected=%s unknownRejected=%s\n' \
    "$eligible_count" "$byok_count" "$unknown_count" >&2
  if [[ "$eligible_count" -le 0 ]]; then
    printf 'Provider allowlist must include at least one resale-eligible family: %s.\n' "$RESALE_ELIGIBLE_PROVIDER_FAMILIES" >&2
    failures=1
  fi
  return "$failures"
}

validate_margin_threshold() {
  if ! [[ "$MIN_MARGIN" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
    printf 'SAGEROUTER_PROVIDER_RESALE_MIN_GROSS_MARGIN_PERCENT must be numeric.\n' >&2
    return 1
  fi
  if ! awk "BEGIN { exit !($MIN_MARGIN >= 30) }"; then
    printf 'SAGEROUTER_PROVIDER_RESALE_MIN_GROSS_MARGIN_PERCENT must be at least 30 for public launch readiness.\n' >&2
    return 1
  fi
}

validate_authorization_reference() {
  if truthy "$TERMS_ACKNOWLEDGED" || truthy "$ENABLE_PUBLIC"; then
    if [[ -z "$AUTHORIZATION_REF" ]]; then
      printf 'SAGEROUTER_PROVIDER_RESALE_AUTHORIZATION_REF is required before acknowledging provider resale terms or requesting public managed access.\n' >&2
      return 1
    fi
  fi
  return 0
}

check_managed_provider_resale() {
  require_cmd curl
  require_cmd jq

  local failures=0 body code enabled requested readiness status allowed_count auth_evidence cost_configured unit_satisfied missing_count
  body="$(mktemp)"
  code="$(curl -sS -o "$body" -w '%{http_code}' https://api.sagerouter.dev/pricing || printf '000')"
  if [[ "$code" == "200" ]]; then
    enabled="$(jq -r '.publicLaunch.managedProviderAccess.enabled // false' "$body")"
    requested="$(jq -r '.publicLaunch.managedProviderAccess.requested // false' "$body")"
    readiness="$(jq -r '.publicLaunch.managedProviderAccess.readinessSatisfied // false' "$body")"
    status="$(jq -r '.publicLaunch.managedProviderAccess.status // empty' "$body")"
    allowed_count="$(jq -r '(.publicLaunch.managedProviderAccess.allowedProviderFamilies // []) | length' "$body")"
    auth_evidence="$(jq -r '.publicLaunch.managedProviderAccess.providerAuthorizationEvidenceConfigured // false' "$body")"
    cost_configured="$(jq -r '.publicLaunch.managedProviderAccess.unitEconomics.costModelConfigured // false' "$body")"
    unit_satisfied="$(jq -r '.publicLaunch.managedProviderAccess.unitEconomics.satisfied // false' "$body")"
    missing_count="$(jq -r '(.publicLaunch.managedProviderAccess.missingControls // []) | length' "$body")"
    printf 'Public managed-provider readiness: enabled=%s requested=%s readinessSatisfied=%s status=%s allowedProviderFamilies=%s authorizationEvidence=%s costModel=%s unitEconomics=%s missingControls=%s\n' \
      "$enabled" "$requested" "$readiness" "${status:-missing}" "$allowed_count" "$auth_evidence" "$cost_configured" "$unit_satisfied" "$missing_count"
    if [[ "$readiness" != "true" ]]; then
      failures=1
    fi
  else
    printf 'Public managed-provider readiness: unavailable HTTP %s from https://api.sagerouter.dev/pricing\n' "$code" >&2
    failures=1
  fi
  rm -f "$body"

  printf 'Local apply inputs: termsUrl=%s marginPolicyUrl=%s termsAcknowledged=%s authorizationEvidence=%s allowedProviders=%s costModel=%s minimumMargin=%s enablePublic=%s\n' \
    "$(presence "$TERMS_URL")" "$(presence "$MARGIN_POLICY_URL")" "$TERMS_ACKNOWLEDGED" "$(presence "$AUTHORIZATION_REF")" "$(presence "$ALLOWED_PROVIDERS")" "$(presence "$COST_CENTS_PER_1K")" "$MIN_MARGIN" "$ENABLE_PUBLIC"
  if [[ -n "$ALLOWED_PROVIDERS" ]] && ! validate_allowed_providers "$ALLOWED_PROVIDERS"; then
    failures=1
  fi
  if [[ -n "$MIN_MARGIN" ]] && ! validate_margin_threshold; then
    failures=1
  fi
  if ! validate_authorization_reference; then
    failures=1
  fi

  if command -v gcloud >/dev/null 2>&1; then
    local service_json service_status enabled_env allowed_env auth_ref_env cost_secret margin_env terms_env ack_env
    service_json="$(mktemp)"
    if gcloud run services describe "$SERVICE_NAME" \
      --project "$PROJECT_ID" \
      --region "$REGION" \
      --platform managed \
      --format=json >"$service_json" 2>/dev/null; then
      service_status="present"
      enabled_env="$(jq -r '(.spec.template.spec.containers[0].env // [])[]? | select(.name == "SAGEROUTER_MANAGED_PROVIDER_RESALE_ENABLED") | (.value // empty)' "$service_json" | tail -n1)"
      allowed_env="$(jq -r '(.spec.template.spec.containers[0].env // [])[]? | select(.name == "SAGEROUTER_PROVIDER_RESALE_ALLOWED_PROVIDERS") | (.value // empty)' "$service_json" | tail -n1)"
      terms_env="$(jq -r '(.spec.template.spec.containers[0].env // [])[]? | select(.name == "SAGEROUTER_PROVIDER_RESALE_TERMS_URL") | (.value // empty)' "$service_json" | tail -n1)"
      margin_env="$(jq -r '(.spec.template.spec.containers[0].env // [])[]? | select(.name == "SAGEROUTER_PROVIDER_RESALE_MARGIN_POLICY_URL") | (.value // empty)' "$service_json" | tail -n1)"
      ack_env="$(jq -r '(.spec.template.spec.containers[0].env // [])[]? | select(.name == "SAGEROUTER_PROVIDER_RESALE_TERMS_ACKNOWLEDGED") | (.value // empty)' "$service_json" | tail -n1)"
      auth_ref_env="$(jq -r '(.spec.template.spec.containers[0].env // [])[]? | select(.name == "SAGEROUTER_PROVIDER_RESALE_AUTHORIZATION_REF") | (.value // empty)' "$service_json" | tail -n1)"
      cost_secret="$(jq -r '(.spec.template.spec.containers[0].env // [])[]? | select(.name == "SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS") | (.valueFrom.secretKeyRef.name // empty)' "$service_json" | tail -n1)"
      printf 'Cloud Run bindings: service=%s enabledEnv=%s allowedProvidersEnv=%s termsUrlEnv=%s termsAckEnv=%s authorizationRefEnv=%s marginPolicyEnv=%s costSecret=%s\n' \
        "$service_status" "$(presence "$enabled_env")" "$(presence "$allowed_env")" "$(presence "$terms_env")" "$(presence "$ack_env")" "$(presence "$auth_ref_env")" "$(presence "$margin_env")" "$(presence "$cost_secret")"
    else
      printf 'Cloud Run bindings: service=unavailable project=%s region=%s service=%s\n' "$PROJECT_ID" "$REGION" "$SERVICE_NAME" >&2
      failures=1
    fi
    rm -f "$service_json"
  else
    printf 'Cloud Run bindings: skipped because gcloud is not installed\n' >&2
  fi

  if [[ "$failures" != "0" ]]; then
    cat >&2 <<'EOF'
Managed provider access is not launch-ready yet.
Stage reviewed provider terms, resale-eligible allowlist, private cost model,
and margin policy with:
  scripts/configure_managed_provider_resale_readiness.sh

The check prints presence, counts, and binding names only; it never prints the
private provider-cost value.
EOF
    return 1
  fi
  printf 'Managed provider access appears launch-ready. Keep public enable disabled until provider authorization evidence is current.\n'
}

secret_exists() {
  gcloud secrets describe "$1" --project "$PROJECT_ID" >/dev/null 2>&1
}

put_secret() {
  local name="$1"
  local value="$2"
  if ! secret_exists "$name"; then
    gcloud secrets create "$name" \
      --project "$PROJECT_ID" \
      --replication-policy automatic >/dev/null
  fi
  printf '%s' "$value" | gcloud secrets versions add "$name" \
    --project "$PROJECT_ID" \
    --data-file=- >/dev/null
}

if [[ "$MODE" == "check" ]]; then
  check_managed_provider_resale
  exit $?
fi

if [[ "$MODE" == "unit-economics" ]]; then
  require_cmd python3
  "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/scripts/managed_provider_unit_economics.py"
  exit $?
fi

require_cmd gcloud
require_cmd awk

if [[ "$MODE" == "stage-public-controls" ]]; then
  if [[ -z "$ALLOWED_PROVIDERS" ]]; then
    ALLOWED_PROVIDERS="ollama,openai,anthropic"
  fi
  validate_allowed_providers "$ALLOWED_PROVIDERS"
  validate_margin_threshold
  validate_authorization_reference
  printf 'Updating Cloud Run service=%s region=%s managed-access non-secret readiness controls\n' "$SERVICE_NAME" "$REGION" >&2
  gcloud run services update "$SERVICE_NAME" \
    --project "$PROJECT_ID" \
    --region "$REGION" \
    --platform managed \
    --update-env-vars "^|^SAGEROUTER_PROVIDER_RESALE_TERMS_URL=${TERMS_URL}|SAGEROUTER_PROVIDER_RESALE_MARGIN_POLICY_URL=${MARGIN_POLICY_URL}|SAGEROUTER_PROVIDER_RESALE_TERMS_ACKNOWLEDGED=${TERMS_ACKNOWLEDGED}|SAGEROUTER_PROVIDER_RESALE_ALLOWED_PROVIDERS=${ALLOWED_PROVIDERS}|SAGEROUTER_PROVIDER_RESALE_MIN_GROSS_MARGIN_PERCENT=${MIN_MARGIN}|SAGEROUTER_MANAGED_PROVIDER_RESALE_ENABLED=0"
  printf 'Managed provider-access public controls staged without writing the private cost model. Review terms acknowledgment and unit economics before enabling managed access.\n' >&2
  if [[ "$RUN_READINESS" != "0" ]]; then
    "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/scripts/check_sagerouter_launch_readiness.sh"
  fi
  exit 0
fi

require_value SAGEROUTER_PROVIDER_RESALE_ALLOWED_PROVIDERS "$ALLOWED_PROVIDERS"
require_value SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS "$COST_CENTS_PER_1K"

if ! [[ "$COST_CENTS_PER_1K" =~ ^[0-9]+([.][0-9]+)?$ ]]; then
  printf 'SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS must be a positive numeric value.\n' >&2
  exit 2
fi

if ! awk "BEGIN { exit !($COST_CENTS_PER_1K > 0) }"; then
  printf 'SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS must be greater than zero.\n' >&2
  exit 2
fi

validate_allowed_providers "$ALLOWED_PROVIDERS"
validate_margin_threshold
validate_authorization_reference

if truthy "$ENABLE_PUBLIC" && ! truthy "$TERMS_ACKNOWLEDGED"; then
  printf 'Refusing to request public managed resale without SAGEROUTER_PROVIDER_RESALE_TERMS_ACKNOWLEDGED=1.\n' >&2
  exit 2
fi

gcloud services enable secretmanager.googleapis.com run.googleapis.com \
  --project "$PROJECT_ID" >/dev/null

printf 'Writing managed provider-access cost-model Secret Manager version in project=%s\n' "$PROJECT_ID" >&2
put_secret SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS "$COST_CENTS_PER_1K"

managed_enabled=0
if truthy "$ENABLE_PUBLIC"; then
  managed_enabled=1
fi

printf 'Updating Cloud Run service=%s region=%s managed-access readiness env\n' "$SERVICE_NAME" "$REGION" >&2
gcloud run services update "$SERVICE_NAME" \
  --project "$PROJECT_ID" \
  --region "$REGION" \
  --platform managed \
  --update-env-vars "^|^SAGEROUTER_PROVIDER_RESALE_TERMS_URL=${TERMS_URL}|SAGEROUTER_PROVIDER_RESALE_MARGIN_POLICY_URL=${MARGIN_POLICY_URL}|SAGEROUTER_PROVIDER_RESALE_TERMS_ACKNOWLEDGED=${TERMS_ACKNOWLEDGED}|SAGEROUTER_PROVIDER_RESALE_AUTHORIZATION_REF=${AUTHORIZATION_REF}|SAGEROUTER_PROVIDER_RESALE_ALLOWED_PROVIDERS=${ALLOWED_PROVIDERS}|SAGEROUTER_PROVIDER_RESALE_MIN_GROSS_MARGIN_PERCENT=${MIN_MARGIN}|SAGEROUTER_MANAGED_PROVIDER_RESALE_ENABLED=${managed_enabled}" \
  --update-secrets "SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS=SAGEROUTER_PROVIDER_RESALE_COST_CENTS_PER_1K_REQUESTS:latest"

printf 'Managed provider-access readiness staged. Verify /pricing before enabling any private-beta managed access.\n' >&2

if [[ "$RUN_READINESS" != "0" ]]; then
  "$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/scripts/check_sagerouter_launch_readiness.sh"
fi
