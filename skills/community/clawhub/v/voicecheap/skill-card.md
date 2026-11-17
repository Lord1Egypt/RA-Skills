## Description:

Helps OpenClaw users connect to VoiceCheap and manage authorized transcription, subtitles, speech, images, dubbing, publishing, and workspace tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voicecheap](https://clawhub.ai/user/voicecheap)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users connect their VoiceCheap accounts to transcribe media, create subtitles and voice or image assets, dub projects, and manage authorized publishing or workspace tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting an account can grant access to private media and workspace data.

Mitigation: Review OAuth permissions in the browser and grant only the scopes required for the task.

Risk: Publishing, sharing, or voice cloning can disclose media or use a person's voice without permission.

Mitigation: Require explicit authorization for each action, confirm publication privacy, and obtain speaker permission for cloning.

Risk: Generation can consume account credits, and webhooks can send future project events to external endpoints.

Mitigation: Confirm credit use and configure webhooks only for specifically authorized HTTPS destinations.

## Reference(s):

- [VoiceCheap skill listing](https://clawhub.ai/voicecheap/skills/voicecheap)
- [VoiceCheap workflows](artifact/references/workflows.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May report authorized task results and links to generated or exported media.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
