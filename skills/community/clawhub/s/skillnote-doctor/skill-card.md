## Description:

SkillNote Doctor is a diagnostic tool for OpenClaw agents that checks SkillNote registry connectivity, AGENTS.md setup, configuration validity, installed skill health, and resolver endpoint behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[latentloop07](https://clawhub.ai/user/latentloop07)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw users use this skill to diagnose SkillNote setup issues through a read-only six-check health report across local configuration, installed skills, and configured SkillNote endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local SkillNote/OpenClaw configuration and contacts the configured SkillNote host during diagnosis.

Mitigation: Install it only for SkillNote/OpenClaw diagnostics and verify the configured host before allowing endpoint checks.

Risk: The skill includes installation advice that may involve global npm installation or ClawHub package commands.

Mitigation: Verify ClawHub and npm package sources before following installation commands.

Risk: Broad trigger phrases could invoke the diagnostic workflow for general debugging requests.

Mitigation: Use or enable the skill when SkillNote/OpenClaw setup troubleshooting is intended.

## Reference(s):

- [SkillNote Doctor on ClawHub](https://clawhub.ai/latentloop07/skills/skillnote-doctor)
- [SkillNote self-host guide](https://github.com/luna-prompts/skillnote)
- [SkillNote issue tracker](https://github.com/luna-prompts/skillnote/issues)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown diagnostic checklist with pass/fail results and remediation commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only diagnostic flow; reports all six checks even if earlier checks fail.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
