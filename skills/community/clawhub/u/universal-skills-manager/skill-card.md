## Description:

The master coordinator for AI skills. Discovers skills from multiple sources (SkillsMP.com, SkillHub, and ClawHub), manages installation, and synchronization across Claude Code, Gemini CLI, Google Anti-Gravity, OpenCode, and other AI tools. Handles User-level (Global) and Project-level (Local) scopes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacob-bd](https://clawhub.ai/user/jacob-bd)

### License/Terms of Use:


## Use Case:

Developers and AI tool users use this skill to find, install, package, and synchronize agent skills across local tools and supported cloud upload workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or synchronize files into AI skill folders, which can overwrite or introduce executable skill content.

Mitigation: Use dry-run first, keep destinations inside one intended skill directory, and manually review target changes before deployment.

Risk: The security evidence flags unsafe remote-shell, archive, destination, and force-bypass behaviors for manual review.

Mitigation: Avoid the curl pipe-to-shell workaround, and do not use --force or --skip-scan unless the target skill has been manually reviewed.

Risk: Cloud ZIP packaging can include an API key in config.json, which may expose credentials if the ZIP is shared or synced.

Mitigation: Do not embed an API key in packages that may be shared, posted, committed, or synchronized outside the intended private environment.

Risk: The skill requires network access to external skill catalogs and GitHub, so cloud or restricted environments may block core functionality.

Mitigation: Use it in an environment with the required outbound access, or limit use to packaging other skills that do not require those network calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jacob-bd/skills/universal-skills-manager)
- [Project homepage](https://github.com/jacob-bd/universal-skills-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code blocks, shell commands, JSON snippets, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce ZIP packaging guidance and local file operation instructions for skill installation or synchronization.]

## Skill Version(s):

1.7.0 (source: server release metadata and artifact version comment, released 2026-03-07)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
