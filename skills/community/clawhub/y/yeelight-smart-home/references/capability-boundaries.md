# Capability Boundaries

Use this reference when the user asks why a capability is unavailable, whether a known cloud action should be enabled, or how to handle risky operations.

## Core Boundary

- The Skill exposes Runtime intents through the local `yeelight-home` CLI, not bypass requests.
- A known historical action name is not executable until Runtime exposes reviewed support, validation, verification, and tests.
- Non-enabled actions are not missing by default; they may be manual guidance, owner-review blocked, app-only, credential-blocked, LAN-only, or unsupported by the current Runtime surface.
- If Runtime returns a block, keep the block. Do not work around it with internal endpoints, guessed payloads, or external tool servers.

## Block Classes

| Class | Skill behavior |
| --- | --- |
| Owner review missing | Keep as plan, explanation, or blocked result until Runtime support and tests exist. |
| App, QR, BLE, or pairing required | Provide Runtime-returned app or manual guidance; do not simulate pairing. |
| LAN or local discovery required | Explain that current cloud Runtime path cannot execute it. |
| Credential-sensitive | Block or redirect to local/official authorization; never ask for secrets in chat. |
| Caller confirmation required | For destructive or permission-sensitive operations, get explicit agreement in conversation before the Runtime call. |
| Unsafe write evidence missing | Keep disabled until safe fixtures and write-after-read evidence exist. |

## Risk Lanes

- R0 read-only: no confirmation.
- R1 reversible temporary control: allowed only when Runtime resolves the target and validates capability.
- R2 persistent configuration: use direct Runtime execution after normal target validation. Use dry-run first only when a preview is useful.
- R2 reviewed delete: `favorite.delete`, `favorite.batch_delete`, and single-target or capped batch delete for room, area, group, scene, and automation are direct Runtime executions after explicit user request and target resolution.
- R3 high-impact operation: ask for explicit chat confirmation first, then call the Runtime intent directly. Current reviewed examples include home delete, gateway delete, device delete/remove, device unbind, member removal, home ownership transfer, and leaving a shared home.
- R4 destructive, account-sensitive, or irreversible action: not supported by the Skill path.

## Explicit Non-Enable Rules

- Do not enable every known historical action name as a Skill capability.
- Do not enable account, login, third-party authorization, token, QR, onboarding, or transfer flows as ordinary Skill execution.
- Do not enable unreviewed batch delete, factory reset, broad member changes, or large bulk operations without Runtime support.
- `device.remove`, `device.unbind`, `gateway.delete`, `home.delete`, `home.member.remove`, `home.member.transfer`, and `home.member.quit` are reviewed R3 Runtime intents. Confirm intent in chat first, then call Runtime directly.
- `home.member.invite`, `home.member.accept_share`, `home.member.configure`, and `gateway.configure` are reviewed Runtime intents and must not be replaced with unreviewed share, role, or gateway requests. Accept-share uses the current local account as recipient; never pass or infer another user's uid.
- Do not use static product names, room names, or marketing names as proof of writable capability.
- Do not treat design, commercial platform, hub internals, internal schema, panel layout, storage, or voice configuration material as user-safe execution unless Runtime exposes reviewed support.
