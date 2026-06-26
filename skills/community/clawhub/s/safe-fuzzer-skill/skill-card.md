## Description: <br>
Sandbox-only behavior-led gray-box skill fuzzer. Spawns a worker subagent, probes an installed target skill, deploys honeypot fixtures, and returns a structured JSON risk report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentsey](https://clawhub.ai/user/agentsey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use SAFE-Fuzzer to run sandboxed behavioral probes against installed OpenClaw skills and produce a structured risk report. It is intended for post-setup fuzzing of a visible target skill using min, balanced, or max presets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fuzzes other skills by executing probe cycles that may exercise file, shell, credential, and network behavior inside the sandbox. <br>
Mitigation: Run only in a locked sandbox with elevated execution unavailable, and use synthetic credentials and fixtures instead of real secrets. <br>
Risk: Server security guidance recommends reviewing the skill files and requested permissions before using it with sensitive data or credentials. <br>
Mitigation: Install only when the publisher and purpose are recognizable, then review the artifact and selected preset before testing sensitive targets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentsey/safe-fuzzer-skill) <br>
- [SAFE project](https://github.com/RiemaLabs/safe) <br>
- [SAFE README](https://github.com/RiemaLabs/safe/blob/main/README.md) <br>
- [Report schema](references/report-schema.md) <br>
- [Min preset](references/presets/min.json) <br>
- [Balanced preset](references/presets/balanced.json) <br>
- [Max preset](references/presets/max.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [One structured JSON risk report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports should be based on executed sandbox behavior and may include findings, evidence, risk counts, honeypot status, and incident status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
