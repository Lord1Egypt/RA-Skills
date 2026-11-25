## Description:

Designs structured test cases for functional, compatibility, API, UI, platform-specific, and AI agent testing from requirements or existing cases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cassianran](https://clawhub.ai/user/cassianran)

### License/Terms of Use:

MIT-0

## Use Case:

QA professionals, product teams, and developers use the skill to turn requirements into structured test cases or identify gaps and add cases to an existing suite.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-volume API test cases could send excessive traffic to an unapproved target.

Mitigation: Run high-volume tests only against an approved target with a defined traffic limit.

Risk: Security review coverage is partial because one referenced local path could not be resolved.

Mitigation: Review the unresolved reference and applicable instructions before relying on related test guidance.

## Reference(s):

- [Common test case rules](artifact/references/templates/common-rules.md)
- [Functional testing guidance](artifact/references/core-capabilities/functional-testing.md)
- [API testing guidance](artifact/references/core-capabilities/api-testing.md)
- [Agent testing guidance](artifact/references/core-capabilities/agent-testing.md)
- [Test case output format](artifact/references/examples/format-spec.md)
- [ClawHub skill release](https://clawhub.ai/cassianran/skills/test-case-design)

## Skill Output:

**Output Type(s):** [Text, Markdown, Test case guidance]

**Output Format:** [Markdown tables of structured test cases, with assumptions or coverage notes when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on test case design; does not produce test plans, strategies, or automation scripts.]

## Skill Version(s):

1.0.9 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
