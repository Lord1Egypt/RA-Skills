# Model-First Email Generation Guide

Use this guide when the user wants outreach emails generated after creator selection.

## Principle

- Model-first for subject/body generation
- Script-first for validation, HTML normalization, fallback, and sending
- Generate only for user-selected creators
- Default language: English (`en`)
- If the user specifies a language, generate in that language

## Required inputs

- selected creators (`selected_blogger_ids` or `selected_ranks`)
- product summary (`productName` at minimum)
- confirmed sender name
- offer type (`sample` / `paid` / `affiliate`)

## Recommended optional inputs

- brand name
- deliverable
- compensation
- target market
- CTA goal

## Model output schema

```json
{
  "items": [
    {
      "bloggerId": "string",
      "nickname": "string",
      "language": "en",
      "style": "creator-friendly-natural",
      "subject": "string",
      "htmlBody": "<p>...</p>",
      "plainTextBody": "string",
      "styleReason": "string"
    }
  ]
}
```

## CLI example

```bash
python3 skills/wotohub-automation/run_campaign.py \
  --input "推广一款美国市场的电动牙刷，价格$50，强调美白和口腔护理" \
  --selected-ranks "1,3" \
  --include-email-preview \
  --sender-name "Kiki" \
  --offer-type sample \
  --email-language en \
  --email-model-drafts-json '{"items":[{"bloggerId":"xxx","nickname":"creator-a","language":"en","style":"creator-friendly-natural","subject":"Quick collab idea for your channel","htmlBody":"<p>Hi creator-a,</p><p>I think there is a strong fit between your content and our product.</p><p>Best regards,<br>Kiki</p>","plainTextBody":"Hi creator-a,\n\nI think there is a strong fit between your content and our product.\n\nBest regards,\nKiki","styleReason":"Warm creator tone."}]}'
```

发布建议：
- `items[*].bloggerId` 视为必需字段，用于和搜索结果稳定绑定
- 不建议仅依赖 `nickname` 绑定 drafts

## Performance guardrails

- Only generate for selected creators
- Recommend max 5 creators per generation batch
- Do not retry model generation in tight loops
- Fallback immediately to script draft if model output is missing or malformed
