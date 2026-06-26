#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  inspect-rest-api.sh --site https://example.com [--route /wp/v2/posts] [--method GET|OPTIONS] [--user USER --app-password PASS]

Examples:
  inspect-rest-api.sh --site https://example.com
  inspect-rest-api.sh --site https://example.com --route /wp/v2/posts
  inspect-rest-api.sh --site https://example.com --route /wp/v2/posts --method OPTIONS
  inspect-rest-api.sh --site https://example.com --user admin --app-password "xxxx xxxx xxxx xxxx"
EOF
}

SITE=""
ROUTE=""
METHOD="GET"
USER_NAME=""
APP_PASSWORD=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --site)
      SITE="${2:-}"
      shift 2
      ;;
    --route)
      ROUTE="${2:-}"
      shift 2
      ;;
    --method)
      METHOD="${2:-}"
      shift 2
      ;;
    --user)
      USER_NAME="${2:-}"
      shift 2
      ;;
    --app-password)
      APP_PASSWORD="${2:-}"
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

if [[ -z "$SITE" ]]; then
  echo "--site is required" >&2
  usage >&2
  exit 1
fi

if [[ -n "$USER_NAME" && -z "$APP_PASSWORD" ]] || [[ -z "$USER_NAME" && -n "$APP_PASSWORD" ]]; then
  echo "--user and --app-password must be provided together" >&2
  exit 1
fi

SITE="${SITE%/}"
METHOD="$(printf '%s' "$METHOD" | tr '[:lower:]' '[:upper:]')"

case "$METHOD" in
  GET|OPTIONS)
    ;;
  *)
    echo "--method must be GET or OPTIONS" >&2
    exit 1
    ;;
esac

if [[ -n "$ROUTE" ]]; then
  if [[ "$ROUTE" == http://* || "$ROUTE" == https://* ]]; then
    TARGET_URL="$ROUTE"
  else
    ROUTE="/${ROUTE#/}"
    if [[ "$ROUTE" == /wp-json/* ]]; then
      TARGET_URL="${SITE}${ROUTE}"
    else
      TARGET_URL="${SITE}/wp-json${ROUTE}"
    fi
  fi
else
  TARGET_URL="${SITE}/wp-json/"
fi

TMP_BODY="$(mktemp)"
trap 'rm -f "$TMP_BODY"' EXIT

CURL_ARGS=(
  --silent
  --show-error
  --location
  --request "$METHOD"
  --header "Accept: application/json"
  --output "$TMP_BODY"
  --write-out "%{http_code}"
)

if [[ -n "$USER_NAME" ]]; then
  CURL_ARGS+=(--user "${USER_NAME}:${APP_PASSWORD}")
fi

STATUS_CODE="$(curl "${CURL_ARGS[@]}" "$TARGET_URL")"

echo "URL: $TARGET_URL"
echo "HTTP: $STATUS_CODE"
echo

python3 - "$TMP_BODY" "$ROUTE" "$METHOD" <<'PY'
import json
import pathlib
import sys

body_path = pathlib.Path(sys.argv[1])
route = sys.argv[2]
method = sys.argv[3]
raw = body_path.read_text()

try:
    data = json.loads(raw)
except json.JSONDecodeError:
    print(raw)
    sys.exit(0)

if isinstance(data, dict) and "routes" in data and "namespaces" in data and not route:
    namespaces = data.get("namespaces", [])
    routes = data.get("routes", {})
    print("Namespaces:")
    for ns in namespaces:
        print(f"- {ns}")
    print()
    print(f"Routes: {len(routes)}")
    for path in sorted(routes):
        item = routes[path]
        methods = []
        if isinstance(item, list):
            for entry in item:
                methods.extend(entry.get("methods", []))
        elif isinstance(item, dict):
            methods.extend(item.get("methods", []))
        method_list = ", ".join(sorted(set(methods))) if methods else "unknown"
        print(f"- {path} [{method_list}]")
    sys.exit(0)

if method == "OPTIONS" and isinstance(data, dict):
    print(json.dumps(data, indent=2, sort_keys=True))
    sys.exit(0)

print(json.dumps(data, indent=2, sort_keys=True))
PY
