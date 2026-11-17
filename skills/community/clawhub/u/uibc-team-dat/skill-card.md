## Description:

Helps agents apply UIBC DAT criterion TH-DAT-001 to memory-transfer identity judgments, evidence, and accountability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT

## Use Case:

Developers and evaluators assessing agent-memory transfers use the DAT-domain criteria to draft judgment rules, replayable evidence requirements, and failure-handling and accountability statements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger terms may cause DAT-domain judging criteria to be applied to loosely related requests.

Mitigation: Confirm that the request calls for UIBC DAT-domain judging before applying TH-DAT-001.

Risk: A PASS from the bundled checker may be mistaken for proof that a memory transfer preserves identity.

Mitigation: Treat PASS as a check of the criteria file, and require independent review of transfer evidence and accountability conclusions.

## Reference(s):

- [DAT-domain judging criteria (TH-DAT-001)](artifact/判据_DAT.md)
- [ClawHub skill listing](https://clawhub.ai/zhaoxinghua09-cell/skills/uibc-team-dat)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Judgment rules, evidence-package guidance, and responsibility statements; the local criteria checker reports PASS/FAIL on the bundled criteria file.]

## Skill Version(s):

1.1.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
