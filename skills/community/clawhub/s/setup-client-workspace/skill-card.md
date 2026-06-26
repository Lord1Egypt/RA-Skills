## Description: <br>
Sets up a dedicated OpenClaw workspace for a new TNCG client, including base workspace files, OpenClaw configuration, WhatsApp linking, sandboxing, escalation, and monitoring guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[superWorldSavior](https://clawhub.ai/user/superWorldSavior) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to provision a client-specific agent workspace with OpenClaw configuration, communication setup, security checks, and operational runbooks. It is intended for onboarding customer-facing assistants that need isolated workspace files, WhatsApp routing, sandbox behavior, escalation, and monitoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad WhatsApp sending permissions may allow messages beyond the intended client scope. <br>
Mitigation: Replace wildcard sending with explicit recipient allowlists and verify WhatsApp bindings before enabling the agent. <br>
Risk: Cross-agent visibility and messaging can expose activity across agents if left too broad. <br>
Mitigation: Limit inter-agent allowlists and session visibility to the agents required for support and escalation. <br>
Risk: Shared or misplaced credentials can mix client usage, billing, or access boundaries. <br>
Mitigation: Use per-client credential stores and sandbox environment variables, and keep secrets out of workspace files. <br>
Risk: Production-facing client agents can retain credentials, sessions, memory files, or cron jobs after a client relationship changes. <br>
Mitigation: Document consent, escalation scope, revocation steps, and retention cleanup before deployment. <br>


## Reference(s): <br>
- [Workflow](artifact/references/workflow.md) <br>
- [OpenClaw config](artifact/references/openclaw-config.md) <br>
- [Security checklist](artifact/references/security-checklist.md) <br>
- [Workspace file templates](artifact/references/templates.md) <br>
- [Legacy monolith](artifact/references/legacy-monolith.md) <br>
- [ClawHub skill page](https://clawhub.ai/superWorldSavior/setup-client-workspace) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces procedural setup guidance for agent workspace files, OpenClaw configuration, WhatsApp linking, sandbox checks, escalation, and monitoring.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
