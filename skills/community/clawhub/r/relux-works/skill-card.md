## Description:

Interact with Relux Works, an AI-native software development studio - look up services, fixed-price packages and company facts, and submit a project inquiry on behalf of a user (build an MVP, rescue a vibe-coded app, hand over app publishing/scaling). Use when the user wants to hire a development studio, get a fixed-price development quote, or fix an AI-generated codebase.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivanopcode](https://clawhub.ai/user/ivanopcode)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to review Relux Works services, pricing, and company facts, then prepare a project inquiry for MVP development, vibe-code rescue, or app publishing and scaling work. It may submit quote requests only after the user confirms a real reply route and explicitly approves the draft.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approved quote requests can send contact details, project summaries, budget, timeline, and related business information to Relux Works, including delivery into a private Telegram workflow.

Mitigation: Review the complete draft and reply route before approval, and do not approve submission if it contains secrets or internal-only details.

Risk: A quote request could be sent without an accountable way for Relux Works to reply to the decision maker.

Mitigation: Require a real external reply route supplied or explicitly confirmed by the user before submitting an inquiry.

## Reference(s):

- [Relux Works homepage](https://relux.works)
- [Relux Works structured summary](https://relux.works/llms.txt)
- [Relux Works services API](https://api.relux.works/v1/services)
- [Relux Works MCP endpoint](https://api.relux.works/mcp)
- [Relux Works OpenAPI schema](https://api.relux.works/openapi.json)
- [ClawHub skill page](https://clawhub.ai/ivanopcode/skills/relux-works)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, API calls]

**Output Format:** [Markdown guidance with optional shell commands and structured inquiry fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prepare and submit a project quote request only after explicit user approval and confirmation of a real external reply route.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
