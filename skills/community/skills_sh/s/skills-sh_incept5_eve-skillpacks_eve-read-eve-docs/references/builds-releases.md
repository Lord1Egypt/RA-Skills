# Builds + Releases (Current)

## Use When
- You need to understand build/run semantics and output artifacts.
- You need to debug build or release failures.
- You need commands for deterministic deploy pipelines and image promotion.

## Load Next
- `references/pipelines-workflows.md` for build/release/deploy pipeline flow.
- `references/cli.md` for inspect and execute build/release commands.
- `references/manifest.md` for image/input and service build configuration.

## Ask If Missing
- Confirm target `project`, `environment`, and pipeline/branch context.
- Confirm manifest build entries and target services.
- Confirm which artifact (image digest, build/run id, or release id) you need to inspect.

## Build Model

Builds are first-class primitives that track container image construction. The model is three-tier:

```
BuildSpec (immutable input) -> BuildRun (execution) -> BuildArtifact (output)
```

### BuildSpec

Created once per unique build configuration. Immutable.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | `bld_xxx` |
| `project_id` | string | Owning project |
| `git_sha` | string | 40-char commit SHA |
| `manifest_hash` | string | Hash of manifest at build time |
| `services` | string[]? | Service names to build (null = all) |
| `inputs` | object? | Additional build inputs |
| `registry` | object? | Registry configuration override |
| `cache` | object? | Cache configuration |
| `created_by` | string? | User/system that created the build |

### BuildRun

Execution instance of a build. Multiple runs can exist per spec (retries).

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Run identifier |
| `build_id` | string | Parent BuildSpec |
| `status` | enum | `pending` -> `building` -> `completed` / `failed` / `cancelled` |
| `backend` | string | `buildkit` (K8s), `buildx` (local), `kaniko` (fallback) |
| `runner_ref` | string? | Pod/runner name |
| `logs_ref` | string? | Log storage reference |
| `error_message` | string? | Failure reason |

### BuildArtifact

Output images from a successful build.

| Field | Type | Description |
|-------|------|-------------|
| `service_name` | string | Which service was built |
| `image_ref` | string | Full image reference (e.g., `registry.eve.example.com/org/api`) |
| `digest` | string | `sha256:...` content digest |
| `platforms` | string[]? | e.g., `["linux/amd64", "linux/arm64"]` |
| `size_bytes` | number? | Image size |

## Build CLI

| Command | Description |
|---------|-------------|
| `eve build list [--project <id>]` | List build specs |
| `eve build show <build_id>` | Build spec details |
| `eve build create --project <id> --ref <sha> --manifest-hash <hash> [--services s1,s2] [--repo-dir <path>]` | Create a build spec |
| `eve build run <build_id>` | Start a build run |
| `eve build runs <build_id>` | List runs for a build |
| `eve build logs <build_id> [--run <id>] [--follow]` | View build logs |
| `eve build artifacts <build_id>` | List image artifacts (digests) |
| `eve build diagnose <build_id>` | Full diagnostic dump (spec + runs + artifacts + last 30 lines) |
| `eve build cancel <build_id>` | Cancel active build |

Builds happen automatically in pipeline `build` steps. Use `eve build diagnose` to debug failures.

### Build Error Classification

| Error Code | Cause | Fix |
|-----------|-------|-----|
| `auth_error` | Registry or git authentication failure | Check registry credentials |
| `clone_error` | Git clone failure | Verify repo URL and GITHUB_TOKEN |
| `build_error` | Dockerfile build step failure | Check build logs for failing stage |
| `timeout_error` | Execution timeout | Increase timeout or optimize build |
| `resource_error` | Resource exhaustion (disk, memory) | Check pod resources |
| `registry_error` | Registry push failure | Verify registry auth and namespace |

### Pre-Build Visibility

Clone, checkout, and workspace preparation phases produce observable log entries. These are visible through `eve build logs` and `eve job diagnose`, providing full traceability from the moment a build begins -- not just from the Dockerfile execution phase.

### BuildKit Failure Output

Build failures include the last 30 lines of buildkit output and identify the failed Dockerfile stage:

```
Error: buildctl failed with exit code 1 at [build 3/5] RUN pnpm install
--- Last 12 lines ---
#8 [build 3/5] RUN pnpm install --frozen-lockfile
#8 ERROR: process "pnpm install --frozen-lockfile" did not complete successfully
...
```

## Container Registry

### Manifest Registry Configuration

For most Eve apps, configure the managed default in `.eve/manifest.yaml`:

```yaml
registry: "eve"
```

Use `registry: "eve"` for standard managed images and built-in auth.

For BYO/private registries, use full object config:

```yaml
registry:
  host: public.ecr.aws/w7c4v0w3
  namespace: myorg
  auth:
    username_secret: REGISTRY_USERNAME    # Secret key for registry username
    token_secret: REGISTRY_PASSWORD       # Secret key for registry token/password
```

- `host`: container registry hostname (for example, `public.ecr.aws/w7c4v0w3`, `docker.io`)
- `namespace`: registry namespace/organization
- `auth.username_secret`: name of the secret containing the registry username (defaults to `REGISTRY_USERNAME`)
- `auth.token_secret`: name of the secret containing the registry token/password (defaults to `REGISTRY_PASSWORD`)

### String Modes

```yaml
registry: "eve"   # Use Eve-native registry (internal JWT-based auth)
registry: "none"  # Skip registry handling (public images or external auth)
```

When `registry: "eve"`, the worker requests a short-lived JWT from the internal
API (`POST /internal/registry/token`) using `EVE_INTERNAL_API_KEY`.  
When using a BYO registry object, credentials are read from secrets and used to build image push/pull auth.

BuildKit registry transport controls:
- `EVE_BUILDKIT_INSECURE_REGISTRIES` (optional): comma-separated hosts that must use insecure/plain-HTTP registry transport.
- `EVE_BUILDKIT_INSECURE_ALL=true` (optional, local troubleshooting only): force insecure registry transport for all BuildKit registry ops.

### Required Secrets (BYO Registry only)

For private BYO registries, set these secrets:

```bash
eve secrets set REGISTRY_USERNAME your-registry-username
eve secrets set REGISTRY_PASSWORD your-registry-token
```

Token requirements:
Use credentials required by your registry provider for image push/pull workflows.

### Deployer ImagePullSecret

When deploying to Kubernetes, the deployer automatically creates an `imagePullSecret` for BYO registries with a `registry.host`:

1. Resolves `username_secret` and `token_secret` from the secrets system.
2. Creates a Docker config JSON with registry auth.
3. Creates/updates a Kubernetes Secret of type `kubernetes.io/dockerconfigjson`.
4. Attaches the secret to the deployment's `imagePullSecrets`.

If `registry` is `"eve"` or `"none"`, no imagePullSecret is needed/created (the managed registry uses platform auth; `"none"` assumes public images or pre-configured cluster auth).

### Image Name Auto-Derivation

When a service has `build` config and a `registry` is configured (`"eve"` or `{ host: ... }`), the `image` field is optional. The platform derives the image name from the service key:

```yaml
# image is auto-derived as "api" from the service key
services:
  api:
    build:
      context: ./apps/api
```

The derived name is prefixed with the registry host at build time (e.g., `registry.eve.example.com/api:sha-abc123`). You can still set `image` explicitly to override the default.

### Zero-Artifact Build Failure

Builds that discover services with `build` config but produce zero buildable artifacts now **fail with guidance** instead of silently succeeding. This catches common misconfigurations:
- Missing `Dockerfile` in the build context
- `build.context` pointing to a non-existent directory
- Services with `build` config but no actual build output

The error message identifies which services were expected to build and suggests corrective action.

### Service Image Tags

Services can specify their full image path without a tag:

```yaml
services:
  api:
    image: registry.eve.example.com/myorg/my-project-api
    build:
      context: ./apps/api
```

The tag is determined by the workflow:
- Local dev: `:local`
- Pipeline builds: Git SHA or version (`:sha-abc123`, `:v1.0.0`)

## Local Dev Workflow (k3d)

For fast iteration without pushing to a remote registry:

```bash
# Build with :local tag
docker build -t registry.eve.example.com/myorg/my-project-api:local ./apps/api

# Import directly into k3d cluster (no push/pull roundtrip)
k3d image import registry.eve.example.com/myorg/my-project-api:local -c eve-local

# Deploy
eve env deploy test --ref main --repo-dir .
```

This avoids the push/pull roundtrip to the registry, making local iteration much faster. Use this pattern when developing and testing deployment configuration before committing to a full pipeline run.

### Build Reuse Fast Path

Build actions reuse the most recent successful build artifacts when these match:
- `project_id`
- `git_sha`
- `manifest_hash`
- requested services/components

This speeds up repeated local deploy loops (same ref, same manifest). Controls:
- Per-run: action input `force_rebuild: true`
- Global: `EVE_BUILD_REUSE=false` in worker env

## Release Model

Releases capture a deployable snapshot: git SHA + manifest hash + image digests.

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | `rel_xxx` |
| `project_id` | string | Owning project |
| `git_sha` | string | 40-char commit SHA |
| `manifest_hash` | string | Hash of manifest |
| `image_digests` | object? | `{ "api": "sha256:...", "web": "sha256:..." }` |
| `build_id` | string? | Source build (if from pipeline) |
| `version` | string? | Semantic version |
| `tag` | string? | Release tag (e.g., `v1.0.0`) |

### Release CLI

```bash
eve release resolve <tag> [--project <id>]    # Resolve release by tag
```

Releases are typically created automatically by pipeline `release` steps.

## Deploy Model

Deploy requests can use a release tag or raw SHA + manifest hash.

```bash
# Deploy via pipeline (recommended)
eve env deploy staging --ref main --repo-dir ./my-app

# Deploy with specific release
eve env deploy staging --inputs '{"release_tag": "v1.0.0"}'

# Direct deploy (bypass pipeline)
eve env deploy staging --ref <sha> --direct

# Deploy with pre-built images
eve env deploy staging --ref <sha> --direct --image-tag sha-abc123
```

### Deploy Request Fields

| Field | Description |
|-------|-------------|
| `git_sha` | 40-char SHA (required unless `release_tag`) |
| `manifest_hash` | Manifest hash (required with `git_sha`) |
| `release_tag` | Resolve from existing release (alternative to sha+hash) |
| `image_digests` | Service -> digest map (skips build) |
| `image_tag` | Tag for pre-built images (e.g., `local`, `sha-abc123`) |
| `direct` | Bypass pipeline, deploy directly |
| `inputs` | Additional pipeline inputs |

## Canonical Pipeline: Build -> Release -> Deploy

The standard deployment pipeline:

```yaml
pipelines:
  deploy:
    trigger:
      github:
        event: push
        branch: main
    steps:
      - name: build
        action: { type: build }
        # Creates BuildSpec + BuildRun, outputs build_id + image_digests

      - name: release
        depends_on: [build]
        action: { type: release }
        # Creates Release from BuildArtifacts (digest-based image refs)

      - name: deploy
        depends_on: [release]
        action: { type: deploy, env_name: staging }
        # Deploys release to environment
```

### Promotion Pattern

1. Deploy to test -- creates release with tag.
2. Resolve release: `eve release resolve v1.0.0`
3. Deploy to staging: `eve env deploy staging --inputs '{"release_tag": "v1.0.0"}'`

## Build Backends

| Backend | Environment | Notes |
|---------|-------------|-------|
| BuildKit | K8s (production) | Runs as K8s job, recommended |
| Buildx | Local development | Uses local Docker |
| Kaniko | K8s (fallback) | No Docker daemon required |

## Validation and Errors

- `manifest_hash` must match the synced manifest for the project ref.
- Releases require a valid `build_id` that exists for the project.
- Mismatches surface explicit errors; re-run build or re-sync the manifest.

## Cleaning Up Builds and Releases

```bash
eve build delete <build_id>
eve build prune --project <id> --keep 10

eve release delete <tag> --project <id>
eve release prune --project <id> --keep 5
```

## API Endpoints

```
POST /projects/{project_id}/builds              # Create build spec
GET  /projects/{project_id}/builds              # List builds
GET  /builds/{build_id}                          # Get build spec
POST /builds/{build_id}/runs                     # Start build run
GET  /builds/{build_id}/runs                     # List runs
GET  /builds/{build_id}/artifacts                # List artifacts
GET  /builds/{build_id}/logs                     # View logs
POST /builds/{build_id}/cancel                   # Cancel build

POST /projects/{project_id}/releases             # Create release
GET  /projects/{project_id}/releases             # List releases
GET  /releases/{tag}                              # Resolve by tag

POST /projects/{project_id}/environments/{env}/deploy  # Deploy
```
