## Description:

Local-first privacy gateway for LLM applications that reformulates sensitive, private, or proprietary prompts locally before routing safe versions to cloud models and synthesizing answers back into the local context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sulgik](https://clawhub.ai/user/sulgik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, security teams, and privacy-sensitive employees use this skill to route LLM requests containing PII, health records, credentials, or proprietary business context through a local Zipsa gateway before any cloud model call. It supports local classification, reformulation, cloud routing when needed, response synthesis, multi-turn session continuity, and admin-console governance workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is intended to process highly sensitive prompts, including personal, health, credential, and proprietary business data.

Mitigation: Install and use it only when the local Zipsa gateway is understood and controlled, and require authenticated local transport before handling regulated, personal, credential, or proprietary data.

Risk: Session continuity can mix private context across turns if session identifiers are reused or shared.

Mitigation: Use a unique per-conversation session_id and avoid reusing test or shared session IDs for real user data.

Risk: Hybrid routing may send reformulated content to cloud providers, creating residual privacy and consent risk.

Mitigation: Require explicit cloud-routing consent and verify that policy, masking, and reformulation behavior are appropriate for the data category before deployment.

Risk: Monitoring, alerting, and audit outputs may expose sensitive prompt details if forwarded without filtering.

Mitigation: Sanitize monitoring, alert, audit-log, SIEM, and SOAR outputs before routing them to external channels.

## Reference(s):

- [Zipsa Technical Reference](references/README.md)
- [Zipsa Admin Console 설계 명세](references/admin-dashboard.md)
- [Zipsa on ClawHub](https://clawhub.ai/sulgik/skills/zipsa)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with configuration snippets, JSON and Python examples, and shell command usage]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs assume a running local Zipsa gateway and a unique session_id for multi-turn continuity.]

## Skill Version(s):

0.4.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
