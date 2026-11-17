## Description:

Orchestrates a XiaoDu movie-mode scene by using the installed xiaodu-control-official skill to prepare lights, curtains, display or playback devices, volume, signal source, and smart-screen confirmation before entering content playback only when the user explicitly requests it.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dueros-mcp](https://clawhub.ai/user/dueros-mcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and home-automation agents use this skill when a user asks to start movie mode or prepare a room for watching a movie. The skill plans a scene-first XiaoDu flow, falls back to supported device-level actions, and avoids choosing or playing content unless the user explicitly names a platform, signal source, or movie.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad phrases such as 'I want to watch a movie' can unexpectedly change lights, curtains, TV or projector state, volume, or signal source in shared spaces.

Mitigation: Install only where XiaoDu movie-mode automation is desired, review saved movie preferences periodically, and ask a minimal confirmation question when target devices or signal sources are ambiguous.

Risk: Physical home-device actions may affect the wrong room or device if the current environment has multiple reasonable targets.

Mitigation: Use only devices discovered from the current xiaodu-control-official environment, prefer matching scenes when available, and confirm between targets such as TV versus projector when the user has not specified one.

Risk: Persisted movie preferences can cause future automations to repeat settings the user no longer wants.

Mitigation: Write preferences only when the user explicitly asks to remember them, prefer short- or medium-term XiaoDu context for home preferences, and avoid claiming a preference was saved unless a file was actually updated.

Risk: Automatically entering a content or playback layer could select the wrong platform or media.

Mitigation: Prepare the room and playback devices by default, and continue to platform, signal-source, search, or playback actions only when the user explicitly requests them.

## Reference(s):

- [Usage Notes](references/usage-notes.md)
- [Test Cases](references/test-cases.md)
- [ClawHub Skill Page](https://clawhub.ai/dueros-mcp/skills/xiaodu-movie-mode-official)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text]

**Output Format:** [Markdown guidance with inline shell commands and natural-language response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands for one movie-mode flow should execute serially; persistent preference writes require explicit user intent.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
