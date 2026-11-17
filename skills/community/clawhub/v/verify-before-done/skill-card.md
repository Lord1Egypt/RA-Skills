## Description:

A completion contract for agents. Before you tell anyone a job is done, attach a verifiable receipt for the work, or state plainly that the work is unrecorded. Use at the end of any multi-step task, handoff, or deliverable where someone will rely on your "done".

This skill is ready for commercial/non-commercial use.

## Publisher:

[zambodotdev](https://clawhub.ai/user/zambodotdev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI agents use this skill at the end of multi-step work, handoffs, or deliverables to report completion with a verifiable receipt or clearly state that the work is unrecorded.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task details in external work records may expose private information; anyone with a shared link may view the page, and automatic redaction can miss sensitive content.

Mitigation: Decide which task details may be recorded, review content before sharing links, and check the provider's retention terms. For confidential work, use an approved recording provider or the skill's unrecorded-work fallback.

## Reference(s):

- [Verify Before Done on ClawHub](https://clawhub.ai/zambodotdev/skills/verify-before-done)
- [Zambo handover guide](https://zambo.dev/handover/)
- [Zambo privacy policy](https://zambo.dev/privacy/)
- [Zambo MCP endpoint](https://zambo.dev/mcp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown completion report with receipt links or an explicit unrecorded-work statement]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include verified receipt identifiers and links.]

## Skill Version(s):

1.0.4 (source: server-resolved ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
