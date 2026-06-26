# Vox Custom Phone Agent Workflow

## Goal

Convert a user's natural-language prompt into a Vox `botType=custom` outbound call. If required fields are missing, ask for the missing fields. If all required fields are present and the request is safe, call Vox immediately.

## Runtime Flow

1. Receive the user prompt.
2. Check whether the user has selected usage mode: trial or formal registration.
3. If usage mode is missing, ask only: `请选择使用方式：1 先用推广试用体验一次；2 使用正式账号/注册 Vox 企业账号后接入。回复“试用”或“正式注册”即可。` Then stop.
4. Load any pending call intent from conversation state.
5. Extract new fields from the prompt.
6. Merge extracted fields into the pending intent.
7. Run content-safety checks.
8. Validate required fields.
9. If required fields are missing, ask targeted follow-up questions and stop.
10. Generate `agent_profile`.
11. Use the user-selected `voiceType`.
12. Load Vox credentials only for formal mode. Trial mode uses the credential-free `/vox/v2/outbound` endpoint and must not ask for `VOX_APP_ID` or `VOX_SECRET`.
13. Build the outbound payload with `botType=custom`.
14. Sign the request with HMAC-SHA256.
15. POST formal calls to `https://vox.teddymobile.cn/vox/v1/outbound`, or trial calls to `https://vox.teddymobile.cn/vox/v2/outbound`.
16. Return masked phone number, bot role, task goal, `requestId`, and status.

## Required Intent Fields

- `callee`: destination phone number.
- `goal`: concrete purpose of the call.
- `role`: caller identity, unless safely inferred.
- `voiceType`: selected by code `0-4` or name 知愈、安辰、景珩、知言、星苒.
- `useMode`: selected by the user before collecting other fields. `trial` means promotion trial. `formal` means using formal enterprise credentials or registering first.
- `businessContext`: scenario-specific background if the prompt is too generic, such as service item, event time, product, follow-up boundaries, or branch handling rules.

## Follow-Up Behavior

When `useMode` is missing, ask only for trial/formal mode and stop. After usage mode is known, ask no more than two questions for other missing fields. Do not show a dry-run preview. Do not call Vox until all required fields are available.

Trial mode uses a lightweight flow: require only phone number, goal, Bot role, selected voice, and safety approval. Do not block trial calls on detailed `businessContext`; collect richer scenario details only for formal mode, complex tasks, or risky domains. Trial follow-up should ask for the single highest-priority missing field.

Examples:

```text
请提供要拨打的手机号。
```

```text
请补充两个信息：要拨打的手机号；这通电话希望达成的具体目标。
```

```text
请说明 Bot 应以什么身份联系对方，例如客服、课程顾问、招聘助理、会议通知助理或商务经理。
```

```text
请选择音色：0 知愈（女，安抚/回访）；1 安辰（男，长辈/老人）；2 景珩（男，商务/课程/科普）；3 知言（女，通知/公告）；4 星苒（女，闲聊/电商/生活服务）。
```

```text
请选择使用方式：1 先用推广试用体验一次；2 使用正式账号/注册 Vox 企业账号后接入。回复“试用”或“正式注册”即可。
```

```text
请补充这次售后/维修回访的业务背景，例如：是哪次维修、维修内容或产品、希望确认哪些问题、不满意时是否安排人工客服跟进，以及不能承诺哪些事项。
```

```text
请补充聊天场景的边界：Bot 身份、聊天目的、可聊话题、不能聊的话题、通话时长或结束条件，以及对方不想聊时是否立即礼貌结束。
```

## Voice Selection

Do not silently choose the voice in normal flow. If the user does not specify a voice, ask them to choose one. Accept either code or name, for example `3`, `知言`, `用知言音色`, or `voiceType=3`.

## Safe Defaults

If unspecified, generate these defaults:

- `name`: 小知
- `gender`: 女
- `age`: 26
- `communicationStyle`: 礼貌, 清晰, 专业
- `constraint`: 保持礼貌；尊重对方意愿；不得索要敏感隐私信息；对方拒绝或不方便时礼貌结束

Identity default: do not proactively disclose AI identity in the opening prompt, but if the callee directly asks whether the caller is AI, a robot, or a real human, answer truthfully that it is an AI voice assistant.

## Scenario Defaults

| Scenario | Role | Suggested Voice Type | Style |
| --- | --- | --- | --- |
| 会议通知 | 会议通知助理 | 3 知言 | 正式, 简洁, 清晰 |
| 售后回访 | 售后客服 | 0 知愈 | 耐心, 真诚, 礼貌 |
| 课程邀约 | 课程顾问 | 2 景珩 | 专业, 温和, 克制 |
| 面试通知 | 招聘助理 | 3 知言 | 正式, 友好, 清晰 |
| 商务合作 | 商务经理 | 2 景珩 | 专业, 稳重, 高效 |
| 健康提醒 | 健康提醒助手 | 1 安辰 | 温和, 清楚, 耐心 |
| 活动提醒 | 活动通知助理 | 3 知言 | 清晰, 友好, 简洁 |

## Vox Outbound Payload Shape

Trial mode uses the same payload shape except it omits `appId` and sends the request to `/vox/v2/outbound` without HMAC headers.

```json
{
  "appId": "VOX_APP_ID",
  "botid": "",
  "callee": "13800138000",
  "requestId": "req_20260522153000001_ab12cd",
  "botType": "custom",
  "extra": "{\"voiceType\":\"2\",\"agent_profile\":{...}}"
}
```

Important: `extra` is a JSON string, not a nested object.

## Error Handling

- Missing user fields: ask follow-up questions.
- Unsafe content: refuse and suggest a safe rewrite.
- Missing credentials: say which Vox configuration is missing.
- Vox `401`: check credentials, server time, and signature.
- Vox `403`: check interface permission, IP whitelist, and account authorization.
- Vox non-zero `code`: return `code`, `msg`, and `requestId` if present.
