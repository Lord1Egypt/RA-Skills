#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PREFERENCE_SCRIPT="$SKILL_DIR/scripts/export_preference.sh"
DEFAULT_BRIDGE_URL="${WEB_COLLECTION_BRIDGE_URL:-http://127.0.0.1:19820}"
DEFAULT_CLOUD_BASE_URL="${WEB_COLLECTION_CLOUD_BASE_URL:-https://i-sync.cn}"

CONFIG_JSON=""
CONFIG_FILE=""
WRITE_PREFERENCES="false"
PROBE_BRIDGE="false"
FORMAT="json"
QUIET_SUCCESS="false"
MODE="cloud"

usage() {
  cat <<'EOF'
Usage:
  preflight_check.sh [options]

Options:
  --config-json <json>      Inline config and/or defaults
  --config-file <path>      Read config JSON from file
  --write-preferences       Persist provided defaults before checking
  --probe-bridge            Probe local /api/status when mode=local
  --mode <local|cloud>      Execution mode, default: cloud
  --format <json|text>      Output format, default: json
  --quiet-success           Print nothing when ready
  -h, --help
EOF
}

die() {
  echo "$*" >&2
  exit 1
}

require_helper_script() {
  local path="${1:-}"
  local label="${2:-helper}"
  [[ -f "$path" ]] || die "missing ${label} script file: $path"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --config-json)
      CONFIG_JSON="${2:-}"
      shift 2
      ;;
    --config-file)
      CONFIG_FILE="${2:-}"
      shift 2
      ;;
    --write-preferences)
      WRITE_PREFERENCES="true"
      shift 1
      ;;
    --probe-bridge)
      PROBE_BRIDGE="true"
      shift 1
      ;;
    --mode)
      MODE="${2:-cloud}"
      shift 2
      ;;
    --format)
      FORMAT="${2:-json}"
      shift 2
      ;;
    --quiet-success)
      QUIET_SUCCESS="true"
      shift 1
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      die "unknown arg: $1"
      ;;
  esac
done

[[ "$FORMAT" == "json" || "$FORMAT" == "text" ]] || die "invalid --format: $FORMAT"
[[ "$MODE" == "local" || "$MODE" == "cloud" ]] || die "invalid --mode: $MODE"

if [[ -n "$CONFIG_FILE" ]]; then
  [[ -f "$CONFIG_FILE" ]] || die "config file not found: $CONFIG_FILE"
  CONFIG_JSON="$(cat "$CONFIG_FILE")"
fi

if [[ -z "$CONFIG_JSON" ]]; then
  CONFIG_JSON='{}'
fi

normalize_config_json() {
  node -e '
const raw = JSON.parse(process.argv[1] || "{}");
const defaults = raw.defaults && typeof raw.defaults === "object" ? raw.defaults : {};
const preferences = raw.preferences && typeof raw.preferences === "object" ? raw.preferences : {};
const merged = { ...raw, ...preferences, ...defaults };

const normalizeBoolean = (value) => {
  if (value === undefined || value === null || value === "") return "";
  if (typeof value === "boolean") return value ? "true" : "false";
  const lower = String(value).trim().toLowerCase();
  if (["true", "1", "yes", "y", "是"].includes(lower)) return "true";
  if (["false", "0", "no", "n", "否"].includes(lower)) return "false";
  return value;
};

const normalizeExportMode = (value) => {
  if (value === undefined || value === null || value === "") return "";
  const lower = String(value).trim().toLowerCase();
  if (["bitable", "personal", "多维表格"].includes(lower)) return "bitable";
  if (["csv"].includes(lower)) return "csv";
  return value;
};

const normalizeDeduplicationStrategy = (value) => {
  if (value === undefined || value === null || value === "") return "";
  const raw = String(value).trim();
  const lower = raw.toLowerCase();
  if (["keepold", "old", "保留原始", "保留原始数据"].includes(lower)) return "keepOld";
  if (["keepnew", "new", "保留新数据"].includes(lower)) return "keepNew";
  return raw;
};

const normalizeMode = (value) => {
  if (value === undefined || value === null || value === "") return "";
  return String(value).trim().toLowerCase();
};

const normalizeString = (value) => {
  if (value === undefined || value === null || value === "") return "";
  return String(value).trim();
};

const normalizeNumber = (value) => {
  if (value === undefined || value === null || value === "") return "";
  const n = Number(value);
  return Number.isFinite(n) ? String(n) : value;
};

const normalizeStringArray = (value) => {
  if (value === undefined || value === null || value === "") return [];
  if (Array.isArray(value)) return value.map((item) => String(item));
  return [String(value)];
};

process.stdout.write(JSON.stringify({
  defaults: {
    defaultConnectionMode: normalizeMode(
      merged.defaultConnectionMode ?? merged.connectionMode ?? merged.mode
    ),
    defaultExportMode: normalizeExportMode(
      merged.defaultExportMode ?? merged.exportTarget ?? merged.exportMode
    ),
    defaultMaxItems: normalizeNumber(merged.defaultMaxItems ?? merged.maxItems),
    defaultFetchDetail: normalizeBoolean(merged.defaultFetchDetail ?? merged.fetchDetail),
    defaultDetailSpeed: normalizeMode(merged.defaultDetailSpeed ?? merged.detailSpeed),
    defaultDeduplicationEnabled: normalizeBoolean(
      merged.defaultDeduplicationEnabled
        ?? merged.deduplicationEnabled
        ?? merged.deduplication?.enabled
        ?? merged.export?.deduplication?.enabled
    ),
    defaultDeduplicationStrategy: normalizeDeduplicationStrategy(
      merged.defaultDeduplicationStrategy
        ?? merged.deduplicationStrategy
        ?? merged.deduplication?.strategy
        ?? merged.export?.deduplication?.strategy
    ),
    defaultPlatform: normalizeMode(merged.defaultPlatform ?? merged.platform),
    defaultBridgeUrl: normalizeString(merged.defaultBridgeUrl ?? merged.baseUrl ?? merged.bridgeUrl),
    defaultCloudBaseUrl: normalizeString(merged.defaultCloudBaseUrl ?? merged.cloudBaseUrl),
    defaultCloudDeviceId: normalizeString(merged.defaultCloudDeviceId ?? merged.cloudDeviceId ?? merged.id),
    defaultCloudToken: normalizeString(merged.defaultCloudToken ?? merged.cloudToken ?? merged.token),
  },
  runtime: {
    platform: normalizeMode(merged.platform),
    method: normalizeString(merged.method),
    keywords: normalizeStringArray(merged.keywords),
    links: normalizeStringArray(merged.links),
    baseUrl: normalizeString(merged.baseUrl ?? merged.defaultBridgeUrl ?? merged.bridgeUrl),
    cloudBaseUrl: normalizeString(merged.cloudBaseUrl ?? merged.defaultCloudBaseUrl),
    cloudDeviceId: normalizeString(merged.cloudDeviceId ?? merged.defaultCloudDeviceId ?? merged.id),
    cloudToken: normalizeString(merged.cloudToken ?? merged.defaultCloudToken ?? merged.token),
    exportTarget: normalizeExportMode(
      merged.exportTarget ?? merged.defaultExportMode ?? merged.exportMode
    ),
  },
}));
' "$CONFIG_JSON"
}

NORMALIZED_CONFIG="$(normalize_config_json)"

write_preferences_from_config() {
  local normalized_json="$1"
  local rows
  rows="$(node -e '
const normalized = JSON.parse(process.argv[1]);
const defaults = normalized.defaults || {};
const order = [
  "defaultConnectionMode",
  "defaultExportMode",
  "defaultMaxItems",
  "defaultFetchDetail",
  "defaultDetailSpeed",
  "defaultDeduplicationEnabled",
  "defaultDeduplicationStrategy",
  "defaultPlatform",
  "defaultBridgeUrl",
  "defaultCloudBaseUrl",
  "defaultCloudDeviceId",
  "defaultCloudToken",
];
for (const key of order) {
  const value = defaults[key];
  if (value === undefined || value === null || value === "") continue;
  process.stdout.write(`${key}\t${String(value)}\n`);
}
' "$normalized_json")"

  if [[ -z "$rows" ]]; then
    return 0
  fi

  while IFS=$'\t' read -r key value; do
    [[ -n "$key" && -n "$value" ]] || continue
    bash "$PREFERENCE_SCRIPT" set-key "$key" "$value" >/dev/null
  done <<<"$rows"
}

if [[ "$WRITE_PREFERENCES" == "true" ]]; then
  require_helper_script "$PREFERENCE_SCRIPT" "preference helper"
  write_preferences_from_config "$NORMALIZED_CONFIG"
fi

build_summary_json() {
  local normalized_json="$1"
  PREF_SCRIPT="$PREFERENCE_SCRIPT" DEFAULT_BRIDGE_URL="$DEFAULT_BRIDGE_URL" DEFAULT_CLOUD_BASE_URL="$DEFAULT_CLOUD_BASE_URL" node -e '
const { execFileSync } = require("node:child_process");
const fs = require("node:fs");

const normalized = JSON.parse(process.argv[1]);
const mode = process.argv[2];
const skillDir = process.argv[3];

const getPref = (key) => {
  try {
    return execFileSync("bash", [process.env.PREF_SCRIPT, "get", key], {
      encoding: "utf8",
      stdio: ["ignore", "pipe", "ignore"],
    }).trim();
  } catch {
    return "";
  }
};

const defaults = normalized.defaults || {};
const runtime = normalized.runtime || {};
const envConfig = {
  bridgeUrl: process.env.WEB_COLLECTION_BRIDGE_URL || "",
  cloudBaseUrl: process.env.WEB_COLLECTION_CLOUD_BASE_URL || process.env.DEFAULT_CLOUD_BASE_URL || "",
  cloudDeviceId: process.env.WEB_COLLECTION_CLOUD_DEVICE_ID || "",
  cloudToken: process.env.WEB_COLLECTION_CLOUD_TOKEN || "",
};
const stored = {
  defaultExportMode: getPref("defaultExportMode"),
  defaultMaxItems: getPref("defaultMaxItems"),
  defaultFetchDetail: getPref("defaultFetchDetail"),
  defaultDetailSpeed: getPref("defaultDetailSpeed"),
  defaultDeduplicationEnabled: getPref("defaultDeduplicationEnabled"),
  defaultDeduplicationStrategy: getPref("defaultDeduplicationStrategy"),
  defaultPlatform: getPref("defaultPlatform"),
  defaultBridgeUrl: getPref("defaultBridgeUrl"),
  defaultCloudBaseUrl: getPref("defaultCloudBaseUrl"),
  defaultCloudDeviceId: getPref("defaultCloudDeviceId"),
  defaultCloudToken: getPref("defaultCloudToken"),
};
const effective = {
  defaultExportMode: defaults.defaultExportMode || stored.defaultExportMode || "",
  defaultMaxItems: defaults.defaultMaxItems || stored.defaultMaxItems || "",
  defaultFetchDetail: defaults.defaultFetchDetail || stored.defaultFetchDetail || "",
  defaultDetailSpeed: defaults.defaultDetailSpeed || stored.defaultDetailSpeed || "",
  defaultDeduplicationEnabled: defaults.defaultDeduplicationEnabled || stored.defaultDeduplicationEnabled || "true",
  defaultDeduplicationStrategy: defaults.defaultDeduplicationStrategy || stored.defaultDeduplicationStrategy || "keepOld",
  defaultPlatform: defaults.defaultPlatform || stored.defaultPlatform || "",
  defaultBridgeUrl: runtime.baseUrl || envConfig.bridgeUrl || defaults.defaultBridgeUrl || stored.defaultBridgeUrl || process.env.DEFAULT_BRIDGE_URL || "",
  defaultCloudBaseUrl: runtime.cloudBaseUrl || envConfig.cloudBaseUrl || defaults.defaultCloudBaseUrl || stored.defaultCloudBaseUrl || process.env.DEFAULT_CLOUD_BASE_URL || "",
  defaultCloudDeviceId: runtime.cloudDeviceId || envConfig.cloudDeviceId || defaults.defaultCloudDeviceId || stored.defaultCloudDeviceId || "",
  defaultCloudToken: runtime.cloudToken || envConfig.cloudToken || defaults.defaultCloudToken || stored.defaultCloudToken || "",
};

const required = [
  "defaultExportMode",
  "defaultMaxItems",
  "defaultFetchDetail",
  "defaultDetailSpeed",
];
const missingDefaults = required.filter((key) => !effective[key]);

const scriptList = [
  "scripts/preflight_check.sh",
  "scripts/run.sh",
  "scripts/export_preference.sh",
  mode === "cloud" ? "scripts/cloud_dispatch_loop.sh" : "scripts/collect_and_export_loop.sh",
];
const scriptChecks = Object.fromEntries(
  scriptList.map((relativePath) => {
    const fullPath = `${skillDir}/${relativePath}`;
    let exists = false;
    let executable = false;
    try {
      const stat = fs.statSync(fullPath);
      exists = stat.isFile();
      executable = (stat.mode & 0o111) !== 0;
    } catch {}
    return [relativePath, { exists, executable }];
  })
);
const binChecks = Object.fromEntries(
  ["bash", "curl", "node"].map((bin) => {
    try {
      const path = execFileSync("bash", ["-lc", `command -v ${bin}`], {
        encoding: "utf8",
        stdio: ["ignore", "pipe", "ignore"],
      }).trim();
      return [bin, { ok: Boolean(path), path }];
    } catch {
      return [bin, { ok: false, path: "" }];
    }
  })
);

process.stdout.write(JSON.stringify({
  ready: Object.values(scriptChecks).every((item) => item.exists)
    && Object.values(binChecks).every((item) => item.ok)
    && missingDefaults.length === 0,
  needsUserDefaults: missingDefaults.length > 0,
  mode,
  missingDefaults,
  effectiveConfig: {
    defaultExportMode: effective.defaultExportMode,
    defaultMaxItems: effective.defaultMaxItems,
    defaultFetchDetail: effective.defaultFetchDetail,
    defaultDetailSpeed: effective.defaultDetailSpeed,
    defaultDeduplicationEnabled: effective.defaultDeduplicationEnabled,
    defaultDeduplicationStrategy: effective.defaultDeduplicationStrategy,
    defaultCloudDeviceId: effective.defaultCloudDeviceId,
    cloudTokenPresent: Boolean(effective.defaultCloudToken),
  },
  checks: {
    scripts: scriptChecks,
    bins: binChecks,
  },
}, null, 2));
' "$normalized_json" "$MODE" "$SKILL_DIR"
}

SUMMARY_JSON="$(build_summary_json "$NORMALIZED_CONFIG")"

if [[ "$PROBE_BRIDGE" == "true" && "$MODE" == "local" ]]; then
  BRIDGE_URL="${WEB_COLLECTION_BRIDGE_URL:-$DEFAULT_BRIDGE_URL}"
  BRIDGE_RAW=""
  if BRIDGE_RAW="$(curl -fsS --max-time 2 "$BRIDGE_URL/api/status" 2>/dev/null)"; then
    SUMMARY_JSON="$(node -e '
const summary = JSON.parse(process.argv[1]);
const bridgeRaw = JSON.parse(process.argv[2]);
summary.checks.bridge = {
  attempted: true,
  reachable: true,
  pluginConnected: bridgeRaw?.data?.pluginConnected ?? null,
};
process.stdout.write(JSON.stringify(summary));
' "$SUMMARY_JSON" "$BRIDGE_RAW")"
  fi
fi

print_text() {
  node -e '
const summary = JSON.parse(process.argv[1]);
const lines = [];
lines.push(`[web-collection] ready=${summary.ready}`);
lines.push(`[web-collection] mode=${summary.mode}`);
if (summary.missingDefaults.length > 0) {
  lines.push(`[web-collection] missingDefaults=${summary.missingDefaults.join(",")}`);
}
lines.push(`[web-collection] export=${summary.effectiveConfig.defaultExportMode || "-"}`);
lines.push(`[web-collection] maxItems=${summary.effectiveConfig.defaultMaxItems || "-"}`);
lines.push(`[web-collection] fetchDetail=${summary.effectiveConfig.defaultFetchDetail || "-"}`);
lines.push(`[web-collection] detailSpeed=${summary.effectiveConfig.defaultDetailSpeed || "-"}`);
lines.push(`[web-collection] deduplication=${summary.effectiveConfig.defaultDeduplicationEnabled || "true"}`);
lines.push(`[web-collection] deduplicationStrategy=${summary.effectiveConfig.defaultDeduplicationStrategy || "keepOld"}`);
if (summary.mode === "cloud") {
  lines.push(`[web-collection] cloudDeviceId=${summary.effectiveConfig.defaultCloudDeviceId || "-"}`);
  lines.push(`[web-collection] cloudTokenPresent=${summary.effectiveConfig.cloudTokenPresent}`);
}
process.stdout.write(lines.join("\n") + "\n");
' "$SUMMARY_JSON"
}

READY="$(node -e 'const summary=JSON.parse(process.argv[1]); process.stdout.write(summary.ready ? "true" : "false");' "$SUMMARY_JSON")"

if [[ "$READY" == "true" && "$QUIET_SUCCESS" == "true" ]]; then
  exit 0
fi

if [[ "$FORMAT" == "text" ]]; then
  print_text
else
  node -e 'const summary=JSON.parse(process.argv[1]); process.stdout.write(JSON.stringify(summary, null, 2) + "\n");' "$SUMMARY_JSON"
fi

if [[ "$READY" == "true" ]]; then
  exit 0
fi

if node -e 'const summary=JSON.parse(process.argv[1]); process.exit(summary.needsUserDefaults ? 0 : 1);' "$SUMMARY_JSON"; then
  exit 2
fi

exit 1
