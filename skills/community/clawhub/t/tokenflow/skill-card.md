## Description:

Converts files and URLs to structured text through the TokenFlow API with per-filetype conversion settings and fallback behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kolemaravilla](https://clawhub.ai/user/kolemaravilla)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to let an agent convert supported documents, spreadsheets, archives, audio files, and pasted URLs into structured text for downstream analysis or conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected files, pasted URLs, and possibly authentication data may be sent to TokenFlow's external service.

Mitigation: Use the skill only for data approved for external processing, avoid confidential documents, regulated data, internal-only URLs, and secrets, and review TokenFlow data handling before broader deployment.

Risk: Broad conversion triggers can automatically send supported attachments or URLs with limited consent guidance.

Mitigation: Configure ask-before-convert behavior or skip rules for sensitive file types, and require explicit user approval where conversion could expose private content.

Risk: Quota, size, unsupported-format, timeout, or service errors can prevent conversion and return the original file instead.

Mitigation: Keep fallback behavior visible to users, check quota and service status when conversion fails, and verify important outputs against the source file.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kolemaravilla/skills/tokenflow)
- [TokenFlow Service](https://tokenflow.ironlion.cc)
- [TokenFlow API Endpoint](https://tokenflow.fly.dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown or HTML text, with JSON responses for structured conversion results and status data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOKENFLOW_API_KEY and network access; output depends on per-filetype conversion settings, retry count, and fallback behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata and release changelog, released 2026-04-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
