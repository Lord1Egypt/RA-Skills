## Description: <br>
Enables agents to run durable ToolFlow workflows in OpenClaw with explicit step graphs, approvals, recovery, and progress visibility. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mcg-tries-to-code](https://clawhub.ai/user/mcg-tries-to-code) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when agent work should be expressed as a bounded, recoverable ToolFlow workflow instead of an improvised single-turn task. It is suited to multi-step diagnostics, approval-bound automation, long-running builds, and other jobs that need durable state and observable progress. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled workflow runner can inspect local files and persist workflow outputs. <br>
Mitigation: Install only when local workflow execution is intended, and inspect workflows with dry-run behavior before submission. <br>
Risk: Optional elevated execution can run commands or modify files when configured. <br>
Mitigation: Keep elevated mode disabled unless needed, and tightly limit the allowed command list before enabling it. <br>
Risk: Command-based progress updates may execute configured commands during long-running work. <br>
Mitigation: Keep command-based progress updates disabled unless required, and review the configured command before use. <br>
Risk: Untrusted workflows may request unsafe local actions. <br>
Mitigation: Do not run workflows from untrusted sources; keep workflows small, explicit, and reviewable. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/mcg-tries-to-code/toolflow-openclaw-operator) <br>
- [Canonical ToolFlow Runtime Repository](https://github.com/mcg-tries-to-code/ToolFlow) <br>
- [Artifact README](artifact/README.md) <br>
- [OpenClaw Bundle README](artifact/toolflow-bundle/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and workflow configuration references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to create, dry-run, submit, inspect, approve, and recover bounded ToolFlow workflows.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata and artifact skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
