## Description:

Analyze OpenClaw SKILL.md files to generate usage guides with examples, best practices, configuration details, common pitfalls, comparisons, and recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoxiao19810912](https://clawhub.ai/user/xiaoxiao19810912)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to inspect SKILL.md files and quickly understand how a skill works, how to invoke it, and what examples, configuration details, warnings, and best practices are documented. It also supports bulk skill indexing, skill comparison, combination discovery, and task-based recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can enumerate and summarize installed OpenClaw skills, which may expose local skill inventory or workflow details in generated reports.

Mitigation: Run it only in workspaces where that inventory may be inspected, and review generated text, Markdown, or JSON before sharing it.

Risk: The installer can overwrite an existing skill-usage-analyzer directory after user confirmation.

Mitigation: Preserve local changes before approving overwrite prompts during installation.

Risk: Unpinned installation through a package runner can execute a changing ClawHub CLI distribution.

Mitigation: Use a pinned or already trusted ClawHub CLI when installing this release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoxiao19810912/skills/skill-usage-analyzer)
- [README](README.md)
- [CHANGELOG](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text, Markdown, or JSON reports with command examples and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports and indexes can be printed to stdout or written to a user-specified output path.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, CHANGELOG.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
