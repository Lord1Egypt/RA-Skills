#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: bash scripts/a11y-audit.sh <http-url> [output-directory]

Run axe, Pa11y, QualWeb ACT rules, and Nu HTML validation against an HTTP page.
Prerequisites: axe, pa11y, vnu, curl, node, @qualweb/cli, Chrome/Chromium, and
matching Chromedriver. Override browser discovery with AXE_CHROME_PATH and
AXE_CHROMEDRIVER_PATH.

In CI (or whenever the CI env var is set to "true"), Chrome is launched
through a thin wrapper that adds --no-sandbox --disable-setuid-sandbox
--disable-dev-shm-usage, since hosted CI runners commonly can't satisfy
Chrome's sandbox requirements and otherwise fail with
"session not created: Chrome instance exited". Set AXE_CHROME_EXTRA_ARGS to
override the flags used (space-separated), or set it to an empty string to
force the sandbox back on. This applies uniformly to axe, Pa11y, and QualWeb,
since all three are pointed at the same Chrome executable path.
EOF
}

if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  usage
  exit 0
fi

if [[ $# -lt 1 || $# -gt 2 ]]; then
  usage >&2
  exit 64
fi

url="$1"
out_dir="${2:-a11y-reports}"
mkdir -p "$out_dir"

# Prefer tools pinned in package.json (installed via `npm ci`) over anything
# found elsewhere on PATH, for reproducible tool versions.
repo_root="$(cd "$(dirname "$0")/.." && pwd)"
if [[ -d "$repo_root/node_modules/.bin" ]]; then
  PATH="$repo_root/node_modules/.bin:$PATH"
fi

for command in axe pa11y vnu curl node npm; do
  command -v "$command" >/dev/null || {
    echo "Missing required command: $command" >&2
    exit 69
  }
done

chrome_path="${AXE_CHROME_PATH:-}"
if [[ -z "$chrome_path" ]]; then
  chrome_path="$(command -v google-chrome || command -v chromium || command -v chromium-browser || true)"
fi
driver_path="${AXE_CHROMEDRIVER_PATH:-$(command -v chromedriver || true)}"
[[ -n "$chrome_path" ]] || { echo "Chrome/Chromium was not found." >&2; exit 69; }
[[ -n "$driver_path" ]] || { echo "Chromedriver was not found." >&2; exit 69; }

# Hosted CI runners frequently can't satisfy Chrome's sandbox requirements,
# which surfaces as "session not created: Chrome instance exited" from
# chromedriver (and equivalent Puppeteer launch failures from Pa11y/QualWeb).
# Wrap the real Chrome binary so all three tools pick up the fix uniformly,
# without touching the sandbox for local/developer runs by default.
chrome_extra_args="${AXE_CHROME_EXTRA_ARGS-}"
if [[ -z "${AXE_CHROME_EXTRA_ARGS+set}" && "${CI:-}" == "true" ]]; then
  chrome_extra_args="--no-sandbox --disable-setuid-sandbox --disable-dev-shm-usage"
fi
if [[ -n "$chrome_extra_args" ]]; then
  chrome_wrapper="$out_dir/.chrome-sandbox-safe-wrapper.sh"
  cat > "$chrome_wrapper" <<WRAPPER
#!/usr/bin/env bash
exec "$chrome_path" $chrome_extra_args "\$@"
WRAPPER
  chmod +x "$chrome_wrapper"
  echo "Wrapping Chrome ($chrome_path) with extra args: $chrome_extra_args"
  chrome_path="$(cd "$out_dir" && pwd)/$(basename "$chrome_wrapper")"
fi

qualweb_cli="$repo_root/node_modules/@qualweb/cli/dist/cli.js"
if [[ ! -f "$qualweb_cli" ]]; then
  qualweb_cli="$(npm root -g)/@qualweb/cli/dist/cli.js"
fi
[[ -f "$qualweb_cli" ]] || { echo "@qualweb/cli was not found at $qualweb_cli" >&2; exit 69; }

echo "Running axe..."
axe "$url" --chrome-path "$chrome_path" --chromedriver-path "$driver_path" --stdout > "$out_dir/axe_report.json"

echo "Running Pa11y..."
# Pa11y intentionally exits 2 (not 0) when it finds accessibility errors on
# the page (exit 1 means an actual technical fault; see pa11y's README).
# This script's job is to produce reports, not gate on findings, so only
# treat pa11y's exit code as fatal when it's neither "success" nor "found
# errors".
pa11y_status=0
PUPPETEER_EXECUTABLE_PATH="$chrome_path" pa11y "$url" --reporter json > "$out_dir/pa11y_report.json" || pa11y_status=$?
if [[ "$pa11y_status" -ne 0 && "$pa11y_status" -ne 2 ]]; then
  echo "Pa11y failed with exit code $pa11y_status" >&2
  exit "$pa11y_status"
fi

echo "Running QualWeb ACT rules..."
PUPPETEER_EXECUTABLE_PATH="$chrome_path" node "$qualweb_cli" -u "$url" -m act-rules --act-levels A AA AAA -o "$out_dir/qualweb_report.json"

echo "Running Nu HTML Checker..."
html_file="$out_dir/fetched-page.html"
curl --fail --location --silent --show-error "$url" > "$html_file"
node "$(dirname "$0")/run-w3c-validator.mjs" "$html_file" "$out_dir/w3c_source_html_report.json" "$url"

echo "Reports written to $out_dir"
