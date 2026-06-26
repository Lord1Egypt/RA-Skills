# Shelly Access and Authentication

Use this guide to keep access mode and credential handling coherent.

## Access Modes

- Local network control:
  - Communicate directly with device RPC endpoints.
  - Best for low-latency state reads and immediate control.

- Cloud control:
  - Use account-scoped API flows with cloud token handling.
  - Best for remote access and centralized fleet operations.

- Mixed mode:
  - Combine local for fast state operations and cloud for remote orchestration.
  - Requires explicit precedence rules to prevent conflicting writes.

## Credential Handling

- Use `SHELLY_CLOUD_TOKEN` only from environment variables.
- Do not store raw token values in `~/shelly/` notes.
- Rotate and scope credentials to least-privilege operations where possible.

## Policy Rules

1. Prefer read-only discovery before any write operation.
2. Require explicit approval for high-impact actions.
3. Re-authenticate or refresh context after repeated unauthorized responses.
4. If cloud and local identities diverge, resolve identity mapping before commands.

## Practical Safeguards

- Validate target device identity before every write.
- Keep local and cloud device references in one mapping table.
- Stop rollout immediately on authentication drift or repeated permission errors.
