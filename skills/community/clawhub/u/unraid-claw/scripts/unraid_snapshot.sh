#!/usr/bin/env bash
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "${SCRIPT_DIR}/unraid_common.sh"

require_base_url
require_api_key
require_timeout
require_command "curl" "required for Unraid API calls"
require_command "jq" "required to normalize snapshot output"
ensure_state_dirs

QUERY_RICH='{"query":"query UnraidMonitorSnapshotRich { info { os { platform distro release uptime } cpu { model cores usage temperature } memory { total used free usage percentage } } array { state syncAction syncProgress errors disks { name status size used fsUsed temperature smartStatus } parity { status lastCheck errors } parities { status lastCheck errors } } docker { enabled containers { id name names image state status uptime } } }"}'
QUERY_COMPAT='{"query":"query UnraidMonitorSnapshotCompat { info { os { platform distro release uptime } cpu { model cores flags } memory { percentage } } array { state capacity parities { status lastCheck errors } disks { name status size fsUsed } } docker { containers { id names image state status } } }"}'
QUERY_MINIMAL='{"query":"query UnraidMonitorSnapshotMinimal { __typename info { os { release uptime } } docker { containers { id state status } } array { state disks { name status } } }"}'

body_file="$(mktemp)"
err_file="$(mktemp)"
snapshot_tmp="$(mktemp)"
errors_tmp="$(mktemp)"
cleanup() {
  rm -f "$body_file" "$err_file" "$snapshot_tmp" "$errors_tmp"
}
trap cleanup EXIT

capture_errors() {
  jq -r '.errors[]?.message' "$body_file" 2>/dev/null >> "$errors_tmp" || true
}

query_variant=""
http_code=""
curl_status=0
have_data=0

for variant in rich compat minimal; do
  case "$variant" in
    rich)
      query_json="$QUERY_RICH"
      ;;
    compat)
      query_json="$QUERY_COMPAT"
      ;;
    minimal)
      query_json="$QUERY_MINIMAL"
      ;;
  esac

  http_code="$(graphql_post "$query_json" "$body_file" "$err_file")"
  curl_status=$?

  if [[ $curl_status -ne 0 ]]; then
    break
  fi

  if [[ "$http_code" == "401" || "$http_code" == "403" ]]; then
    break
  fi

  if [[ "$http_code" -lt 200 || "$http_code" -ge 300 ]]; then
    capture_errors
    continue
  fi

  if jq -e '.data != null' "$body_file" >/dev/null 2>&1; then
    have_data=1
    query_variant="$variant"
    capture_errors
    break
  fi

  capture_errors
done

if [[ $curl_status -ne 0 ]]; then
  echo "FAIL: Network request failed for $(endpoint)."
  echo "DETAIL: $(sanitize_error_file "$err_file")"
  exit 3
fi

if [[ "$http_code" == "401" || "$http_code" == "403" ]]; then
  echo "FAIL: Authentication to Unraid API failed. Verify UNRAID_API_KEY permissions/validity."
  exit 4
fi

if [[ "$http_code" -lt 200 || "$http_code" -ge 300 ]]; then
  echo "FAIL: Unraid API returned HTTP ${http_code}."
  exit 5
fi

if [[ "$have_data" -ne 1 ]]; then
  echo "FAIL: GraphQL response did not contain data."
  if [[ -s "$errors_tmp" ]]; then
    echo "DETAIL: $(head -n 1 "$errors_tmp")"
  fi
  exit 6
fi

timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

jq \
  --arg ts "$timestamp" \
  --arg endpoint "$(endpoint)" \
  --arg qv "$query_variant" '
  def parity_obj:
    if (.data.array.parity? | type) == "object" then .data.array.parity
    elif ((.data.array.parities? // []) | length) > 0 then (.data.array.parities[0] // {})
    else {} end;

  def normalize_containers:
    (.data.docker.containers // [])
    | map(
        . + {
          name: (.name // ((.names // ["unknown"]) | .[0] // "unknown")),
          uptime: (.uptime // "unknown")
        }
      );

  def normalize_disks:
    (.data.array.disks // [])
    | map(
        . + {
          used: (.used // .fsUsed // 0),
          temperature: (.temperature // "unknown"),
          smartStatus: (.smartStatus // .status // "unknown")
        }
      );

  def normalized_data:
    {
      info: {
        os: (.data.info.os // {}),
        cpu: {
          model: (.data.info.cpu.model // "unknown"),
          cores: (.data.info.cpu.cores // 0),
          usage: (.data.info.cpu.usage // 0),
          temperature: (.data.info.cpu.temperature // "unknown")
        },
        memory: {
          total: (.data.info.memory.total // 0),
          used: (.data.info.memory.used // 0),
          free: (.data.info.memory.free // 0),
          usage: (.data.info.memory.usage // .data.info.memory.percentage // 0)
        }
      },
      array: {
        state: (.data.array.state // "unknown"),
        syncAction: (.data.array.syncAction // "none"),
        syncProgress: (.data.array.syncProgress // "0"),
        errors: (.data.array.errors // 0),
        disks: normalize_disks,
        parity: {
          status: (parity_obj.status // "unknown"),
          lastCheck: (parity_obj.lastCheck // "unknown"),
          errors: (parity_obj.errors // 0)
        }
      },
      docker: {
        enabled: (.data.docker.enabled // (((.data.docker.containers // []) | length) > 0)),
        containers: normalize_containers
      }
    };

  {
    timestamp: $ts,
    endpoint: $endpoint,
    query_variant: $qv,
    warnings: (if has("errors") then ["Some API fields were unavailable for this Unraid version; output is partial."] else [] end),
    graphql_errors: (.errors // []),
    data: normalized_data
  }
' "$body_file" > "$snapshot_tmp"

latest_path="$(latest_snapshot_path)"
archived_path="$(timestamped_snapshot_path)"
cp "$snapshot_tmp" "$latest_path"
cp "$snapshot_tmp" "$archived_path"

if jq -e '.graphql_errors | length > 0' "$latest_path" >/dev/null 2>&1; then
  echo "PASS: Snapshot captured with partial-data warning."
  echo "LATEST_SNAPSHOT: ${latest_path}"
  echo "ARCHIVE_SNAPSHOT: ${archived_path}"
  exit 0
fi

echo "PASS: Snapshot captured successfully."
echo "LATEST_SNAPSHOT: ${latest_path}"
echo "ARCHIVE_SNAPSHOT: ${archived_path}"
exit 0