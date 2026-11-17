## Description:

Control Ecovacs/DEEBOT robot vacuums via the Ecovacs IoT API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1209823208](https://clawhub.ai/user/1209823208)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and robot vacuum owners use this skill to operate Ecovacs/DEEBOT devices, inspect status, adjust cleaning settings, manage schedules, and issue supported IoT API commands.

### Deployment Geography for Use:

China domestic Ecovacs accounts

## Known Risks and Mitigations:

Risk: The helper controls a physical robot and can start, stop, dock, schedule, or otherwise alter cleaning behavior.

Mitigation: Use the skill only with trusted accounts and devices, review intended commands before execution, and require confirmation for persistent or disruptive actions.

Risk: Reusable Ecovacs authentication material is stored locally after login.

Mitigation: Avoid placing real passwords or MD5 password values in shell history, restrict or delete ~/.ecovacs_session.json after use, and prefer storage with minimal tokens and 0600 permissions.

Risk: Device command requests rely on hosts returned by the Ecovacs device service metadata.

Mitigation: Validate command hostnames before use and restrict execution to a known allowlist of supported commands.

## Reference(s):

- [Ecovacs Robot Control API Reference](artifact/references/api.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets; script output may be JSON or terminal text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Controls a live robot through Ecovacs account credentials and device API calls.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
