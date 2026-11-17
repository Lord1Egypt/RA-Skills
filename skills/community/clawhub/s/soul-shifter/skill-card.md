## Description:

Create, save, and switch OpenClaw's persona (Soul). Research characters to generate new souls or load existing ones from the library.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xhrisfu](https://clawhub.ai/user/xhrisfu)

### License/Terms of Use:


## Use Case:

External OpenClaw users use this skill to create, store, list, and activate reusable persona files for character-style agent behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Activating a persona persistently overwrites the active agent persona file with generated or saved behavioral instructions.

Mitigation: Review each generated or loaded soul before activation and keep restorable backups of ~/clawd/SOUL.md and ~/clawd/souls/.

Risk: Persona creation from untrusted or obscure web sources may introduce behavior-changing instructions into future agent sessions.

Mitigation: Use trusted source material where possible and avoid activating generated personas from sources you have not reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xhrisfu/skills/soul-shifter)
- [ClawHub publisher profile](https://clawhub.ai/user/xhrisfu)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, guidance]

**Output Format:** [Markdown persona profiles and concise text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes persona files under ~/clawd/souls/ and overwrites ~/clawd/SOUL.md when activating a persona.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
