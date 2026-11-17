## Description:

Orchestrates Xiaodu-connected scenes, lights, smart-screen speech, and auto-off timing for safer, low-disruption nighttime movement by older adults.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dueros-mcp](https://clawhub.ai/user/dueros-mcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and caregivers use this skill to help an assistant respond to short nighttime Chinese-language requests such as opening a night light or lighting a path to the bathroom. The skill favors low brightness, brief speech, serial device control, and automatic light shutoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad nighttime phrases could trigger unintended Xiaodu-connected light or scene control in a shared home.

Mitigation: Require clear activation wording and ask one minimal confirmation question when the target room, path, or light is ambiguous.

Risk: Stored night-use preferences may reveal sensitive household routines.

Mitigation: Obtain consent before writing recurring preferences and define whether XIAODU_CONTEXT.md or MEMORY.md may retain nighttime routine details.

Risk: Incorrect device selection could over-light the home or affect the wrong room at night.

Mitigation: Use only server-listed devices, avoid whole-home defaults, prefer low warm light, and execute commands serially so failures can be handled step by step.

## Reference(s):

- [Usage Notes](artifact/references/usage-notes.md)
- [Test Cases](artifact/references/test-cases.md)
- [ClawHub Skill Page](https://clawhub.ai/dueros-mcp/skills/xiaodu-senior-night-assist-official)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and short user-facing responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces serial execution plans for Xiaodu scene, IoT light, smart-screen speech, optional thermal comfort, and auto-off actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
