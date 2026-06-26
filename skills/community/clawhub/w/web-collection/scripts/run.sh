#!/usr/bin/env bash
set -euo pipefail

# Unified entry for local/cloud deployment.
# - local: run the local send-command script
# - cloud: run the cloud send-command script

PLATFORM="douyin"
METHOD=""
KEYWORDS=()
LINKS=()
MAX_ITEMS="10"
ENSURE_BRIDGE="false"
BRIDGE_CMD="${WEB_COLLECTION_BRIDGE_CMD:-}"
FEATURE=""
MODE=""
INTERVAL_VAL=""
FETCH_DETAIL=""
DETAIL_SPEED=""
DETAIL_DELAY=""
REPLY_LEVEL=""
AUTO_EXPORT=""
EXPORT_MODE=""
EXPORT_TARGET=""
TABLE_NAME=""
FIELDS_JSON=""
FILTERS_JSON=""
DEDUPLICATION=""
DEDUPLICATION_STRATEGY=""

CONNECTION_MODE="${WEB_COLLECTION_CONNECTION_MODE:-cloud}"
BRIDGE_URL="${WEB_COLLECTION_BRIDGE_URL:-http://127.0.0.1:19820}"
CLOUD_BASE_URL="${WEB_COLLECTION_CLOUD_BASE_URL:-https://i-sync.cn}"
CLOUD_DEVICE_ID="${WEB_COLLECTION_CLOUD_DEVICE_ID:-}"
CLOUD_TOKEN="${WEB_COLLECTION_CLOUD_TOKEN:-}"
SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"

HAS_CONNECTION_MODE_ARG="false"
HAS_PLATFORM_ARG="false"
HAS_MAX_ITEMS_ARG="false"
HAS_FETCH_DETAIL_ARG="false"
HAS_DETAIL_SPEED_ARG="false"
HAS_BASE_URL_ARG="false"
HAS_CLOUD_BASE_URL_ARG="false"
HAS_CLOUD_DEVICE_ID_ARG="false"
HAS_CLOUD_TOKEN_ARG="false"
HAS_EXPORT_TARGET_ARG="false"
HAS_DEDUPLICATION_ARG="false"
HAS_DEDUPLICATION_STRATEGY_ARG="false"

usage() {
  cat <<'EOF'
Usage:
  run.sh [options]

Common examples:
  run.sh --keyword "小龙虾AI助手" --max-items 10 --ensure-bridge
  run.sh --connection-mode cloud --cloud-device-id desktop-local-smoke-fix --cloud-token '<user_api_key>' --keyword "AI员工"
  run.sh --platform amazon --keyword "Chinese antiques" --max-items 20 --ensure-bridge
  run.sh --platform amazon --method productLink --link "https://www.amazon.com/dp/B0..." --ensure-bridge
  run.sh --platform amazon --method productReview --link "https://www.amazon.com/dp/B0..." --filters-json '{"sortBy":"recent"}' --ensure-bridge
  run.sh --platform bilibili --keyword "古董" --max-items 20 --ensure-bridge
  run.sh --platform bilibili --method videoInfo --link "https://www.bilibili.com/video/BV..." --ensure-bridge
  run.sh --keyword "小龙虾" --export-target csv --max-items 20 --ensure-bridge
  run.sh --keyword "小龙虾" --export-target bitable --max-items 20 --ensure-bridge

Options:
  --connection-mode <local|cloud> default: cloud
  --platform <name>              default: douyin
  --method <name>                optional; default depends on platform
  --keyword <text>               repeatable
  --link <url>                   repeatable
  --max-items <n>                default: 10
  --feature <name>               optional override
  --mode <name>                  optional override
  --interval <n>                 optional override
  --fetch-detail <true|false>    optional override
  --detail-speed <text>          optional override
  --detail-delay <n>             optional override
  --reply-level <n>              optional override
  --auto-export <true|false>     optional override
  --export-mode <name>           optional override
  --export-target <csv|bitable>  override stored export preference for this run
  --deduplication <true|false>    override stored export deduplication preference
  --deduplication-strategy <keepOld|keepNew>
  --table-name <text>            optional
  --fields-json <json-array>     optional
  --filters-json <json-object>   optional
  --base-url <url>               optional override, same as WEB_COLLECTION_BRIDGE_URL
  --cloud-base-url <url>         optional override, same as WEB_COLLECTION_CLOUD_BASE_URL
  --cloud-device-id <id>         optional override, same as WEB_COLLECTION_CLOUD_DEVICE_ID
  --cloud-token <token>          optional override, same as WEB_COLLECTION_CLOUD_TOKEN
  --ensure-bridge
  --bridge-cmd '<cmd>'

Env:
  WEB_COLLECTION_CONNECTION_MODE default: cloud
  WEB_COLLECTION_BRIDGE_URL       default: http://127.0.0.1:19820
  WEB_COLLECTION_CLOUD_BASE_URL   optional override, default: https://i-sync.cn
  WEB_COLLECTION_CLOUD_DEVICE_ID  optional, target connector device_id
  WEB_COLLECTION_CLOUD_TOKEN      optional, bearer token for cloud dispatch
  WEB_COLLECTION_BRIDGE_CMD       optional bridge start command
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --connection-mode)
      CONNECTION_MODE="${2:-cloud}"
      HAS_CONNECTION_MODE_ARG="true"
      shift 2
      ;;
    --platform)
      PLATFORM="${2:-}"
      HAS_PLATFORM_ARG="true"
      shift 2
      ;;
    --method)
      METHOD="${2:-}"
      shift 2
      ;;
    --keyword)
      KEYWORDS+=("${2:-}")
      shift 2
      ;;
    --link)
      LINKS+=("${2:-}")
      shift 2
      ;;
    --max-items)
      MAX_ITEMS="${2:-10}"
      HAS_MAX_ITEMS_ARG="true"
      shift 2
      ;;
    --feature)
      FEATURE="${2:-}"
      shift 2
      ;;
    --mode)
      MODE="${2:-}"
      shift 2
      ;;
    --interval)
      INTERVAL_VAL="${2:-}"
      shift 2
      ;;
    --fetch-detail)
      FETCH_DETAIL="${2:-}"
      HAS_FETCH_DETAIL_ARG="true"
      shift 2
      ;;
    --detail-speed)
      DETAIL_SPEED="${2:-}"
      HAS_DETAIL_SPEED_ARG="true"
      shift 2
      ;;
    --detail-delay)
      DETAIL_DELAY="${2:-}"
      shift 2
      ;;
    --reply-level)
      REPLY_LEVEL="${2:-}"
      shift 2
      ;;
    --auto-export)
      AUTO_EXPORT="${2:-}"
      shift 2
      ;;
    --export-mode)
      EXPORT_MODE="${2:-}"
      shift 2
      ;;
    --export-target)
      EXPORT_TARGET="${2:-}"
      HAS_EXPORT_TARGET_ARG="true"
      shift 2
      ;;
    --deduplication)
      DEDUPLICATION="${2:-}"
      HAS_DEDUPLICATION_ARG="true"
      shift 2
      ;;
    --deduplication-strategy)
      DEDUPLICATION_STRATEGY="${2:-}"
      HAS_DEDUPLICATION_STRATEGY_ARG="true"
      shift 2
      ;;
    --table-name)
      TABLE_NAME="${2:-}"
      shift 2
      ;;
    --fields-json)
      FIELDS_JSON="${2:-}"
      shift 2
      ;;
    --filters-json)
      FILTERS_JSON="${2:-}"
      shift 2
      ;;
    --base-url|--bridge-url)
      BRIDGE_URL="${2:-}"
      HAS_BASE_URL_ARG="true"
      shift 2
      ;;
    --cloud-base-url)
      CLOUD_BASE_URL="${2:-}"
      HAS_CLOUD_BASE_URL_ARG="true"
      shift 2
      ;;
    --cloud-device-id)
      CLOUD_DEVICE_ID="${2:-}"
      HAS_CLOUD_DEVICE_ID_ARG="true"
      shift 2
      ;;
    --cloud-token)
      CLOUD_TOKEN="${2:-}"
      HAS_CLOUD_TOKEN_ARG="true"
      shift 2
      ;;
    --ensure-bridge)
      ENSURE_BRIDGE="true"
      shift 1
      ;;
    --bridge-cmd)
      BRIDGE_CMD="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown arg: $1" >&2
      usage
      exit 1
      ;;
  esac
done

die() {
  echo "$*" >&2
  exit 1
}

normalize_bool_or_empty() {
  local raw="${1:-}"
  local lower
  if [[ -z "$raw" ]]; then
    echo ""
    return 0
  fi
  lower="$(printf '%s' "$raw" | tr '[:upper:]' '[:lower:]')"
  case "$lower" in
    true|1|yes|y) echo "true" ;;
    false|0|no|n) echo "false" ;;
    *) die "invalid boolean value: $raw" ;;
  esac
}

normalize_deduplication_strategy_or_empty() {
  local raw="${1:-}"
  local lower
  if [[ -z "$raw" ]]; then
    echo ""
    return 0
  fi
  lower="$(printf '%s' "$raw" | tr '[:upper:]' '[:lower:]')"
  case "$lower" in
    keepold|old) echo "keepOld" ;;
    keepnew|new) echo "keepNew" ;;
    *) die "invalid deduplication strategy: $raw (expected keepOld or keepNew)" ;;
  esac
}

json_array_from_lines() {
  if [[ $# -eq 0 ]]; then
    echo "[]"
    return 0
  fi

  printf '%s\n' "$@" | node -e 'const fs=require("fs"); const arr=fs.readFileSync(0,"utf8").split(/\n/).filter(Boolean); process.stdout.write(JSON.stringify(arr));'
}

resolve_export_pref_script() {
  printf '%s\n' "$SKILL_DIR/scripts/export_preference.sh"
}

require_helper_script() {
  local path="${1:-}"
  local label="${2:-helper}"
  [[ -f "$path" ]] || die "missing ${label} script file: $path"
}

resolve_preference_value() {
  local key="${1:-}"
  local pref_script
  pref_script="$(resolve_export_pref_script)"
  if [[ ! -f "$pref_script" ]]; then
    return 0
  fi
  bash "$pref_script" get "$key" || true
}

apply_export_target() {
  local target="${1:-}"
  if [[ -z "$target" ]]; then
    return 0
  fi

  case "$target" in
    csv)
      AUTO_EXPORT="true"
      EXPORT_MODE="csv"
      ;;
    bitable)
      AUTO_EXPORT="true"
      EXPORT_MODE="personal"
      ;;
    *)
      die "invalid --export-target: $target (expected csv or bitable)"
      ;;
  esac
}

apply_stored_preferences() {
  local pref_connection_mode pref_platform pref_max_items pref_fetch_detail pref_detail_speed pref_deduplication pref_deduplication_strategy pref_bridge_url pref_cloud_base_url pref_cloud_device_id pref_cloud_token

  pref_connection_mode="$(resolve_preference_value defaultConnectionMode)"
  pref_platform="$(resolve_preference_value defaultPlatform)"
  pref_max_items="$(resolve_preference_value defaultMaxItems)"
  pref_fetch_detail="$(resolve_preference_value defaultFetchDetail)"
  pref_detail_speed="$(resolve_preference_value defaultDetailSpeed)"
  pref_deduplication="$(resolve_preference_value defaultDeduplicationEnabled)"
  pref_deduplication_strategy="$(resolve_preference_value defaultDeduplicationStrategy)"
  pref_bridge_url="$(resolve_preference_value defaultBridgeUrl)"
  pref_cloud_base_url="$(resolve_preference_value defaultCloudBaseUrl)"
  pref_cloud_device_id="$(resolve_preference_value defaultCloudDeviceId)"
  pref_cloud_token="$(resolve_preference_value defaultCloudToken)"

  [[ "$HAS_CONNECTION_MODE_ARG" == "true" || -z "$pref_connection_mode" ]] || CONNECTION_MODE="$pref_connection_mode"
  [[ "$HAS_PLATFORM_ARG" == "true" || -z "$pref_platform" ]] || PLATFORM="$pref_platform"
  [[ "$HAS_MAX_ITEMS_ARG" == "true" || -z "$pref_max_items" ]] || MAX_ITEMS="$pref_max_items"
  [[ "$HAS_FETCH_DETAIL_ARG" == "true" || -z "$pref_fetch_detail" ]] || FETCH_DETAIL="$pref_fetch_detail"
  [[ "$HAS_DETAIL_SPEED_ARG" == "true" || -z "$pref_detail_speed" ]] || DETAIL_SPEED="$pref_detail_speed"
  [[ "$HAS_DEDUPLICATION_ARG" == "true" || -z "$pref_deduplication" ]] || DEDUPLICATION="$pref_deduplication"
  [[ "$HAS_DEDUPLICATION_STRATEGY_ARG" == "true" || -z "$pref_deduplication_strategy" ]] || DEDUPLICATION_STRATEGY="$pref_deduplication_strategy"
  [[ "$HAS_BASE_URL_ARG" == "true" || -z "$pref_bridge_url" ]] || BRIDGE_URL="$pref_bridge_url"
  [[ "$HAS_CLOUD_BASE_URL_ARG" == "true" || -z "$pref_cloud_base_url" ]] || CLOUD_BASE_URL="$pref_cloud_base_url"
  [[ "$HAS_CLOUD_DEVICE_ID_ARG" == "true" || -z "$pref_cloud_device_id" ]] || CLOUD_DEVICE_ID="$pref_cloud_device_id"
  [[ "$HAS_CLOUD_TOKEN_ARG" == "true" || -z "$pref_cloud_token" ]] || CLOUD_TOKEN="$pref_cloud_token"
}

preferences_are_effectively_complete() {
  [[ -n "${AUTO_EXPORT:-}" && -n "${EXPORT_MODE:-}" && -n "${MAX_ITEMS:-}" && -n "${FETCH_DETAIL:-}" && -n "${DETAIL_SPEED:-}" ]]
}

ensure_required_preferences() {
  local pref_script
  pref_script="$(resolve_export_pref_script)"
  require_helper_script "$pref_script" "preference helper"

  if preferences_are_effectively_complete; then
    return 0
  fi

  if bash "$pref_script" check >/dev/null 2>&1; then
    return 0
  fi

  die "web-collection setup incomplete: ask the user to choose 推荐配置 or 自己配置 first, then persist all required defaults (export mode, max items, fetch detail, detail speed)"
}

normalize_connection_mode() {
  local raw="${1:-cloud}"
  local lower
  lower="$(printf '%s' "$raw" | tr '[:upper:]' '[:lower:]')"
  case "$lower" in
    local|cloud)
      printf '%s\n' "$lower"
      ;;
    *)
      die "invalid connection mode: $raw (expected local or cloud)"
      ;;
  esac
}

ensure_cloud_preferences() {
  [[ -n "$CLOUD_BASE_URL" ]] || die "cloud mode requires cloud base URL (set defaultCloudBaseUrl or pass --cloud-base-url)"
  [[ -n "$CLOUD_DEVICE_ID" ]] || die "cloud mode requires cloud device id (set defaultCloudDeviceId or pass --cloud-device-id)"
  [[ -n "$CLOUD_TOKEN" ]] || die "cloud mode requires cloud token (set defaultCloudToken or pass --cloud-token)"
}

apply_cloud_strict_defaults() {
  if [[ "$CONNECTION_MODE" != "cloud" ]]; then
    return 0
  fi

  # Cloud mode uses a strict template to avoid silently dropping fields when values are empty.
  [[ -n "$MAX_ITEMS" ]] || MAX_ITEMS="20"
  [[ -n "$FEATURE" ]] || FEATURE="video"
  [[ -n "$MODE" ]] || MODE="search"
  [[ -n "$INTERVAL_VAL" ]] || INTERVAL_VAL="300"
  [[ -n "$FETCH_DETAIL" ]] || FETCH_DETAIL="true"
  [[ -n "$DETAIL_SPEED" ]] || DETAIL_SPEED="fast"
}

route_config_rows() {
  cat <<'EOF'
douyin|videoKeyword|keywords|video|search|300|true|fast
douyin|creatorKeyword|keywords|account|search|||
douyin|creatorLink|links|account|account|||
douyin|creatorVideo|links|video|account|||
douyin|videoComment|links|comment|video_detail|||
douyin|videoInfo|links|video|video_detail|||
douyin|videoLink|links|video|video_detail|||
tiktok|keywordSearch|keywords|video|search|||
tiktok|userVideo|links|video|userVideo|||
tiktok|tiktokComment|links|comment|video_detail|||
tiktok|tiktokCreatorKeyword|keywords|account|search|||
tiktok|tiktokCreatorLink|links|account|account|||
xiaohongshu|keywordSearch|keywords|note|search|||
xiaohongshu|creatorNote|links|note|account|||
xiaohongshu|creatorLink|links|account|account|||
xiaohongshu|creatorKeyword|keywords|account|search|||
xiaohongshu|noteLink|links|note|note|||
xiaohongshu|noteComment|links|comment|note|||
amazon|keywordSearch|keywords|product|search|||
amazon|productLink|links|product|product_detail|||
amazon|productReview|links|comment|product_detail|||
bilibili|keywordSearch|keywords|video|search|||
bilibili|videoInfo|links|video|video_detail|||
bilibili|creatorVideo|links|video|account|||
bilibili|bilibiliComment|links|comment|video_detail|||
EOF
}

default_method_rows() {
  cat <<'EOF'
douyin|videoKeyword
tiktok|keywordSearch
xiaohongshu|keywordSearch
amazon|keywordSearch
bilibili|keywordSearch
EOF
}

lookup_route_config() {
  local platform="$1"
  local method="$2"
  while IFS='|' read -r row_platform row_method row_input row_feature row_mode row_interval row_fetch_detail row_detail_speed; do
    if [[ "$row_platform" == "$platform" && "$row_method" == "$method" ]]; then
      printf '%s|%s|%s|%s|%s|%s\n' \
        "$row_input" "$row_feature" "$row_mode" "$row_interval" "$row_fetch_detail" "$row_detail_speed"
      return 0
    fi
  done < <(route_config_rows)
  return 1
}

resolve_default_method() {
  local platform="$1"
  while IFS='|' read -r row_platform row_method; do
    if [[ "$row_platform" == "$platform" ]]; then
      printf '%s\n' "$row_method"
      return 0
    fi
  done < <(default_method_rows)
  return 1
}

resolve_defaults() {
  local route_config input_kind default_feature default_mode default_interval default_fetch_detail default_detail_speed

  if [[ -z "$METHOD" ]]; then
    if (( ${#LINKS[@]} > 0 )); then
      die "--method is required for link collection on platform=$PLATFORM"
    fi
    METHOD="$(resolve_default_method "$PLATFORM" || true)"
  fi

  if [[ -z "$METHOD" ]]; then
    die "unsupported platform: $PLATFORM"
  fi

  route_config="$(lookup_route_config "$PLATFORM" "$METHOD" || true)"
  if [[ -z "$route_config" ]]; then
    die "unsupported platform/method: $PLATFORM/$METHOD"
  fi

  IFS='|' read -r input_kind default_feature default_mode default_interval default_fetch_detail default_detail_speed <<<"$route_config"

  [[ -n "$FEATURE" ]] || FEATURE="$default_feature"
  [[ -n "$MODE" ]] || MODE="$default_mode"
  [[ -n "$INTERVAL_VAL" || -z "$default_interval" ]] || INTERVAL_VAL="$default_interval"
  [[ -n "$FETCH_DETAIL" || -z "$default_fetch_detail" ]] || FETCH_DETAIL="$default_fetch_detail"
  [[ -n "$DETAIL_SPEED" || -z "$default_detail_speed" ]] || DETAIL_SPEED="$default_detail_speed"
}

validate_inputs() {
  local route_config input_kind

  if [[ -z "$PLATFORM" ]]; then
    die "--platform is required"
  fi
  if [[ -z "$METHOD" ]]; then
    die "--method is required"
  fi

  route_config="$(lookup_route_config "$PLATFORM" "$METHOD" || true)"
  if [[ -z "$route_config" ]]; then
    die "unsupported platform/method: $PLATFORM/$METHOD"
  fi

  IFS='|' read -r input_kind _ <<<"$route_config"

  case "$input_kind" in
    keywords)
      if (( ${#KEYWORDS[@]} == 0 )); then
        die "--keyword is required for method=$METHOD"
      fi
      ;;
    links)
      if (( ${#LINKS[@]} == 0 )); then
        die "--link is required for method=$METHOD"
      fi
      ;;
  esac
}

build_payload_json() {
  local keywords_json links_json fetch_detail_bool auto_export_bool deduplication_bool deduplication_strategy

  keywords_json="$(json_array_from_lines "${KEYWORDS[@]-}")"
  links_json="$(json_array_from_lines "${LINKS[@]-}")"
  fetch_detail_bool="$(normalize_bool_or_empty "$FETCH_DETAIL")"
  auto_export_bool="$(normalize_bool_or_empty "$AUTO_EXPORT")"
  deduplication_bool="$(normalize_bool_or_empty "$DEDUPLICATION")"
  deduplication_strategy="$(normalize_deduplication_strategy_or_empty "$DEDUPLICATION_STRATEGY")"

  export PLATFORM METHOD MAX_ITEMS FEATURE MODE INTERVAL_VAL DETAIL_SPEED DETAIL_DELAY REPLY_LEVEL EXPORT_MODE TABLE_NAME FIELDS_JSON FILTERS_JSON keywords_json links_json fetch_detail_bool auto_export_bool deduplication_bool deduplication_strategy
  node -e '
const out = {};
const parseJSON = (value, fallback) => {
  if (!value) return fallback;
  try { return JSON.parse(value); } catch (error) {
    process.stderr.write(`invalid json input: ${error.message}\n`);
    process.exit(2);
  }
};
const set = (key, value) => {
  if (value === "" || value === undefined || value === null) return;
  out[key] = value;
};

const keywords = parseJSON(process.env.keywords_json, []);
const links = parseJSON(process.env.links_json, []);
const fields = process.env.FIELDS_JSON ? parseJSON(process.env.FIELDS_JSON, null) : null;
const filters = process.env.FILTERS_JSON ? parseJSON(process.env.FILTERS_JSON, null) : null;

set("platform", process.env.PLATFORM);
set("method", process.env.METHOD);
if (Array.isArray(keywords) && keywords.length > 0) out.keywords = keywords;
if (Array.isArray(links) && links.length > 0) out.links = links;
set("maxItems", process.env.MAX_ITEMS ? Number(process.env.MAX_ITEMS) : "");
set("feature", process.env.FEATURE);
set("mode", process.env.MODE);
set("interval", process.env.INTERVAL_VAL ? Number(process.env.INTERVAL_VAL) : "");
set("fetchDetail", process.env.fetch_detail_bool === "" ? "" : process.env.fetch_detail_bool === "true");
set("detailSpeed", process.env.DETAIL_SPEED);
set("detailDelay", process.env.DETAIL_DELAY ? Number(process.env.DETAIL_DELAY) : "");
set("replyLevel", process.env.REPLY_LEVEL ? Number(process.env.REPLY_LEVEL) : "");
set("autoExport", process.env.auto_export_bool === "" ? "" : process.env.auto_export_bool === "true");
set("exportMode", process.env.EXPORT_MODE);
set("tableName", process.env.TABLE_NAME);
if (fields !== null) out.fields = fields;
if (filters !== null) out.filters = filters;

const exportMode = process.env.EXPORT_MODE || "";
if (process.env.auto_export_bool !== "" || exportMode) {
  const exportPlan = {
    enabled: process.env.auto_export_bool === "" ? true : process.env.auto_export_bool === "true",
  };
  if (exportMode) {
    exportPlan.mode = exportMode;
  }
  if (exportMode === "personal") {
    exportPlan.deduplication = {
      enabled: process.env.deduplication_bool === "" ? true : process.env.deduplication_bool === "true",
      strategy: process.env.deduplication_strategy || "keepOld",
    };
  }
  out.export = exportPlan;
}

process.stdout.write(JSON.stringify(out));
'
}

build_preflight_config_json() {
  local keywords_json links_json
  keywords_json="$(json_array_from_lines "${KEYWORDS[@]-}")"
  links_json="$(json_array_from_lines "${LINKS[@]-}")"

  export CONNECTION_MODE PLATFORM METHOD MAX_ITEMS FETCH_DETAIL DETAIL_SPEED EXPORT_TARGET DEDUPLICATION DEDUPLICATION_STRATEGY BRIDGE_URL CLOUD_BASE_URL CLOUD_DEVICE_ID CLOUD_TOKEN keywords_json links_json
  node -e '
const config = {};

const parseJSON = (value, fallback) => {
  if (!value) return fallback;
  try { return JSON.parse(value); } catch { return fallback; }
};

const set = (key, value) => {
  if (value === "" || value === undefined || value === null) return;
  config[key] = value;
};

set("connectionMode", process.env.CONNECTION_MODE);
set("platform", process.env.PLATFORM);
set("method", process.env.METHOD);
const keywords = parseJSON(process.env.keywords_json, []);
const links = parseJSON(process.env.links_json, []);
if (Array.isArray(keywords) && keywords.length > 0) config.keywords = keywords;
if (Array.isArray(links) && links.length > 0) config.links = links;
set("defaultMaxItems", process.env.MAX_ITEMS ? Number(process.env.MAX_ITEMS) : "");
set("defaultFetchDetail", process.env.FETCH_DETAIL);
set("defaultDetailSpeed", process.env.DETAIL_SPEED);
set("defaultDeduplicationEnabled", process.env.DEDUPLICATION);
set("defaultDeduplicationStrategy", process.env.DEDUPLICATION_STRATEGY);
set("defaultBridgeUrl", process.env.BRIDGE_URL);
set("defaultCloudBaseUrl", process.env.CLOUD_BASE_URL);
set("defaultCloudDeviceId", process.env.CLOUD_DEVICE_ID);
set("defaultCloudToken", process.env.CLOUD_TOKEN);
set("exportTarget", process.env.EXPORT_TARGET);

process.stdout.write(JSON.stringify(config));
'
}

run_preflight_check() {
  local preflight_script config_json
  preflight_script="$SKILL_DIR/scripts/preflight_check.sh"
  require_helper_script "$preflight_script" "preflight helper"
  config_json="$(build_preflight_config_json)"
  bash "$preflight_script" \
    --config-json "$config_json" \
    --mode "$CONNECTION_MODE" \
    --format json \
    --quiet-success >/dev/null
  echo "[web-collection] preflight ok" >&2
}

default_bridge_cmd() {
  local source_server="/Users/zhym/coding/web_pluging/web_collection/bridge/bridge-server.js"
  if command -v node >/dev/null 2>&1 && [[ -f "$source_server" ]]; then
    printf "node '%s'" "$source_server"
    return 0
  fi

  local runtime="/Library/Application Support/meixi-connector/runtime/node"
  local server="/Library/Application Support/meixi-connector/connector/connector-server.js"
  if [[ -x "$runtime" && -f "$server" ]]; then
    printf "'%s' '%s'" "$runtime" "$server"
    return 0
  fi
  return 1
}

resolve_loop_script() {
  printf '%s\n' "$SKILL_DIR/scripts/collect_and_export_loop.sh"
}

resolve_cloud_loop_script() {
  printf '%s\n' "$SKILL_DIR/scripts/cloud_dispatch_loop.sh"
}

if [[ -z "$BRIDGE_CMD" ]]; then
  BRIDGE_CMD="$(default_bridge_cmd || true)"
fi

apply_stored_preferences
[[ -n "$DEDUPLICATION" ]] || DEDUPLICATION="true"
[[ -n "$DEDUPLICATION_STRATEGY" ]] || DEDUPLICATION_STRATEGY="keepOld"
CONNECTION_MODE="$(normalize_connection_mode "$CONNECTION_MODE")"
run_preflight_check

if [[ -n "$EXPORT_TARGET" ]]; then
  apply_export_target "$EXPORT_TARGET"
elif [[ -z "${EXPORT_MODE:-}" && -z "${AUTO_EXPORT:-}" ]]; then
  pref_mode="$(resolve_preference_value defaultExportMode)"
  if [[ -z "$pref_mode" ]]; then
    die "web-collection setup incomplete: choose 推荐配置 or 自己配置 first (or run scripts/export_preference.sh apply-recommended)"
  fi
  apply_export_target "$pref_mode"
fi

ensure_required_preferences

resolve_defaults
apply_cloud_strict_defaults
validate_inputs
PAYLOAD_JSON="$(build_payload_json)"

run_collect_local() {
  local bridge_url="$1"
  local payload_json="$2"
  local loop_script
  loop_script="$(resolve_loop_script)"
  local cmd=(
    bash "$loop_script"
    --payload "$payload_json"
    --force-stop-before-start
    --base-url "$bridge_url"
  )

  if [[ "$ENSURE_BRIDGE" == "true" ]]; then
    cmd+=(--ensure-bridge)
    if [[ -n "$BRIDGE_CMD" ]]; then
      cmd+=(--bridge-cmd "$BRIDGE_CMD")
    fi
  fi

  "${cmd[@]}"
}

run_collect_cloud() {
  local cloud_base_url="$1"
  local cloud_device_id="$2"
  local cloud_token="$3"
  local payload_json="$4"
  local loop_script
  loop_script="$(resolve_cloud_loop_script)"

  bash "$loop_script" \
    --payload "$payload_json" \
    --base-url "$cloud_base_url" \
    --device-id "$cloud_device_id" \
    --token "$cloud_token"
}

if [[ "$CONNECTION_MODE" == "cloud" ]]; then
  ensure_cloud_preferences
  echo "[web-collection] mode=cloud base=$CLOUD_BASE_URL device=$CLOUD_DEVICE_ID" >&2
  run_collect_cloud "$CLOUD_BASE_URL" "$CLOUD_DEVICE_ID" "$CLOUD_TOKEN" "$PAYLOAD_JSON"
else
  echo "[web-collection] mode=local bridge=$BRIDGE_URL" >&2
  run_collect_local "$BRIDGE_URL" "$PAYLOAD_JSON"
fi
