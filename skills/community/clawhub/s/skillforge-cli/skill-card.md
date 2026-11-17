## Description:

Generate and audit OpenClaw agent skills from natural language for template-based or AI-assisted skill development.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shadoprizm](https://clawhub.ai/user/shadoprizm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use SkillForge to generate publish-ready OpenClaw skills, audit existing skill directories, and prepare skills for optional ClawHub publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on installing and running an external npm package.

Mitigation: Install only after reviewing and trusting the SkillForge package, and prefer a pinned package version.

Risk: Pro audit and generation modes may send skill contents to the operator's selected AI provider.

Mitigation: Do not run Pro mode against directories containing secrets, private keys, credentials, or sensitive unpublished code.

Risk: Provider API keys can be stored locally for Pro features.

Mitigation: Avoid storing provider keys unless necessary and protect local SkillForge configuration like other credential files.

Risk: Publishing commands can release generated or existing skills to ClawHub.

Mitigation: Require explicit operator approval before any ClawHub publication step.

## Reference(s):

- [ClawHub SkillForge listing](https://clawhub.ai/shadoprizm/skills/skillforge-cli)
- [SkillForge repository](https://github.com/shadoprizm/skillforge)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional table, JSON, or Markdown audit output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate skill files on disk and can publish to ClawHub only after operator approval.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
