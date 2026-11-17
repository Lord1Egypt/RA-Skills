## Description:

Reads a SimplePractice Client Portal for appointments, billing records, saved payment methods, paperwork, documents, and practice announcements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

External users with a SimplePractice Client Portal can ask an agent to retrieve their appointments, balances and billing records, saved payment methods, outstanding paperwork, documents, and practice announcements. Confirm whose records are in scope before sharing results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP server receives sign-in links and accesses private health and billing records; its storage protections were unavailable for review.

Mitigation: Use only a trusted SimplePractice MCP server and confirm whose records are in scope before sharing results.

Risk: Local sign-out forgets the saved session but does not revoke the SimplePractice session token.

Mitigation: Describe sign-out as clearing the server's saved session, not as signing the user out of SimplePractice.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/chrischall/skills/simplepractice)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Natural-language summaries of Client Portal records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contain private health and billing information.]

## Skill Version(s):

1.3.1 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
