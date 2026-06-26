## Description: <br>
Smart Prompt Builder generates structured Chinese fiction-writing prompts from scene type, context, corpus snippets, and optional voice-profile style settings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuzhihui886](https://clawhub.ai/user/yuzhihui886) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, writers, and agent builders use this skill to assemble reusable writing prompts for description, dialogue, action, and emotion scenes. It can incorporate story context, retrieved corpus examples, and voice-profile configuration before handing the prompt to a downstream generation step. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional LLM builder can send writing context and voice-profile style data to DashScope when DASHSCOPE_API_KEY is configured. <br>
Mitigation: Use the local scripts/build_prompt.py path for local-only prompt construction, or review and approve any context before running scripts/build_prompt_llm.py. <br>
Risk: License evidence is inconsistent between server metadata and artifact documentation. <br>
Mitigation: Confirm the authoritative license before publishing or relying on redistribution terms. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuzhihui886/smart-prompt-builder) <br>
- [DashScope chat completions endpoint](https://coding.dashscope.aliyuncs.com/v1/chat/completions) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or JSON prompt structures with optional Markdown-style command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Local prompt construction can produce terminal or file output; the optional LLM builder sends context and style data to DashScope when configured.] <br>

## Skill Version(s): <br>
2.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
