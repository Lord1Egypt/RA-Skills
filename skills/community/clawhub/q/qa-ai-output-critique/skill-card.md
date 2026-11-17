## Description:

Reviews AI-generated test cases for completeness, correctness, executability, risk coverage, formatting, consistency, traceability, and redundancy, and recommends specific corrections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers and developers use this skill to review AI-generated test cases before accepting them, identify missing coverage or unclear steps, and prioritize revisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad QA review phrases may trigger this review when it is not intended.

Mitigation: Confirm the requested review scope and input test cases before applying the gate.

Risk: The optional installation command runs third-party package tooling.

Mitigation: Independently verify the package and command before running it.

Risk: Recommendations to merge or remove test cases could discard useful coverage.

Mitigation: Back up original test cases and review coverage before making bulk changes.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/kokxi/skills/qa-ai-output-critique)
- [Review dimensions and scoring](references/review-dimensions.md)
- [Deep review techniques](references/deep-review-techniques.md)
- [Critique report template](assets/critique-report.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown critique report with dimension scores, labeled findings, coverage gaps, improvement actions, and a review decision]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings reference the reviewed test case IDs; documented gaps cite available requirement, scenario, or risk IDs.]

## Skill Version(s):

1.8.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
