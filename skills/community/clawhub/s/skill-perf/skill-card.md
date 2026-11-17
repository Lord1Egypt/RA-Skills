## Description:

Skill Perf measures token consumption and performance overhead for OpenClaw skills by running calibrated subagent tests and generating performance reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kincaidwoo](https://clawhub.ai/user/kincaidwoo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use Skill Perf to benchmark OpenClaw skills, compare token costs across runs, and produce reports before release or optimization work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill spawns OpenClaw subagents and reads local OpenClaw session and workspace metadata.

Mitigation: Run it only in intended OpenClaw workspaces and review benchmark tasks before execution.

Risk: Generated reports may be exposed through an unauthenticated local report server.

Mitigation: Bind report serving to 127.0.0.1, serve only the current report, and stop the server after use.

Risk: Session-derived report diagnostics may include sensitive transcript or bootstrap details.

Mitigation: Use redaction and make transcript or bootstrap analysis opt-in before sharing reports.

## Reference(s):

- [Skill Perf ClawHub Page](https://clawhub.ai/kincaidwoo/skills/skill-perf)
- [README](artifact/README.md)
- [Token Guide](artifact/references/TOKEN_GUIDE.md)
- [Subagent Architecture Spec](artifact/docs/subagent-architecture-spec.md)
- [Bugfix Notes](artifact/docs/2026-03-27-bugfix-notes.md)
- [OpenClaw Token Use Reference](https://docs.openclaw.ai/reference/token-use.md)
- [Anthropic Pricing](https://www.anthropic.com/pricing)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands and generated HTML performance reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports summarize calibrated token totals, net token estimates, confidence, and session-derived diagnostics.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
