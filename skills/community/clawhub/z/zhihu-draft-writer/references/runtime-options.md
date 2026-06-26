# Runtime Options

Resolve these values from the user's request before running the workflow.

## Defaults

```json
{
  "topic_mode": "general_hot",
  "custom_topic_keywords": [],
  "draft_count": 1,
  "comment_count": 3,
  "writing_style": {
    "mode": "default",
    "summary": "理性、自然、偏知乎高赞回答风格，2-4 段，观点明确但不过度煽动。"
  }
}
```

If the user does not provide any explicit parameter, run with these defaults directly. Do not ask follow-up questions.

## Rules

- `topic_mode`
  - `general_hot`（默认）：不限制话题类型，从合规热门题里直接选。
  - `custom`：按用户指定的关键词筛选，例如 `职场`、`亲子`、`考研`、`专业选择`、`健身`。多个关键词之间为 OR 逻辑，匹配任意一个即可。
  - 不再支持 `education_first` 模式；如果用户明确要求教育类，改用 `custom` 并设置教育相关关键词。

- `custom_topic_keywords`
  - 仅在 `topic_mode = custom` 时使用。
  - 从用户要求里提取 1–5 个正向关键词（中文词组）。
  - 如果用户表达了排除条件（如"不要法律援助"），不要将排除条件放入关键词；仅提取正向词，并在跳过候选题时以排除条件作为 skip-reason。
  - 不要自行将关键词扩展到政治或敏感方向。

- `draft_count`
  - 本次要生成并保存到草稿箱的问题数量。
  - 默认 `1`，最小 `1`，最大 `5`。
  - 若用户要求超过 `5`，按 `5` 执行并在结果里说明已截断至 5。

- `comment_count`
  - 每个问题优先读取多少条高热评论。
  - 默认 `3`，允许范围 `3–5`。
  - 若用户指定超过 `5`，按 `5` 截断；若低于 `3`，按 `3` 提升；若用户指定 `2` 或更低，同样提升到 `3`。

- `writing_style`
  - `mode = default`：使用默认知乎长回答风格（理性、自然、2–4 段，观点明确但不过度煽动）。
  - `mode = user_defined`：`summary` 保存用户的风格描述，例如"更口语化""像老师讲道理""更克制冷静""偏经验贴""犀利但不攻击人"。
  - 用户风格只影响表达方式，不改变安全限制、合规限制和禁止发布限制。
  - 当用户风格与话题调性冲突时（例如要求"激进风格"但话题较为严肃），以话题适配为准，在不违反安全规则的前提下尽量靠近用户风格。

## Extraction Guidance

- 如果用户说"写 3 个草稿"或"回答 2 个问题"，设置 `draft_count` 为对应数字。
- 如果用户说"按职场类问题来写""健身相关的""只选科技类"，设置 `topic_mode = custom`，并提取对应关键词。
- 如果用户说"随便选热门题"或没有限定类型，设置 `topic_mode = general_hot`。
- 如果用户说"风格更像过来人分享""更犀利一点但别攻击人"，放进 `writing_style.summary`，并将 `mode` 设为 `user_defined`。
- 如果用户没有显式给出风格要求，保持 `mode = default`，不要追问。

## Example Requests

- `帮我写 1 个知乎草稿` → `topic_mode=general_hot, draft_count=1`
- `今天挑 3 个亲子教育问题，每个都写进草稿箱` → `topic_mode=custom, keywords=["亲子教育"], draft_count=3`
- `选 2 个大学专业选择相关的问题，风格偏理性分析` → `topic_mode=custom, keywords=["专业选择","大学"], draft_count=2, writing_style={mode:user_defined, summary:"偏理性分析"}`
- `从热门里选 1 个职场类问题，口吻像真实过来人，不要鸡汤` → `topic_mode=custom, keywords=["职场"], draft_count=1, writing_style={mode:user_defined, summary:"像真实过来人，不要鸡汤"}`
- `随便选个热门问题写一篇` → `topic_mode=general_hot, draft_count=1`
- `帮我写 2 个关于法律的草稿，但不是法律援助类` → `topic_mode=custom, keywords=["法律"], draft_count=2`（在评估候选题时，跳过标题/摘要明显属于法律援助求助的题目）
