## Description: <br>
End-to-end trace debugging from trace_id. Fetch Jaeger trace and Elasticsearch logs, analyze possible bugs (optionally with local repository context), and generate a fixed-structure Markdown report for CI or tickets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gakkiismywife](https://clawhub.ai/user/gakkiismywife) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to collect Jaeger trace data and Elasticsearch logs for a trace_id, optionally compare them with local repository context, and produce a structured debugging report for CI runs or tickets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Raw logs and local repository context may be sent into Codex during analysis. <br>
Mitigation: Use only approved trace, log, and repository data, and redact secrets, personal data, and confidential identifiers before running the skill. <br>
Risk: The local Markdown report is deleted after the chat workflow sends it, which can reduce auditability. <br>
Mitigation: Keep an approved copy of the generated report when audit records or ticket attachments are required. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Text, Files] <br>
**Output Format:** [Markdown report file plus fixed plain-text summary lines] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The report includes trace overview, span details, log details, bug analysis, repair suggestions, and optional repository evidence.] <br>

## Skill Version(s): <br>
0.2.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
