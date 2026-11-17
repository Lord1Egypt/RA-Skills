## Description:

Guides a final, risk-aware review of AI-generated test cases for business validity, scenario coverage, and executability before release.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers and reviewers use this skill to sample and assess AI-generated test cases, document defects and corrections, and feed recurring findings into future test-case generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the suggested broader skill set could run code from an unverified source.

Mitigation: Verify the Kokxi/qa-test-skills source and prefer a pinned version or trusted commit before running the suggested npx command.

Risk: Sampling can miss important gaps in AI-generated test cases.

Mitigation: Review all highest-priority and high-risk cases, trace coverage to available requirements, and repeat review after correcting systematic gaps.

## Reference(s):

- [Meta-learning reference](references/meta-learning.md)
- [ClawHub skill release](https://clawhub.ai/kokxi/skills/qa-expert-review)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown review report with scores, issue table, corrections, and improvement recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes review and test-case IDs, sampling rate, requirements traceability, and prompt-optimization suggestions.]

## Skill Version(s):

1.8.0 (source: skill frontmatter and ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
