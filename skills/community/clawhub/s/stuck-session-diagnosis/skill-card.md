## Description:

Use when another Claude Code session appears frozen, stuck, or abnormally slow and needs process-level diagnosis and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wimi321](https://clawhub.ai/user/wimi321)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect local Claude Code or agent sessions that appear frozen or abnormally slow, confirm whether suspicious process metrics are sustained, and produce an escalation-ready diagnosis report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Process metadata and related debug log excerpts may expose local session details in the diagnosis report.

Mitigation: Use the skill intentionally on machines where sharing process metadata and log excerpts is acceptable, and review the report before forwarding it.

Risk: Transient CPU, memory, or process-state changes can be mistaken for a confirmed hang.

Mitigation: Confirm suspicious metrics with repeated sampling before reporting a stuck session.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown diagnosis report with process-inspection evidence and recommended next steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Diagnostic only; does not kill or signal processes unless explicitly requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
