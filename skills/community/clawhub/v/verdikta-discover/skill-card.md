## Description:

Helps agents decide when public, bounded work needs outside help and prepare a read-only work-order assessment with acceptance criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nigelon11](https://clawhub.ai/user/nigelon11)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their operators use this skill to check what they can resolve locally and scope independent source checks, public-artifact reviews, evidence packs, or real-world tasks for outside work. It prepares a preview rather than commissioning or paying for work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A work-order preview could expose sensitive task details if shared externally.

Mitigation: Use only public, non-sensitive inputs and review the assessment before sharing it.

Risk: A preview could be mistaken for authorization to commission or fund work.

Mitigation: Keep the planning agent free of wallets and secrets; obtain separate owner authorization for funding or commissioning.

## Reference(s):

- [Verdikta Discover on ClawHub](https://clawhub.ai/nigelon11/skills/verdikta-discover)
- [Service templates](references/service-templates.md)
- [Drafting guidance](references/drafting.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Markdown decision and, when authorized, JSON assessment input for a work-order preview]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only planning; no purchase, upload, signing, or spending.]

## Skill Version(s):

1.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
