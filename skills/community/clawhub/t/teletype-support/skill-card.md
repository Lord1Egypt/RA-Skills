## Description:

Guides Teletype support teams through inbox triage, customer replies, client summaries, issue escalation, and shift handovers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[warlikelaux](https://clawhub.ai/user/warlikelaux)

### License/Terms of Use:

MIT-0

## Use Case:

Support agents and operators use this skill to review Teletype conversations, prepare customer-facing replies for approval, summarize client history, escalate issues, and hand over an unanswered queue.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A project API token could be exposed during setup.

Mitigation: Keep the token in private configuration or environment variables; never paste it into chat or public files.

Risk: An outbound reply or conversation change could target the wrong customer or contain an unverified promise.

Mitigation: Verify the project identity, preview ambiguous targets, separate confirmed facts from proposed actions, and obtain explicit approval for each change.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/warlikelaux/skills/teletype-support)
- [Connection instructions](references/installation.md)
- [Teletype MCP client setup guide](https://github.com/Teletype-App/teletype-mcp-server/blob/main/docs/CLIENTS.md)
- [Teletype MCP client setup guide (Russian)](https://github.com/Teletype-App/teletype-mcp-server/blob/main/docs/ru/CLIENTS.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Configuration instructions, Shell commands]

**Output Format:** [Markdown summaries, draft replies, tables, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Customer replies and conversation changes require explicit approval.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
