## Description:

Deterministic setup and remediation helper for installed OpenClaw skills. Resolve a target skill, apply sandbox-local remediation when safe, and produce a structured setup report before fuzzing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentsey](https://clawhub.ai/user/agentsey)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill evaluators use SAFE-Bootstrapper to prepare installed OpenClaw skills for behavioral fuzzing by resolving a target skill, applying safe sandbox-local setup fixes, and reporting remaining blockers. It is intended for deterministic setup work such as git initialization, environment-file creation, local state directory creation, runtime checks, and reruns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or modify local setup files and rerun local commands inside the active sandbox.

Mitigation: Install and run it only in a sandboxed fuzzer workspace, review the target skill and workspace before use, and rely on its documented refusal of host-level, network, credential, and persistent behavior.

## Reference(s):

- [Setup Report Schema](references/setup-report-schema.md)
- [SAFE: Skilled Agent Fuzzing Engine](https://github.com/RiemaLabs/safe)
- [SAFE README](https://github.com/RiemaLabs/safe/blob/main/README.md)
- [ClawHub skill page](https://clawhub.ai/agentsey/skills/safe-bootstrapper)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Single JSON object with setup status, applied fixes, blockers, commands, and evidence]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The summary field is first, ready is second, and the report contains no surrounding Markdown.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
