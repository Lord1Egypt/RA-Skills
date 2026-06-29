#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WEB_DIR="${ROOT}/web"

PAGES_PROJECT="${SAGEROUTER_CLOUDFLARE_PAGES_PROJECT:-sage-router-web}"
PAGES_PRODUCTION_BRANCH="${SAGEROUTER_CLOUDFLARE_PAGES_PRODUCTION_BRANCH:-main}"
DEPLOY_PAGES="${SAGEROUTER_DEPLOY_PAGES:-1}"
DEPLOY_CLOUD_RUN="${SAGEROUTER_DEPLOY_CLOUD_RUN:-0}"
RUN_READINESS="${SAGEROUTER_DEPLOY_RUN_READINESS:-1}"
GHCR_IMAGE_DIGEST="${GHCR_IMAGE_DIGEST:-${SAGEROUTER_GHCR_IMAGE_DIGEST:-}}"

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    printf 'Missing required command: %s\n' "$1" >&2
    exit 2
  fi
}

git_value() {
  git -C "$ROOT" "$@" 2>/dev/null || true
}

resolve_release_digest_from_actions() {
  require_cmd gh
  local run_id digest
  run_id="$(
    gh run list \
      --repo earlvanze/sage-router \
      --workflow "Release image" \
      --branch master \
      --limit 1 \
      --json databaseId,conclusion \
      --jq '.[] | select(.conclusion == "success") | .databaseId' \
      | head -n1
  )"
  if [[ -z "$run_id" ]]; then
    return 1
  fi
  digest="$(
    gh run view "$run_id" --repo earlvanze/sage-router --log \
      | sed -n 's/.*"containerimage.digest": "\(sha256:[0-9a-f]\{64\}\)".*/\1/p' \
      | tail -n1
  )"
  [[ -n "$digest" ]] || return 1
  printf '%s\n' "$digest"
}

deploy_pages() {
  require_cmd npm
  require_cmd npx

  local tmp commit_hash commit_message
  tmp="$(mktemp -d /tmp/sage-router-web.XXXXXX)"
  commit_hash="$(git_value rev-parse HEAD)"
  commit_message="$(git_value log -1 --pretty=%s)"

  printf 'Building Cloudflare Pages from clean temp copy: %s\n' "$tmp" >&2
  (
    cd "$WEB_DIR"
    tar \
      --exclude='./node_modules' \
      --exclude='./dist' \
      --exclude='./.wrangler' \
      -cf - .
  ) | tar -xf - -C "$tmp"

  (
    cd "$tmp"
    npm ci
    npm run build
    if [[ -d functions ]]; then
      npx wrangler pages functions build functions \
        --outdir dist/_worker.js \
        --output-routes-path dist/_routes.json \
        --build-output-directory dist
    fi
  )

  printf 'Deploying Cloudflare Pages project=%s branch=%s\n' "$PAGES_PROJECT" "$PAGES_PRODUCTION_BRANCH" >&2
  local wrangler_args=(
    pages deploy "$tmp/dist"
    --project-name "$PAGES_PROJECT"
    --branch "$PAGES_PRODUCTION_BRANCH"
    --commit-dirty=true
  )
  if [[ -n "$commit_hash" ]]; then
    wrangler_args+=(--commit-hash "$commit_hash")
  fi
  if [[ -n "$commit_message" ]]; then
    wrangler_args+=(--commit-message "$commit_message")
  fi
  npx wrangler "${wrangler_args[@]}"
}

deploy_cloud_run() {
  if [[ -z "$GHCR_IMAGE_DIGEST" ]]; then
    printf 'GHCR_IMAGE_DIGEST not set; resolving latest successful Release image digest from GitHub Actions.\n' >&2
    GHCR_IMAGE_DIGEST="$(resolve_release_digest_from_actions || true)"
  fi
  if [[ -z "$GHCR_IMAGE_DIGEST" ]]; then
    printf 'Could not resolve GHCR image digest. Set GHCR_IMAGE_DIGEST=sha256:... and retry.\n' >&2
    exit 2
  fi

  printf 'Deploying Cloud Run from GHCR digest %s\n' "$GHCR_IMAGE_DIGEST" >&2
  DEPLOY_FROM_GHCR_REMOTE=1 GHCR_IMAGE_DIGEST="$GHCR_IMAGE_DIGEST" \
    "$ROOT/deploy/gcp/cloudrun-deploy.sh"
}

if [[ "$DEPLOY_PAGES" != "0" ]]; then
  deploy_pages
else
  printf 'Skipping Cloudflare Pages deploy because SAGEROUTER_DEPLOY_PAGES=0\n' >&2
fi

if [[ "$DEPLOY_CLOUD_RUN" == "1" || -n "$GHCR_IMAGE_DIGEST" ]]; then
  deploy_cloud_run
else
  printf 'Skipping Cloud Run deploy. Set SAGEROUTER_DEPLOY_CLOUD_RUN=1 or GHCR_IMAGE_DIGEST=sha256:... to update it.\n' >&2
fi

if [[ "$RUN_READINESS" != "0" ]]; then
  "$ROOT/scripts/check_sagerouter_launch_readiness.sh"
else
  printf 'Skipping launch readiness because SAGEROUTER_DEPLOY_RUN_READINESS=0\n' >&2
fi
