## Description:

Converts one video or script into four Instagram trial-reel hook variants, producing transparent 1080x1920 overlays, an editor mounting sheet, and a publication plan for comparing hook performance before posting to the main grid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[formula100k](https://clawhub.ai/user/formula100k)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, editors, and social-media operators use this skill to turn a single recorded video or script into four controlled hook variants, then compare trial-reel performance signals before deciding what to publish to the main profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may ask the agent to install Homebrew or npm tools as part of setup.

Mitigation: Require manual approval for dependency installation and review the exact packages before running setup commands.

Risk: Generated local HTML may contact jsDelivr during rendering.

Mitigation: Vendor required JavaScript locally or render in a network-restricted environment after reviewing dependencies.

Risk: Using the reminder flag can create Apple Reminders on the host system.

Mitigation: Use the OpenClaw-limited flow without `--recordatorios` unless the user explicitly approves reminder creation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/formula100k/skills/trial-reels-lab-f100k)
- [criterios-gancho.md](artifact/criterios-gancho.md)
- [matriz-variantes.md](artifact/matriz-variantes.md)
- [reglas-publicacion.md](artifact/reglas-publicacion.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration, shell commands, local HTML compositions, transparent PNG overlays, and publication-plan files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can generate local overlay compositions and planning files; the OpenClaw flow does not publish to Instagram or compose the final video.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
