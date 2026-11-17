## Description:

Control Tokei waitlist and giveaway campaigns from an agent by creating and managing pages, entries, analytics, and webhooks through the CLI or MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gilesdawe](https://clawhub.ai/user/gilesdawe)

### License/Terms of Use:

MIT

## Use Case:

Developers and campaign operators use the skill to manage Tokei launch, waitlist, and giveaway pages; review signups and campaign analytics; and configure webhooks. Write actions that affect public pages or participants should follow the documented human-approval guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Write-enabled access can publish or change public campaigns, import participants, or create live webhooks.

Mitigation: Use an expiring read-only key unless writes are needed, and require human approval before public changes, participant imports, or live webhooks.

Risk: Participant data and webhook signing secrets require careful handling.

Mitigation: Protect participant data and webhook secrets, use only trusted webhook destinations, and record marketing consent only when it is actually collected.

## Reference(s):

- [Tokei agent documentation](https://tokei.io/agent)
- [Tokei API reference](https://tokei.io/docs/api)
- [Tokei product website](https://tokei.io)
- [ClawHub release page](https://clawhub.ai/gilesdawe/skills/tokei-agent)
- [npm package](https://www.npmjs.com/package/tokei-agent)

## Skill Output:

**Output Type(s):** [JSON, Shell commands]

**Output Format:** [JSON API responses from CLI commands or MCP tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOKEI_API_KEY; Node.js 22.12 or later. Responses can include campaign and participant information.]

## Skill Version(s):

0.3.8 (source: package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
