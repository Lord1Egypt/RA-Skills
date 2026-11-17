## Description:

Monitor and control Snapmaker U1 3D printers through the Moonraker/Klipper API, including status, temperatures, filament data, progress, file listings, and print controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucakaufmann](https://clawhub.ai/user/lucakaufmann)

### License/Terms of Use:

MIT

## Use Case:

Developers, makers, and printer operators use this skill to let an agent monitor Snapmaker U1 printer state, temperatures, filament RFID and sensor data, progress, available G-code files, and active print controls. It is also suitable when an agent needs to prepare or run documented Snapmaker CLI commands for Moonraker/Klipper-based printer management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw G-code support can move hardware, heat components, invoke printer macros, or otherwise change physical printer state.

Mitigation: Remove or restrict the raw G-code command path when it is not required, and require explicit operator confirmation before sending raw G-code.

Risk: State-changing controls such as cancel, pause, and resume can interrupt or alter an active physical print.

Mitigation: Confirm the target printer and requested action before state-changing commands, especially cancel, and limit use to trusted operators and printers.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes monitoring/status output, filament and temperature summaries, print control commands, file listings, and raw G-code command support.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
