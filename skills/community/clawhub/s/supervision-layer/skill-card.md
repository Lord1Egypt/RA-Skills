## Description: <br>
Wrap every tool call with timeouts, circuit breakers, audit logging, and crash loop protection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[larios613-hub](https://clawhub.ai/user/larios613-hub) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to add opt-in Python supervision around agent tool execution, including timeouts, circuit breakers, audit logging, and crash-loop tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill claims non-bypassable enforcement, but the security review characterizes it as an opt-in Python helper rather than guaranteed platform enforcement. <br>
Mitigation: Deploy it only where tool calls are explicitly routed through the helper, and document any uncovered execution paths. <br>
Risk: Audit and crash-state files may contain sensitive operational data. <br>
Mitigation: Use a controlled log directory, limit retention and access, and avoid passing secrets or full raw tool arguments into args_summary. <br>
Risk: The security review calls for fixes before production use. <br>
Mitigation: Address redaction, HALF_OPEN circuit limiting, crash-loop recovery, and storage/retention disclosure before relying on it in production. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/larios613-hub/supervision-layer) <br>
- [Publisher profile](https://clawhub.ai/user/larios613-hub) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with Python and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local Python helper code and JSONL audit/crash-state files when integrated by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
