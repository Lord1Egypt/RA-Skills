## Description:

Automatically refines unclear prompts, matches relevant skills, integrates context, and suggests execution steps for AI assistant workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[janussilence](https://clawhub.ai/user/janussilence)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI assistant builders use this skill to turn vague user requests into clearer prompts, identify matching skill categories, and generate suggested execution guidance. It is intended for prompt engineering, agent routing, task refinement, and context-aware workflow planning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation instructions use an unpinned npx command, which can pull changing package contents.

Mitigation: Install only from a trusted or pinned ClawHub/npm source and do not run the installer with elevated privileges.

Risk: The skill can recommend file, web, and system-operation tools that may affect local files or external services.

Mitigation: Keep file writes, web access, and system-operation recommendations behind normal user confirmation.

Risk: Context integration and export functions may include sensitive user or project information.

Mitigation: Avoid passing secrets into context and do not export configuration or skill data to shared locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/janussilence/skills/smart-refinement)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Structured result containing refined prompt text, skill matches, suggested actions, context fields, and an execution guide.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include confidence scores, processing timing, and system statistics.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, README.md, SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
