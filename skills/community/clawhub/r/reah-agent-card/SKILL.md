---
name: reah
description: >-
  Retrieve masked card info from Reah using an access key.
  Handles session generation, secure fetch, and decryption for agents
  automatically.
metadata: {"openclaw":{"requires":{"anyBins":["node","curl"],"anyEnvVars":["REAH_AGENT_KEYS"]}}}
---

# Reah Skill

This skill is organized by modules.

## Modules

### `reah_card`

Handle Reah card key flow for `agents.reah.com`.

This module handles two tasks.

#### Task 1: Ask for access key

If user did not provide an `access key`, ask user with this exact message:

```text
To continue, I need your Reah card access key.

You can get it from agents.reah.com:
- Open your card
- Click "Generate agent key"

Paste it here and I'll securely fetch your card details.
```

If the workflow uses `REAH_AGENT_KEYS` from environment:

- MUST ask for manual confirmation before each key read, even within the same conversation.
- MUST NOT reuse prior confirmation.
- Use this exact confirmation message:

```text
I can read the access key from REAH_AGENT_KEYS for this request.

Please confirm I should proceed with this key read now.
```

- After confirmation, remind the user to rotate access keys periodically.

Do not proceed to Task 2 before key is provided or key-read confirmation is granted.

#### Task 2: Get and decrypt card info

##### Example script (reference only)

Use the example script below as reference for the full process:

```bash
node {baseDir}/scripts/get-card-info-example.mjs \
  --access-key "<accessKey>"
```

This script includes all steps in one place:
- generate `sessionId` / `secretKey`
- request `individualCardByAccessKey(accessKey, sessionId)` from `https://agents.reah.com/graphql`
- decrypt `encryptedPan` and `encryptedCvc`

This script is for reference only. It intentionally ends after decryption and does not output raw `pan`/`cvv`.

##### Script Files

- `{baseDir}/scripts/get-card-info-example.mjs`

##### Security Constraints

- MUST use only the default Reah GraphQL endpoint: `https://agents.reah.com/graphql`.
- MUST NOT allow endpoint override.
- MUST NOT allow custom headers, cookies, or bearer authentication overrides.
- MUST NOT send card data to any external endpoint.
- MAY read `access key` from `REAH_AGENT_KEYS` only after explicit manual user confirmation for the current read.
- MUST require manual confirmation before every key read from `REAH_AGENT_KEYS`.
- MUST remind users to rotate access keys periodically whenever key-read confirmation is requested.
- MUST NOT expose full `access key` in any user-facing response.
- MUST NOT expose raw `secretKey` in any user-facing response.
- MUST NOT return raw card info in any user-facing response. Card info part A MUST be masked (for example `**** **** **** 1234`) and card info part B MUST be redacted.

##### Error Handling

- If access key is invalid, ask user to regenerate a new agent key and retry.
- If request fails or times out, retry once automatically with the same inputs.
- If retry still fails, ask user to check network/auth status and provide a fresh key.
