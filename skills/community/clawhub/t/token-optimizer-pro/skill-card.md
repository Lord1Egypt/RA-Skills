## Description: <br>
Agent token usage optimizer that analyzes usage logs, transcript excerpts, model bills, or runtime traces to produce token and cost breakdowns, waste patterns, compaction opportunities, caching suggestions, and before/after optimization actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent operators use this skill to understand where token usage and model cost are going, then reduce waste without hurting task quality. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Usage logs, billing exports, transcripts, and tool traces may contain API keys, credentials, personal identifiers, or private customer data. <br>
Mitigation: Redact secrets and private data before analysis, and review supplied logs or transcripts for sensitive material. <br>
Risk: Cost estimates can be misleading when based on partial traces or unofficial billing data. <br>
Mitigation: Treat estimates as approximate unless official billing exports or complete runtime traces are provided. <br>
Risk: Uploading logs or transcripts to external services can expose confidential data. <br>
Mitigation: Do not upload logs or transcripts externally unless the user explicitly chooses that route. <br>


## Reference(s): <br>
- [Token Optimizer Pro on ClawHub](https://clawhub.ai/harrylabsj/token-optimizer-pro) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, guidance, configuration] <br>
**Output Format:** [Markdown with structured recommendations and estimates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cost and token breakdowns, waste-pattern findings, optimization checklists, caching or compaction suggestions, and approximate before/after estimates.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
