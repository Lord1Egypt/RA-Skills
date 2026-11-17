## Description:

Skill Discoverer helps users find suitable skills, recommend skill combinations by task type, and provide usage guidance and tutorials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pagoda111king](https://clawhub.ai/user/pagoda111king)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ClawHub users use this skill to discover relevant skills, compare recommendations for a task, assemble skill combinations, and receive onboarding guidance for selected skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests command execution and file-write permissions beyond the needs described by its recommendation behavior.

Mitigation: Install only after reviewing and reducing requested permissions to the minimum needed for search, recommendation, and guidance workflows.

Risk: The security guidance flags the dev dependency lockfile for attention before tests or CI are run.

Mitigation: Update and review the development dependency lockfile before using this package in automated test or CI environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pagoda111king/skills/skill-discoverer-pro)
- [Skill Discoverer documentation](https://docs.cloud-shrimp.com/skill-discoverer)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown or structured text with recommendation lists, usage guides, and JavaScript helper outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include ranked skill matches, task-type recommendations, skill-combination workflows, and onboarding steps.]

## Skill Version(s):

0.1.0 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
