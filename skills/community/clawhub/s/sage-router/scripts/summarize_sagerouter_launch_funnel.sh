#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: scripts/summarize_sagerouter_launch_funnel.sh [--days N] [--json]

Fetch the operator-only /analytics/funnel endpoint and print a privacy-safe
launch snapshot. The script never prints operator tokens, emails, generated API
keys, prompts, provider credentials, OAuth tokens, raw campaign URLs, or raw
provider responses.

Environment:
  SAGEROUTER_SECRET_ENV_FILE       Optional env file to source first
  SAGEROUTER_API_BASE_URL          Defaults to https://api.sagerouter.dev
  SAGE_ROUTER_ANALYTICS_TOKEN      Preferred read-only funnel token
  SAGE_ROUTER_OPERATOR_TOKEN       Fallback operator token
  SAGE_ROUTER_API_KEY              Final fallback admin token
EOF
}

load_local_env_file() {
  local path="$1"
  [[ -f "$path" ]] || return 0

  local key value current
  while IFS='=' read -r -d '' key value; do
    case "$key" in
      SAGEROUTER_API_BASE_URL|SAGE_ROUTER_ANALYTICS_TOKEN|SAGE_ROUTER_OPERATOR_TOKEN|SAGE_ROUTER_API_KEY)
        ;;
      *)
        continue
        ;;
    esac
    current="${!key:-}"
    if [[ -z "$current" && -n "$value" ]]; then
      printf -v "$key" '%s' "$value"
      export "$key"
    fi
  done < <(set +u; set -a; source "$path" >/dev/null 2>&1; env -0)
}

require_tool() {
  local name="$1"
  if ! command -v "$name" >/dev/null 2>&1; then
    printf 'Missing required tool: %s\n' "$name" >&2
    exit 2
  fi
}

DAYS=30
RAW_JSON=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --days)
      if [[ $# -lt 2 || "${2:-}" == -* ]]; then
        printf '%s\n' '--days requires a positive integer value' >&2
        exit 2
      fi
      DAYS="${2:-}"
      shift 2
      ;;
    --json)
      RAW_JSON=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Unknown argument: %s\n' "$1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if ! [[ "$DAYS" =~ ^[0-9]+$ ]] || [[ "$DAYS" -lt 1 ]]; then
  printf '%s\n' '--days must be a positive integer' >&2
  exit 2
fi

require_tool curl
require_tool jq

load_local_env_file "${SAGEROUTER_SECRET_ENV_FILE:-/home/digit/.openclaw/.env}"

API_BASE="${SAGEROUTER_API_BASE_URL:-https://api.sagerouter.dev}"
TOKEN="${SAGE_ROUTER_ANALYTICS_TOKEN:-${SAGE_ROUTER_OPERATOR_TOKEN:-${SAGE_ROUTER_API_KEY:-}}}"
if [[ -z "$TOKEN" ]]; then
  printf 'Missing SAGE_ROUTER_ANALYTICS_TOKEN, SAGE_ROUTER_OPERATOR_TOKEN, or SAGE_ROUTER_API_KEY\n' >&2
  exit 2
fi

tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT

curl -fsS "${API_BASE%/}/analytics/funnel?days=${DAYS}&limit=10000" \
  -H "Authorization: Bearer ${TOKEN}" \
  -o "$tmp"

if [[ "$RAW_JSON" == "1" ]]; then
  jq '{
    generatedAt,
    stages,
    rates,
    mrr,
    nextBestAction,
    activationFollowUps: (
      .activationFollowUps
      | if type == "object" then
          del(
            .emailReadiness.dryRunCommand,
            .emailReadiness.sendCommandTemplate,
            .emailReadiness.setupCommand
          )
        else . end
    ),
    operatorExecutionPacket: (
      .operatorExecutionPacket
      | if type == "object" then
          del(
            .draft.body,
            .emailReadiness.dryRunCommand,
            .emailReadiness.sendCommandTemplate,
            .emailReadiness.setupCommand
          )
        else . end
    ),
    activationQueue: {
      total: (
        .operatorExecutionPacket.totalQueued
        // .activationFollowUps.total
        // .nextBestAction.evidence.noKeyFollowUpsQueued
        // 0
      ),
      sendableQueued: (
        .operatorExecutionPacket.sendableQueued
        // .activationFollowUps.sendableQueued
        // .nextBestAction.evidence.sendableQueued
        // 0
      ),
      reviewOnlyQueued: (
        .operatorExecutionPacket.reviewOnlyQueued
        // .activationFollowUps.reviewOnlyQueued
        // .nextBestAction.evidence.reviewOnlyQueued
        // 0
      ),
      unknownQueued: (
        .activationFollowUps.unknownQueued
        // .nextBestAction.evidence.unknownQueued
        // 0
      ),
      sendableSegments: (
        .activationFollowUps.sendableSegments
        // .nextBestAction.evidence.sendableSegments
        // []
      ),
      reviewOnlySegments: (
        .activationFollowUps.reviewOnlySegments
        // .nextBestAction.evidence.reviewOnlySegments
        // []
      ),
      dryRunRecipients: (.operatorExecutionPacket.sendTelemetry.dryRunRecipients // 0),
      sentRecipients: (.operatorExecutionPacket.sendTelemetry.sentRecipients // 0),
      sendApprovalRequired: (.operatorExecutionPacket.sendTelemetry.sendApprovalRequired // false),
      nextSendSegment: (.operatorExecutionPacket.sendTelemetry.nextSendSegment // "")
    },
    acquisitionActions: (.acquisitionActions // [])[0:8],
    privacy
  }' "$tmp"
  exit 0
fi

jq -r --arg days "$DAYS" '
  def n($v): ($v // 0);
  def pct($v): if $v == null then "n/a" else (($v * 10000 | round) / 100 | tostring) + "%" end;
  def money($v): "$" + ((n($v) | tostring));
  def list($v): (($v // []) | join(", "));

  . as $root
  | ($root.stages // {}) as $stages
  | ($root.rates // {}) as $rates
  | ($root.mrr // {}) as $mrr
  | ($root.nextBestAction // {}) as $action
  | ($root.activationFollowUps // {}) as $followups
  | ($root.operatorExecutionPacket // {}) as $packet
  | [
      "# Sage Router launch funnel snapshot",
      "",
      "- Window: last \($days) days",
      "- Generated at epoch: \(n($root.generatedAt))",
      "- Marketing intent events: \(n($stages.marketingIntentEvents))",
      "- Signups: \(n($stages.signups))",
      "- Generated-key customers: \(n($stages.customersWithGeneratedApiKeys))",
      "- First-routed-request customers: \(n($stages.customersWithFirstRoutedRequest))",
      "- Paid customers: \(n($stages.paidCustomers))",
      "- Estimated MRR: \(money($mrr.estimatedCurrentMrrUsd)) / \(money($mrr.targetMrrUsd)) target (\(pct($mrr.targetAttainment)))",
      "",
      "## Current Bottleneck",
      "",
      "- Metric: \($action.metric // "unknown")",
      "- Priority: \($action.priority // "unknown")",
      "- Owner/surface: \($action.owner // "unknown") / \($action.surface // "unknown")",
      "- Action: \($action.action // "Review the live launch funnel.")",
      "- Success metric: \($action.successMetric // "Improve the next funnel stage.")",
      "- CTA: \($action.ctaPath // "https://app.sagerouter.dev/launch-funnel.html")",
      "",
      "## Activation Queue",
      "",
      "- Total no-key follow-ups: \(n($followups.total))",
      "- Sendable queued: \(n($packet.sendableQueued // $action.evidence.sendableQueued))",
      "- Review-only queued: \(n($packet.reviewOnlyQueued // $action.evidence.reviewOnlyQueued))",
      "- Unknown queued: \(n($action.evidence.unknownQueued))",
      "- Dry-run recipients: \(n($packet.sendTelemetry.dryRunRecipients))",
      "- Real sends recorded: \(n($packet.sendTelemetry.sentRecipients))",
      "- Send approval required: \($packet.sendTelemetry.sendApprovalRequired // false)",
      "- Recommended send segments: \(list($action.evidence.sendableSegments))",
      "- Review-only segments: \(list($action.evidence.reviewOnlySegments))",
      "",
      "## Top Acquisition Actions",
      (
        (($root.acquisitionActions // [])[0:5])
        | map("- \(.kind)/\(.bucket): \(n(.clicks)) clicks - \(.action)")
        | .[]
      ),
      "",
      "## Revenue Gap",
      (
        (($mrr.planRevenueActions // [])[0:3])
        | map("- \(.plan): \(n(.customerGap)) customers, \(money(.remainingMrrToTargetUsd)) remaining MRR - \(.action)")
        | .[]
      ),
      "",
      "## Privacy",
      "",
      "- Contains emails: \($root.privacy.containsEmails // false)",
      "- Contains API keys: \($root.privacy.containsApiKeys // false)",
      "- Contains provider credentials: \($root.privacy.containsProviderCredentials // false)",
      "- Prompts stored: \($root.privacy.promptsStored // false)"
    ]
    | .[]
' "$tmp"
