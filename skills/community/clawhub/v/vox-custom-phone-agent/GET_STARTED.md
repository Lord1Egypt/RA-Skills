# Get Started

## Install

This package uses only Node.js built-ins. Use Node.js 18 or newer.

```bash
cd vox-custom-phone-agent
npm run smoke
```

The smoke command runs with `--no-call`, so it does not call Vox.

## Direct Vox Mode

Trial prompts such as `先试用...` call `https://vox.teddymobile.cn/vox/v2/outbound` and do not require `VOX_APP_ID` or `VOX_SECRET`.

Formal account calls use `https://vox.teddymobile.cn/vox/v1/outbound` and require credentials.

Configure credentials in environment variables:

```bash
export VOX_APP_ID="your-vox-app-id"
export VOX_SECRET="your-vox-secret"
export VOX_BOT_ID=""
```

On Windows PowerShell:

```powershell
$env:VOX_APP_ID="your-vox-app-id"
$env:VOX_SECRET="your-vox-secret"
$env:VOX_BOT_ID=""
```

Then run:

```bash
node resources/run_demo.js "给 13800138000 打电话，作为会议通知助理通知明天下午三点会议改到四点，使用知言音色。"
```

Direct mode sends the call request to Vox as soon as required fields are complete.

## Hosted Mode

Hosted mode is recommended for Agent or Claw distribution because the Vox secret stays on your backend.

```bash
export VOX_APP_ID="your-vox-app-id"
export VOX_SECRET="your-vox-secret"
export SKILL_API_TOKEN="change-me"
node resources/hosted_api_example.js
```

Agent or Claw calls:

```http
POST http://localhost:3000/api/vox/custom-call
Authorization: Bearer change-me
Content-Type: application/json
```

```json
{
  "prompt": "给 13800138000 打电话，作为课程顾问介绍周末 AI 编程体验课，目标是确认是否愿意预约试听，使用景珩音色。"
}
```

## Missing Field Guidance

If the prompt is incomplete, the handler returns `status: needs_input` and a user-facing question.

Example:

```json
{
  "status": "needs_input",
  "missing": ["callee"],
  "message": "请提供要拨打的手机号。"
}
```

Pass the saved `intent` back as `previousIntent` when the user answers.

```json
{
  "prompt": "手机号是 13800138000",
  "previousIntent": {
    "scenario": "会议通知",
    "role": "会议通知助理",
    "goal": "通知明天下午三点会议改到四点"
  }
}
```

## Important

- Do not put real `VOX_SECRET` in a public skill package.
- Use hosted mode when distributing the skill to third-party users.
- Confirm with Vox that your account is authorized for `botType=custom`, outbound calls, and your server IP whitelist.
- Trial mode can guide users to register after testing. See `REGISTRATION_GUIDE.md`.
