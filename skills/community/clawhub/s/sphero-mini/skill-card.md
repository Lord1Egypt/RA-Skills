## Description:

Control Sphero Mini robot ball via Bluetooth Low Energy. Roll, change colors, read sensors, draw shapes, and play with cats. Uses bleak for cross-platform BLE support (macOS/Windows/Linux).

This skill is ready for commercial/non-commercial use.

## Publisher:

[joneschi](https://clawhub.ai/user/joneschi)

### License/Terms of Use:

MIT

## Use Case:

Developers and robot hobbyists use this skill to control a Sphero Mini over Bluetooth LE, including movement, LED color changes, battery checks, sensor reads, and prebuilt activity scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Some documentation describes downloading unpinned Python files from GitHub master.

Mitigation: Use reviewed local files or pinned, verified sources instead of following moving-branch curl commands.

Risk: Some troubleshooting guidance suggests broad or persistent Bluetooth privilege escalation.

Mitigation: Use least-privilege Bluetooth permissions and avoid running examples with sudo or applying capabilities to the system Python interpreter.

Risk: The skill can move a physical robot ball, including random pet-play movements.

Mitigation: Operate the device only while supervised in a clear, flat area away from stairs, cords, fragile items, people, and pets that could be struck.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joneschi/skills/sphero-mini)
- [Sphero Mini API Reference](artifact/references/api.md)
- [Troubleshooting Sphero Mini](artifact/references/troubleshooting.md)
- [sphero_mini_win](https://github.com/trflorian/sphero_mini_win)
- [bleak](https://github.com/hbldh/bleak)
- [pysphero](https://github.com/EnotYoyo/pysphero)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python snippets and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, bleak, Bluetooth LE access, and a Sphero Mini device address.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
