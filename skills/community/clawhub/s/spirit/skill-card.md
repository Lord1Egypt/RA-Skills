## Description:

SPIRIT preserves AI agent identity, memory, and project files to a private Git repository and provides workspace-mode sync guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gopinathnelluri](https://clawhub.ai/user/gopinathnelluri)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to initialize and schedule SPIRIT syncs so agent identity, memory, and selected project files can be backed up to a private Git repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended sync can continuously back up sensitive agent memory, identity, and project files to a remote repository.

Mitigation: Review exactly what .spirit-tracked will sync, use a private repository with least-privilege credentials, start with manual syncs, and enable cron or autobackup only when continuous remote backups are intentional.

Risk: Restore and authentication flows can expose credentials or run unreviewed installer code.

Mitigation: Prefer the declared Homebrew install or a pinned verified release, avoid the curl-to-bash restore path, avoid tokens in remote URLs, and do not use persistent git credential.helper store for this workflow.

## Reference(s):

- [SPIRIT Cron Setup Guide](references/cron-setup.md)
- [SPIRIT project](https://github.com/TheOrionAI/spirit)
- [GitHub CLI](https://cli.github.com)
- [ClawHub skill listing](https://clawhub.ai/gopinathnelluri/skills/spirit)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash command examples and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the spirit and git command-line tools; the release metadata declares a Homebrew install for the spirit CLI.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
