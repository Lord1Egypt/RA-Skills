## Description:

Controls Windows music playback by issuing nircmd media shortcut commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[showx](https://clawhub.ai/user/showx)

### License/Terms of Use:

MIT-0

## Use Case:

External users or agents on Windows use this skill to handle explicit music playback requests, including next track, previous track, and play/pause.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends local keyboard shortcuts to the host, which may affect the active Windows session or focused application.

Mitigation: Use only for explicit play, pause, next-track, or previous-track requests on hosts where nircmd media-key control is intended.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands target local Windows media playback through nircmd keyboard shortcuts.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
