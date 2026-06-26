# WorkBuddy Result Display Notes

WorkBuddy may render tool results from selected top-level fields instead of showing the full `message` string. For that reason, the skill returns formal registration guidance in several redundant top-level fields after trial usage.

## Fields To Display After Trial

Prefer displaying these fields when present:

- `summaryTitle`
- `summaryRows`
- `summaryFooter`
- `callTask`
- `taskBriefing.taskBriefing`
- `resultMeaning.meaning`
- `failureAdvice.userMessage`
- `actionPrompt`
- `actions`
- `buttons`
- `quickReplies`
- `suggestedActions`
- `registrationMessage`
- `registrationUrl`
- `registrationBenefits`
- `registrationSwitchInstruction`
- `nextStep`

If WorkBuddy supports clickable choices, render `buttons` or `actions` as user-selectable options. The skill returns three actions:

```json
[
  {
    "id": "register_formal_account",
    "type": "url",
    "label": "注册正式账号",
    "url": "https://vox-ai.teddymobile.cn/trial/apply",
    "value": "正式注册"
  },
  {
    "id": "continue_trial",
    "type": "reply",
    "label": "继续试用",
    "value": "继续试用"
  },
  {
    "id": "setup_formal_credentials",
    "type": "reply",
    "label": "我已有正式凭证",
    "value": "我已有正式凭证"
  }
]
```

The most complete field is:

```text
registrationMessage
```

Example:

```text
正式使用建议
如果你希望继续使用电话 Bot，请现在注册 Vox 企业账号。
注册入口：https://vox-ai.teddymobile.cn/trial/apply
注册后你将获得：专属 VOX_APP_ID / VOX_SECRET、正式外呼额度、企业权限、号码资源和生产接入支持。
完成注册后，把新的 VOX_APP_ID / VOX_SECRET 替换当前试用配置，即可切换为正式账号。
```

If WorkBuddy supports nested display fields, it can also use:

```text
display.registrationGuide
display.actionPrompt
display.actions
display.buttons
display.nextStep
display.registrationUrl
```

## Why This Exists

The user must perceive the full journey:

```text
choose trial or formal mode -> complete trial -> see formal registration guidance
```

Do not hide the formal registration guidance after an accepted trial call.
