## Description: <br>
一句指令，把白话需求变成可直接发给 GPT / Claude / Gemini / Cursor 的专业 Prompt。支持 `@prt` / `@prompt` 随手触发；不需要转换时自动正常回复，不打断聊天。 Turn plain-language requests into copy-ready prompts for GPT, Claude, Gemini, Cursor, and similar tools, while replying normally when prompt conversion is unnecessary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[keyzzzoe](https://clawhub.ai/user/keyzzzoe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use TransPrompt to turn plain-language requests into copy-ready prompts for GPT, Claude, Gemini, Cursor, Claude Code, and similar tools. It also helps keep normal chat natural by bypassing prompt conversion when the prefixed input is a greeting, simple question, or other low-value prompt-writing case. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A generated prompt may ask a downstream AI tool to write code, browse the web, modify files, or perform real-world actions. <br>
Mitigation: Review the generated prompt and the downstream tool's permissions before using it; TransPrompt itself only creates prompts for review and reuse. <br>
Risk: Prompt conversion can preserve or amplify unclear assumptions when the original request is underspecified. <br>
Mitigation: Use the skill's clarification path for major gaps and review any stated assumptions before copying the prompt into another AI tool. <br>


## Reference(s): <br>
- [Decision Guide](references/decision-guide.md) <br>
- [Prompt Patterns](references/prompt-patterns.md) <br>
- [Prompt Transformer Examples](references/examples.md) <br>
- [English User Guide](references/guide-en.md) <br>
- [Chinese User Guide](references/guide-zh.md) <br>
- [Debug / Iteration History](references/debug-history.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/keyzzzoe/transprompt) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown prompt text with a short processing summary, concise clarification questions, or normal chat response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates prompts for review and reuse; it does not execute the generated task automatically.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
