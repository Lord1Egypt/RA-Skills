# Capability Boundaries

Use this reference when the user asks why a capability is unavailable, whether a known cloud action should be enabled, or how to handle risky operations.

## Core Boundary

- The Skill exposes semantic intents through the local Runtime, not raw API fan-out.
- A known API or historical action name is not executable until Runtime has a reviewed adapter, validation, verification, and tests.
- Non-enabled actions are not missing by default; they may be plan-only, manual guidance, owner-review blocked, app-only, credential-blocked, LAN-only, or local-approval blocked.
- If Runtime returns a block, keep the block. Do not work around it with raw HTTP, guessed payloads, external tool servers, or compatibility projects.

## Block Classes

| Class | Skill behavior |
| --- | --- |
| Owner review missing | Keep as plan, explanation, or blocked result until adapter semantics and tests exist. |
| App, QR, BLE, or pairing required | Provide Runtime-returned app or manual guidance; do not simulate pairing. |
| LAN or local discovery required | Explain that current cloud Runtime path cannot execute it. |
| Credential-sensitive | Block or redirect to local/official authorization; never ask for secrets in chat. |
| Local approve required | Follow Runtime-returned `approveCommand` only for reviewed R3 plans. Ordinary chat confirmation, guessed challenge text, or raw API calls are not approval. |
| Unsafe write evidence missing | Keep disabled until safe fixtures and write-after-read evidence exist. |

## Risk Lanes

- R0 read-only: no confirmation.
- R1 reversible temporary control: allowed only when Runtime resolves the target and validates capability.
- R2 persistent configuration: must create a pending plan and commit only by `planId`; this includes whole-home reset lock/unlock and capped device/scene batch rename.
- R2 reviewed delete: `favorite.delete`, `favorite.batch_delete`, and single-target or capped batch delete for room, area, group, scene, and automation use pending-plan confirmation and write-after-read verification.
- R3 high-impact operation: requires Runtime-created pending plan plus local terminal approval; ordinary chat confirmation is insufficient. Current reviewed examples include home delete, gateway delete, device delete/remove, device unbind, member removal, home ownership transfer, and leaving a shared home.
- R4 destructive, account-sensitive, or irreversible action: not supported by the Skill path.

## Explicit Non-Enable Rules

- Do not enable every known API row or action name as a Skill capability.
- Do not enable account, login, third-party authorization, token, QR, onboarding, or transfer flows as ordinary Skill execution.
- Do not enable unreviewed batch delete, factory reset, broad member changes, or large bulk operations without Runtime local approval support.
- `device.remove`, `device.unbind`, `gateway.delete`, `home.delete`, `home.member.remove`, `home.member.transfer`, and `home.member.quit` are reviewed R3 plans only when Runtime returns `confirmation_required` with `approvalMode=local_terminal_approve`; commit only after the local approval command succeeds.
- `home.member.invite`, `home.member.accept_share`, `home.member.configure`, and `gateway.configure` are reviewed semantic adapters, but they still use pending-plan confirmation and must not be replaced with raw share, role, or gateway API calls. Accept-share uses the current local account as recipient; never pass or infer another user's uid.
- Do not use static product names, room names, or marketing names as proof of writable capability.
- Do not treat design, commercial platform, hub internals, raw schema, panel layout, storage, or voice configuration material as user-safe execution unless Runtime exposes a reviewed semantic adapter.
