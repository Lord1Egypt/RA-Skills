## Description:

Helps agents format WhatsApp-bound messages with WhatsApp-specific markup rules so recipients see clean styled text instead of raw Markdown syntax.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, agents, and end users can use this skill when preparing text for WhatsApp so bold, italic, lists, quotes, monospace text, and prohibited Markdown patterns are handled in the platform's expected style.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact contains boilerplate that mentions exec access, API keys, and network setup even though the security evidence describes the release as a markdown-only WhatsApp formatting skill.

Mitigation: Do not grant shell, network, or credential permissions for normal use; treat those sections as poor boilerplate unless a future release clearly justifies them.

Risk: Complex Markdown or special characters may still render incorrectly in WhatsApp-bound messages.

Mitigation: Review generated messages for raw Markdown markers, unsupported headers, tables, or malformed WhatsApp markup before sending.

## Reference(s):

- [WhatsApp Styler ClawHub Listing](https://clawhub.ai/thcjp/skills/whatsapp-style-guide)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [WhatsApp-ready message text with platform-specific markup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable output; intended for message wording and formatting guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
