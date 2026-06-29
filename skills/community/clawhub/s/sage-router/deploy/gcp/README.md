# Sage Router on GCP Free-Tier-Style Cloud Run

This deployment is for a public Phase 2 demo of Sage Router on Google Cloud Run.

## Cost posture

- Cloud Run: `min-instances=0`, `max-instances=1`, 512Mi memory.
- No provider/customer API keys are deployed by default.
- Dario is bundled for Anthropic-compatible routing, but is not authenticated unless credentials are supplied via Secret Manager or a private runtime config.
- Ollama is bundled and started without local models so users can route to Ollama Cloud when they provide their own Ollama auth/config.
- Artifact Registry stores one small Python image.
- The service is public for demoability and exposes `/health`, but hosted
  deployments with `SAGE_ROUTER_CLIENT_AUTH_REQUIRED=1` must still block
  anonymous model, setup, admin, discovery, and dashboard config routes at the
  origin. Treat the public edge as the customer API surface, not as the only
  auth gate.


## Live Phase 2 deployment

- Project: `sage-router-demo-20260428`
- Region: `us-central1`
- Service: `sage-router`
- URL: discover with `gcloud run services describe sage-router --project sage-router-demo-20260428 --region us-central1 --format 'value(status.url)'`
- Public API DNS: `https://api.sagerouter.dev`
- Verified endpoints: `/`, `/health`, authenticated `/v1/models`
- Runtime boundary: Dario binary and Ollama daemon are present. Dario requires user-provided auth before Anthropic-compatible provider traffic can use it. Ollama requires user-provided Ollama Cloud auth/config for cloud inference; no local model weights are bundled.

## Deploy

The script defaults to the live hosted project, `sage-router-demo-20260428`.
Set `PROJECT_ID` only when intentionally deploying a separate environment.

For the hosted service, prefer updating Cloud Run to a GitHub release image
through the Artifact Registry GHCR remote cache. This preserves the existing
Cloud Run environment variables and Secret Manager bindings instead of
rebuilding and redeploying the full service configuration:

```bash
DEPLOY_FROM_GHCR_REMOTE=1 \
GHCR_IMAGE_DIGEST=sha256:... \
./deploy/gcp/cloudrun-deploy.sh
```

For the combined public release flow, use:

```bash
GHCR_IMAGE_DIGEST=sha256:... scripts/deploy_sagerouter_public.sh
```

That path deploys Cloudflare Pages production branch `main`, updates Cloud Run
by immutable image digest when a digest is supplied, and reruns the hosted launch
readiness gate. If `SAGEROUTER_DEPLOY_CLOUD_RUN=1` is set without a digest, it
resolves the latest successful GitHub Actions `Release image` digest from the
run log instead of trusting the mutable `latest` tag.

### Activation follow-up email sender

Signup-to-key recovery can send private operator follow-ups through Resend once
the sender is configured. Store sender values in Secret Manager and bind them to
Cloud Run with:

```bash
SAGE_ROUTER_ACTIVATION_EMAIL_FROM='Sage Router <activation@sagerouter.dev>' \
SAGE_ROUTER_RESEND_API_KEY='re_...' \
SAGE_ROUTER_ACTIVATION_EMAIL_REPLY_TO='support@sagerouter.dev' \
scripts/configure_activation_email_sender.sh
```

The script never prints secret values. It updates these runtime variables:

- `SAGE_ROUTER_ACTIVATION_EMAIL_PROVIDER=resend`
- `SAGE_ROUTER_ACTIVATION_EMAIL_FROM` from Secret Manager
- `SAGE_ROUTER_RESEND_API_KEY` from Secret Manager
- optional `SAGE_ROUTER_ACTIVATION_EMAIL_REPLY_TO` from Secret Manager
- `SAGE_ROUTER_ACTIVATION_EMAIL_MAX_BATCH`

Afterward, `/analytics/funnel` should report
`activationFollowUps.emailReadiness.configured=true`; use a dry run from the
operator dashboard before sending a real batch. Full source-built Cloud Run
deploys preserve these bindings automatically when the corresponding Secret
Manager secrets exist.

Defaults for that path:

- Project: `sage-router-demo-20260428`
- Region: `us-central1`
- Service: `sage-router`
- Artifact Registry remote repo: `ghcr-remote`
- Upstream: `https://ghcr.io`
- Image: `earlvanze/sage-router-public`

You can also pass an exact image path when recovering or rolling back:

```bash
CLOUD_RUN_IMAGE=us-central1-docker.pkg.dev/sage-router-demo-20260428/ghcr-remote/earlvanze/sage-router-public@sha256:... \
./deploy/gcp/cloudrun-deploy.sh
```

For a source build into a project-local Artifact Registry image:

```bash
export REGION=us-central1
./deploy/gcp/cloudrun-deploy.sh
```

The script enables required APIs, creates an Artifact Registry Docker repo if needed, builds the minimal Cloud Run image, deploys the service, and prints the Cloud Run URL.

## Verify

```bash
SERVICE_URL=$(gcloud run services describe sage-router --project sage-router-demo-20260428 --region us-central1 --format 'value(status.url)')
curl "$SERVICE_URL/health"
curl -i "$SERVICE_URL/v1/models"      # expect 401 without an operator/customer token
curl -i "$SERVICE_URL/setup/state"    # expect 401 without an operator token
```

The `tech-mvp` OpenClaw agent used Sage Router as a frontier profile with an OpenAI-compatible config like:

```json
{
  "baseUrl": "http://localhost:8790/v1",
  "apiKey": "local",
  "api": "openai-completions",
  "models": [
    { "id": "auto", "name": "Sage Router" },
    { "id": "frontier", "name": "Sage Router Frontier" }
  ]
}
```

Use that pattern as a harness-agnostic smoke test: point an agent at `/v1`, select `frontier`, and verify `/health`, `/v1/models`, and one small chat completion before promoting DNS or a new container image.

## Recover existing infrastructure

`api.sagerouter.dev` is already wired to a Google-hosted service. Before changing Cloudflare DNS or replacing the service, authenticate `gcloud` and inspect the known project:

```bash
gcloud auth login
gcloud config set project sage-router-demo-20260428
gcloud run services list --region us-central1
gcloud run services describe sage-router --region us-central1
gcloud run domain-mappings list --region us-central1
gcloud app domain-mappings list
```

Cloudflare Pages remains the static site for `sagerouter.dev`; do not deploy router runtime config or provider credentials to Pages.

## Boundary

Do not deploy local OpenClaw configs, customer provider credentials, `.env` files, Dario credentials, or OAuth cookies to Cloud Run. This Phase 2 deployment is a public demo / credibility deployment, not a hosted customer key-custody layer.
