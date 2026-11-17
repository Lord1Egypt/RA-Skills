## Description:

Helps QA teams plan and troubleshoot non-production test environments, manage configurations, and prepare and maintain test data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kokxi](https://clawhub.ai/user/kokxi)

### License/Terms of Use:

MIT-0

## Use Case:

QA engineers and developers use this skill to check test-environment health, plan environment setup and maintenance, and prepare, mask, and clean up test data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Environment changes or test-data cleanup could disrupt shared services or remove needed data.

Mitigation: Confirm the exact authorized non-production target, backup, approval, rollback path and team coordination before changes; dry-run or test on a small scope first.

Risk: The optional companion-skill installation uses an unpinned npx command.

Mitigation: Install only from a trusted source and pin or verify the package and version before running the command.

## Reference(s):

- [Test data management reference](artifact/references/data-management.md)
- [qa-test-env-data release on ClawHub](https://clawhub.ai/kokxi/skills/qa-test-env-data)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration guidance]

**Output Format:** [Markdown checklists and environment-management guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes environment requirements, design, configuration and maintenance plans; environment configurations use ENV-XXXX identifiers.]

## Skill Version(s):

1.8.0 (source: skill frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
