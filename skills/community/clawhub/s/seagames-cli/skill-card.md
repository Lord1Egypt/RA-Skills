## Description:

Guides agents in using the SeaGames CLI to create and process game images, video, audio, text, and 3D assets, including uploads, task recovery, and downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[indieaipm-tidu](https://clawhub.ai/user/indieaipm-tidu)

### License/Terms of Use:

MIT-0

## Use Case:

Game developers and artists use this skill to select available SeaGames capabilities, generate and refine project assets, and verify downloads or delivery to the intended project.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled executable uses a SeaGames account to upload assets and create or recover tasks.

Mitigation: Install only if the publisher is trusted, and keep saved session credentials private.

Risk: Paid commands or automatic project-canvas delivery may incur costs or change the wrong project.

Mitigation: Confirm pricing and project ID before execution; use --no-attach when only local output is wanted.

Risk: File-processing commands may overwrite important local assets.

Mitigation: Back up important assets and confirm output paths before running commands.

## Reference(s):

- [SeaGames CLI release on ClawHub](https://clawhub.ai/indieaipm-tidu/skills/seagames-cli)
- [SeaGames CLI usage guide](artifact/references/USAGE.md)
- [Output and recovery rules](artifact/references/OUTPUT_RULES.md)
- [3D model guide](artifact/references/3D_MODEL_GUIDE.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may create remote assets or change a selected project; confirm completion and delivery before reporting success.]

## Skill Version(s):

1.2.1 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
