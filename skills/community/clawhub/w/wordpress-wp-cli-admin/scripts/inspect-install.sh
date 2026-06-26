#!/usr/bin/env bash
set -euo pipefail

export PATH=/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

usage() {
  cat <<'EOF'
Usage:
  inspect-install.sh --path /srv/www/site [--url https://example.com]

Examples:
  inspect-install.sh --path /srv/www/site
  inspect-install.sh --path /srv/www/site --url https://example.com
EOF
}

WP_PATH=""
WP_URL=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --path)
      WP_PATH="${2:-}"
      shift 2
      ;;
    --url)
      WP_URL="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "unknown argument: $1" >&2
      usage >&2
      exit 1
      ;;
  esac
done

if [[ -z "$WP_PATH" ]]; then
  echo "--path is required" >&2
  usage >&2
  exit 1
fi

if ! command -v wp >/dev/null 2>&1; then
  echo "wp not found in PATH" >&2
  exit 1
fi

if [[ ! -d "$WP_PATH" ]]; then
  echo "path does not exist: $WP_PATH" >&2
  exit 1
fi

if [[ ! -f "$WP_PATH/wp-config.php" && ! -f "$WP_PATH/wp-load.php" ]]; then
  echo "path does not look like a WordPress install: $WP_PATH" >&2
  exit 1
fi

WP_ARGS=(--path="$WP_PATH")

if [[ -n "$WP_URL" ]]; then
  WP_ARGS+=(--url="$WP_URL")
fi

echo "=== target ==="
printf 'path: %s\n' "$WP_PATH"
if [[ -n "$WP_URL" ]]; then
  printf 'url: %s\n' "$WP_URL"
fi
echo

echo "=== core ==="
wp "${WP_ARGS[@]}" core is-installed >/dev/null && echo "installed: yes" || echo "installed: no"
wp "${WP_ARGS[@]}" core version || true
echo

echo "=== urls ==="
wp "${WP_ARGS[@]}" option get home || true
wp "${WP_ARGS[@]}" option get siteurl || true
echo

echo "=== plugins ==="
wp "${WP_ARGS[@]}" plugin list --fields=name,status,version,update --format=table || true
echo

echo "=== themes ==="
wp "${WP_ARGS[@]}" theme list --fields=name,status,version,update --format=table || true
echo

echo "=== users ==="
wp "${WP_ARGS[@]}" user list --fields=ID,user_login,roles --format=table || true
echo

echo "=== cron ==="
wp "${WP_ARGS[@]}" cron event list --fields=hook,next_run_gmt,next_run_relative --format=table || true
