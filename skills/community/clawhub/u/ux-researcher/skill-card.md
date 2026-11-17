## Description:

Generate user personas, pain points, journey maps, and UX recommendations without conducting interviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Product teams, founders, designers, and agents use this skill to produce synthetic UX research deliverables for product ideas or existing products. It supports persona generation, pain point analysis, journey mapping, heuristic evaluation, competitive UX analysis, and prioritized UX recommendations based on domain patterns rather than user interviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can ask the agent to save broad future activation preferences in shared memory.

Mitigation: Keep activation preferences session-local or store only narrowly scoped settings under ~/ux-researcher/ with clear instructions for viewing and deleting them.

Risk: Synthetic UX research may be mistaken for evidence from real user interviews.

Mitigation: Label outputs as based on domain patterns and validate major product decisions with real users before acting on them.

Risk: Local research notes may contain product context or sensitive planning details.

Mitigation: Review what is stored under ~/ux-researcher/ and avoid saving confidential product information unless local retention is acceptable.

## Reference(s):

- [UX Researcher on ClawHub](https://clawhub.ai/ivangdavila/skills/ux-researcher)
- [UX Researcher homepage](https://clawic.com/skills/ux-researcher)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown research deliverables and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local Markdown notes and research files under ~/ux-researcher/ when memory is enabled.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
