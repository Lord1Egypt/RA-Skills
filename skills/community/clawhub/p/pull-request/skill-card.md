## Description:

Create high-quality pull requests with pre-submission validation, maintainer-friendly formatting, and automated quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and engineering agents use this skill before creating or suggesting pull requests to check repository contribution requirements, validate scope, disclose AI assistance when applicable, and prepare maintainer-friendly PR descriptions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated pull request changes or descriptions may be incorrect, incomplete, or misaligned with a target repository's contribution policy.

Mitigation: Review generated code and PR text before opening a pull request, read the target repository's contribution files, and disclose testing limitations.

Risk: Pull request preparation may expose private repository context or secrets if the agent reads or shares sensitive files.

Mitigation: Avoid sharing secrets or private repository content unnecessarily and follow the skill's guidance to avoid reading or logging secret and credential files.

## Reference(s):

- [Pull Request skill source](artifact/SKILL.md)
- [Pull Request checklist](artifact/checklist.md)
- [Pull Request red flags](artifact/red-flags.md)
- [Repository context gathering](artifact/repo-context.md)
- [Pull Request templates](artifact/templates.md)
- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/pull-request)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown guidance with checklists, templates, and inline command suggestions when repository workflows call for them]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces review-ready pull request guidance and descriptions; it does not execute hidden code or require credentials.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
