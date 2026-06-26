## Description: <br>
AI governance layer that logs, audits, and enforces kill-switch rules on agent tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SMJAI](https://clawhub.ai/user/SMJAI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use TrustLoop to check sensitive tool calls before execution, log decisions, and route destructive, external, financial, or bulk actions through hosted governance rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive tool-call metadata and arguments are sent to a hosted TrustLoop service. <br>
Mitigation: Minimize and redact arguments before submission, protect TRUSTLOOP_API_KEY, review TrustLoop retention and access controls, and avoid sending credentials, file contents, customer data, or full prompts. <br>
Risk: The included helper can fail open on missing API keys, network failures, timeouts, invalid responses, and service errors. <br>
Mitigation: Wrap or modify enforcement to fail closed for sensitive actions and test blocked, error, and timeout paths before relying on it as a kill switch. <br>
Risk: The security verdict is suspicious and calls for review before deployment. <br>
Mitigation: Review and scan the skill before installation, with special attention to external data transmission and fail-open behavior. <br>


## Reference(s): <br>
- [TrustLoop homepage](https://trustloop.live) <br>
- [TrustLoop ClawHub page](https://clawhub.ai/SMJAI/trustloop) <br>
- [TrustLoop API reference](artifact/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash commands, JavaScript helper usage, and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRUSTLOOP_API_KEY and sends minimized tool-call metadata and arguments to the TrustLoop API.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
