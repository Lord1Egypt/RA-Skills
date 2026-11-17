## Description:

Helps medical-device teams assess recall severity against NMPA rules and prepare a structured decision for human review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Medical-device quality and regulatory teams use this skill to review product defects, estimate recall levels and notification obligations, and document regulatory references for human assessment. It does not replace a regulator's final determination.

### Deployment Geography for Use:

China (NMPA regulatory context)

## Known Risks and Mitigations:

Risk: The skill requests local command, file-write, and web access beyond its prompt-only workflow.

Mitigation: Review before installing; remove or tightly limit command and write permissions and restrict web retrieval to official regulatory sources.

Risk: An incorrect recall classification or regulatory reference could mislead a compliance decision.

Mitigation: Check cited rules and proposed obligations against current official texts and require qualified human review before acting.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zhaoxinghua09-cell/skills/recall-decision-checker)
- [LGD theory background (linked in README; not release provenance)](https://github.com/zhaoxinghua09-cell/lgd-theory)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requested JSON IR includes a recommended recall level, regulatory references, and a confidence score; the README also describes notification deadlines, obligations, and warnings. Human review is required.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
