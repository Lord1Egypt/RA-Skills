## Description:

Installs, lists, removes, and diagnoses World2Agent sensors on an OpenClaw machine through the openclaw-sensor-bridge supervisor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daibor](https://clawhub.ai/user/daibor)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to subscribe to outside-world sources such as Hacker News, GitHub, X, market data, RSS, and papers, then manage the installed World2Agent sensors that deliver those signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install npm packages, including the bridge package globally and sensor packages under the World2Agent npm root.

Mitigation: Use it only with sensor and bridge packages the user trusts, and avoid sudo npm installs unless the package and permissions are reviewed.

Risk: Bootstrap can change OpenClaw hook settings and register or start a background supervisor.

Mitigation: Review OpenClaw hook changes, backup paths, and launchd or systemd registration before allowing setup to proceed.

Risk: Installed sensors may auto-deliver agent replies to configured chat channels.

Mitigation: Confirm where notifications will be delivered and prefer dashboard-only delivery when the destination is uncertain.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daibor/skills/world2agent-manage)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON result handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Most management scripts emit one JSON object; log streaming emits raw text.]

## Skill Version(s):

0.1.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
