## Description: <br>
Sensor is a terminal utility for locally logging, reviewing, searching, and exporting sensor-related notes and activity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ckchzh](https://clawhub.ai/user/ckchzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and field users can use Sensor to record sensor readings, device status notes, telemetry observations, and local activity history. It should be treated as a local note logger rather than a real sensor polling, conversion, connectivity, or analysis system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is described as sensor management, but security evidence says it behaves as a local free-form logger with command conflicts, so documented actions may not perform real polling, conversion, connectivity checks, or analysis. <br>
Mitigation: Use it only for local sensor-note logging, and verify command behavior plus export or status output before relying on results. <br>
Risk: User-provided notes are persisted locally under ~/.local/share/sensor/. <br>
Mitigation: Avoid entering secrets, credentials, private network details, or sensitive infrastructure information unless persistent local storage in that directory is acceptable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ckchzh/sensor) <br>
- [Publisher Homepage](https://bytesagain.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance, files] <br>
**Output Format:** [Terminal text with local log and export files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local data under ~/.local/share/sensor/ unless the runtime environment changes the data directory.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
