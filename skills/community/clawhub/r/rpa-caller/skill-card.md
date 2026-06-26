## Description: <br>
RPA Caller helps an agent prepare, confirm, and call HTTP endpoints for RPA automation tasks such as file downloads, form filling, screenshots, status checks, and task stops. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operators and developers use this skill to translate user requests into documented RPA HTTP calls, collect required parameters, confirm the request before execution, and explain task status or errors. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RPA calls can trigger sensitive automation against external systems or files. <br>
Mitigation: Install only when the RPA server and exposed workflows are trusted, review endpoint and parameters before confirming execution, and use a limited-scope API key. <br>
Risk: Stopping or forcing a task can leave work incomplete. <br>
Mitigation: Review the task ID and stop settings before confirmation, and check the RPA system status or logs after cancellation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lvjunjie-byte/rpa-caller) <br>
- [RPA API map](references/rpa-api-map.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown guidance with structured HTTP request details and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation before sending RPA requests; may include endpoint, parameter, task ID, and status-response details.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
