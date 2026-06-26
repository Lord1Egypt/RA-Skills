# Auth and Access - Shelly BluTRV

Use this guide to keep local control, cloud fallback, and credentials aligned with the intended scope of this skill.

## Access Model

- Local control:
  - Preferred for BluTRV status checks and target temperature changes.
  - Uses Shelly gateway RPC on the local network.

- Cloud fallback:
  - Used only when local status retrieval fails or when supported WiFi sensor data is needed.
  - Not the preferred source of truth when the local gateway is reachable.

## Credential Handling

- Store Shelly variables only in `~/.openclaw/skills/.shelly-blutrv-manager.env`.
- Never store cloud tokens in the repository.
- Never paste production tokens into chat logs or notes.
- Restrict the local env file with `chmod 600`.

## Safety Rules

1. Prefer local reads before any write.
2. Use cloud access only for the documented fallback path.
3. Verify target identity before every write:
   gateway, `trv_id`, and `trv_device_id` must match the intended target.
4. Treat write acknowledgment as incomplete until post-write verification succeeds.
5. Stop on identity mismatches or repeated cloud authentication failures.

## Operational Scope

- This published skill is intentionally limited to:
  - local RPC status reads
  - local RPC target temperature changes
  - cloud status fallback

- It does not include experimental WebSocket write tooling in the published package.
