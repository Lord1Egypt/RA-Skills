## Description:

Operate the local X-Claw agent runtime for intents, approvals, execution, reporting, and wallet operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fourtytwo42](https://clawhub.ai/user/fourtytwo42)

### License/Terms of Use:


## Use Case:

External users, developers, and wallet operators use X-Claw to operate a local agent wallet runtime for EVM-compatible blockchain actions, approvals, execution, reporting, and policy management. The skill supports owner-controlled approve and deny workflows through Telegram and web management surfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can move wallet funds and change approval policy.

Mitigation: Review the default policy before use, require per-operation approvals where appropriate, and set low spend limits.

Risk: The skill can modify and restart the local OpenClaw gateway.

Mitigation: Disable or explicitly review gateway auto-patching before installation.

Risk: The skill can return sensitive management links and uses API keys and wallet signatures.

Mitigation: Treat API keys, management URLs, and wallet signatures as sensitive and avoid sharing them in chat, logs, or transcripts.

## Reference(s):

- [X-Claw Command Contract](references/commands.md)
- [X-Claw Approval and Policy Rules](references/policy-rules.md)
- [X-Claw Install and Config](references/install-and-config.md)
- [X-Claw Website](https://xclaw.trade)
- [X-Claw API Base URL](https://xclaw.trade/api/v1)
- [ClawHub Skill Page](https://clawhub.ai/fourtytwo42/skills/x-claw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Structured JSON envelope with human-readable Markdown sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sensitive values are redacted by default, with management links returned only for explicit owner-link workflows.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
