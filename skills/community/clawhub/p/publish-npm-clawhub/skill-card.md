## Description:

Publish OpenClaw skills or plugins to npm and ClawHub with a guarded workflow for release metadata, local-only account configuration, temporary release directories, and suspicious-scan review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[humanlike2026](https://clawhub.ai/user/humanlike2026)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers and release maintainers use this skill to publish OpenClaw skills or plugins through npm and ClawHub, validate release metadata, prepare a sanitized release directory, and review ClawHub suspicious or flagged scan results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release-staging script may delete an existing directory supplied through --prepare-release-dir.

Mitigation: Use only a fresh, disposable staging path and avoid sensitive or existing directories until path containment and deletion safeguards are fixed.

Risk: Publishing directly from a repository root can include local configuration, tokens, package archives, or editor files.

Mitigation: Publish from a sanitized temporary release directory built from an explicit allowlist and review the staged files before publishing.

Risk: npm or ClawHub commands can publish artifacts externally.

Mitigation: Require explicit final approval before running publish commands and verify account, slug, package, version, and scan status before and after release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/humanlike2026/skills/publish-npm-clawhub)
- [Publisher profile](https://clawhub.ai/user/humanlike2026)
- [Source homepage](https://gitlab.ttyuyin.com/personalization_group/publish_npm_clawhub_skill)
- [Publishing workflow](references/workflow.md)
- [Scanner review playbook](references/scanner-playbook.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may propose local command sequences for npm and ClawHub publishing and expects explicit user approval before release commands are run.]

## Skill Version(s):

1.0.6 (source: server release metadata, skill.json, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
