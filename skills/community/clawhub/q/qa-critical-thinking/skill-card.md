## Description:

Helps QA reviewers challenge hidden assumptions in requirements and test cases to uncover overlooked failure scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT-0

## Use Case:

QA testers and developers use this skill to review requirements and test cases, challenge implicit assumptions, and identify missing edge cases and risks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases may invoke this skill outside a QA review.

Mitigation: Use it only for testing or requirement-review tasks.

Risk: Requirements and test cases may contain sensitive customer, payment, identity, or production data.

Mitigation: Remove or mask sensitive data before sharing it with the agent.

Risk: The optional install command fetches a larger, unpinned skill package.

Mitigation: Review the full package before running the optional install command.

## Reference(s):

- [Critical thinking exercises](references/thinking-exercises.md)
- [ClawHub skill release](https://clawhub.ai/kokxi/skills/qa-critical-thinking)

## Skill Output:

**Output Type(s):** [Analysis, Guidance]

**Output Format:** [Markdown text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Identifies thinking gaps, challenged assumptions, alternative scenarios, and reassessed risks; link findings to requirement or scenario IDs when available.]

## Skill Version(s):

1.8.0 (source: skill frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
