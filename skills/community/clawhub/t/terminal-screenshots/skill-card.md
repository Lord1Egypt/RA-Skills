## Description:

Create terminal screenshots, animated GIFs, or videos using VHS scripts for documentation, demos, and reproducible CLI visuals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricardodantas](https://clawhub.ai/user/ricardodantas)

### License/Terms of Use:

GPL-3.0

## Use Case:

Developers and technical writers use this skill to create reproducible terminal screenshots, animated CLI demos, and tutorial recordings for documentation and product examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing VHS through package managers, sudo commands, or Docker images can introduce supply-chain and privilege risks.

Mitigation: Install only from trusted package managers or container images and approve sudo or Docker commands explicitly before use.

Risk: VHS tape files execute typed commands, including commands hidden from the final recording with Hide.

Mitigation: Review tape files before running them and confirm hidden setup or cleanup commands are expected.

## Reference(s):

- [terminal-screenshots on ClawHub](https://clawhub.ai/ricardodantas/skills/terminal-screenshots)
- [VHS GitHub](https://github.com/charmbracelet/vhs)
- [VHS Themes](https://github.com/charmbracelet/vhs/blob/main/THEMES.md)
- [VHS Example Tapes](https://github.com/charmbracelet/vhs/tree/main/examples)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash and tape code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces VHS tape syntax, command examples, installation guidance, and workflow recommendations for generating screenshots, GIFs, videos, or PNG frame sequences.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
