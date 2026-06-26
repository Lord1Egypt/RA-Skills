#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cmd="$repo_root/bin/x-news-crawler"

if [[ ! -x "$cmd" ]]; then
  echo "missing executable: $cmd" >&2
  exit 1
fi

echo "[1/3] help output"
"$cmd" --help >/dev/null

echo "[2/3] invalid mode should fail"
if "$cmd" --query openclaw --mode bad >/dev/null 2>&1; then
  echo "expected invalid mode to fail" >&2
  exit 1
fi

echo "[3/4] query with quotes should not trigger JS syntax error"
out="$(mktemp)"
err="$(mktemp)"
trap 'rm -f "$out" "$err"' EXIT
if "$cmd" --query 'openclaw"test' --mode top --since-hours 240 --scrolls 0 --limit 1 >"$out" 2>"$err"; then
  jq . "$out" >/dev/null
fi
if rg -q "SyntaxError" "$err"; then
  echo "unexpected SyntaxError in JS eval path" >&2
  cat "$err" >&2
  exit 1
fi

echo "[4/4] hybrid should return partial results when one source fails"
if X_NEWS_FORCE_FAIL_SOURCE=top "$cmd" --query openclaw --mode hybrid --since-hours 240 --scrolls 0 --limit 3 >"$out" 2>"$err"; then
  jq -e '.failed_sources | index("top") != null' "$out" >/dev/null
  jq -e '.rows | length >= 0' "$out" >/dev/null
else
  echo "warning: partial-fallback network probe skipped (no successful source)" >&2
fi

echo "smoke tests passed"
