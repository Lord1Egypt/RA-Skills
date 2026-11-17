## Description:

Helps UIBC government-domain teams assess identity and accountability after agent memory transfer using the TH-GOV-001 criteria.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

UIBC government-domain participants and reviewers use the skill to document memory-transfer identity criteria, assemble replayable evidence, and assign responsibility when a judgment fails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad government or migration terms may trigger this skill for unrelated requests.

Mitigation: Confirm the request concerns UIBC government-domain judging or TH-GOV-001 before applying its criteria.

Risk: A PASS from the bundled checker may be mistaken for proof of agent identity.

Mitigation: Treat PASS as a criteria-file structure check; independently review the judgment and supporting evidence.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/uibc-team-gov)
- [TH-GOV-001 criteria summary](artifact/判据_GOV.md)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Markdown judgments and evidence statements; plain-text PASS/FAIL criteria checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Judgments state the L0–L4 formalization level and include evidence and accountability statements.]

## Skill Version(s):

1.1.0 (source: server release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
