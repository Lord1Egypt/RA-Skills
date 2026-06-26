#!/bin/bash
# unified-search.sh — unified entrypoint for legacy merged search + vendored deep search suite
#
# Default: preserve legacy merged three-engine search (Tavily + Exa + Google)
# New subcommands:
#   search-layer            -> vendored multi-source deep search
#   fetch-thread            -> vendored issue/PR/thread fetcher
#   content-extract         -> vendored URL -> Markdown extractor
#   mineru-extract          -> vendored MinerU single-URL parser
#   mineru-parse-documents  -> vendored MinerU MCP-style wrapper
#
# Auto-routing:
#   - GitHub issue/PR/discussion and similar thread URLs -> fetch-thread
#   - Document URLs (.pdf/.docx/...) -> mineru-extract
#   - Generic URLs -> content-extract
#   - Comparison / status / research style natural-language queries -> search-layer
#   - Plain everyday lookup -> legacy merged search

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
LEGACY_SCRIPT="$SCRIPT_DIR/unified-search-legacy.sh"
SEARCH_LAYER_WRAPPER="$SCRIPT_DIR/run-search-layer.sh"
FETCH_THREAD_WRAPPER="$SCRIPT_DIR/run-fetch-thread.sh"
CONTENT_EXTRACT_WRAPPER="$SCRIPT_DIR/run-content-extract.sh"
MINERU_EXTRACT_WRAPPER="$SCRIPT_DIR/run-mineru-extract.sh"
MINERU_PARSE_DOCS_WRAPPER="$SCRIPT_DIR/run-mineru-parse-documents.sh"

usage() {
  cat <<'EOF'
Usage:
  bash unified-search.sh "<query>" [legacy flags]
  bash unified-search.sh --deep "<query>" [deep-search flags]
  bash unified-search.sh search-layer <args...>
  bash unified-search.sh fetch-thread <url> [args...]
  bash unified-search.sh content-extract --url <url> [args...]
  bash unified-search.sh mineru-extract <url> [args...]
  bash unified-search.sh mineru-parse-documents <args...>

Legacy flags:
  --num N --topic general|news --days N --save-run DIR --json --legacy

Deep-search flags:
  --deep   (alias of --mode deep)
  --fast   (alias of --mode fast)
  --answer (alias of --mode answer)
  --mode --intent --freshness --queries --source --extract-refs --extract-refs-urls --domain-boost
  --save-run DIR (save stdout to DIR/<mode>-<timestamp>.json for all modes)

Automatic routing:
  - discussion/thread URLs             -> fetch-thread
  - document/file URLs                 -> mineru-extract
  - generic content URLs               -> content-extract
  - comparison/status/research queries -> search-layer
  - ordinary lookups                   -> legacy merged search
EOF
}

has_arg() {
  local needle="$1"
  shift || true
  local arg
  for arg in "$@"; do
    [[ "$arg" == "$needle" ]] && return 0
  done
  return 1
}

normalize_mode_aliases() {
  local explicit_mode=0
  local arg
  for arg in "$@"; do
    if [[ "$arg" == "--mode" ]]; then
      explicit_mode=1
      break
    fi
  done

  NORMALIZED_ARGS=()
  for arg in "$@"; do
    case "$arg" in
      --deep)
        if [[ "$explicit_mode" == "0" ]]; then
          NORMALIZED_ARGS+=(--mode deep)
        fi
        ;;
      --fast)
        if [[ "$explicit_mode" == "0" ]]; then
          NORMALIZED_ARGS+=(--mode fast)
        fi
        ;;
      --answer)
        if [[ "$explicit_mode" == "0" ]]; then
          NORMALIZED_ARGS+=(--mode answer)
        fi
        ;;
      *)
        NORMALIZED_ARGS+=("$arg")
        ;;
    esac
  done
}

first_url() {
  local arg
  for arg in "$@"; do
    if [[ "$arg" =~ ^https?:// ]]; then
      printf '%s\n' "$arg"
      return 0
    fi
  done
  return 1
}

lower() {
  printf '%s' "$1" | tr '[:upper:]' '[:lower:]'
}

is_thread_url() {
  local url
  url="$(lower "$1")"
  [[ "$url" =~ github\.com/.+/(issues|pull|pulls|discussions)/[0-9]+ ]] && return 0
  [[ "$url" =~ news\.ycombinator\.com/item\?id= ]] && return 0
  [[ "$url" =~ reddit\.com/r/.+/comments/ ]] && return 0
  [[ "$url" =~ stackoverflow\.com/questions/[0-9]+ ]] && return 0
  [[ "$url" =~ stackexchange\.com/questions/[0-9]+ ]] && return 0
  [[ "$url" =~ /t/[^/]+/[0-9]+ ]] && return 0
  [[ "$url" =~ x\.com/.+/status/[0-9]+ ]] && return 0
  [[ "$url" =~ twitter\.com/.+/status/[0-9]+ ]] && return 0
  return 1
}

is_document_url() {
  local url
  url="$(lower "$1")"
  [[ "$url" =~ \.(pdf|doc|docx|ppt|pptx|xls|xlsx|csv|epub|mobi|rtf|odt|ods|odp)([?#].*)?$ ]] && return 0
  [[ "$url" =~ /download([/?#].*)?$ ]] && return 0
  return 1
}

query_text() {
  local joined=""
  local arg
  for arg in "$@"; do
    [[ "$arg" == --* ]] && continue
    joined+="$arg "
  done
  printf '%s' "${joined% }"
}

expand_query_variants() {
  local query="$1"
  python3 - "$query" <<'PY'
import json
import re
import sys
import urllib.parse
import urllib.request

query = sys.argv[1].strip()
if not query:
    raise SystemExit(0)

variants = [query]
if re.search(r'[\u3400-\u9fff]', query):
    translated = ""
    try:
        url = "https://translate.googleapis.com/translate_a/single?" + urllib.parse.urlencode({
            "client": "gtx",
            "sl": "auto",
            "tl": "en",
            "dt": "t",
            "q": query,
        })
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json,text/plain,*/*",
            },
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            payload = json.loads(resp.read().decode("utf-8", "replace"))
        if isinstance(payload, list) and payload and isinstance(payload[0], list):
            translated = "".join(
                segment[0]
                for segment in payload[0]
                if isinstance(segment, list) and segment and isinstance(segment[0], str)
            )
    except Exception:
        translated = ""
    translated = " ".join((translated or "").split()).strip()
    if translated and translated.casefold() != query.casefold():
        variants.append(translated)

seen = set()
for item in variants:
    key = item.casefold()
    if not item or key in seen:
        continue
    seen.add(key)
    print(item)
PY
}

infer_intent() {
  local q
  q="$(lower "$1")"
  if [[ "$q" =~ (^|[[:space:]])(vs|versus)([[:space:]]|$) ]] || [[ "$q" == *"对比"* ]] || [[ "$q" == *"区别"* ]] || [[ "$q" == *"比较"* ]] || [[ "$q" == *"哪个好"* ]]; then
    echo comparison
  elif [[ "$q" == *"教程"* ]] || [[ "$q" == *"guide"* ]] || [[ "$q" == *"how to"* ]] || [[ "$q" == *"怎么"* ]] || [[ "$q" == *"步骤"* ]]; then
    echo tutorial
  elif [[ "$q" == *"新闻"* ]] || [[ "$q" == *"news"* ]] || [[ "$q" == *"发布"* ]] || [[ "$q" == *"breaking"* ]]; then
    echo news
  elif [[ "$q" == *"资源"* ]] || [[ "$q" == *"合集"* ]] || [[ "$q" == *"清单"* ]] || [[ "$q" == *"list"* ]] || [[ "$q" == *"awesome"* ]]; then
    echo resource
  elif [[ "$q" == *"最新"* ]] || [[ "$q" == *"最近"* ]] || [[ "$q" == *"现状"* ]] || [[ "$q" == *"状态"* ]] || [[ "$q" == *"目前"* ]] || [[ "$q" == *"进展"* ]] || [[ "$q" == *"status"* ]] || [[ "$q" == *"current"* ]] || [[ "$q" == *"latest"* ]]; then
    echo status
  elif [[ "$q" == *"研究"* ]] || [[ "$q" == *"追踪"* ]] || [[ "$q" == *"汇总"* ]] || [[ "$q" == *"综述"* ]] || [[ "$q" == *"调研"* ]] || [[ "$q" == *"explore"* ]] || [[ "$q" == *"survey"* ]]; then
    echo exploratory
  else
    echo factual
  fi
}

should_use_search_layer() {
  local q
  q="$(lower "$1")"
  [[ "$q" == *"对比"* ]] && return 0
  [[ "$q" == *"区别"* ]] && return 0
  [[ "$q" == *"比较"* ]] && return 0
  [[ "$q" == *"哪个好"* ]] && return 0
  [[ "$q" == *"最新"* ]] && return 0
  [[ "$q" == *"最近"* ]] && return 0
  [[ "$q" == *"状态"* ]] && return 0
  [[ "$q" == *"现状"* ]] && return 0
  [[ "$q" == *"目前"* ]] && return 0
  [[ "$q" == *"research"* ]] && return 0
  [[ "$q" == *"compare"* ]] && return 0
  [[ "$q" == *"status"* ]] && return 0
  [[ "$q" == *"latest"* ]] && return 0
  [[ "$q" == *"current"* ]] && return 0
  return 1
}

run_search_layer_auto() {
  local query="$1"
  local intent
  local variants=()
  local variant
  intent="$(infer_intent "$query")"
  while IFS= read -r variant; do
    [[ -n "$variant" ]] && variants+=("$variant")
  done < <(expand_query_variants "$query")
  if [[ ${#variants[@]} -gt 1 ]]; then
    run_with_save "$SEARCH_LAYER_WRAPPER" --queries "${variants[@]}" --intent "$intent" --mode deep --source exa,tavily,grok,tinyfish
    return
  fi
  run_with_save "$SEARCH_LAYER_WRAPPER" "$query" --intent "$intent" --mode deep --source exa,tavily,grok,tinyfish
}

if [[ ${1:-} == "--help" || ${1:-} == "-h" ]]; then
  usage
  exit 0
fi

if [[ $# -eq 0 ]]; then
  usage >&2
  exit 1
fi

normalize_mode_aliases "$@"
set -- "${NORMALIZED_ARGS[@]}"

# Parse --save-run early (before routing) and strip it from args
SAVE_RUN_DIR=""
FILTERED=()
SKIP_SAVE=false
for arg in "$@"; do
  if $SKIP_SAVE; then
    SAVE_RUN_DIR="$arg"
    SKIP_SAVE=false
    continue
  fi
  if [[ "$arg" == "--save-run" ]]; then
    SKIP_SAVE=true
    continue
  fi
  FILTERED+=("$arg")
done
set -- "${FILTERED[@]}"

# Fallback to env var if --save-run not explicitly passed on command line
if [[ -z "$SAVE_RUN_DIR" && -n "${UNIFIED_SEARCH_SAVE_DIR:-}" ]]; then
  SAVE_RUN_DIR="$UNIFIED_SEARCH_SAVE_DIR"
fi

# Prepare legacy passthrough args
LEGACY_SAVE=()
if [[ -n "$SAVE_RUN_DIR" ]]; then
  LEGACY_SAVE=(--save-run "$SAVE_RUN_DIR")
fi

# Helper: run a sub-command wrapper, optionally saving stdout to a file.
# When --save-run is not set, behaviour is identical to exec (replaces process).
run_with_save() {
  local wrapper="$1"
  shift
  if [[ -n "$SAVE_RUN_DIR" ]]; then
    mkdir -p "$SAVE_RUN_DIR"
    local ts mode
    ts="$(date +%Y%m%dT%H%M%S)"
    mode="$(basename "$wrapper" .sh | sed 's/^run-//;s/^unified-search-legacy$/legacy/')"
    echo "[save-run] $mode → $SAVE_RUN_DIR/${mode}-${ts}.json" >&2
    bash "$wrapper" "$@" | tee "$SAVE_RUN_DIR/${mode}-${ts}.json"
    exit "${PIPESTATUS[0]}"
  else
    exec bash "$wrapper" "$@"
  fi
}

cmd="${1:-}"
case "$cmd" in
  search-layer)
    shift
    run_with_save "$SEARCH_LAYER_WRAPPER" "$@"
    ;;
  fetch-thread)
    shift
    run_with_save "$FETCH_THREAD_WRAPPER" "$@"
    ;;
  content-extract)
    shift
    run_with_save "$CONTENT_EXTRACT_WRAPPER" "$@"
    ;;
  mineru-extract)
    shift
    run_with_save "$MINERU_EXTRACT_WRAPPER" "$@"
    ;;
  mineru-parse-documents)
    shift
    run_with_save "$MINERU_PARSE_DOCS_WRAPPER" "$@"
    ;;
  legacy)
    shift
    run_with_save "$LEGACY_SCRIPT" "${LEGACY_SAVE[@]}" "$@"
    ;;
  *)
    ;;
esac

force_legacy=0
if has_arg --legacy "$@"; then
  force_legacy=1
fi

if [[ "$force_legacy" == "0" ]]; then
  local_like_flags=0
  for arg in "$@"; do
    case "$arg" in
      --mode|--intent|--freshness|--queries|--source|--extract-refs|--extract-refs-urls|--domain-boost)
        local_like_flags=1
        ;;
    esac
  done
  if [[ "$local_like_flags" == "1" ]]; then
    run_with_save "$SEARCH_LAYER_WRAPPER" "$@"
  fi
fi

url="$(first_url "$@" || true)"
if [[ -n "$url" && "$force_legacy" == "0" ]]; then
  if is_thread_url "$url"; then
    run_with_save "$FETCH_THREAD_WRAPPER" "$url"
  elif is_document_url "$url"; then
    run_with_save "$MINERU_EXTRACT_WRAPPER" "$url"
  else
    run_with_save "$CONTENT_EXTRACT_WRAPPER" --url "$url"
  fi
fi

query="$(query_text "$@")"
if [[ -n "$query" && "$force_legacy" == "0" ]]; then
  # Default chat /unified_search behavior: route ordinary lookups to deep search-layer.
  # Use --legacy or the explicit "legacy" subcommand to keep the old Tavily + Exa + Google path.
  run_search_layer_auto "$query"
fi

run_with_save "$LEGACY_SCRIPT" "${LEGACY_SAVE[@]}" "$@"
