#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="${SERVICE_NAME:-sage-router}"
REGION="${REGION:-us-central1}"
REPOSITORY="${REPOSITORY:-sage-router}"
IMAGE_TAG="${IMAGE_TAG:-phase2}"
PROJECT_ID="${PROJECT_ID:-${SAGE_ROUTER_GCP_PROJECT_ID:-sage-router-demo-20260428}}"
DEPLOY_FROM_GHCR_REMOTE="${DEPLOY_FROM_GHCR_REMOTE:-0}"
CLOUD_RUN_IMAGE="${CLOUD_RUN_IMAGE:-${SAGE_ROUTER_CLOUD_RUN_IMAGE:-}}"
GHCR_REMOTE_REPOSITORY="${GHCR_REMOTE_REPOSITORY:-ghcr-remote}"
GHCR_REMOTE_UPSTREAM="${GHCR_REMOTE_UPSTREAM:-https://ghcr.io}"
GHCR_IMAGE="${GHCR_IMAGE:-earlvanze/sage-router-public}"
GHCR_IMAGE_TAG="${GHCR_IMAGE_TAG:-latest}"
GHCR_IMAGE_DIGEST="${GHCR_IMAGE_DIGEST:-}"
PUBLIC_BASE_URL="${SAGE_ROUTER_PUBLIC_BASE_URL:-https://app.sagerouter.dev}"
MARKETING_BASE_URL="${SAGE_ROUTER_MARKETING_BASE_URL:-https://sagerouter.dev}"
APP_BASE_URL="${SAGE_ROUTER_APP_BASE_URL:-https://app.sagerouter.dev}"
API_BASE_URL="${SAGE_ROUTER_API_BASE_URL:-https://api.sagerouter.dev}"
CORS_ORIGIN="${SAGE_ROUTER_CORS_ORIGIN:-https://sagerouter.dev,https://www.sagerouter.dev,https://app.sagerouter.dev}"
STRIPE_PRICE_IDS="${SAGE_ROUTER_STRIPE_PRICE_IDS:-}"

secret_exists() {
  gcloud secrets describe "$1" --project "${PROJECT_ID}" >/dev/null 2>&1
}

optional_activation_email_secret_bindings() {
  local bindings=()
  if secret_exists SAGE_ROUTER_ACTIVATION_EMAIL_FROM; then
    bindings+=("SAGE_ROUTER_ACTIVATION_EMAIL_FROM=SAGE_ROUTER_ACTIVATION_EMAIL_FROM:latest")
  fi
  if secret_exists SAGE_ROUTER_RESEND_API_KEY; then
    bindings+=("SAGE_ROUTER_RESEND_API_KEY=SAGE_ROUTER_RESEND_API_KEY:latest")
  fi
  if secret_exists SAGE_ROUTER_ACTIVATION_EMAIL_REPLY_TO; then
    bindings+=("SAGE_ROUTER_ACTIVATION_EMAIL_REPLY_TO=SAGE_ROUTER_ACTIVATION_EMAIL_REPLY_TO:latest")
  fi
  if ((${#bindings[@]})); then
    IFS=,
    printf ',%s' "${bindings[*]}"
  fi
}

if [[ -z "${STRIPE_PRICE_IDS}" && -n "${STRIPE_SECRET_KEY:-}" ]]; then
  STRIPE_PRICE_IDS="$(
    python3 - <<'PY'
import json
import os
import urllib.parse
import urllib.request

key = os.environ.get("STRIPE_SECRET_KEY") or os.environ.get("SAGE_ROUTER_STRIPE_SECRET_KEY")
if not key:
    raise SystemExit(0)

url = "https://api.stripe.com/v1/prices?" + urllib.parse.urlencode(
    {"active": "true", "limit": "100", "expand[]": "data.product"}
)
req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}"})
with urllib.request.urlopen(req, timeout=20) as resp:
    prices = json.load(resp).get("data", [])

lookup_to_plan = {
    "sage_router_lite_monthly": "lite",
    "sage_router_pro_monthly": "pro",
    "sage_router_max_monthly": "max",
}
mapped = {}
for price in prices:
    plan = lookup_to_plan.get(price.get("lookup_key") or "")
    if plan and price.get("id"):
        mapped[plan] = price["id"]

print(",".join(f"{plan}={mapped[plan]}" for plan in ("lite", "pro", "max") if plan in mapped))
PY
  )"
fi

if [[ -z "${PROJECT_ID}" || "${PROJECT_ID}" == "(unset)" ]]; then
  echo "PROJECT_ID is required. Set PROJECT_ID or SAGE_ROUTER_GCP_PROJECT_ID." >&2
  exit 2
fi

echo "Using Cloud Run project=${PROJECT_ID} region=${REGION} service=${SERVICE_NAME}" >&2

if [[ "${DEPLOY_FROM_GHCR_REMOTE}" == "1" || -n "${CLOUD_RUN_IMAGE}" || -n "${GHCR_IMAGE_DIGEST}" ]]; then
  gcloud services enable \
    run.googleapis.com \
    artifactregistry.googleapis.com \
    --project "${PROJECT_ID}"

  if [[ -z "${CLOUD_RUN_IMAGE}" ]]; then
    if ! gcloud artifacts repositories describe "${GHCR_REMOTE_REPOSITORY}" --location "${REGION}" --project "${PROJECT_ID}" >/dev/null 2>&1; then
      gcloud artifacts repositories create "${GHCR_REMOTE_REPOSITORY}" \
        --repository-format=docker \
        --mode=remote-repository \
        --remote-docker-repo="${GHCR_REMOTE_UPSTREAM}" \
        --location "${REGION}" \
        --description "GHCR remote cache for Sage Router images" \
        --project "${PROJECT_ID}"
    fi

    if [[ -n "${GHCR_IMAGE_DIGEST}" ]]; then
      digest="${GHCR_IMAGE_DIGEST}"
      if [[ "${digest}" != sha256:* ]]; then
        digest="sha256:${digest}"
      fi
      CLOUD_RUN_IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${GHCR_REMOTE_REPOSITORY}/${GHCR_IMAGE}@${digest}"
    else
      CLOUD_RUN_IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${GHCR_REMOTE_REPOSITORY}/${GHCR_IMAGE}:${GHCR_IMAGE_TAG}"
    fi
  fi

  echo "Updating ${SERVICE_NAME} to ${CLOUD_RUN_IMAGE}" >&2
  gcloud run services update "${SERVICE_NAME}" \
    --image "${CLOUD_RUN_IMAGE}" \
    --project "${PROJECT_ID}" \
    --region "${REGION}" \
    --platform managed

  gcloud run services describe "${SERVICE_NAME}" \
    --project "${PROJECT_ID}" \
    --region "${REGION}" \
    --format 'value(status.url)'
  exit 0
fi

IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPOSITORY}/${SERVICE_NAME}:${IMAGE_TAG}"

gcloud services enable \
  run.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  firestore.googleapis.com \
  --project "${PROJECT_ID}"

if ! gcloud artifacts repositories describe "${REPOSITORY}" --location "${REGION}" --project "${PROJECT_ID}" >/dev/null 2>&1; then
  gcloud artifacts repositories create "${REPOSITORY}" \
    --repository-format=docker \
    --location "${REGION}" \
    --description "Sage Router Cloud Run images" \
    --project "${PROJECT_ID}"
fi

BUILD_ID="$(
  gcloud builds submit . \
    --async \
    --project "${PROJECT_ID}" \
    --config deploy/gcp/cloudbuild.yaml \
    --substitutions _IMAGE="${IMAGE}" \
    --format 'value(id)'
)"

echo "Cloud Build started: ${BUILD_ID}"
while true; do
  BUILD_STATUS="$(gcloud builds describe "${BUILD_ID}" --project "${PROJECT_ID}" --format 'value(status)')"
  case "${BUILD_STATUS}" in
    SUCCESS)
      break
      ;;
    FAILURE|INTERNAL_ERROR|TIMEOUT|CANCELLED|EXPIRED)
      echo "Cloud Build ${BUILD_ID} ended with status ${BUILD_STATUS}" >&2
      exit 1
      ;;
    *)
      echo "Cloud Build status: ${BUILD_STATUS}"
      sleep 5
      ;;
  esac
done

gcloud run deploy "${SERVICE_NAME}" \
  --image "${IMAGE}" \
  --project "${PROJECT_ID}" \
  --region "${REGION}" \
  --platform managed \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 1 \
  --concurrency 20 \
  --timeout 300 \
  --set-env-vars '^|^SAGE_ROUTER_HOME=/app|SAGE_ROUTER_BUNDLED_OLLAMA_AUTOSTART=0|SAGE_ROUTER_OLLAMA_AUTO_PULL_PATTERNS=|SAGE_ROUTER_PROFILE_OVERLAYS=ollama|SAGE_ROUTER_MAX_PROVIDER_ATTEMPTS=10|SAGE_ROUTER_OLLAMA_TIMEOUT_SECONDS=120|SAGE_ROUTER_MAX_ACTIVE_API_KEYS_PER_CUSTOMER=5|SAGE_ROUTER_FIRESTORE_PROJECT_ID='"${PROJECT_ID}"'|SAGE_ROUTER_SUPABASE_URL=https://awtangrlqqsdpksarhwo.supabase.co|SAGE_ROUTER_SUPABASE_AUTH_ENABLED=1|SAGE_ROUTER_SUPABASE_MIRROR_ENABLED=1|SAGE_ROUTER_MODEL_MODALITIES_SHARED_ENABLED=1|SAGE_ROUTER_SUPABASE_MODEL_MODALITIES_RPC=sage_router_record_model_modalities|SAGE_ROUTER_CLIENT_AUTH_REQUIRED=1|SAGE_ROUTER_PUBLIC_BASE_URL='"${PUBLIC_BASE_URL}"'|SAGE_ROUTER_MARKETING_BASE_URL='"${MARKETING_BASE_URL}"'|SAGE_ROUTER_APP_BASE_URL='"${APP_BASE_URL}"'|SAGE_ROUTER_API_BASE_URL='"${API_BASE_URL}"'|SAGE_ROUTER_CORS_ORIGIN='"${CORS_ORIGIN}"'|SAGE_ROUTER_STRIPE_PRICE_IDS='"${STRIPE_PRICE_IDS}" \
  --set-secrets "OLLAMA_API_KEY=OLLAMA_API_KEY:latest,SAGE_ROUTER_OLLAMA_API_KEY=SAGE_ROUTER_OLLAMA_API_KEY:latest,SAGE_ROUTER_OPENAI_API_KEY=SAGE_ROUTER_OPENAI_API_KEY:latest,SAGE_ROUTER_OPENROUTER_API_KEY=SAGE_ROUTER_OPENROUTER_API_KEY:latest,SAGE_ROUTER_ANALYTICS_TOKEN=SAGE_ROUTER_ANALYTICS_TOKEN:latest,SAGE_ROUTER_SUPABASE_ANON_KEY=AOPS_SUPABASE_ANON_KEY:latest,SAGE_ROUTER_SUPABASE_SERVICE_ROLE_KEY=AOPS_SUPABASE_SERVICE_ROLE_KEY:latest,SAGE_ROUTER_CLIENT_API_KEYS=SAGE_ROUTER_CLIENT_API_KEYS:latest,SAGE_ROUTER_API_KEY_HASH_PEPPER=SAGE_ROUTER_API_KEY_HASH_PEPPER:latest,SAGE_ROUTER_SIGNING_SECRET=SAGE_ROUTER_API_KEY_HASH_PEPPER:latest,SAGE_ROUTER_STRIPE_SECRET_KEY=SAGE_ROUTER_STRIPE_SECRET_KEY:latest,SAGE_ROUTER_STRIPE_WEBHOOK_SECRET=SAGE_ROUTER_STRIPE_WEBHOOK_SECRET:latest,NVIDIA_API_KEY=NVIDIA_API_KEY:latest,SAGE_ROUTER_NVIDIA_API_KEY=NVIDIA_API_KEY:latest$(optional_activation_email_secret_bindings)"

gcloud run services describe "${SERVICE_NAME}" \
  --project "${PROJECT_ID}" \
  --region "${REGION}" \
  --format 'value(status.url)'
