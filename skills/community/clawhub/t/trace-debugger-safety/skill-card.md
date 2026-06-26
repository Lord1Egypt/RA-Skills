## Description: <br>
Generates Markdown trace debugging reports from Jaeger and Elasticsearch data with Codex-assisted analysis and documented safeguards for untrusted logs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gakkiismywife](https://clawhub.ai/user/gakkiismywife) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and site reliability engineers use this skill to investigate a trace_id by collecting Jaeger spans, Elasticsearch logs, and optional repository context into a trace debugging report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence flags that the skill may read observability logs, inspect a local repository, write reports, and invoke Codex from that repository context using log-derived prompts. <br>
Mitigation: Use only trusted or redacted logs, confirm Codex execution is explicitly opt-in, provide repository paths deliberately, and review generated analysis before acting on it. <br>
Risk: Trace and log data can include sensitive operational details. <br>
Mitigation: Redact sensitive log fields before analysis and limit report sharing to the intended debugging audience. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gakkiismywife/trace-debugger-safety) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Markdown report with command-line status summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes a local Markdown trace report; the skill documentation asks the agent to deliver the report as an attachment and delete the local file after delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
