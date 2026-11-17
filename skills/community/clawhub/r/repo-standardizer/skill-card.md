## Description:

Polish GitHub repository metadata and configuration, including labels, issue forms, PR templates, CI workflows, CODEOWNERS, rulesets, and documentation, without touching application code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[programmingwtf](https://clawhub.ai/user/programmingwtf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to standardize new or existing GitHub repositories by auditing repository state, proposing a dry-run plan, and applying selected metadata and configuration modules. It is intended for repository surface polish such as labels, templates, CI, rulesets, and docs, not source-code logic changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make live GitHub repository-configuration changes.

Mitigation: Review the dry-run plan, confirm scope before protected or destructive changes, and use the least-privileged GitHub credential that can perform the selected modules.

Risk: Generated CI, ruleset, CODEOWNERS, AGENTS.md, CLAUDE.md, and documentation files may not match an important repository's policy.

Mitigation: Inspect generated files before pushing them and keep existing customized content unless the user explicitly approves replacement.

Risk: GitHub authentication tokens or credentials could be mishandled during setup.

Mitigation: Use gh authentication or a properly scoped GH_TOKEN, never paste tokens into chat, logs, or files, and revoke any token that is accidentally exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/programmingwtf/skills/repo-standardizer)
- [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
- [Semantic Versioning](https://semver.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated repository configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May make live GitHub repository metadata and configuration changes after authentication, dry-run review, and user confirmation.]

## Skill Version(s):

1.0.1 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
