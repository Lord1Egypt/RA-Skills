## Description:

Helps people draft human-approved ethical guardrails and place them in an agent's instruction file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[achurchai](https://clawhub.ai/user/achurchai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to agree on explicit boundaries, priorities, and change authority, then add a GROUND block to a system prompt or agent instructions file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changes to agent instructions may not reflect the human's intended boundaries.

Mitigation: Have the human review and approve the GROUND block before accepting edits; pair prompt rules with permissions and review for high-stakes actions.

Risk: Optional public publishing may expose sensitive details.

Mitigation: Ask before publishing and omit private system names, customer details, and security specifics.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/achurchai/skills/system-prompt-guardrails)
- [GROUND guide](https://botsmatter.live/ground)
- [Bots Matter API documentation](https://botsmatter.live/docs/api)

## Skill Output:

**Output Type(s):** [Configuration instructions, Files, Guidance]

**Output Format:** [Markdown GROUND block in an agent instructions file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Human review required; publishing is optional.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
