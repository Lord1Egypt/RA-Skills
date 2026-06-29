#!/usr/bin/env bash
# skill-hub-query: query the local cache
# Usage:
#   bash query.sh keyword <kw>
#   bash query.sh time today | this_week | last_week | this_month | last_N_days | YYYY-MM-DD | YYYY-MM-DD:YYYY-MM-DD
#   bash query.sh author <author> [--exact]
#   bash query.sh slug <exact-slug>
#   bash query.sh combo --keyword=xx --since=YYYY-MM-DD --author=xx --source=official [--exact]
set -euo pipefail
SELF_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# shellcheck source=./_lib.sh
source "${SELF_DIR}/_lib.sh"

setup_legacy_notice

# ---------- skillhub.cn provider branch ----------
# This provider intercepts query.sh entirely. It supports:
#   slug <s>      -> detail
#   versions <s>  -> versions
#   keyword <kw>  -> live search (no local cache)
#   today         -> browse/recent (live)
#   combo         -> keyword + optional --category / --source
#   author <h>    -> unsupported (skillhub.cn has no author filter)
if is_skillhub_cn; then
  # Pretty-print helper for skillhub.cn search results.
  # Reads JSON on stdin, prints a numbered table and "Showing N of TOTAL".
  shcn_print_results() {
    local title="${1:-Results}"
    local resp
    resp="$(cat)"
    local total count
    total="$(echo "$resp" | jq -r '.data.total // 0')"
    count="$(echo "$resp" | jq -r '.data.skills | length')"
    echo "=== ${title} ==="
    if [[ "$count" == "0" ]]; then
      echo "(no results)"
      echo "Showing 0 of ${total} matches"
      return 0
    fi
    echo "$resp" | jq -r '
      .data.skills | to_entries[] |
      "[\(.key + 1)] slug=\(.value.slug)\n" +
      "    name        : \(.value.name // .value.slug)\n" +
      "    source      : \(.value.source // "?")   version: \(.value.version // "?")   verified: \(if .value.verified then "yes" else "no" end)\n" +
      "    installs    : \(.value.installs // 0)   downloads: \(.value.downloads // 0)   stars: \(.value.stars // 0)\n" +
      "    description : \(((.value.description_zh // "") | select(. != "")) // (.value.description // "") | .[0:80])"
    '
    echo ""
    echo "Showing ${count} of ${total} matches"
  }

  MODE="${1:-}"; shift || true
  case "$MODE" in
    slug)
      S="${1:-}"
      if [[ -z "$S" ]]; then
        echo "[error] slug: missing argument" >&2
        echo "        Usage: SKILL_HUB_PROVIDER=skillhub_cn bash query.sh slug <exact-slug>" >&2
        exit 1
      fi
      validate_slug "$S" || exit 1
      detail="$(shcn_detail "$S")" || exit $?
      echo "$detail" | jq '{
        slug: .skill.slug,
        displayName: .skill.displayName,
        summary: .skill.summary,
        summary_zh: .skill.summary_zh,
        latestVersion: .latestVersion,
        owner: .owner,
        tags: .skill.tags,
        category: .skill.category,
        source: .skill.source,
        sourceUrl: .skill.sourceUrl,
        contentZhAvailable: .contentZhAvailable,
        securityReports: .securityReports,
        stats: .skill.stats,
        createdAt: .skill.createdAt,
        updatedAt: .skill.updatedAt
      }'
      exit 0
      ;;
    versions)
      S="${1:-}"
      if [[ -z "$S" ]]; then
        echo "[error] versions: missing argument" >&2
        echo "        Usage: SKILL_HUB_PROVIDER=skillhub_cn bash query.sh versions <exact-slug>" >&2
        exit 1
      fi
      validate_slug "$S" || exit 1
      vresp="$(shcn_versions "$S")" || exit $?
      echo "$vresp" | jq '{
        slug: .slug,
        source: .source,
        versions: [.versions[] | {version, createdAt, changelog, securityReports}]
      }'
      exit 0
      ;;
    keyword)
      KW="${1:-}"
      if [[ -z "$KW" ]]; then
        echo "[error] keyword: missing argument" >&2
        echo "        Usage: SKILL_HUB_PROVIDER=skillhub_cn bash query.sh keyword <kw>" >&2
        exit 1
      fi
      resp="$(shcn_search "$KW" 1 24 "score" "desc")" || exit $?
      echo "$resp" | shcn_print_results "Search: \"${KW}\" (skillhub.cn)"
      exit 0
      ;;
    today)
      # skillhub.cn doesn't advertise a recency sort key; sortBy=updated is a
      # best-effort attempt that gracefully falls back to score if unsupported.
      resp="$(shcn_search "" 1 24 "updated" "desc")" || \
        resp="$(shcn_search "" 1 24 "" "")" || exit $?
      echo "$resp" | shcn_print_results "Recent / browse (skillhub.cn)"
      exit 0
      ;;
    combo)
      KW=""; CAT=""; SRC=""
      for arg in "$@"; do
        case "$arg" in
          --keyword=*)  KW="${arg#*=}" ;;
          --category=*) CAT="${arg#*=}" ;;
          --source=*)   SRC="${arg#*=}" ;;
          --author=*|--since=*|--until=*|--exact)
            echo "[warn] combo: '$arg' is ignored on skillhub.cn (no equivalent filter)" >&2
            ;;
          *)
            echo "[error] combo: unknown flag: $arg" >&2
            echo "        Valid on skillhub.cn: --keyword=xx --category=xx --source=xx" >&2
            exit 1
            ;;
        esac
      done
      resp="$(shcn_search "$KW" 1 24 "score" "desc" "$CAT" "$SRC")" || exit $?
      label="Combo:"
      [[ -n "$KW" ]]  && label="${label} keyword=\"${KW}\""
      [[ -n "$CAT" ]] && label="${label} category=${CAT}"
      [[ -n "$SRC" ]] && label="${label} source=${SRC}"
      echo "$resp" | shcn_print_results "${label} (skillhub.cn)"
      exit 0
      ;;
    author)
      cat >&2 <<EOF
[error] Author filtering is not supported on skillhub.cn.

The public search API has no author/handle filter parameter. Try a keyword
search using the author's handle or name:

  SKILL_HUB_PROVIDER=skillhub_cn bash query.sh keyword <author-handle>
EOF
      exit 1
      ;;
    time)
      cat >&2 <<EOF
[error] Time-range filtering is not supported on skillhub.cn.

The public search API has no time-range filter. For recent items try:

  SKILL_HUB_PROVIDER=skillhub_cn bash query.sh today
EOF
      exit 1
      ;;
    "")
      cat >&2 <<EOF
Usage (skillhub.cn provider):
  SKILL_HUB_PROVIDER=skillhub_cn bash query.sh keyword <kw>
  SKILL_HUB_PROVIDER=skillhub_cn bash query.sh today
  SKILL_HUB_PROVIDER=skillhub_cn bash query.sh combo --keyword=xx [--category=xx] [--source=xx]
  SKILL_HUB_PROVIDER=skillhub_cn bash query.sh slug <exact-slug>
  SKILL_HUB_PROVIDER=skillhub_cn bash query.sh versions <exact-slug>

Notes:
  - Search is live (no local cache). No author/time filters available.
EOF
      exit 1
      ;;
    *)
      echo "[error] skillhub.cn provider: unknown mode '$MODE'" >&2
      echo "        Supported: keyword <kw> | today | combo ... | slug <s> | versions <s>" >&2
      exit 1
      ;;
  esac
fi

if [[ ! -f "$CACHE_FILE" ]]; then
  echo "[error] Cache not found. Run: bash $SELF_DIR/sync.sh" >&2
  echo "        If this is your first use, also run: bash $SELF_DIR/doctor.sh" >&2
  exit 1
fi

MODE="${1:-}"
shift || true

# ---------- Time range parser ----------
# Output: epoch ms on stdout; on failure, write error to stderr and return non-zero
parse_time_to_ms() {
  local arg="$1"
  case "$arg" in
    today)
      date -d "today 00:00:00" +%s%3N 2>/dev/null || \
        python3 -c "import datetime as d;t=d.datetime.combine(d.date.today(),d.time.min);print(int(t.timestamp()*1000))"
      ;;
    this_week)
      date -d "last monday 00:00:00" +%s%3N 2>/dev/null || \
        python3 -c "import datetime as d;t=d.date.today();m=t-d.timedelta(days=t.weekday());print(int(d.datetime.combine(m,d.time.min).timestamp()*1000))"
      ;;
    last_week)
      date -d "last monday -7 days 00:00:00" +%s%3N 2>/dev/null || \
        python3 -c "import datetime as d;t=d.date.today();m=t-d.timedelta(days=t.weekday()+7);print(int(d.datetime.combine(m,d.time.min).timestamp()*1000))"
      ;;
    this_month)
      date -d "$(date +%Y-%m-01) 00:00:00" +%s%3N
      ;;
    last_*_days)
      local n
      n="$(echo "$arg" | sed -E 's/last_([0-9]+)_days/\1/')"
      date -d "${n} days ago 00:00:00" +%s%3N
      ;;
    [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9])
      date -d "${arg} 00:00:00" +%s%3N
      ;;
    *)
      echo "[error] Unsupported time range: $arg" >&2
      echo "        Valid: today / this_week / last_week / this_month / last_N_days / YYYY-MM-DD / YYYY-MM-DD:YYYY-MM-DD" >&2
      return 1
      ;;
  esac
}

# End-of-day timestamp (YYYY-MM-DD 23:59:59.999)
day_end_ms() {
  local d="$1"
  date -d "${d} 23:59:59" +%s%3N
}

# Common jq filter builder (uses --arg/--argjson, no shell injection)
# Args: keyword author source since(ms) until(ms) [exact=0/1]
#       empty string means "don't filter on this dimension"
#       exact=1 means author matches owner.handle / .email / .displayName exactly,
#       otherwise default contains-substring (backwards compatible)
run_combo_filter() {
  local kw="${1:-}" author="${2:-}" src="${3:-}" since="${4:-0}" until="${5:-0}" exact="${6:-0}"
  # Lowercase keyword via jq (avoid shell `tr` byte-level handling for UTF-8 input)
  local kw_lower
  kw_lower="$(echo "$kw" | jq -Rr 'ascii_downcase' 2>/dev/null || echo "$kw")"
  local result
  result="$(jq \
    --arg kw "$kw_lower" \
    --arg author "$author" \
    --arg src "$src" \
    --argjson since "$since" \
    --argjson until "$until" \
    --argjson exact "$exact" \
    '
    [to_entries[].value | select(
      (
        ($kw == "")
        or (.slug // "" | ascii_downcase | contains($kw))
        or (.displayName // "" | ascii_downcase | contains($kw))
        or (.summary // "" | ascii_downcase | contains($kw))
      )
      and
      (
        ($author == "")
        or (
          if $exact == 1 then
            ((.owner.displayName // "") == $author)
            or ((.owner.handle // "") == $author)
            or ((.owner.email // "") == $author)
          else
            (.owner.displayName // "" | contains($author))
            or (.owner.handle // "" | contains($author))
            or (.owner.email // "" | contains($author))
          end
        )
      )
      and
      (
        ($src == "") or (.source == $src)
      )
      and
      (
        ($since == 0) or ((.updatedAt // 0) >= $since)
      )
      and
      (
        ($until == 0) or ((.updatedAt // 0) <= $until)
      )
    )] | sort_by(.updatedAt) | reverse
    ' "$CACHE_FILE")"

  if [[ "$(echo "$result" | jq 'length' 2>/dev/null || echo 0)" == "0" ]]; then
    echo "[info] No matching skill. Try:" >&2
    echo "       - different keyword or check spelling" >&2
    echo "       - refresh cache: bash $SELF_DIR/sync.sh --full" >&2
  fi
  echo "$result"
}

case "$MODE" in
  keyword)
    KW="${1:-}"
    if [[ -z "$KW" ]]; then
      echo "[error] keyword: missing argument" >&2
      exit 1
    fi
    run_combo_filter "$KW" "" "" 0 0
    ;;

  time)
    arg="${1:-}"
    if [[ -z "$arg" ]]; then
      echo "[error] time: missing argument" >&2
      exit 1
    fi
    if [[ "$arg" == *":"* ]]; then
      start_str="${arg%:*}"; end_str="${arg#*:}"
      since="$(parse_time_to_ms "$start_str")" || exit 1
      until="$(day_end_ms "$end_str")" || exit 1
      run_combo_filter "" "" "" "$since" "$until"
    elif [[ "$arg" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
      since="$(parse_time_to_ms "$arg")" || exit 1
      until="$(day_end_ms "$arg")" || exit 1
      run_combo_filter "" "" "" "$since" "$until"
    else
      since="$(parse_time_to_ms "$arg")" || exit 1
      run_combo_filter "" "" "" "$since" 0
    fi
    ;;

  author)
    A=""
    EXACT=0
    for arg in "$@"; do
      case "$arg" in
        --exact) EXACT=1 ;;
        --*)
          echo "[error] author: unknown flag: $arg (valid: --exact)" >&2
          exit 1
          ;;
        *)
          if [[ -z "$A" ]]; then
            A="$arg"
          else
            echo "[error] author: only one argument allowed; extra: $arg" >&2
            exit 1
          fi
          ;;
      esac
    done
    if [[ -z "$A" ]]; then
      echo "[error] author: missing argument" >&2
      echo "        Usage: bash query.sh author <author> [--exact]" >&2
      echo "        Example (exact): bash query.sh author alice@example.com --exact" >&2
      exit 1
    fi
    run_combo_filter "" "$A" "" 0 0 "$EXACT"
    ;;

  slug)
    S="${1:-}"
    if [[ -z "$S" ]]; then
      echo "[error] slug: missing argument" >&2
      exit 1
    fi
    slug_result="$(jq --arg s "$S" '.[$s] // null' "$CACHE_FILE")"
    if [[ "$slug_result" == "null" ]]; then
      echo "[info] Slug '$S' not found in cache. May be: typo / stale cache / removed." >&2
      echo "       Try: bash $SELF_DIR/sync.sh --full and re-query, or use 'keyword' for fuzzy search." >&2
    fi
    echo "$slug_result"
    ;;

  combo)
    KW=""; AUTHOR=""; SOURCE=""; SINCE=0; UNTIL=0; EXACT=0
    for arg in "$@"; do
      case "$arg" in
        --keyword=*) KW="${arg#*=}" ;;
        --author=*)  AUTHOR="${arg#*=}" ;;
        --source=*)  SOURCE="${arg#*=}" ;;
        --exact)     EXACT=1 ;;
        --since=*)
          SINCE="$(parse_time_to_ms "${arg#*=}")" || exit 1
          ;;
        --until=*)
          if [[ "${arg#*=}" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
            UNTIL="$(day_end_ms "${arg#*=}")"
          else
            UNTIL="$(parse_time_to_ms "${arg#*=}")" || exit 1
          fi
          ;;
        *)
          echo "[error] combo: unknown flag: $arg" >&2
          echo "        Valid: --keyword=xx --author=xx --source=official|personal|external --since=YYYY-MM-DD --until=YYYY-MM-DD [--exact]" >&2
          exit 1
          ;;
      esac
    done
    if [[ -n "$SOURCE" && "$SOURCE" != "official" && "$SOURCE" != "personal" && "$SOURCE" != "external" ]]; then
      echo "[error] --source must be one of: official / personal / external (got: $SOURCE)" >&2
      exit 1
    fi
    run_combo_filter "$KW" "$AUTHOR" "$SOURCE" "$SINCE" "$UNTIL" "$EXACT"
    ;;

  *)
    cat >&2 <<EOF
Usage:
  bash query.sh keyword <kw>
  bash query.sh time today | this_week | last_week | this_month | last_N_days | YYYY-MM-DD | YYYY-MM-DD:YYYY-MM-DD
  bash query.sh author <author> [--exact]
  bash query.sh slug <exact-slug>
  bash query.sh combo --keyword=xx --author=xx --source=official|personal|external --since=YYYY-MM-DD --until=YYYY-MM-DD [--exact]

Notes:
  author / combo default to substring (contains) matching.
  With --exact, owner.email / owner.handle / owner.displayName must match exactly,
  which is useful when an exact handle/email needs to be locked in
  (e.g. avoid 'alice' matching 'alice2' too).
EOF
    exit 1
    ;;
esac
