## Description: <br>
Orchestrates a Xiaodu smart-home movie mode by using the installed xiaodu-control-official skill to prepare scenes, lights, curtains, display devices, volume, inputs, and brief smart-screen confirmations without choosing content unless the user asks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dueros-mcp](https://clawhub.ai/user/dueros-mcp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Household users and agents use this skill to turn natural movie-night requests into a serial smart-home preparation flow. It prepares the room and playback devices first, asks only minimal confirmations when needed, and enters content playback only when the user specifies a title, platform, input, or device. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change real smart-home device states, including lights, curtains, TVs, projectors, signal sources, volume, and smart-screen speech. <br>
Mitigation: Use it only in trusted Xiaodu environments, confirm ambiguous device or room targets, and route device actions through the separate xiaodu-control-official skill. <br>
Risk: Natural phrases such as wanting to watch a movie can be interpreted as control intent in this setup. <br>
Mitigation: Treat trigger phrases as smart-home commands and ask one minimal confirmation when the target device, room, or signal source is ambiguous. <br>
Risk: Saved movie-mode preferences can become stale or inappropriate when household defaults change. <br>
Mitigation: Persist preferences only when the user explicitly asks and review or clear XIAODU_CONTEXT.md or MEMORY.md when defaults change. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dueros-mcp/xiaodu-movie-mode-official) <br>
- [Usage notes](references/usage-notes.md) <br>
- [Test cases](references/test-cases.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and natural-language status messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands should be executed serially; content playback is entered only when the user explicitly specifies content or a platform.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
