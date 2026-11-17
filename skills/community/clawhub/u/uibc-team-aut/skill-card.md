## Description:

Guides UIBC autonomous-driving team reviewers in assessing memory-transfer identity and accountability against criterion TH-AUT-001.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

UIBC team members and reviewers use the AUT-domain criterion to document memory-transfer identity decisions, replayable evidence, failure handling, and accountability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad AUT/UIBC trigger terms may activate the skill outside its intended judging task.

Mitigation: Confirm the user needs TH-AUT-001 judging before applying its guidance.

Risk: Primarily Chinese-language criteria may be hard for English-only reviewers to assess.

Mitigation: Provide a translation for review and check it against the original criterion.

Risk: A checker PASS may be mistaken for proof of the identity decision rather than criterion-file completeness.

Mitigation: Review the actual migration evidence and decision separately; use PASS only to confirm the criterion file's structure.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/uibc-team-aut)
- [AUT-domain judging criterion (TH-AUT-001)](判据_AUT.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Text]

**Output Format:** [Markdown decision rules and evidence descriptions; plain-text checker results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checker emits PASS/FAIL for criterion structure; proposed deliverables include an evidence package and accountability statement.]

## Skill Version(s):

1.1.0 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
