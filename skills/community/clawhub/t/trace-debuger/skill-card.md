## Description:

End-to-end trace debugging from trace_id. Fetch Jaeger trace and Elasticsearch logs, analyze possible bugs (optionally with local repository context), and generate a fixed-structure Markdown report for CI or tickets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gakkiismywife](https://clawhub.ai/user/gakkiismywife)

### License/Terms of Use:


## Use Case:

Developers and operations engineers use this skill to investigate a trace_id by collecting Jaeger spans and Elasticsearch logs, optionally adding repository context, and producing a fixed-structure Markdown debug report for CI or tickets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trace logs and selected repository context may be processed by Codex and written into a local Markdown report.

Mitigation: Use sanitized logs, avoid production secrets or customer data, restrict Jaeger and Elasticsearch URLs to trusted endpoints, and delete generated reports when they should not persist.

Risk: The security review verdict is suspicious because the skill lacks sufficient scoping, redaction, or user control for raw operational logs and repository context.

Mitigation: Review inputs before execution, scope repository access to the minimum relevant code, and confirm the generated report is appropriate before sharing it.

## Reference(s):

- [Trace Debuger ClawHub listing](https://clawhub.ai/gakkiismywife/skills/trace-debuger)
- [Publisher profile](https://clawhub.ai/user/gakkiismywife)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report file with fixed summary lines printed to stdout]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The report includes trace overview, span details, Elasticsearch log details, bug analysis, repair suggestions, and optional repository-context evidence.]

## Skill Version(s):

0.2.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
