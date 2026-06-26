## Description: <br>
Adapt markdown-style replies into Telegram-friendly rich text without broken rendering for Telegram destinations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lqqk7](https://clawhub.ai/user/lqqk7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and assistants use this skill to rewrite Markdown-heavy replies into Telegram-readable rich text while preserving structure, emphasis, lists, code snippets, and links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram rendering may change message presentation through bold labels, compact lists, HTML tags when supported, or message splitting. <br>
Mitigation: Review the final Telegram output for meaning and readability before sending important messages. <br>
Risk: Unsupported HTML tags or unescaped characters can break Telegram rich-text rendering. <br>
Mitigation: Use only the documented safe Telegram HTML subset, escape raw angle brackets and ampersands, and fall back to structured plain text when parse-mode support is uncertain. <br>


## Reference(s): <br>
- [Telegram Format Rules](references/telegram-format-rules.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Telegram-safe structured text or Markdown-style rich text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend compact message splitting, safe Telegram HTML tags, shallow lists, visible links, and concise code formatting.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
