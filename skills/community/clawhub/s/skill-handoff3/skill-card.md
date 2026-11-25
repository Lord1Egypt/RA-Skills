## Description:

Maintains per-session, append-only agent memory and assembles handoff reports with timestamped source quotes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skpll](https://clawhub.ai/user/skpll)

### License/Terms of Use:

MIT

## Use Case:

Developers working across AI agent sessions use Handoff3 to preserve session-scoped decisions and constraints, then create traceable handoff reports for later work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Activation behavior and the cross-session write boundary need clarification; the security assessment is partial.

Mitigation: Before installing, confirm when memory updates activate and verify that the configured library path and write scope match the intended project.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/skpll/skills/skill-handoff3)
- [Server-resolved source repository](https://github.com/skpll/skill_handoff3)
- [Server-resolved source commit](https://github.com/skpll/skill_handoff3/commit/b3e4d048a179c3dc4fd906b818a6f46463ef7bb3)
- [Command triggers and boundaries](references/commands.md)
- [Memory file schema](references/schema.md)
- [Agent adapter interfaces](references/adapters/index.md)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Timestamped Markdown memory entries and handoff reports with source quotes.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Append-only per-session memory; report content follows the conversation language.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact metadata declares 1.0.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
