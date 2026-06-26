# Criteria for Voice Preferences / 语音偏好判断标准

Reference only — consult when deciding whether to update SKILL.md.
仅供参考 — 决定是否更新 SKILL.md 时查阅。

## When to Add / 何时添加

**Immediate (1 occurrence) / 即时（1 次）:**
- User explicitly requests voice change ("use a deeper voice") / 用户明确要求改变声音（"用低沉一点的声音"）
- User comments on pace ("too fast", "slow down") / 用户评论语速（"太快了"、"慢一点"）
- User requests style change ("be more casual when speaking") / 用户要求风格变化（"说话随意一点"）
- User says "that sounds good" after voice adjustment / 用户在声音调整后说"听着不错"

**After pattern (2+ occurrences) / 确认模式（2+ 次）:**
- User consistently prefers certain formality level / 用户一贯偏好某种正式程度
- User skips long spoken responses / 用户跳过长的语音回复
- User engages more with certain speaking styles / 用户更积极参与某种说话风格

## When NOT to Add / 何时不添加
- Situational request ("just this once, read it faster") / 情境请求（"就这一次，读快点"）
- Topic-specific ("use serious tone for this legal doc") / 主题特定（"这份法律文件用严肃语气"）
- One-off feedback / 一次性反馈

## How to Write Entries / 如何写条目

**Ultra-compact / 超简洁:**

Voice examples / 语音示例:
- `openai: nova`
- `elevenlabs: custom clone`
- `edge: en-GB-SoniaNeural`

Style examples / 风格示例:
- `casual, conversational` / `随意、会话式`
- `professional, measured` / `专业、克制`
- `brief, to the point` / `简洁、直接`
- `warm, friendly` / `温暖、友好`
- `no filler words` / `无填充词`

Spoken Text examples / 语音文本示例:
- `short sentences` / `短句`
- `spell out abbreviations` / `拼出缩写`
- `use contractions` / `使用缩写`
- `round numbers` / `四舍五入数字`
- `no lists, use prose` / `不用列表，用散文`

Avoid examples / 避免示例:
- `no long monologues` / `不要长篇独白`
- `avoid technical jargon spoken` / `避免念技术术语`
- `skip parentheticals` / `跳过括号内容`
- `no markdown read aloud` / `不念 markdown`

## Context Qualifiers / 上下文限定
- `work calls: formal` / `工作通话：正式`
- `casual chat: relaxed` / `休闲聊天：放松`
- `reading emails: brief summary first` / `读邮件：先简短总结`

## Maintenance / 维护
- Keep total SKILL.md under 35 lines / SKILL.md 总行数控制在 35 行以内
- Group similar preferences / 将相似偏好归为一组
- Note what DOESN'T work in Avoid section / 在 Avoid 部分记录什么不奏效
