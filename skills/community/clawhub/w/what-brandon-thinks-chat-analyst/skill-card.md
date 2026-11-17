## Description:

Turns anonymized WhatsApp or iMessage observations into evidence-aware analysis briefs, interaction-signal summaries, and cautious claim audits for relationship, friendship, family, group-chat, reciprocity, effort, tone-shift, and turning-point questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gpt-img-2](https://clawhub.ai/user/gpt-img-2)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to examine anonymized chat observations while keeping facts, interpretations, alternatives, unknowns, confidence, and next checks distinct.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional MCP setup can run unpinned code from GitHub with npx.

Mitigation: Install the MCP only from a trusted source, preferably using a pinned commit, audited release, checksum, or sandboxed setup before using it with sensitive conversations.

Risk: Chat exports and excerpts can contain sensitive personal information or third-party details.

Mitigation: Use aliases, aggregate counts, and short necessary excerpts; remove passwords, payment data, identity documents, health records, addresses, and unrelated third-party details.

Risk: Incomplete conversation records can lead to overconfident interpretations about intent or relationships.

Mitigation: Keep observable facts separate from interpretations and unknowns, include alternative explanations, label confidence, and route high-stakes decisions to qualified human support.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/gpt-img-2/skills/what-brandon-thinks-chat-analyst)
- [Sample report](https://whatbrandonthinks.org/sample-report)
- [WhatsApp analyzer](https://whatbrandonthinks.org/whatsapp-chat-analyzer)
- [iMessage analyzer](https://whatbrandonthinks.org/imessage-chat-analyzer)
- [Safety and deletion](https://whatbrandonthinks.org/safety)
- [Raw Skill](https://whatbrandonthinks.org/skills/what-brandon-thinks-chat-analyst/SKILL.md)
- [Optional MCP source](https://github.com/gpt-img-2/whatbrandonthinks-chat-mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown sections with optional inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces evidence-aware analysis briefs and may provide optional MCP setup guidance when requested.]

## Skill Version(s):

1.0.0 (source: release evidence and openclaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
