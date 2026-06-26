# Binding and 2FA Delete

## Owner binding

Owner binding links the agent to a human owner through WebAuthn passkey authentication. Treat this as part of onboarding, not as an advanced feature.

This is a mixed agent and human flow:

- The agent prepares and verifies the flow
- The user only opens a URL and completes passkey authentication

## Accepted owner identifiers

Both `bind prepare` and `bind check-passkey` accept:

- A raw AI ID
- An Owner AI Name ending in `.ai`

Do not accept an Agent AI Name ending in `.agent` as an owner identifier.

If the user provides an Owner AI Name, use it directly. The CLI resolves it automatically. Do not ask the user to manually look up the raw AI ID first.

## Passkey pre-check

Before binding, verify that the target owner has a registered passkey. Owners created only through OAuth may not have one yet.

```bash
zcloak-ai bind check-passkey <user_ai_id>
zcloak-ai bind check-passkey alice.ai
```

## Binding flow

Present the binding flow in three steps:

1. The agent prepares the request and returns an authentication URL
2. The user opens the URL and completes passkey authentication
3. The agent verifies the final binding result

Internal command reference:

```bash
zcloak-ai bind prepare alice.ai
zcloak-ai bind prepare <user_ai_id>
zcloak-ai register get-owner <agent_ai_id>
```

If no owner is yet bound, explain briefly that binding enables passkey-backed authorization for protected operations such as secure delete.

## File deletion with 2FA

Deleting a file requires owner-confirmed WebAuthn authorization. The agent must never delete the file before 2FA is confirmed.

### Step 1: Prepare 2FA request

```bash
zcloak-ai delete prepare <file_path>
```

Expected outputs:

- A challenge string
- A browser authentication URL such as `https://id.zcloak.ai/agent/2fa?challenge=...`

### Step 2: User completes passkey authentication

The user opens the URL and authorizes the deletion in the browser.

### Step 3: Optional status check

```bash
zcloak-ai delete check <challenge>
```

### Step 4: Confirm and delete

```bash
zcloak-ai delete confirm <challenge> <file_path>
```

Only confirm deletion after the challenge shows successful owner authorization.

## User-facing guidance

In delete flows:

- Tell the user exactly which file is pending deletion
- Surface the authentication URL clearly
- Explain that no deletion happens until passkey confirmation succeeds
- After deletion, confirm the file path that was removed
