## Description:

Help someone export a WhatsApp, iMessage, KakaoTalk, LINE, Instagram or Messenger conversation and read it carefully, separating what the messages show from what they cannot prove.

This skill is ready for commercial/non-commercial use.

## Publisher:

[niallferguson6](https://clawhub.ai/user/niallferguson6)

### License/Terms of Use:

MIT-0

## Use Case:

External users can follow platform-specific steps to export a chat and get a grounded reading of repeated communication patterns. The skill helps distinguish message evidence from possible interpretations and unknowns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chat exports may contain sensitive personal details or information about other people.

Mitigation: Only analyze conversations the user has a right to use, and remove passwords, financial details, addresses, health information, and unrelated third-party details before sharing an export.

Risk: The scanner did not assess the destinations of six Markdown links, so their content and privacy practices were not verified.

Mitigation: Review linked pages and their privacy terms before using an external service; do not send chat content to tools or the read-only MCP server.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/NiallFerguson6/whatbrandonthinks-mcp/tree/main/skills/what-brandon-thinks-chat-report)
- [What Brandon Thinks](https://whatbrandonthinks.net)
- [WhatsApp export guide](https://whatbrandonthinks.net/whatsapp-chat-analyzer)
- [iMessage chat analyzer](https://whatbrandonthinks.net/imessage-chat-analyzer)
- [KakaoTalk chat analyzer](https://whatbrandonthinks.net/kakaotalk-chat-analyzer)
- [Relationship chat analyzer](https://whatbrandonthinks.net/relationship-chat-analyzer)
- [Sample report](https://whatbrandonthinks.net/sample-report)
- [Privacy and limitations review](https://whatbrandonthinks.net/what-brandon-thinks-review)
- [Hosted report setup](https://whatbrandonthinks.net/setup)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, Shell commands, Configuration]

**Output Format:** [Markdown with platform export steps, evidence-based chat analysis, and optional JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
