## Description:

Orchestrates a dynamic multi-agent team where a lead agent plans work, delegates specialized subtasks to worker agents, and synthesizes their results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aa-rick](https://clawhub.ai/user/aa-rick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to break complex tasks into parallel specialist workstreams, including code review, market research, document generation, debugging, and trading-signal analysis. It is intended for situations where coordinated sub-agent work and a synthesized final report are useful.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation rules may cause multi-agent delegation in contexts where sharing information across workers is not appropriate.

Mitigation: Use only when multi-agent delegation is intentional, and pass workers only the scoped context required for their assigned tasks.

Risk: Worker agents may receive sensitive logs, secrets, private business data, or other information that should not be distributed across sessions.

Mitigation: Avoid use with secrets, private logs, and sensitive business data unless the user has explicitly approved scoped sharing.

Risk: Trading-signal outputs may be mistaken for financial advice.

Mitigation: Treat trading outputs as informational analysis and require independent financial review before action.

## Reference(s):

- [Role Patterns](references/role-patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/aa-rick/skills/xqe-agent-team)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or structured text with task plans, worker progress updates, and synthesized findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include role assignments, inter-agent dependency notes, risk observations, and final recommendations.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
