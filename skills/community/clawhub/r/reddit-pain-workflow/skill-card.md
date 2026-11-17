## Description:

Automates a daily workflow that scans Reddit communities, classifies developer pain points, generates Markdown reports, pushes them to GitHub, and tracks metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[minirr890112-byte](https://clawhub.ai/user/minirr890112-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation maintainers use this skill to schedule Reddit scans, classify recurring developer pain points, and publish Markdown reports to a GitHub repository for product research and content planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The described workflow can push generated reports to a GitHub repository.

Mitigation: Confirm the target repository before use and run with narrowly scoped GitHub credentials.

Risk: Scheduled Reddit scanning may rely on Reddit credentials or access tokens.

Mitigation: Use narrowly scoped Reddit credentials and review rate limits, retention, and community rules before running the workflow on a schedule.

Risk: Automated classification can mislabel community posts or overstate product pain signals.

Mitigation: Review generated reports before publishing or using them for product or content decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/minirr890112-byte/skills/reddit-pain-workflow)
- [HermesMade project page](https://github.com/minirr890112-byte/HermesMade)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces scheduled workflow guidance and Markdown-style daily pain point reports; no bundled executable code is included in the skill artifact.]

## Skill Version(s):

1.1.0 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
