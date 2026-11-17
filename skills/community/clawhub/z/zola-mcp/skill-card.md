## Description:

This skill helps an agent work with Zola wedding planning data, including vendors, budget, guests, seating, RSVPs, events, registry, gifts, and marketplace discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to manage Zola wedding planning records and retrieve planning status across vendors, guests, budget, seating, RSVPs, registry, and gifts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose sensitive wedding-planning data such as guest addresses, RSVPs, invitations, budget, vendors, registry, and gifts.

Mitigation: Install only when the agent is intended to access this Zola data, and review outputs before sharing or acting on them.

Risk: The skill describes write-capable actions for vendors, guests, addresses, seating, events, invitations, budget items, and registry reconciliation.

Mitigation: Require explicit user review before any add, update, remove, invite, seating, budget, or bulk event change.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chrischall/skills/zola-mcp)
- [Publisher profile](https://clawhub.ai/user/chrischall)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, guidance]

**Output Format:** [Markdown or plain text responses that may summarize tool results and propose wedding-planning actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve sensitive wedding-planning records and write-capable actions through Zola-related tools]

## Skill Version(s):

1.7.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
