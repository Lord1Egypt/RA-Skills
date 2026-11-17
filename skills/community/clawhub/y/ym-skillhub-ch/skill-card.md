## Description:

Search, review, install, publish, update, and verify SkillHub skills using documented SkillHub CLI workflows and bundled helper scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyuming0823](https://clawhub.ai/user/liuyuming0823)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to find SkillHub packages, review and install third-party skills in isolation, publish or update their own skills, and check whether releases are live or still under review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The batch workflow can publish local skill folders publicly and synchronize GitHub repositories.

Mitigation: Run dry-run mode first, inspect the planned release targets, and use the publish-only stage when GitHub synchronization is not intended.

Risk: Installation guidance includes flattening commands that can move or delete skill directories.

Mitigation: Install into a quarantine directory first, review paths carefully, and back up or manually verify the destination before running move or delete commands.

Risk: The GitHub synchronization path may rely on a local helper script outside this skill package.

Mitigation: Inspect and trust the local push helper before use, or fall back to a standard reviewed git workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuyuming0823/skills/ym-skillhub-ch)
- [Publisher profile](https://clawhub.ai/user/liuyuming0823)
- [Server-resolved GitHub repository](https://github.com/liuyuming0823/ym-skillhub)
- [CHANGELOG](references/CHANGELOG.md)
- [SkillHub platform field reference](references/platform-fields.md)
- [Search and install reference](references/search-install.md)
- [Publishing troubleshooting reference](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, markdown]

**Output Format:** [Markdown guidance with inline shell commands, Python command invocations, checklists, and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May suggest running bundled helper scripts and SkillHub CLI commands; publishing workflows can make network calls and change local skill metadata.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
