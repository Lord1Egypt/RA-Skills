## Description:

Generate or edit AI media, including image, video, audio, and 3D outputs, by guiding an agent to use the WaveSpeed CLI on the user's machine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnsonbuilds](https://clawhub.ai/user/johnsonbuilds)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and content teams use this skill to choose WaveSpeed models, confirm run parameters, and generate or edit image, video, audio, or 3D media through the local WaveSpeed CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected media files may be uploaded to WaveSpeed during generation or editing workflows.

Mitigation: Confirm each upload explicitly and avoid sending sensitive, confidential, or regulated media unless the user has approved that service use.

Risk: WaveSpeed model runs may incur charges.

Mitigation: Confirm the model, prompt, important parameters, and expected cost posture with the user before running CLI commands.

Risk: API keys could be exposed if pasted into chat or placed directly on command lines.

Mitigation: Prefer browser login or a secure credential flow; avoid echoing or storing API keys in conversation logs or shell history.

Risk: Installing or running an unreviewed CLI package can execute code on the user's machine.

Mitigation: Use a reviewed, pinned CLI version where possible and install without sudo unless elevated permissions are explicitly required.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/johnsonbuilds/awesome-hermes-skills/tree/main/creative/wavespeed)
- [ClawHub skill page](https://clawhub.ai/johnsonbuilds/skills/wavespeed-2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON result handling guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include CLI model IDs, prompts, input parameters, upload steps, authentication guidance, local download paths, and output URLs.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
