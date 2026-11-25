## Description:

Write the first DM after a LinkedIn connection request is accepted, or after a comment exchange turns into a connection. The goal is to open a real conversation, not pitch. Returns 3 short, warm, specific options that earn a reply, referencing the real exchange when the person came from the user's comments. Use when the user just got a new connection and does not know what to say, or always falls into the auto-pitch trap. Requires the Taplio MCP to pull the user's voice and the comment thread the connection started from.

This skill is ready for commercial/non-commercial use.

## Publisher:

[porenes](https://clawhub.ai/user/porenes)

### License/Terms of Use:

MIT-0

## Use Case:

LinkedIn users can use the skill to draft a first message to a new connection or continue a comment exchange. It creates three concise, personalized opener options using the user's voice and available LinkedIn context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A suggested opener could misstate or over-share a person's comment, post, or connection context if the source is mismatched or stale.

Mitigation: Check the recipient and referenced LinkedIn activity before sending; remove details that are inaccurate or too personal.

Risk: Some references in the skill could not be matched to bundled files, so their destinations were not fully covered by the review.

Mitigation: Verify referenced links before following setup instructions or relying on their contents.

## Reference(s):

- [Taplio LinkedIn DM Opener on ClawHub](https://clawhub.ai/porenes/skills/taplio-linkedin-dm-opener)
- [Taplio MCP](https://mcp.taplio.com)
- [Taplio Claude connector setup](https://claude.ai/customize/connectors/id/taplio)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown with three drafted LinkedIn message options]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Three options, each under 600 characters, with one recommended option and a brief rationale. Drafts are for the user to paste into LinkedIn; the skill cannot send messages.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
