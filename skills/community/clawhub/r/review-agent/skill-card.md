## Description:

Review Agent is a pre-meeting review coach for Lark/Feishu or WeCom that ingests drafts, proposals, plans, or agendas, runs a four-pillar and responder-simulation review, and produces a decision-ready brief.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinghaojia](https://clawhub.ai/user/yinghaojia)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and managers use this skill to prepare meeting materials before a decision conversation. It helps a requester clarify background, supporting materials, decision framework, and intended ask, then returns prioritized findings and a six-section decision brief.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confidential drafts and meeting materials may be processed through external model calls.

Mitigation: Confirm OpenRouter data handling is acceptable for the intended material before use and avoid sending confidential drafts without approval.

Risk: Installation may rely on external installer code and OpenClaw patching that changes gateway behavior.

Mitigation: Have an admin review the installer and OpenClaw patch at a pinned commit, then test in a staging workspace before production use.

Risk: Non-Feishu/WeCom channels fall back to a shared main-agent mode without per-requester isolation.

Mitigation: Restrict normal deployments to isolated Feishu or WeCom workspaces, or disable the skill on shared-context channels.

Risk: Delivery, purge, and legacy credential behaviors can expose or remove user data if configured too broadly.

Mitigation: Scope Lark, drive, email, and purge permissions narrowly, audit configuration before release, and require explicit admin approval for destructive cleanup paths.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yinghaojia/skills/review-agent)
- [Agent Persona](references/agent_persona.md)
- [Four Pillars](references/four_pillars.md)
- [Annotation Schema](references/annotation_schema.md)
- [Summary Output Contract](references/summary_template.md)
- [Delivery Reference](references/delivery/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, guidance]

**Output Format:** [Requester-facing text, Markdown briefs, JSON annotations and verdicts, and local session files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces normalized input, finding queues, revised drafts, changelogs, final-gate verdicts, and a six-section decision brief.]

## Skill Version(s):

2.1.2 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
