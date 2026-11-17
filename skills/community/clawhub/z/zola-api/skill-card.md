## Description:

Query or update Zola wedding-planning data (vendors, budget, guests, seating, events/RSVPs, registry, gift tracker, inquiries, wedding website) straight from a shell with curl against mobile-api.zola.com, instead of running the zola-mcp server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and wedding planners can ask an agent to retrieve or update wedding-planning details in Zola from a shell, including guest, event, vendor, budget, registry, and website data, without running the Zola MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan marks the skill suspicious for handling a long-lived account credential and for QR-code and card-project capabilities beyond the stated wedding-planning purpose; its inspection was partial.

Mitigation: Follow the scanner guidance before installing: confirm the token is loaded without being printed and clarify or remove the QR-code and card-project capabilities. Keep the token out of command output and shared text.

## Reference(s):

- [Zola mobile API endpoint recipes](artifact/references/mobile-api-endpoints.md)
- [Zola](https://www.zola.com)
- [Zola mobile API](https://mobile-api.zola.com)

## Skill Output:

**Output Type(s):** [JSON data, Text]

**Output Format:** [Zola API JSON responses with concise text summaries; shell commands when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include read or write results for wedding-planning records.]

## Skill Version(s):

2.2.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
