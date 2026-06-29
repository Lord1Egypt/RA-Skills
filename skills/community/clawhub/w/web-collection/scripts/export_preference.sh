#!/usr/bin/env bash
set -euo pipefail

resolve_state_dir() {
  if [[ -n "${OPENCLAW_STATE_DIR:-}" ]]; then
    printf '%s\n' "$OPENCLAW_STATE_DIR"
    return 0
  fi
  printf '%s\n' "${HOME}/.openclaw"
}

resolve_preferences_path() {
  local state_dir
  state_dir="$(resolve_state_dir)"
  printf '%s\n' "${state_dir}/skill-state/web-collection/preferences.json"
}

resolve_legacy_export_mode_path() {
  local state_dir
  state_dir="$(resolve_state_dir)"
  printf '%s\n' "${state_dir}/skill-state/web-collection/export-mode.json"
}

read_preferences_json() {
  local pref_path="$1"
  local legacy_path="$2"

  if [[ -f "$pref_path" ]]; then
    cat "$pref_path"
    return 0
  fi

  if [[ -f "$legacy_path" ]]; then
    cat "$legacy_path"
    return 0
  fi

  printf '{}\n'
}

normalize_key() {
  local key="${1:-}"
  case "$key" in
    mode|connectionMode|defaultConnectionMode)
      printf '%s\n' "defaultConnectionMode"
      ;;
    export|exportMode|defaultExportMode|"")
      printf '%s\n' "defaultExportMode"
      ;;
    platform|defaultPlatform)
      printf '%s\n' "defaultPlatform"
      ;;
    maxItems|defaultMaxItems)
      printf '%s\n' "defaultMaxItems"
      ;;
    fetchDetail|defaultFetchDetail)
      printf '%s\n' "defaultFetchDetail"
      ;;
    detailSpeed|defaultDetailSpeed)
      printf '%s\n' "defaultDetailSpeed"
      ;;
    deduplication|dedupe|deduplicationEnabled|defaultDeduplicationEnabled)
      printf '%s\n' "defaultDeduplicationEnabled"
      ;;
    deduplicationStrategy|dedupeStrategy|defaultDeduplicationStrategy)
      printf '%s\n' "defaultDeduplicationStrategy"
      ;;
    localBaseUrl|defaultLocalBaseUrl|bridgeUrl|defaultBridgeUrl)
      printf '%s\n' "defaultBridgeUrl"
      ;;
    cloudBaseUrl|defaultCloudBaseUrl)
      printf '%s\n' "defaultCloudBaseUrl"
      ;;
    cloudDeviceId|defaultCloudDeviceId)
      printf '%s\n' "defaultCloudDeviceId"
      ;;
    cloudToken|defaultCloudToken)
      printf '%s\n' "defaultCloudToken"
      ;;
    *)
      printf '%s\n' "$key"
      ;;
  esac
}

validate_key_value() {
  local key="$1"
  local value="$2"

  case "$key" in
    defaultConnectionMode)
      [[ "$value" == "local" || "$value" == "cloud" ]] || {
        echo "invalid connection mode: $value (expected local or cloud)" >&2
        exit 1
      }
      ;;
    defaultExportMode)
      [[ "$value" == "csv" || "$value" == "bitable" ]] || {
        echo "invalid export mode: $value (expected csv or bitable)" >&2
        exit 1
      }
      ;;
    defaultPlatform)
      case "$value" in
        douyin|tiktok|xiaohongshu|amazon|bilibili) ;;
        *)
          echo "invalid platform: $value" >&2
          exit 1
          ;;
      esac
      ;;
    defaultMaxItems)
      [[ "$value" =~ ^[0-9]+$ ]] || {
        echo "invalid max items: $value (expected integer)" >&2
        exit 1
      }
      ;;
    defaultFetchDetail)
      case "$value" in
        true|false) ;;
        *)
          echo "invalid fetchDetail: $value (expected true or false)" >&2
          exit 1
          ;;
      esac
      ;;
    defaultDetailSpeed)
      case "$value" in
        slow|medium|fast) ;;
        *)
          echo "invalid detailSpeed: $value (expected slow, medium, or fast)" >&2
          exit 1
          ;;
      esac
      ;;
    defaultDeduplicationEnabled)
      case "$value" in
        true|false) ;;
        *)
          echo "invalid deduplication enabled: $value (expected true or false)" >&2
          exit 1
          ;;
      esac
      ;;
    defaultDeduplicationStrategy)
      case "$value" in
        keepOld|keepNew) ;;
        *)
          echo "invalid deduplication strategy: $value (expected keepOld or keepNew)" >&2
          exit 1
          ;;
      esac
      ;;
    defaultBridgeUrl)
      [[ -n "$value" ]] || {
        echo "invalid bridgeUrl: empty" >&2
        exit 1
      }
      ;;
    defaultCloudBaseUrl)
      [[ -n "$value" ]] || {
        echo "invalid cloudBaseUrl: empty" >&2
        exit 1
      }
      ;;
    defaultCloudDeviceId)
      [[ -n "$value" ]] || {
        echo "invalid cloudDeviceId: empty" >&2
        exit 1
      }
      ;;
    defaultCloudToken)
      [[ -n "$value" ]] || {
        echo "invalid cloudToken: empty" >&2
        exit 1
      }
      ;;
  esac
}

print_value() {
  local key="$1"
  local pref_path="$2"
  local legacy_path="$3"

  node -e '
const fs = require("node:fs");
const prefPath = process.argv[1];
const legacyPath = process.argv[2];
const key = process.argv[3];

const read = (filePath) => {
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch {
    return null;
  }
};

const data = read(prefPath) ?? read(legacyPath) ?? {};
const value = data[key];
if (value === undefined || value === null) {
  process.exit(0);
}
if (typeof value === "object") {
  process.stdout.write(JSON.stringify(value));
} else {
  process.stdout.write(String(value));
}
' "$pref_path" "$legacy_path" "$key"
}

write_value() {
  local key="$1"
  local value="$2"
  local pref_path="$3"
  local legacy_path="$4"

  mkdir -p "$(dirname "$pref_path")"

  node -e '
const fs = require("node:fs");
const prefPath = process.argv[1];
const legacyPath = process.argv[2];
const key = process.argv[3];
const rawValue = process.argv[4];

const read = (filePath) => {
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch {
    return null;
  }
};

let value = rawValue;
if (rawValue === "true") value = true;
else if (rawValue === "false") value = false;
else if (/^[0-9]+$/.test(rawValue)) value = Number(rawValue);

const data = read(prefPath) ?? read(legacyPath) ?? {};
data[key] = value;
data.updatedAt = new Date().toISOString();
data.updatedBy = "user";

const tempPath = `${prefPath}.tmp-${process.pid}`;
fs.writeFileSync(tempPath, JSON.stringify(data, null, 2) + "\n", "utf8");
fs.renameSync(tempPath, prefPath);
' "$pref_path" "$legacy_path" "$key" "$value"
}

unset_value() {
  local key="$1"
  local pref_path="$2"
  local legacy_path="$3"

  mkdir -p "$(dirname "$pref_path")"

  node -e '
const fs = require("node:fs");
const prefPath = process.argv[1];
const legacyPath = process.argv[2];
const key = process.argv[3];

const read = (filePath) => {
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch {
    return null;
  }
};

const data = read(prefPath) ?? read(legacyPath) ?? {};
delete data[key];
data.updatedAt = new Date().toISOString();
data.updatedBy = "user";

const tempPath = `${prefPath}.tmp-${process.pid}`;
fs.writeFileSync(tempPath, JSON.stringify(data, null, 2) + "\n", "utf8");
fs.renameSync(tempPath, prefPath);
' "$pref_path" "$legacy_path" "$key"
}

show_preferences() {
  local pref_path="$1"
  local legacy_path="$2"

  node -e '
const fs = require("node:fs");
const prefPath = process.argv[1];
const legacyPath = process.argv[2];

const read = (filePath) => {
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch {
    return null;
  }
};

const mask = (value) => {
  if (typeof value !== "string" || value.length === 0) return value;
  if (value.length <= 8) return "****";
  return `${value.slice(0, 4)}...${value.slice(-4)}`;
};

const data = read(prefPath) ?? read(legacyPath) ?? {};
if (typeof data.defaultCloudToken === "string" && data.defaultCloudToken) {
  data.defaultCloudToken = mask(data.defaultCloudToken);
}
process.stdout.write(JSON.stringify(data, null, 2) + "\n");
' "$pref_path" "$legacy_path"
}

check_required_preferences() {
  local pref_path="$1"
  local legacy_path="$2"

  node -e '
const fs = require("node:fs");
const prefPath = process.argv[1];
const legacyPath = process.argv[2];

const read = (filePath) => {
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch {
    return null;
  }
};

const data = read(prefPath) ?? read(legacyPath) ?? {};
const envMode = typeof process.env.WEB_COLLECTION_CONNECTION_MODE === "string" && process.env.WEB_COLLECTION_CONNECTION_MODE
  ? process.env.WEB_COLLECTION_CONNECTION_MODE
  : "";
const mode = envMode || (typeof data.defaultConnectionMode === "string" && data.defaultConnectionMode
  ? data.defaultConnectionMode
  : "cloud");
const envCloudDeviceId = typeof process.env.WEB_COLLECTION_CLOUD_DEVICE_ID === "string"
  ? process.env.WEB_COLLECTION_CLOUD_DEVICE_ID
  : "";
const envCloudToken = typeof process.env.WEB_COLLECTION_CLOUD_TOKEN === "string"
  ? process.env.WEB_COLLECTION_CLOUD_TOKEN
  : "";
const redactedPreferences = { ...data };
if (typeof redactedPreferences.defaultCloudToken === "string" && redactedPreferences.defaultCloudToken) {
  const token = redactedPreferences.defaultCloudToken;
  redactedPreferences.defaultCloudToken = token.length <= 8 ? "****" : `${token.slice(0, 4)}...${token.slice(-4)}`;
}
const required = [
  "defaultExportMode",
  "defaultMaxItems",
  "defaultFetchDetail",
  "defaultDetailSpeed",
];

const missing = required.filter((key) => data[key] === undefined || data[key] === null || data[key] === "");
const result = {
  complete: missing.length === 0,
  mode,
  missing,
  envConfig: {
    cloudDeviceIdPresent: Boolean(envCloudDeviceId),
    cloudTokenPresent: Boolean(envCloudToken),
  },
  preferences: redactedPreferences,
};

process.stdout.write(JSON.stringify(result, null, 2) + "\n");
process.exit(missing.length === 0 ? 0 : 1);
' "$pref_path" "$legacy_path"
}

apply_recommended_preferences() {
  local pref_path="$1"
  local legacy_path="$2"
  write_value "defaultConnectionMode" "cloud" "$pref_path" "$legacy_path"
  write_value "defaultExportMode" "bitable" "$pref_path" "$legacy_path"
  write_value "defaultMaxItems" "20" "$pref_path" "$legacy_path"
  write_value "defaultFetchDetail" "true" "$pref_path" "$legacy_path"
  write_value "defaultDetailSpeed" "fast" "$pref_path" "$legacy_path"
  write_value "defaultDeduplicationEnabled" "true" "$pref_path" "$legacy_path"
  write_value "defaultDeduplicationStrategy" "keepOld" "$pref_path" "$legacy_path"
  show_preferences "$pref_path" "$legacy_path"
}

usage() {
  cat <<'EOF'
Usage:
  export_preference.sh path
  export_preference.sh show
  export_preference.sh check
  export_preference.sh get [key]
  export_preference.sh set <csv|bitable>
  export_preference.sh apply-recommended
  export_preference.sh set-key <key> <value>
  export_preference.sh unset-key <key>
  export_preference.sh clear

Supported keys:
  defaultConnectionMode local | cloud
  defaultExportMode   csv | bitable
  defaultPlatform     douyin | tiktok | xiaohongshu | amazon | bilibili
  defaultMaxItems     integer
  defaultFetchDetail  true | false
  defaultDetailSpeed  slow | medium | fast
  defaultDeduplicationEnabled true | false
  defaultDeduplicationStrategy keepOld | keepNew
  defaultBridgeUrl    string
  defaultCloudBaseUrl string
  defaultCloudDeviceId string
  defaultCloudToken   string
EOF
}

main() {
  local cmd="${1:-}"
  local pref_path legacy_path key value
  pref_path="$(resolve_preferences_path)"
  legacy_path="$(resolve_legacy_export_mode_path)"

  case "$cmd" in
    path)
      printf '%s\n' "$pref_path"
      ;;
    show)
      show_preferences "$pref_path" "$legacy_path"
      ;;
    check)
      check_required_preferences "$pref_path" "$legacy_path"
      ;;
    get)
      key="$(normalize_key "${2:-}")"
      print_value "$key" "$pref_path" "$legacy_path"
      ;;
    set)
      value="${2:-}"
      key="defaultExportMode"
      validate_key_value "$key" "$value"
      write_value "$key" "$value" "$pref_path" "$legacy_path"
      printf '%s\n' "$value"
      ;;
    apply-recommended)
      apply_recommended_preferences "$pref_path" "$legacy_path"
      ;;
    set-key)
      key="$(normalize_key "${2:-}")"
      value="${3:-}"
      if [[ -z "$key" || -z "$value" ]]; then
        echo "set-key requires <key> <value>" >&2
        exit 1
      fi
      validate_key_value "$key" "$value"
      write_value "$key" "$value" "$pref_path" "$legacy_path"
      printf '%s=%s\n' "$key" "$value"
      ;;
    unset-key)
      key="$(normalize_key "${2:-}")"
      if [[ -z "$key" ]]; then
        echo "unset-key requires <key>" >&2
        exit 1
      fi
      unset_value "$key" "$pref_path" "$legacy_path"
      ;;
    clear)
      rm -f "$pref_path" "$legacy_path"
      ;;
    -h|--help|help|"")
      usage
      ;;
    *)
      echo "unknown subcommand: $cmd" >&2
      usage
      exit 1
      ;;
  esac
}

main "$@"
