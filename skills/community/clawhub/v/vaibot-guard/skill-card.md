## Description:

Local VAIBot Guard skill for OpenClaw that helps run a local guard service, enforce tool decisions, manage approvals, and validate receipts and audit logs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[briantanthony](https://clawhub.ai/user/briantanthony)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure and operate VAIBot Guard as a local OpenClaw policy decision service for shell execution, tool gating, human approvals, and tamper-evident audit review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports that the local guard service can fail open and may allow high-risk tool behavior by default.

Mitigation: Prefer foreground/manual operation for evaluation, review the policy before use, and do not rely on the guard as the only enforcement layer until high-risk default-allow behavior is fixed.

Risk: The service can be installed as a persistent background user service and writes configuration under the user's home directory.

Mitigation: Make systemd installation an explicit operator choice, review the generated service and environment file, keep secret-bearing env files chmod 600, and start with manual foreground execution.

Risk: If exposed beyond localhost or used without a strong token, the guard API could allow unauthorized policy decisions or approval actions.

Mitigation: Keep VAIBOT_GUARD_HOST bound to 127.0.0.1 and require a strong VAIBOT_GUARD_TOKEN for protected endpoints.

Risk: Operational logs and optional VAIBot receipt uploads can contain sensitive workflow details.

Mitigation: Treat VAIBOT_GUARD_LOG_DIR as sensitive, configure retention, review redaction behavior, and only enable VAIBOT_API_URL and VAIBOT_API_KEY for trusted endpoints.

Risk: The security scan reports path validation and redaction weaknesses.

Mitigation: Avoid using the skill with untrusted workspaces or sensitive paths until path validation and redaction behavior have been reviewed and corrected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/briantanthony/skills/vaibot-guard)
- [VAIBot Guard API](references/api.md)
- [OpenClaw integration](references/openclaw-bridge.md)
- [VAIBot Guard Policy](references/policy.md)
- [Default policy JSON](references/policy.default.json)
- [Receipt schema](references/receipt-schema.md)
- [Checkpoint schema](references/checkpoint-schema.md)
- [Required mode semantics](references/required-mode.md)
- [Merkle roots and replay](references/merkle-replay.md)
- [Inclusion proofs](references/inclusion-proofs.md)
- [Metadata indexing](references/metadata-indexing.md)
- [Operations runbook](references/ops-runbook.md)
- [Persistence and installation notes](references/persistence-and-install.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON schemas, JavaScript commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local service commands, policy and receipt configuration guidance, approval workflow guidance, and audit verification steps.]

## Skill Version(s):

0.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
