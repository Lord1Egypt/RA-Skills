---
name: runpod-compute
description: RunPod API integration with API key authentication. Create and manage GPU clusters, serverless endpoints, templates, and secrets for ML inference and distributed computing workloads.
---

# RunPod

![RunPod](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/brand-logos/runpod.webp)

Deploy and manage GPU-accelerated compute infrastructure on RunPod. Create clusters, configure serverless endpoints, manage templates, and handle secrets for ML training, inference, and distributed computing workloads.

This skill uses [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=runpod-compute) for hosted connection flows and credentials so you do not need to configure RunPod API access yourself.

### Setup in 3 Steps

| Step 1: Install | Step 2: Pair Account | Step 3: Connect RunPod |
|:---:|:---:|:---:|
| ![Install](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/pairing/initialstep_1.gif) | ![Pair](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/approve_process.gif) | *App-specific connection GIF coming soon* |
| Run the install command in OpenClaw | Sign in and approve the device | Open the dashboard and connect RunPod |

## How It Works

```
┌─────────────────┐     ┌──────────────┐     ┌──────────────────┐
│   OpenClaw      │────▶│   ClawLink   │────▶│    RunPod API    │
│   (User Chat)   │     │   (Proxy)    │     │   (Clusters,     │
│                 │     │              │     │  Endpoints)      │
└─────────────────┘     └──────────────┘     └──────────────────┘
         │                    │                      │
         │  1. Install Plugin │                      │
         │  2. Pair Device    │                      │
         │  3. Connect RunPod  │                      │
         │                    │  4. API Key Proxy     │
         │                    │  5. Request Forward   │
         │                    │                      │
         ▼                    ▼                      ▼
   ┌──────────┐        ┌──────────┐         ┌──────────┐
   │   SKILL  │        │ Dashboard│         │  RunPod  │
   │   File   │        │   Auth   │         │  Cloud   │
   └──────────┘        └──────────┘         └──────────┘
```

## Install

Install the verified ClawLink plugin from ClawHub. After the user confirms, complete the full setup so ClawLink tools are visible in the next OpenClaw chat.

```bash
openclaw plugins install clawhub:clawlink-plugin
openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
openclaw gateway restart
```

Then tell the user: "OpenClaw has been restarted. Send `/new` as a standalone message to start a fresh chat, then ask for RunPod again."

## Quick Start

```bash
# List available GPU types
clawlink_call_tool --tool "runpod_get_gpu_types"

# Get current user info
clawlink_call_tool --tool "runpod_get_myself"

# Get pod details
clawlink_call_tool --tool "runpod_get_pod" --params '{"pod_id": "YOUR_POD_ID"}'
```

## Authentication

All RunPod tool calls are authenticated automatically by ClawLink using your RunPod API key stored securely in the dashboard.

**No API key is required in chat.** ClawLink injects your API key into every RunPod GraphQL request on your behalf.

### Getting Connected

1. Install the ClawLink plugin (see Install above).
2. Pair the plugin with `clawlink_begin_pairing` if it is not configured yet.
3. Open https://claw-link.dev/dashboard?add=runpod and connect RunPod with your API key.
4. Call `clawlink_list_integrations` to verify the connection is active.

## Connection Management

### List Connections

```bash
clawlink_list_integrations
```

**Response:** Returns all connected integrations. Look for `runpod` in the list.

### Verify Connection

```bash
clawlink_list_tools --integration runpod
```

**Response:** Returns the live tool catalog for RunPod.

### Reconnect

If RunPod tools are missing or the connection shows an error:

1. Direct the user to https://claw-link.dev/dashboard?add=runpod
2. After they confirm, call `clawlink_list_integrations` to verify
3. Then call `clawlink_list_tools --integration runpod`

## Security & Permissions

- Access is scoped to the RunPod account associated with the connected API key.
- **All write operations require explicit user confirmation.** Before executing any create, update, or delete call, confirm the target resource and intended effect with the user.
- Destructive actions (delete template, delete registry auth) are marked as high-impact and must be confirmed.
- Secrets are stored securely and injected as environment variables (`RUNPOD_SECRET_<name>`) in pods and endpoints.

## Tool Reference

### Compute & GPU Operations

| Tool | Description | Mode |
|------|-------------|------|
| `runpod_get_gpu_types` | Retrieve available GPU types, specs, pricing, and availability | Read |
| `runpod_list_cpu_types` | Retrieve available CPU types and specifications | Read |
| `runpod_get_pod` | Get details of a specific pod by ID (GPU count, memory, cost, status) | Read |

### Cluster Management

| Tool | Description | Mode |
|------|-------------|------|
| `runpod_create_cluster` | Create a new GPU cluster for multi-node distributed computing workloads | Write |

### Serverless Endpoints

| Tool | Description | Mode |
|------|-------------|------|
| `runpod_save_endpoint` | Create or update a GPU-accelerated serverless endpoint (include `id` to update, omit to create) | Write |

### Template Management

| Tool | Description | Mode |
|------|-------------|------|
| `runpod_save_template` | Create a new template or update an existing one with container configuration | Write |
| `runpod_delete_template` | Remove a template (must not be in use by pods or serverless endpoints) | Write |

### Secrets Management

| Tool | Description | Mode |
|------|-------------|------|
| `runpod_create_secret` | Create a secure secret for credential management (accessible as `RUNPOD_SECRET_<name>`) | Write |

### Registry Authentication

| Tool | Description | Mode |
|------|-------------|------|
| `runpod_save_registry_auth` | Save container registry authentication credentials for private Docker images | Write |
| `runpod_update_registry_auth` | Update existing container registry authentication credentials | Write |
| `runpod_delete_registry_auth` | Delete container registry authentication from RunPod | Write |

### User Settings

| Tool | Description | Mode |
|------|-------------|------|
| `runpod_get_myself` | Retrieve authenticated user info (ID, email, MFA settings) | Read |
| `runpod_update_user_settings` | Update user settings (e.g., SSH public key for pod access) | Write |

## Code Examples

### List available GPU types

```bash
clawlink_call_tool --tool "runpod_get_gpu_types"
```

### Get pod details

```bash
clawlink_call_tool --tool "runpod_get_pod" \
  --params '{"pod_id": "YOUR_POD_ID"}'
```

### Create a secret

```bash
clawlink_call_tool --tool "runpod_create_secret" \
  --params '{"name": "OPENAI_API_KEY", "value": "sk-..."}'
```

### Save a serverless endpoint

```bash
clawlink_call_tool --tool "runpod_save_endpoint" \
  --params '{
    "name": "my-endpoint",
    "gpu_type_id": "RTX_4090",
    "image_url": "your-docker-image:latest",
    "env": [{"key": "MODEL_PATH", "value": "/models/llama"}]
  }'
```

## Discovery Workflow

1. Call `clawlink_list_integrations` to confirm RunPod is connected.
2. Call `clawlink_list_tools --integration runpod` to see the live catalog.
3. Treat the returned list as the source of truth. Do not guess or assume what tools exist.
4. If the user describes a capability but the exact tool is unclear, call `clawlink_search_tools` with a short query and integration `runpod`.
5. If no RunPod tools appear, direct the user to https://claw-link.dev/dashboard?add=runpod.

## Execution Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  READ OPERATIONS (Safe)                                     │
│  list → get → describe → call                                │
│                                                             │
│  Example: List GPU types → Get pod details → Show results   │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  WRITE OPERATIONS (Require Confirmation)                    │
│  describe → preview → confirm → call                        │
│                                                             │
│  Example: Describe tool → Preview changes → User approves    │
│           → Execute create                                   │
└─────────────────────────────────────────────────────────────┘
```

1. For unfamiliar tools, ambiguous requests, or any write action, call `clawlink_describe_tool` first.
2. Use the returned guidance, schema, `whenToUse`, `askBefore`, `safeDefaults`, `examples`, and `followups` to shape the call.
3. Prefer read, list, and get operations before writes when that reduces ambiguity.
4. For writes or anything marked as requiring confirmation, call `clawlink_preview_tool` first.
5. Execute with `clawlink_call_tool`. Pass confirmation only after the preview matches the user's intent.
6. If the tool call fails, report the real error. Do not invent results or restate the failure as a missing capability unless the live catalog supports that conclusion.

## Notes

- GPU types and pricing change frequently — always call `runpod_get_gpu_types` to get current availability before deploying.
- Serverless templates must set `volumeInGb` to `0` (no persistent storage for serverless).
- Pods and endpoints reference secrets via `RUNPOD_SECRET_<name>` environment variables — create secrets before referencing them in templates.
- Templates must not be in use when deleted — reassign or remove affected pods/endpoints first.
- API key must have sufficient permissions for cluster and endpoint operations.

## Error Handling

| Status / Error | Meaning |
|----------------|---------|
| Tool not found | The tool name does not exist in the current catalog. Verify with `clawlink_list_tools --integration runpod`. |
| Missing connection | RunPod is not connected. Direct the user to https://claw-link.dev/dashboard?add=runpod. |
| `template_in_use` | Template is assigned to active pods or endpoints. Reassign or delete them first. |
| `invalid_gpu_type` | The specified GPU type is not available in the selected region. Check `runpod_get_gpu_types`. |
| `permission_denied` | API key lacks required permissions for the operation. |
| Write rejected | User did not confirm a write action. Always confirm before executing writes. |

### Troubleshooting: Tools Not Visible

1. Check that the ClawLink plugin is installed:
   ```bash
   openclaw plugins list
   ```
2. If the plugin is installed but tools are missing, tell the user to send `/new` as a standalone message to reload the catalog.
3. If a fresh chat does not help, run:
   ```bash
   openclaw config set tools.alsoAllow '["clawlink-plugin"]' --strict-json
   openclaw gateway restart
   ```
4. After restart, tell the user to send `/new` again and retry.

### Troubleshooting: Invalid Tool Call

1. Ensure the integration slug is exactly `runpod`.
2. Use `clawlink_describe_tool` to verify parameter names and types before calling.
3. For write operations, always call `clawlink_preview_tool` first.

## Resources

- [RunPod API Documentation](https://docs.runpod.io)
- [GPU Cloud Pods](https://docs.runpod.io/pods)
- [Serverless Endpoints](https://docs.runpod.io/serverless-endpoints)
- [Templates](https://docs.runpod.io/templates)
- [Secrets Management](https://docs.runpod.io/secrets)
- ClawLink: https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=runpod-compute
- ClawLink Docs: https://docs.claw-link.dev/openclaw
- ClawLink Verification: https://claw-link.dev/verify

## Related Skills

- [Google Cloud Compute](https://clawhub.ai/hith3sh/google-cloud-compute) — For GCP compute engine management
- [AWS EC2](https://clawhub.ai/hith3sh/aws-ec2-instances) — For AWS EC2 instance management

---

**Powered by [ClawLink](https://claw-link.dev/?utm_source=clawhub&utm_medium=referral&utm_content=runpod-compute)** — an integration hub for OpenClaw

![ClawLink Logo](https://raw.githubusercontent.com/ClawLink-HQ/clawlink/main/public/images/logo/link_logo_black_small.png)