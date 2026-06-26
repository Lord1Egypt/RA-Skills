## Description: <br>
Deterministic setup and remediation helper for installed OpenClaw skills that resolves a target skill, applies sandbox-local remediation when safe, and produces a structured setup report before fuzzing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentsey](https://clawhub.ai/user/agentsey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to prepare installed OpenClaw skills for behavioral fuzzing by resolving a target, applying bounded sandbox-local remediation, and returning a setup report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read and write local workspace files and run simple local commands during setup. <br>
Mitigation: Run it only inside the intended OpenClaw sandbox with writable workspace access, and review the JSON setup report before acting on changes. <br>
Risk: A target skill may require dependency installation, network downloads, service startup, credentials, or host-level configuration outside the safe setup scope. <br>
Mitigation: Stop at those blockers and handle them manually; the skill should not ask for real secrets, install dependencies, use the network, or modify host-level OpenClaw configuration. <br>


## Reference(s): <br>
- [Setup Report Schema](references/setup-report-schema.md) <br>
- [SAFE README](https://github.com/RiemaLabs/safe/blob/main/README.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/agentsey/safe-bootstrapper) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON object] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The JSON setup report starts with a human-readable summary, readiness status, run status, applied fixes, remaining blockers, rerun command, tool-call evidence, confidence, and duration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
