#!/usr/bin/env sh

set -eu

ROOT="$(CDPATH= cd -- "$(dirname "$0")/.." && pwd)"
WORKSPACE_ROOT="$(CDPATH= cd -- "$ROOT/../.." && pwd)"
CLAWHUB_JSON="$ROOT/clawhub.json"
VALIDATOR="$WORKSPACE_ROOT/tmp/validate_clawhub_skill_dir.sh"
VERSION="$(node -e "process.stdout.write(require(process.argv[1]).version)" "$CLAWHUB_JSON")"
SLUG="reviewlens"
NAME="评论透镜"
CHANGELOG="Launch 评论透镜 (ReviewLens), a review-intelligence skill that compresses marketplace reviews into a decision card with repeated praise, repeated complaints, fit, regret risk, and cheap-versus-steady judgment."
TAGS="latest,reviews,shopping,review-intelligence,review-analysis,buyer-regret,user-fit,ecommerce,taobao,tmall,jd,pdd"
PUBLISH_ROOT="$ROOT"
TMP_DIR=""

if ! command -v clawhub >/dev/null 2>&1; then
  echo "clawhub CLI not found in PATH" >&2
  exit 1
fi

if ! command -v node >/dev/null 2>&1; then
  echo "node is required to read version metadata from clawhub.json" >&2
  exit 1
fi

if [ -d "$ROOT/.git" ]; then
  TMP_DIR="$(mktemp -d)"
  PUBLISH_ROOT="$TMP_DIR/$SLUG"
  mkdir -p "$PUBLISH_ROOT"
  cp "$ROOT/SKILL.md" "$PUBLISH_ROOT/SKILL.md"
  cp "$ROOT/RELEASE.md" "$PUBLISH_ROOT/RELEASE.md"
  cp "$ROOT/clawhub.json" "$PUBLISH_ROOT/clawhub.json"
  cp -R "$ROOT/agents" "$PUBLISH_ROOT/agents"
  cp -R "$ROOT/references" "$PUBLISH_ROOT/references"
  cp -R "$ROOT/scripts" "$PUBLISH_ROOT/scripts"
  trap 'rm -rf "$TMP_DIR"' EXIT HUP INT TERM
fi

if [ "${1:-}" = "--print" ]; then
  cat <<EOF
clawhub publish "$PUBLISH_ROOT" \\
  --slug "$SLUG" \\
  --name "$NAME" \\
  --version "$VERSION" \\
  --changelog "$CHANGELOG" \\
  --tags "$TAGS"
EOF
  exit 0
fi

if [ -f "$VALIDATOR" ]; then
  bash "$VALIDATOR" "$PUBLISH_ROOT"
fi

echo "Publishing ReviewLens from: $PUBLISH_ROOT"
echo "Version: $VERSION"
echo "Name: $NAME"
echo "Tags: $TAGS"

clawhub publish "$PUBLISH_ROOT" \
  --slug "$SLUG" \
  --name "$NAME" \
  --version "$VERSION" \
  --changelog "$CHANGELOG" \
  --tags "$TAGS"
