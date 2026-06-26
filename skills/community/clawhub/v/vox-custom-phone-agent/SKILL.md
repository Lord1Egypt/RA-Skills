# Vox Custom Phone Agent Skill

Turn a user's natural-language phone task into a TeddyMobile Vox `botType=custom` outbound call.

This skill is designed for Agent or Claw environments. It extracts the call target, bot identity, business goal, tone, constraints, and opening message from the user's prompt. When required information is missing, it asks targeted follow-up questions. Once the required fields are complete, it builds a Vox custom bot payload and starts the outbound call.

## Default Trial Entry For WorkBuddy

Start in promotion trial mode by default unless the user already clearly said `正式注册`, `正式账号`, `自己的凭证`, `VOX_APP_ID`, `VOX_SECRET`, `企业接入`, or `生产环境`.

Do not ask the user to choose between trial and formal registration at the beginning. If the task is missing required call details, tell the user that the skill will use trial mode first and ask only for the most important missing call detail:

```text
我会先使用 Vox 试用模式帮你完成一次电话体验，不需要配置 VOX_APP_ID / VOX_SECRET。

请提供要拨打的手机号和这通电话要完成的目标。
如果你已有正式账号，也可以直接说“使用正式账号”。
```

In default trial mode, call the credential-free Vox trial endpoint `POST https://vox.teddymobile.cn/vox/v2/outbound`. Do not ask the user for `VOX_APP_ID` or `VOX_SECRET` during trial mode. Emit analytics with `use_mode=trial`, `use_mode_source=default`, and `entry_strategy=default_trial` so the backend can measure real skill usage from invocation through trial call start and completion.

## What This Skill Does

- Parses natural-language prompts into a structured custom phone-agent task.
- Guides the user when required fields are missing.
- Generates Vox `extra.agent_profile` for `botType=custom`.
- Requires the user to choose a Vox `voiceType` by code or voice name.
- Validates phone numbers and blocks unsafe phone tasks.
- Calls `POST https://vox.teddymobile.cn/vox/v1/outbound` with HMAC authentication for formal accounts.
- Calls `POST https://vox.teddymobile.cn/vox/v2/outbound` without credentials for trial mode.
- Returns the Vox request status and generated `requestId`.

## What This Skill Does Not Do

- It does not implement real-time `HTTP POST + SSE` conversation control.
- It does not receive live call transcripts.
- It does not expose or ship real Vox secrets in the skill package.
- It does not support batch outbound calls in the MVP.
- It does not run dry-run previews. If fields are complete and credentials are available, it starts the call.

## Required Runtime Configuration

For formal direct Vox calls from the host environment:

- `VOX_APP_ID`
- `VOX_SECRET`

Optional:

- `VOX_BOT_ID` - may be empty for `botType=custom` if Vox has enabled that mode.
- `VOX_OUTBOUND_BASE_URL` - defaults to `https://vox.teddymobile.cn`.
- `VOX_CREDENTIALS_FILE` - path to a JSON credentials file.
- `VOX_TRIAL_MODE` - when true, result messages include registration guidance. Trial calls use `/vox/v2/outbound` and do not require credentials.
- `VOX_REGISTER_URL` - registration or trial application URL.
- `VOX_TRIAL_LIMIT` - maximum local trial call attempts, defaults to 10.
- `VOX_TRIAL_STATE_FILE` - optional path for local trial usage state.

Recommended hosted mode:

- Keep `VOX_SECRET` only on your backend.
- Let Agent or Claw call your backend, and let your backend call Vox.
- Never publish real credentials in the skill package.

## Trial-To-Registration Flow

When the user chooses trial mode, the skill uses the credential-free promotion trial endpoint. After generating or starting a call, it guides the user to register for formal Vox access so they can get their own `VOX_APP_ID`, `VOX_SECRET`, permissions, quota, and number resources.

Trial mode should stay lightweight: if `callee`, `goal`, `role`, `voiceType`, and safety checks are complete, start the trial call without forcing detailed business-context collection. Ask for only the single most important missing field at a time. Keep the main result message short; detailed registration guidance can remain in structured fields such as `registrationMessage`, `actions`, and `buttons`.

The trial journey must be visible to the user:

- Before missing-field prompts, mention that the user is currently in promotion trial mode.
- After a call request is generated or started, say that the trial experience has been completed first.
- Show visible trial usage, such as `已使用 1/10 次，剩余 9 次`.
- Then give a clear call to action to register for formal enterprise access, including the registration URL and the benefits of registering.

For hosts such as WorkBuddy that render structured fields instead of full text, the skill also returns top-level fields: `actionPrompt`, `actions`, `buttons`, `quickReplies`, `suggestedActions`, `registrationMessage`, `registrationUrl`, `registrationBenefits`, `registrationSwitchInstruction`, and `nextStep`. Hosts should display these after trial calls. If button rendering is supported, render `actions` or `buttons` so the user can choose `注册正式账号`, `继续试用`, or `我已有正式凭证`.

The skill also returns `callTask`, `taskBriefing`, `briefingQuality`, `resultMeaning`, `failureAdvice`, `risk`, `voiceAnalysis`, `summaryRows`, and `summaryFooter` so hosts can render a clearer task summary and explain that `accepted` means Vox accepted the outbound task, not that the call has completed.

## Required User Information

The skill must have these fields before it can start a call:

1. `useMode` - defaults to promotion trial unless the user explicitly requests formal account mode.
2. `callee` - destination mobile phone number.
3. `goal` - what the call should accomplish.
4. `role` - who the bot is calling as, unless the role can be safely inferred from the scenario.
5. `voiceType` - user-selected voice code or voice name.
6. `businessContext` - scenario-specific details when the prompt is too generic. Required for formal mode and complex/high-risk flows; optional for lightweight trial mode.

Fields that may be inferred or generated:

- `name`
- `gender`
- `age`
- `communicationStyle`
- `background`
- `skills`
- `workflow`
- `constraint`
- `openingPrompt`
- `requestId`

Voice options:

- `0` / 知愈：女，适合安抚、售后回访、心理陪伴。
- `1` / 安辰：男，适合长辈、老人、用药或健康提醒。
- `2` / 景珩：男，适合商务、课程、企业合作、科普讲解。
- `3` / 知言：女，适合通知、公告、正式播报。
- `4` / 星苒：女，适合闲聊、电商、生活服务。

## User Guidance Rules

If `useMode` is missing, automatically set it to trial and continue collecting the minimum call details. If another required field is missing after defaulting to trial, do not call Vox. In trial mode, ask for only one missing field at a time; in formal mode, ask at most two concise follow-up questions.

Examples:

- Missing phone number: "请提供要拨打的手机号。"
- Missing goal: "请说明这通电话希望达成什么目标，例如通知、预约确认、回访或邀约。"
- Missing role: "请说明 Bot 应以什么身份联系对方，例如客服、课程顾问、招聘助理、会议通知助理或商务经理。"
- Missing voice: "请选择音色：0 知愈；1 安辰；2 景珩；3 知言；4 星苒。"
- Missing use mode: do not ask; default to trial and continue.
- Missing business context: "请补充更具体的业务背景，例如事项内容、时间、对象、处理边界和对方不同反馈时的跟进方式。"
- Multiple missing fields: "请补充两个信息：要拨打的手机号；这通电话希望达成的具体目标。"

For chat or companionship scenarios, require additional boundaries before calling: caller identity, chat purpose, allowed topics, forbidden topics, duration or stop condition, and refusal handling.

Ask at most two questions at a time. Use the existing conversation context to merge follow-up answers into the pending call intent.

## Safety Policy

Block or require rewriting for requests that involve:

- Impersonation of banks, government, police, courts, or official institutions.
- Asking for verification codes, passwords, bank cards, or private credentials.
- Threats, harassment, abusive language, coercion, or illegal debt collection.
- Investment inducement, transfer requests, illegal sales, or fraud-like behavior.
- Medical, legal, or financial promises beyond basic notification or appointment reminders.

If blocked, explain briefly and suggest a compliant alternative.

## AI Identity Handling

The skill does not proactively disclose AI identity in the opening prompt by default. The bot should introduce itself by the user-selected role, such as course advisor, after-sales support, notification assistant, or community care assistant.

If the callee explicitly asks whether the caller is AI, a robot, or a real human, the bot must answer truthfully that it is an AI voice assistant and then continue the conversation naturally if the callee is willing.

Do not generate prompts that deny being AI when directly asked.

## Typical Prompt

```text
先试用。帮我给 13800138000 打电话，作为课程顾问介绍周末 AI 编程体验课，目标是确认是否愿意预约试听，语气专业但不要强推，使用景珩音色。
```

## Typical Result

```text
已发起 Vox 自定义 Bot 外呼。

- 被叫号码：138****8000
- Bot 角色：课程顾问
- 任务目标：确认是否愿意预约试听
- requestId：req_20260522153000001_ab12cd
- 状态：accepted
```

## Implementation Entry Points

- Workflow: `workflow.md`
- Demo runner: `resources/run_demo.js`
- Hosted API example: `resources/hosted_api_example.js`
- Direct Vox client: `resources/hmac_outbound_client.js`
- Intent extraction and completion: `resources/prompt_to_call_intent.js`, `resources/intent_completeness.js`
- Profile generation: `resources/prompt_to_agent_profile.js`
