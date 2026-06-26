---
name: chanjing-credentials-guard
description: Guide users to configure local Chanjing credentials safely via local commands only, and validate local token status when needed.
metadata:
  openclaw:
    requires:
      env:
        - CHANJING_CONFIG_DIR
    homepage: https://open-api.chanjing.cc
---

# Chanjing Credentials Guard

## When to Run

1. **When user asks to configure/get Chanjing keys (AK/SK)**: use this skill to guide local setup.
2. **When credentials are missing/invalid before a Chanjing API call**: use this skill to recover local config.

This skill is a **local credential guide**, not a runtime dependency for other skills.
It does not require bundled helper scripts to be present.

## Execution Flow

```
1. Check if local AK/SK exists
   └─ No  → Open login page URL in browser → Ask user to configure local file
   └─ Yes → Continue

2. Check if local Token exists and is not expired
   └─ No  → Call API to request/refresh Token → Save to local file
   └─ Yes → Continue

3. Prompt user to continue target action
```

## Credential Storage

AK/SK and Token are read from the same local config file.

- **Path**: `~/.chanjing/credentials.json` (overridable by env `CHANJING_CONFIG_DIR`)
- **Format**:
```json
{
  "app_id": "Your Access Key",
  "secret_key": "Your Secret Key",
  "access_token": "Optional, auto-generated",
  "expire_in": 1721289220
}
```

`expire_in` is a Unix timestamp. Token is valid for about 24 hours; refresh 5 minutes before expiry.

## When AK/SK Is Missing

When local `app_id` or `secret_key` is missing:

1. **Open login page**: open `https://www.chanjing.cc/openapi/login` in the default browser.
2. **Require local setup** after the user obtains keys:
   - User updates local `credentials.json` file.
3. **Do not request secrets in chat**:
   - Never ask user to paste AK/SK in conversation.
   - Never echo or store AK/SK in chat summaries.
4. **After setting**:
   - Ask user to run status check and then proceed to target action.

Manual update example:

```json
{
  "app_id": "<your_app_id>",
  "secret_key": "<your_secret_key>"
}
```

## Guide When User Wants to Generate Keys

When the user clearly wants to **generate chanjing keys**, **get keys**, or **configure AK/SK**, follow this flow:

### Step 1: Check if already configured

Check if local AK/SK already exists (read `~/.chanjing/credentials.json` for non-empty `app_id` and `secret_key`).

### Step 2: Branch on result

- **If already configured**: ask whether user wants to overwrite local config.
  - If yes, run guide steps.
  - If no, stop.

- **If not configured**: Run the “Guide steps” below directly.

### Guide steps (when not configured or user confirmed re-apply)

1. Open `https://www.chanjing.cc/openapi/login` in browser.
2. **Explain the page flow clearly**:
   - New users are registered automatically and the current page will display `App ID` and `Secret Key` with copy buttons.
   - Existing users may be redirected to the console; tell them to open the left-side **API 密钥** page to view or reset keys.
3. **Ask user to configure local file** `~/.chanjing/credentials.json` (or `$CHANJING_CONFIG_DIR/credentials.json`) with `app_id` and `secret_key`.
4. **Secret handling rule**:
   - Do not ask user to paste AK/SK in chat.
   - If user shares secret in chat anyway, remind them to rotate keys and continue with local-command-only flow.
5. **After setting**:
   - Re-open the local file to confirm non-empty `app_id` and `secret_key`.
   - Then proceed to target Chanjing action.

## Token API (see chanjing-openapi.yaml)

```http
POST https://open-api.chanjing.cc/open/v1/access_token
Content-Type: application/json
```

Request body:
```json
{
  "app_id": "{{app_id}}",
  "secret_key": "{{secret_key}}"
}
```

Response (success `code: 0`):
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "access_token": "xxx",
    "expire_in": 1721289220
  }
}
```

- `expire_in`: Unix timestamp for token expiry
- If `code !== 0`, AK/SK is invalid or the request failed

## Validation Logic

1. **AK/SK**: Read from config (path/format above); ensure `app_id` and `secret_key` are non-empty.
2. **Token**: Ensure `access_token` exists and `expire_in > current_time + 300` (refresh 5 minutes early).
3. **Token refresh**: Call the API above and write returned `access_token` and `expire_in` back to the file.

## Security Boundary

- This skill only handles **local credential guidance**.
- It does not require install hooks or elevated/system-wide privileges.
- It should not automatically execute unrelated skills.
- It should not accept AK/SK via chat content.

## Packaging Note

- This skill can work as a documentation-only guide.
- If a package variant includes helper scripts, they are optional convenience utilities, not required for core behavior.

## With Other Skills

- Other Chanjing skills may use the same local config path/format, but should keep their own runtime auth logic.
- Guard can be used as an optional setup helper when users explicitly ask for credential guidance.

## Reference

- [reference.md](reference.md): API and storage format details
- chanjing-openapi.yaml: `/access_token`, `dto.OpenAccessTokenReq`, `dto.OpenAccessTokenResp`
