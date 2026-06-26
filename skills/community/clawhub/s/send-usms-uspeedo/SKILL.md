---
name: send-usms-uspeedo
description: Sends international SMS (USMS) via uspeedo platform HTTP API. Use when the user needs to send international SMS, batch SMS, verification/notification/marketing messages, or when integrating with uspeedo SendBatchUSMSMessage API.
homepage: https://uspeedo.com
metadata: {"openclaw":{"homepage":"https://uspeedo.com","requires":{"env":["USPEEDO_ACCESSKEY_ID","USPEEDO_ACCESSKEY_SECRET"]},"primaryEnv":"USPEEDO_ACCESSKEY_ID"}}
---

# Send International SMS via uspeedo

## Skill Overview

This skill sends **international SMS (USMS)** through the **uspeedo HTTP API**, supporting verification codes, notifications, and marketing. After configuring environment variables, you can send in batch and fill content by template. See the [uspeedo console](https://uspeedo.com/en/ai-communication?SaleCode=JD4651&ChannelCode=OpenClaw) for API docs and account management.

## Environment Variables

Configure before use (read from environment or `.env`):

| Variable | Required | Description |
|----------|----------|-------------|
| `USPEEDO_ACCESSKEY_ID` | Yes | AccessKey ID (create in console) |
| `USPEEDO_ACCESSKEY_SECRET` | Yes | AccessKey Secret (create in console) |
| `USPEEDO_ACCOUNT_ID` | No | Account ID (optional), see [docs](https://docs.uspeedo.com/docs/sms/api/) |
| `USPEEDO_TEMPLATE_ID_VERIFICATION` | As needed | Verification template ID |
| `USPEEDO_TEMPLATE_ID_NOTIFICATION` | As needed | Notification template ID |
| `USPEEDO_TEMPLATE_ID_MARKETING` | As needed | Marketing template ID |
| `USPEEDO_SENDER_ID` | No | Sender ID; use empty string if none |

Configure the template ID for each SMS type you use. **All template IDs in this skill are full-variable templates**; `TemplateParams` is the **actual full SMS body** (usually a single-element array, e.g. `["Your verification code is 123456, valid for 5 minutes."]`).

## Pre-checks and User Guidance

Before sending, check environment variables. When not configured, guide the user as follows:

**1. When `USPEEDO_ACCESSKEY_ID` or `USPEEDO_ACCESSKEY_SECRET` is not set, or there is no .env / no environment variables**

Tell the user to follow these steps directly. **After giving this guidance, stop—do not perform sending or any further steps**:

1. Open the [uspeedo console](https://uspeedo.com/en/ai-communication?SaleCode=JD4651&ChannelCode=OpenClaw) to register and log in.
2. In the console, create an **AccessKey** and save the ACCESSKEY_ID and ACCESSKEY_SECRET.
3. Open [SMS template management](https://console.uspeedo.com/sms/template), create a **full-variable template**: choose purpose “Verification” or “Notification/Marketing” (according to the type you want to send), set template content to `{1}`, submit and wait for approval.
4. After approval, copy the **template ID** from the template list. It is recommended to create one template per type (verification, notification, marketing) and set `USPEEDO_TEMPLATE_ID_VERIFICATION`, `USPEEDO_TEMPLATE_ID_NOTIFICATION`, `USPEEDO_TEMPLATE_ID_MARKETING` accordingly.
5. Write ACCESSKEY_ID, ACCESSKEY_SECRET, and template IDs into `.env` or environment variables, then retry sending.

**2. When AccessKey is set but the template ID for the SMS type being sent is not configured**

(e.g. sending verification SMS but `USPEEDO_TEMPLATE_ID_VERIFICATION` is not set)  
Tell the user: **You are sending [verification/notification/marketing] SMS but the corresponding template ID is not configured. Go to [SMS template management](https://console.uspeedo.com/sms/template), create a full-variable template for that type (template content `{1}`), and after approval set the template ID in `USPEEDO_TEMPLATE_ID_VERIFICATION` / `USPEEDO_TEMPLATE_ID_NOTIFICATION` / `USPEEDO_TEMPLATE_ID_MARKETING`.**

## Request

- **URL**: `POST https://api.uspeedo.com/api/v1/usms/SendBatchUSMSMessage`
- **Content-Type**: `application/json`
- **Auth**: Header `Authorization: Basic base64(ACCESSKEY_ID:ACCESSKEY_SECRET)`. Base64-encode `USPEEDO_ACCESSKEY_ID:USPEEDO_ACCESSKEY_SECRET` and set the header to `Basic <encoded_result>`.

## Request Body

Send only the **TaskContent** array. Each item has:
- **TemplateId**: Template ID for that type
- **SenderId**: Set if you have one, otherwise `""`
- **Target**: Array of:
  - **Phone**: Number, e.g. `13800138000` or international format `(852)55311111`
  - **TemplateParams**: String array. For full-variable templates this is the **full SMS content** to send, usually one element (e.g. `["Your verification code is 123456, valid for 5 minutes."]`)

## Examples

**Request body (single verification):**

```json
{
  "TaskContent": [
    {
      "TemplateId": "template_id_1",
      "SenderId": "USpeedo",
      "Target": [
        {
          "Phone": "13800138000",
          "TemplateParams": ["Your verification code is 123456"]
        }
      ]
    }
  ]
}
```

**curl:**

```bash
curl -X POST "https://api.uspeedo.com/api/v1/usms/SendBatchUSMSMessage" \
  -H "Content-Type: application/json" \
  -H "Authorization: Basic $(echo -n 'YOUR_ACCESSKEY_ID:YOUR_ACCESSKEY_SECRET' | base64)" \
  -d '{
    "TaskContent": [
      {
        "TemplateId": "template_id_1",
        "SenderId": "USpeedo",
        "Target": [
          {
            "Phone": "13800138000",
            "TemplateParams": ["Your verification code is 123456"]
          }
        ]
      }
    ]
  }'
```

## Workflow

1. **Pre-check**: If `USPEEDO_ACCESSKEY_ID` or `USPEEDO_ACCESSKEY_SECRET` is not set, or there is no .env / no environment variables, follow “Pre-checks and User Guidance” item 1 and stop. If the user is sending a type that has no template ID configured (e.g. verification but `USPEEDO_TEMPLATE_ID_VERIFICATION` not set), follow item 2.
2. Confirm SMS type (verification / notification / marketing) and choose the corresponding template ID env var.
3. Read `USPEEDO_ACCESSKEY_ID`, `USPEEDO_ACCESSKEY_SECRET`, the chosen template ID, and optional `USPEEDO_SENDER_ID` from env. Set header `Authorization: Basic base64(ACCESSKEY_ID:ACCESSKEY_SECRET)` and POST to `https://api.uspeedo.com/api/v1/usms/SendBatchUSMSMessage`.
4. Build `TemplateParams` (for full-variable template, the full SMS content). Format phone in international form (with country/region code) if needed.
5. Send the POST, parse `RetCode` and `Message`, and report success or failure. On error codes, see “Common errors” below.

## Common Errors

- **`{"Message":"Failed to parse token","RetCode":215398}`**  
  AccessKey (ACCESSKEY_ID / ACCESSKEY_SECRET) is invalid or expired. Tell the user: **AccessKey is invalid. Please sign in at the [uspeedo console](https://console.uspeedo.com/) and update ACCESSKEY_ID and ACCESSKEY_SECRET.**

## Notes

- **Do not write any script to send SMS**; use the reference curl command in this document.
- Do not hardcode ACCESSKEY_ID or ACCESSKEY_SECRET in code or config; read from environment.
- Phone should be in international format (with country/region code), e.g. `(852)55311111`.
- If you have no SenderId, use empty string `""`; do not omit the field or the API may error.
