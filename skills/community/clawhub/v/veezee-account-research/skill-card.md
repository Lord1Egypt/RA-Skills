## Description:

Deep research on one target company before outreach, covering company facts, key people, and recent posts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veezee-build](https://clawhub.ai/user/veezee-build)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, customer success, and account teams use this skill to prepare for outreach or calls with one target company by collecting LinkedIn-based company facts, recent posts, and relevant people.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account-research queries and usage metadata are sent to Veezee.

Mitigation: Confirm that the user is comfortable using a third-party API before running the workflow.

Risk: The all-tools MCP endpoint exposes more capability than this LinkedIn-only workflow needs.

Mitigation: Use the LinkedIn-scoped MCP endpoint for this skill.

Risk: A full account briefing can exceed the free daily trial budget or spend more credits than intended.

Mitigation: Check usage first and set max_credits on each paid call.

Risk: The optional npx SDK command can run an unpinned package and store an API key locally.

Mitigation: Review or pin the SDK version and confirm where credentials are stored before using the command.

## Reference(s):

- [Account Research on ClawHub](https://clawhub.ai/veezee-build/skills/veezee-account-research)
- [Veezee LinkedIn MCP endpoint](https://mcp.veezee.io/linkedin)
- [Veezee key mint API](https://api.veezee.io/v1/keys/mint)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown briefing with concise company facts, recent posts, key people, and credits spent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Point-in-time LinkedIn-only account briefing; does not provide emails, phone numbers, or monitoring.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
