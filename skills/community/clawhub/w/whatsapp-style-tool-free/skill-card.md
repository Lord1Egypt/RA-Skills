## Description: <br>
WhatsApp样式工具免费版 helps agents format, clean, preview, and validate WhatsApp-compatible message text using bold, italic, strikethrough, monospace, list, and quote syntax. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to convert Markdown-like message drafts into WhatsApp-compatible formatting and to check messages before sending. It is suited for personal messages, notifications, order updates, event announcements, and other formatted WhatsApp text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Message text may contain sensitive personal or business content. <br>
Mitigation: Use the skill only in trusted host agents and avoid providing sensitive message content when the processing environment is not trusted. <br>
Risk: The artifact mentions callback_url-style workflows without server evidence clarifying data flow. <br>
Mitigation: Do not use callback_url workflows unless the publisher clarifies how message content and callback data are handled. <br>
Risk: Documentation inconsistencies could produce imperfect WhatsApp formatting guidance. <br>
Mitigation: Preview or manually review formatted messages before sending them to recipients. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with text examples, optional Python snippets, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local text-formatting guidance and validation results; avoid sensitive message content unless the host agent is trusted.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
