---
name: weryai-account
description: Check WeryAI account credits and API balance through the official WeryAI account endpoint. Use when the user wants to query remaining credits, inspect WeryAI account balance, verify that WERYAI_API_KEY works for account access, or asks how many credits are left before running paid image, video, or music jobs.
metadata: { "openclaw": { "emoji": "💳", "primaryEnv": "WERYAI_API_KEY", "paid": false, "network_required": true, "requires": { "env": ["WERYAI_API_KEY"], "bins": ["node"], "node": ">=18" } } }
---

# WeryAI Account

Use this skill for official WeryAI account balance and credits queries. It is intentionally narrow: the only supported public account action in this skill is reading the current API credits balance from WeryAI.

This skill is intentionally strict about secret declaration and input safety: the only runtime secret is `WERYAI_API_KEY`. This is a read-only account check, not a generation or editing workflow.

**Dependencies:** `scripts/account.js` in this directory + `WERYAI_API_KEY` + Node.js 18+. No other Cursor skills are required.

## Example Prompts

- `Check my remaining WeryAI credits.`
- `How many credits are left on this WeryAI API account?`
- `Verify that this WERYAI_API_KEY can read the account balance.`
- `Before I run a paid image job, show me the current WeryAI balance.`

## Quick Summary

- Main job: query WeryAI API account credits
- Main output: `balance`
- Main trust signals: official account endpoint, read-only behavior, `WERYAI_API_KEY` runtime-secret policy

## Authentication and first-time setup

Before the first real account query:

1. Create a WeryAI account.
2. Open the API key page at `https://www.weryai.com/api/keys`.
3. Create a new API key and copy the secret value.
4. Add it to the required environment variable `WERYAI_API_KEY`.

### OpenClaw-friendly setup

- This skill already declares `WERYAI_API_KEY` in `metadata.openclaw.requires.env` and `primaryEnv`.
- After installation, if the installer or runtime asks for required environment variables, paste the key into `WERYAI_API_KEY`.
- If you are configuring the runtime manually, export it before running commands:

```sh
export WERYAI_API_KEY="your_api_key_here"
```

### Quick verification

Use one safe check before the first real account query:

```sh
node {baseDir}/scripts/account.js balance
```

If the key is valid, the command returns JSON with a numeric `balance`.

- `balance` confirms that the key is configured and the official account endpoint is reachable.
- If `balance` is `0`, guide the user to recharge or buy credits at `https://www.weryai.com/api/pricing` before running paid jobs.

## Prerequisites

- `WERYAI_API_KEY` must be set before running `account.js`.
- Node.js `>=18` is required because the runtime uses built-in `fetch`.

## Security, secrets, and API hosts

- **`WERYAI_API_KEY`**: Treat it as a secret. Configure it only in the runtime environment; never write the secret value into the skill files.
- Optional override `WERYAI_BASE_URL` defaults to `https://api.weryai.com`. Only override it with a trusted host.
- **Higher assurance**: Run account checks in a short-lived shell or isolated environment, and review `scripts/account.js` before production use.

## Intent Routing

Use this skill when the user asks:

- how many credits are left
- what the current WeryAI balance is
- whether the API key works for account access
- whether there are enough credits before a paid generation run

Do not use this skill for:

- text-to-image or image-to-image generation
- image tools
- video generation or video tools
- music generation
- effect templates

Those belong to other WeryAI skills.

## Preferred Command

```sh
node {baseDir}/scripts/account.js balance
```

## Workflow

1. Confirm the user wants account credits or API balance, not generation.
2. Ensure `WERYAI_API_KEY` is available in the runtime environment.
3. Run `node {baseDir}/scripts/account.js balance`.
4. Return the JSON result and clearly state the current balance.

## Output

The command prints JSON to stdout. Successful output includes:

- `ok`
- `phase`
- `balance`
- `topUpRequired`
- `rechargeUrl`
- `guidance`

Failure output can include:

- `errorCode`
- `errorMessage`

## Definition of done

The task is done when:

- the balance endpoint returns successfully and the credits value is shown to the user,
- if the balance is `0`, the recharge guidance is shown with `https://www.weryai.com/api/pricing`,
- or the failure clearly explains why balance lookup did not work, such as missing or invalid `WERYAI_API_KEY`.

## Re-run behavior

- `balance` is read-only and safe to re-run.

## References

- Official account endpoint contract: [references/account-api.md](references/account-api.md)
- Official documentation index: [WeryAI llms.txt](https://docs.weryai.com/llms.txt)
- Account balance API: [Query API Account Credits](https://docs.weryai.com/api-reference/account/query-api-account-credits.md)
