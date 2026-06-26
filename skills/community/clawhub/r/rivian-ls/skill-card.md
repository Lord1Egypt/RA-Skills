## Description: <br>
Access Rivian vehicle telemetry, including battery, range, charge state, locks, doors, tires, cabin temperature, and location, through the rivian-ls CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pfrederiksen](https://clawhub.ai/user/pfrederiksen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Rivian owners and developers use this skill to ask an agent for vehicle status summaries, security checks, battery and range information, tire pressure readings, and telemetry-backed dashboard or automation guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vehicle telemetry can include sensitive GPS location, VIN, lock state, and door or window status. <br>
Mitigation: Restrict access to dashboards, endpoints, logs, and shared outputs that expose telemetry. <br>
Risk: Cached Rivian credentials are stored locally by the rivian-ls CLI. <br>
Mitigation: Install only on trusted machines and restrict access to ~/.config/rivian-ls/credentials.json. <br>
Risk: Passwords and OTPs can leak through shell history or reusable command snippets. <br>
Mitigation: Avoid placing real passwords or OTPs in shell history, logs, or checked-in examples. <br>
Risk: The skill depends on an unofficial Rivian API and the separate rivian-ls CLI. <br>
Mitigation: Review and trust the CLI before use and expect API behavior to change without notice. <br>


## Reference(s): <br>
- [Rivian LS API Fields](references/api-fields.md) <br>
- [rivian-ls CLI Repository](https://github.com/pfrederiksen/rivian-ls) <br>
- [ClawHub Skill Page](https://clawhub.ai/pfrederiksen/rivian-ls) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands and optional text or JSON telemetry output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the separate rivian-ls CLI to be installed and authenticated; offline mode reads cached telemetry by default.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
