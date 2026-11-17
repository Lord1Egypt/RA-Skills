## Description:

Install and initialise Tribunal, the Claude Code quality enforcement plugin, when setting up AI-assisted development with TDD enforcement, secret scanning, Claude Code quality gates, or Tribunal project protection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[koshaji](https://clawhub.ai/user/koshaji)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to install, initialize, verify, and troubleshoot Tribunal quality enforcement in Claude Code projects. It is intended for projects that need TDD enforcement, secret scanning, quality gates, hook checks, or CI-oriented Tribunal checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill tells agents to install and immediately run an unpinned external tool that modifies Claude Code project settings and hooks.

Mitigation: Review the Tribunal package source and version before installing, avoid the one-line install-and-run command in sensitive repositories, prefer a pinned local install where possible, and inspect changes to .claude/settings.json and generated hooks before use.

## Reference(s):

- [Tribunal documentation](https://tribunal.dev)
- [Tribunal repository](https://github.com/thebotclub/tribunal)
- [ClawHub skill page](https://clawhub.ai/koshaji/skills/tribunal-install)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance with shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides installation, project initialization, setup verification, quality pack installation, and standalone CI checks.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
