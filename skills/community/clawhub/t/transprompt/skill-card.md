## Description:

一句指令，把白话需求变成可直接发给 GPT / Claude / Gemini / Cursor 的专业 Prompt。支持 `@prt` / `@prompt` 随手触发；不需要转换时自动正常回复，不打断聊天。 Turn plain-language requests into copy-ready prompts for GPT, Claude, Gemini, Cursor, and similar tools, while replying normally when prompt conversion is unnecessary.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keyzzzoe](https://clawhub.ai/user/keyzzzoe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn plain-language requests prefixed with `@prt` or `@prompt` into concise, copy-ready prompts for GPT, Claude, Gemini, Cursor, Claude Code, and similar AI tools. It also supports normal conversational replies when prompt conversion is not useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated prompts may contain assumptions or wording that does not match the user's intent.

Mitigation: Review generated prompts before copying them into other AI tools.

Risk: Some default labels and examples may appear in Chinese.

Mitigation: Adapt section labels and examples to the user's preferred language when needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/keyzzzoe/skills/transprompt)
- [Guide EN](references/guide-en.md)
- [Guide ZH](references/guide-zh.md)
- [Decision Guide](references/decision-guide.md)
- [Prompt Patterns](references/prompt-patterns.md)
- [Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown prompt text with a short summary or concise clarification questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Chinese section labels by default unless the agent adapts output language to the user.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
