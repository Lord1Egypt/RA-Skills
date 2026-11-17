## Description:

Build, measure, edit, or switch a personal writing voice profile for the rabbit-writes plugin.

This skill is ready for commercial/non-commercial use.

## Publisher:

[whit3rabbit](https://clawhub.ai/user/whit3rabbit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and agent users use this skill to create or maintain reusable personal writing voice profiles from samples, interviews, or corrections to drafts that do not sound like the intended author.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The host installer can persistently change Claude Code output styles and hooks.

Mitigation: Run install_host.py only when that behavior is intended; inspect the generated style and claude_hook.py first, and use the documented dry run before installation.

Risk: The optional model-apply path can send draft passages to an endpoint selected from configuration or environment variables.

Mitigation: Avoid --apply-model in untrusted repositories, inspect any .rabbit-model file, use an endpoint you control, and scope RABBIT_MODEL_API_KEY to this tool.

Risk: Voice profiles and fingerprints can encode personal writing habits or copied exemplars.

Mitigation: Use samples with the writer's consent, exclude sensitive or contaminated samples, and review generated profile files before sharing or installing them.

## Reference(s):

- [Voice reference](references/voice.md)
- [ClawHub skill page](https://clawhub.ai/whit3rabbit/skills/voice-setup)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON/file descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can guide users toward creating or changing voice profile files when they run the supplied scripts.]

## Skill Version(s):

0.5.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
