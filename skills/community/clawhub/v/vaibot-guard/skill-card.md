## Description: <br>
VAIBot Guard provides a local OpenClaw guard service and CLI for gating tool and shell execution, managing approvals, and validating tamper-evident receipts and audit logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[BriantAnthony](https://clawhub.ai/user/BriantAnthony) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to run a local policy decision service for OpenClaw, gate tool and shell execution, manage human approvals, and inspect audit receipts. It also supports setup and operation of an optional systemd user service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install or run a persistent local guard service and write secret-bearing environment files. <br>
Mitigation: Review the generated systemd unit path before enabling it, keep persistence opt-in, set a strong VAIBOT_GUARD_TOKEN, and restrict ownership and permissions on the env file. <br>
Risk: The guard can execute or gate shell and tool actions, so an incorrect policy or approval could allow unwanted local changes. <br>
Mitigation: Use the documented policy defaults, review approval decisions before execution, and test the guard flow locally before relying on it for sensitive work. <br>
Risk: When VAIBot API posting is enabled, command names, working directories, session IDs, policy decisions, and result summaries may leave the machine. <br>
Mitigation: For fully local use, do not set VAIBOT_API_KEY and prefer VAIBOT_PROVE_MODE=off; enable API posting only when that metadata exposure is acceptable. <br>


## Reference(s): <br>
- [VAIBot Guard API](references/api.md) <br>
- [VAIBot Guard Policy](references/policy.md) <br>
- [OpenClaw Integration](references/openclaw-bridge.md) <br>
- [VAIBot Guard Ops Runbook](references/ops-runbook.md) <br>
- [Receipt Schema](references/receipt-schema.md) <br>
- [Checkpoint Schema](references/checkpoint-schema.md) <br>
- [Inclusion Proofs](references/inclusion-proofs.md) <br>
- [Required Mode Semantics](references/required-mode.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, JSON] <br>
**Output Format:** [Markdown guidance with shell commands, configuration examples, JavaScript commands, and JSON schemas] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes local service, optional systemd user service, policy, audit receipt, checkpoint, and proof workflows.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
