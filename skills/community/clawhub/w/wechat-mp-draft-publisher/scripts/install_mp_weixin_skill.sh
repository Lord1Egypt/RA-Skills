#!/usr/bin/env bash
set -euo pipefail

REPO=""
TAG="latest"
ASSET_NAME=""
OUT=""
URL=""

usage() {
  cat <<'EOF'
Usage:
  install_mp_weixin_skill.sh (--url https://... | --repo owner/repo) [--tag latest|vX.Y.Z] [--asset asset-name] [--out /path/to/mp-weixin-skill]

Options:
  --url     Direct download URL for release asset (zip or binary)
  --repo    GitHub repository in owner/repo format
  --tag     Release tag, default latest
  --asset   Release asset name; if omitted, auto-detect by platform
  --out     Output binary path; default: <skill>/bin/mp-weixin-skill
  -h, --help
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --repo)
      REPO="$2"; shift 2 ;;
    --url)
      URL="$2"; shift 2 ;;
    --tag)
      TAG="$2"; shift 2 ;;
    --asset)
      ASSET_NAME="$2"; shift 2 ;;
    --out)
      OUT="$2"; shift 2 ;;
    -h|--help)
      usage; exit 0 ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1 ;;
  esac
done

if [ -z "$REPO" ] && [ -z "$URL" ]; then
  echo "Either --url or --repo is required" >&2
  usage
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
if [ -z "$OUT" ]; then
  OUT="$SKILL_DIR/bin/mp-weixin-skill"
fi
mkdir -p "$(dirname "$OUT")"

os="$(uname -s | tr '[:upper:]' '[:lower:]')"
arch="$(uname -m)"
case "$arch" in
  arm64|aarch64) arch="arm64" ;;
  x86_64|amd64) arch="amd64" ;;
esac

if [ -z "$ASSET_NAME" ]; then
  ASSET_NAME="mp-weixin-skill-${os}-${arch}"
  if [ "$os" = "windows" ]; then
    ASSET_NAME="${ASSET_NAME}.exe"
  fi
fi

auth_header=()
if [ -n "${GITHUB_TOKEN:-}" ]; then
  auth_header=(-H "Authorization: Bearer ${GITHUB_TOKEN}")
fi

asset_url="$URL"
if [ -z "$asset_url" ]; then
  if [ "$TAG" = "latest" ]; then
    api_url="https://api.github.com/repos/${REPO}/releases/latest"
  else
    api_url="https://api.github.com/repos/${REPO}/releases/tags/${TAG}"
  fi

  if [ -n "${GITHUB_TOKEN:-}" ]; then
    release_json="$(curl -fsSL -H "Authorization: Bearer ${GITHUB_TOKEN}" -H "Accept: application/vnd.github+json" "$api_url")"
  else
    release_json="$(curl -fsSL -H "Accept: application/vnd.github+json" "$api_url")"
  fi
  asset_url="$(
  printf '%s' "$release_json" | python3 - "$ASSET_NAME" <<'PY'
import json, sys
asset_name = sys.argv[1]
data = json.loads(sys.stdin.read())
assets = data.get("assets", [])
exact = [a for a in assets if a.get("name") == asset_name]
if exact:
    print(exact[0].get("browser_download_url", ""))
    raise SystemExit(0)
contains = [a for a in assets if asset_name in (a.get("name") or "")]
if contains:
    print(contains[0].get("browser_download_url", ""))
    raise SystemExit(0)
print("")
PY
)"
fi

if [ -z "$asset_url" ]; then
  echo "Asset not found in release." >&2
  echo "repo: $REPO, tag: $TAG, expected asset: $ASSET_NAME" >&2
  exit 1
fi

tmp_file="${OUT}.download"
if [ -n "${GITHUB_TOKEN:-}" ]; then
  curl -fsSL -H "Authorization: Bearer ${GITHUB_TOKEN}" -H "Accept: application/octet-stream" -o "$tmp_file" "$asset_url"
else
  curl -fsSL -H "Accept: application/octet-stream" -o "$tmp_file" "$asset_url"
fi

is_zip=0
if [ "${asset_url##*.}" = "zip" ]; then
  is_zip=1
fi
if [ "$is_zip" -eq 0 ] && command -v file >/dev/null 2>&1; then
  if file "$tmp_file" | grep -qi 'zip archive'; then
    is_zip=1
  fi
fi

if [ "$is_zip" -eq 1 ]; then
  if ! command -v unzip >/dev/null 2>&1; then
    echo "unzip is required to extract zip asset" >&2
    exit 1
  fi
  extract_dir="$(mktemp -d)"
  unzip -o "$tmp_file" -d "$extract_dir" >/dev/null
  candidate="$extract_dir/mp-weixin-skill"
  if [ ! -f "$candidate" ]; then
    candidate="$(find "$extract_dir" -type f -name 'mp-weixin-skill*' | head -n1 || true)"
  fi
  if [ -z "${candidate:-}" ] || [ ! -f "$candidate" ]; then
    echo "cannot find mp-weixin-skill in zip asset" >&2
    rm -rf "$extract_dir"
    exit 1
  fi
  chmod +x "$candidate"
  mv "$candidate" "$OUT"
  rm -rf "$extract_dir" "$tmp_file"
else
  chmod +x "$tmp_file"
  mv "$tmp_file" "$OUT"
fi

echo "Installed mp-weixin-skill to: $OUT"
