#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BIN_DEFAULT="$SKILL_DIR/bin/mp-weixin-skill"
BIN="${MP_WECHAT_CLI_BIN:-$BIN_DEFAULT}"
GITHUB_REPO="${MP_WECHAT_GITHUB_REPO:-}"
RELEASE_TAG="${MP_WECHAT_RELEASE_TAG:-latest}"
ASSET_NAME="${MP_WECHAT_ASSET_NAME:-}"
RELEASE_URL="${MP_WECHAT_RELEASE_URL:-}"
ARTICLE_IMAGE=""
COVER_IMAGE=""
CONTENT_FILE=""
TITLE=""
AUTHOR=""
DIGEST=""
THUMB_MEDIA_ID=""

usage() {
  cat <<'EOF'
Usage:
  publish_draft.sh [--bin /path/to/mp-weixin-skill] \
    [--article-image /path/to/article.png] \
    --cover-image /path/to/cover.png \
    --content-file /path/to/content.html \
    --title "Article Title" [--author "Author"] [--digest "Digest"] [--thumb-media-id "MEDIA_ID"]

Options:
  --bin              Path to executable (default: <skill>/bin/mp-weixin-skill, or env MP_WECHAT_CLI_BIN)
  --repo             GitHub repo owner/repo for auto-download (or env MP_WECHAT_GITHUB_REPO)
  --tag              GitHub release tag (default: latest, or env MP_WECHAT_RELEASE_TAG)
  --asset            Release asset name override (or env MP_WECHAT_ASSET_NAME)
  --url              Direct release asset URL (or env MP_WECHAT_RELEASE_URL)
  --article-image    Optional local article image path
  --cover-image      Local cover image path
  --content-file     Local article content file path
  --title            Draft title
  --author           Optional author
  --digest           Optional digest
  --thumb-media-id   Optional override for addDraft --thumb-media-id
  -h, --help         Show this help
EOF
}

err_json() {
  printf '{"error":"%s"}\n' "$1" >&2
}

escape_json() {
  printf '%s' "$1" | sed 's/\\/\\\\/g; s/"/\\"/g'
}

extract_json_field() {
  local json="$1"
  local key="$2"
  printf '%s\n' "$json" | sed -n 's/.*"'"$key"'"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n1
}

run_cli() {
  local output
  if ! output="$($BIN "$@" 2>&1)"; then
    err_json "command failed: $BIN $* ; $output"
    exit 1
  fi

  local last_line
  last_line="$(printf '%s\n' "$output" | awk 'NF{p=$0} END{print p}')"
  if [ -z "$last_line" ]; then
    printf '{}\n'
    return
  fi

  printf '%s\n' "$last_line"
}

ensure_bin() {
  if [ -x "$BIN" ]; then
    return
  fi

  if [ -z "$GITHUB_REPO" ] && [ -z "$RELEASE_URL" ]; then
    err_json "executable not found: $BIN ; set --bin or configure --url/MP_WECHAT_RELEASE_URL or --repo/MP_WECHAT_GITHUB_REPO"
    exit 1
  fi

  local installer="$SCRIPT_DIR/install_mp_weixin_skill.sh"
  if [ ! -x "$installer" ]; then
    err_json "installer script missing or not executable: $installer"
    exit 1
  fi

  local cmd=(bash "$installer" --out "$BIN")
  if [ -n "$RELEASE_URL" ]; then
    cmd+=(--url "$RELEASE_URL")
  else
    cmd+=(--repo "$GITHUB_REPO" --tag "$RELEASE_TAG")
    if [ -n "$ASSET_NAME" ]; then
      cmd+=(--asset "$ASSET_NAME")
    fi
  fi
  if ! "${cmd[@]}" >/dev/null 2>&1; then
    err_json "failed to download executable from release"
    exit 1
  fi

  if [ ! -x "$BIN" ]; then
    err_json "download completed but executable is unavailable: $BIN"
    exit 1
  fi
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --bin)
      BIN="$2"
      shift 2
      ;;
    --article-image)
      ARTICLE_IMAGE="$2"
      shift 2
      ;;
    --repo)
      GITHUB_REPO="$2"
      shift 2
      ;;
    --tag)
      RELEASE_TAG="$2"
      shift 2
      ;;
    --asset)
      ASSET_NAME="$2"
      shift 2
      ;;
    --url)
      RELEASE_URL="$2"
      shift 2
      ;;
    --cover-image)
      COVER_IMAGE="$2"
      shift 2
      ;;
    --content-file)
      CONTENT_FILE="$2"
      shift 2
      ;;
    --title)
      TITLE="$2"
      shift 2
      ;;
    --author)
      AUTHOR="$2"
      shift 2
      ;;
    --digest)
      DIGEST="$2"
      shift 2
      ;;
    --thumb-media-id)
      THUMB_MEDIA_ID="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      err_json "unknown option: $1"
      usage >&2
      exit 1
      ;;
  esac
done

ensure_bin
if [ -z "$COVER_IMAGE" ] || [ -z "$CONTENT_FILE" ] || [ -z "$TITLE" ]; then
  err_json "--cover-image, --content-file, --title are required"
  usage >&2
  exit 1
fi
if [ ! -f "${HOME}/.weixin_credentials" ]; then
  err_json "missing credentials file: ${HOME}/.weixin_credentials (required by getAuth)"
  exit 1
fi

# 1) getAuth
AUTH_JSON="$(run_cli getAuth)"
ACCESS_TOKEN="$(extract_json_field "$AUTH_JSON" "access_token")"
if [ -z "$ACCESS_TOKEN" ]; then
  err_json "getAuth succeeded but access_token not found in: $AUTH_JSON"
  exit 1
fi

# 2) uploadArticleImage (optional)
ARTICLE_URL=""
if [ -n "$ARTICLE_IMAGE" ]; then
  ARTICLE_JSON="$(run_cli uploadArticleImage --token "$ACCESS_TOKEN" --path "$ARTICLE_IMAGE")"
  ARTICLE_URL="$(extract_json_field "$ARTICLE_JSON" "url")"
fi

# 3) uploadCoverImage
COVER_JSON="$(run_cli uploadCoverImage --token "$ACCESS_TOKEN" --path "$COVER_IMAGE")"
if [ -z "$THUMB_MEDIA_ID" ]; then
  THUMB_MEDIA_ID="$(extract_json_field "$COVER_JSON" "media_id")"
fi
if [ -z "$THUMB_MEDIA_ID" ]; then
  THUMB_MEDIA_ID="$(extract_json_field "$COVER_JSON" "mediaId")"
fi
if [ -z "$THUMB_MEDIA_ID" ]; then
  THUMB_MEDIA_ID="$(extract_json_field "$COVER_JSON" "url")"
fi
if [ -z "$THUMB_MEDIA_ID" ]; then
  err_json "cannot resolve thumb_media_id; pass --thumb-media-id, cover response: $COVER_JSON"
  exit 1
fi

# 4) addDraft
DRAFT_JSON="$(run_cli addDraft \
  --token "$ACCESS_TOKEN" \
  --title "$TITLE" \
  --author "$AUTHOR" \
  --content-file "$CONTENT_FILE" \
  --digest "$DIGEST" \
  --thumb-media-id "$THUMB_MEDIA_ID")"

printf '{"access_token":"%s","article_image_url":"%s","cover_upload":%s,"thumb_media_id_used":"%s","draft":%s}\n' \
  "$(escape_json "$ACCESS_TOKEN")" \
  "$(escape_json "$ARTICLE_URL")" \
  "$COVER_JSON" \
  "$(escape_json "$THUMB_MEDIA_ID")" \
  "$DRAFT_JSON"
