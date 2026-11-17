## Description:

Helps agents design voices, clone authorized voice samples, synthesize speech, and plan multi-voice or sound-scene audio with Uydi.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvyinchao](https://clawhub.ai/user/lvyinchao)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and creators use the skill to draft voice and audio projects, guide authorized cloning, and run Uydi voice-generation workflows with user approval for paid actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice cloning may misuse someone else's recording.

Mitigation: Clone only voices the user owns or is explicitly authorized to use; obtain their rights confirmation first.

Risk: Voice generation can spend Uydi credits.

Mitigation: Check the available balance and current quote, and get approval before paid generation.

Risk: OAuth credentials are stored locally.

Mitigation: Protect the local credentials and use logout to revoke and remove the token when finished.

Risk: Deletion commands can permanently remove voices or projects.

Mitigation: Confirm the exact item and user intent before deletion.

## Reference(s):

- [Uydi Voice release on ClawHub](https://clawhub.ai/lvyinchao/skills/uydi-voice)
- [Uydi](https://uydi.com)
- [Voice Canvas reference](references/voice-canvas.md)
- [Sound Scenes reference](references/sound-scenes.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can produce WAV audio and JSON project drafts through Uydi.]

## Skill Version(s):

1.2.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
