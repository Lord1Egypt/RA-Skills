#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  x-news-crawler --query <text> [options]

Options:
  --mode <hybrid|top|latest>   Crawl strategy (default: hybrid)
  --since-hours <int>          Keep posts newer than this window (default: 72)
  --limit <int>                Max rows in final JSON (default: 30)
  --scrolls <int>              Scroll rounds before extraction (default: 4)
  --cdp <port|url>             CDP endpoint for abs (default: 9333)
  --output <file>              Write JSON output to file (default: stdout)
  -h, --help                   Show help
EOF
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "missing dependency: $1" >&2
    exit 1
  }
}

MODE="hybrid"
QUERY=""
SINCE_HOURS=72
LIMIT=30
SCROLLS=4
CDP_TARGET="9333"
OUTFILE=""
FORCE_FAIL_SOURCE="${X_NEWS_FORCE_FAIL_SOURCE:-}"
declare -a WARNINGS=()
declare -a FAILED_SOURCES=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --query)
      QUERY="${2:-}"
      shift 2
      ;;
    --mode)
      MODE="${2:-}"
      shift 2
      ;;
    --since-hours)
      SINCE_HOURS="${2:-}"
      shift 2
      ;;
    --limit)
      LIMIT="${2:-}"
      shift 2
      ;;
    --scrolls)
      SCROLLS="${2:-}"
      shift 2
      ;;
    --cdp)
      CDP_TARGET="${2:-}"
      shift 2
      ;;
    --output)
      OUTFILE="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "$QUERY" ]]; then
  echo "--query is required" >&2
  usage >&2
  exit 2
fi
if [[ -z "$CDP_TARGET" ]]; then
  echo "--cdp must not be empty" >&2
  exit 2
fi

case "$MODE" in
  hybrid|top|latest) ;;
  *)
    echo "invalid --mode: $MODE (expected: hybrid|top|latest)" >&2
    exit 2
    ;;
esac

if ! [[ "$SINCE_HOURS" =~ ^[0-9]+$ ]]; then
  echo "--since-hours must be a non-negative integer" >&2
  exit 2
fi
if ! [[ "$LIMIT" =~ ^[0-9]+$ ]] || [[ "$LIMIT" -eq 0 ]]; then
  echo "--limit must be a positive integer" >&2
  exit 2
fi
if ! [[ "$SCROLLS" =~ ^[0-9]+$ ]]; then
  echo "--scrolls must be a non-negative integer" >&2
  exit 2
fi

require_cmd abs
require_cmd jq
require_cmd python3

# X.com can be slow; use a safer default unless caller overrides it.
: "${AGENT_BROWSER_DEFAULT_TIMEOUT:=30000}"
export AGENT_BROWSER_DEFAULT_TIMEOUT

to_json_array() {
  if [[ "$#" -eq 0 ]]; then
    printf '[]'
  else
    printf '%s\n' "$@" | jq -R . | jq -s .
  fi
}

abs_cmd() {
  abs --cdp "$CDP_TARGET" "$@"
}

ensure_cdp_ready() {
  if abs_cmd get url >/dev/null 2>&1; then
    return 0
  fi

  cat >&2 <<EOF
failed to connect abs to CDP endpoint: $CDP_TARGET

Use your regular Chrome profile with CDP enabled, then rerun crawler.
Do not use --user-data-dir, otherwise Chrome will run in an isolated profile.

Example (macOS):
  /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9333
EOF
  exit 1
}

encoded_query="$(python3 - "$QUERY" <<'PY'
import sys, urllib.parse
print(urllib.parse.quote(sys.argv[1]))
PY
)"

workdir="$(mktemp -d "${TMPDIR:-/tmp}/x-news-crawler.XXXXXX")"
trap 'rm -rf "$workdir"' EXIT
ensure_cdp_ready

extract_js_template='
(() => {
  const rows = [];
  const seen = new Set();
  for (const a of Array.from(document.querySelectorAll("article"))) {
    const statusAnchor = a.querySelector("a[href*=\"/status/\"]");
    if (!statusAnchor) continue;
    const hrefRaw = statusAnchor.getAttribute("href") || "";
    const m = hrefRaw.match(/^\/[^/]+\/status\/\d+/);
    if (!m) continue;
    const status = `https://x.com${m[0]}`;
    if (seen.has(status)) continue;
    seen.add(status);

    const user = m[0].split("/")[1] || "";
    const datetime = (a.querySelector("time")?.getAttribute("datetime") || "").trim();
    const text = Array
      .from(a.querySelectorAll("div[lang]"))
      .map(x => (x.textContent || "").trim())
      .filter(Boolean)
      .join(" ")
      .slice(0, 400);
    const metricText = (ids) => {
      for (const id of ids) {
        const el = a.querySelector(`[data-testid="${id}"]`);
        if (!el) continue;
        const v = ((el.innerText || "").replace(/\s+/g, " ").trim());
        if (v) return v;
        const aria = (el.getAttribute("aria-label") || "").trim();
        if (aria) return aria;
      }
      return "";
    };
    const labels = Array
      .from(a.querySelectorAll("button,a"))
      .map(n => (n.getAttribute("aria-label") || "").trim())
      .filter(Boolean);
    const replies = metricText(["reply"]) || labels.find(v => /Replies?\./.test(v)) || "";
    const reposts = metricText(["retweet", "unretweet"]) || labels.find(v => /reposts?\./i.test(v)) || "";
    const likes = metricText(["like", "unlike"]) || labels.find(v => /Likes?\./.test(v)) || "";

    rows.push({
      source: "__SOURCE__",
      user,
      datetime,
      status_url: status,
      text,
      replies,
      reposts,
      likes
    });
    if (rows.length >= 100) break;
  }

  return JSON.stringify({
    fetched_at: new Date().toISOString(),
    source: "__SOURCE__",
    page: location.href,
    count: rows.length,
    rows
  }, null, 2);
})()
'

crawl_mode() {
  local source="$1"
  local url="https://x.com/search?q=${encoded_query}&src=typed_query&f=${source}"
  local js out cleaned eval_ok
  local rows_json
  local rows_file="$workdir/${source}.rows.jsonl"
  local error_prefix="[${source}]"

  if [[ -n "$FORCE_FAIL_SOURCE" ]] && [[ "$FORCE_FAIL_SOURCE" == "$source" ]]; then
    WARNINGS+=("${error_prefix} forced failure by X_NEWS_FORCE_FAIL_SOURCE")
    return 1
  fi

  js="$extract_js_template"
  js="${js//__SOURCE__/$source}"

  eval_ok=0
  : >"$rows_file"
  abs_cmd tab new >/dev/null || true
  if ! abs_cmd open "$url" >/dev/null; then
    WARNINGS+=("${error_prefix} open failed: ${url}")
    abs_cmd close >/dev/null 2>&1 || true
    return 1
  fi
  abs_cmd wait 4500 >/dev/null || true

  for ((i=0; i<=SCROLLS; i++)); do
    if out="$(abs_cmd eval "$js" 2>/dev/null)"; then
      cleaned="$(printf '%s' "$out" | jq -r . 2>/dev/null || printf '%s' "$out")"
      if printf '%s\n' "$cleaned" | jq -c '.rows[]?' >>"$rows_file"; then
        eval_ok=1
      else
        WARNINGS+=("${error_prefix} parse rows failed on iteration ${i}")
      fi
    else
      WARNINGS+=("${error_prefix} eval failed on iteration ${i}")
    fi

    if (( i < SCROLLS )); then
      abs_cmd scroll down 2200 >/dev/null || true
      abs_cmd wait 1200 >/dev/null || true
    fi
  done

  abs_cmd close >/dev/null 2>&1 || true

  if [[ "$eval_ok" -eq 0 ]]; then
    WARNINGS+=("${error_prefix} no successful eval results")
    return 1
  fi

  if [[ -s "$rows_file" ]]; then
    rows_json="$(jq -s '.' "$rows_file")"
  else
    rows_json='[]'
  fi

  jq -n \
    --arg source "$source" \
    --arg query "$QUERY" \
    --arg page "$url" \
    --arg fetched_at "$(date -u +"%Y-%m-%dT%H:%M:%SZ")" \
    --argjson rows "$rows_json" '
    {
      fetched_at: $fetched_at,
      query: $query,
      source: $source,
      page: $page,
      count: ($rows | length),
      rows: $rows
    }
  '
}

inputs=()
case "$MODE" in
  top)
    if crawl_mode top >"$workdir/top.json"; then
      inputs+=("$workdir/top.json")
    else
      FAILED_SOURCES+=("top")
    fi
    ;;
  latest)
    if crawl_mode latest >"$workdir/latest.json"; then
      inputs+=("$workdir/latest.json")
    else
      FAILED_SOURCES+=("latest")
    fi
    ;;
  hybrid)
    if crawl_mode top >"$workdir/top.json"; then
      inputs+=("$workdir/top.json")
    else
      FAILED_SOURCES+=("top")
    fi
    if crawl_mode latest >"$workdir/latest.json"; then
      inputs+=("$workdir/latest.json")
    else
      FAILED_SOURCES+=("latest")
    fi
    ;;
esac

if [[ "${#inputs[@]}" -eq 0 ]]; then
  printf 'crawl failed: no sources succeeded (%s)\n' "$MODE" >&2
  exit 1
fi

warnings_json='[]'
failed_sources_json='[]'
if [[ "${#WARNINGS[@]}" -gt 0 ]]; then
  warnings_json="$(to_json_array "${WARNINGS[@]}")"
fi
if [[ "${#FAILED_SOURCES[@]}" -gt 0 ]]; then
  failed_sources_json="$(to_json_array "${FAILED_SOURCES[@]}")"
fi

result="$(
  jq -s \
    --arg query "$QUERY" \
    --arg mode "$MODE" \
    --argjson limit "$LIMIT" \
    --argjson since_hours "$SINCE_HOURS" '
      def ts:
        (.datetime // "") as $d
        | if $d == "" then 0
          else (
            $d
            | if test("\\.[0-9]+Z$") then sub("\\.[0-9]+Z$"; "Z") else . end
            | (try fromdateiso8601 catch 0)
          )
          end;
      def keep_recent: select(ts >= (now - ($since_hours * 3600)));
      def dedupe_status:
        reduce .[] as $i ([]; if any(.[]; .status_url == $i.status_url) then . else . + [$i] end);

      {
        fetched_at: (now | todateiso8601),
        query: $query,
        mode: $mode,
        since_hours: $since_hours,
        count: (
          [ .[].rows[] | keep_recent ]
          | sort_by(ts) | reverse
          | dedupe_status
          | length
        ),
        rows: (
          [ .[].rows[] | keep_recent ]
          | sort_by(ts) | reverse
          | dedupe_status
          | .[:$limit]
        )
      }
    ' "${inputs[@]}" \
  | jq \
    --argjson warnings "$warnings_json" \
    --argjson failed_sources "$failed_sources_json" \
    '. + {
      warnings: $warnings,
      failed_sources: $failed_sources
    }'
)"

if [[ -n "$OUTFILE" ]]; then
  mkdir -p "$(dirname "$OUTFILE")"
  printf '%s\n' "$result" >"$OUTFILE"
  echo "$OUTFILE"
else
  printf '%s\n' "$result"
fi
