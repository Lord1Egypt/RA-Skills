## Description: <br>
Enterprise-grade API key generation, verification, and lifecycle management with centralized administrative control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, administrators, and security teams use this skill to interact with a remote service for generating, verifying, revoking, and auditing API keys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Remote API-key management operations can expose or change sensitive credentials and session state. <br>
Mitigation: Use only with a trusted provider and avoid production credentials until authentication, tenant isolation, audit logging, retention, and revocation rollback behavior are clarified. <br>
Risk: The listing and API documentation do not clearly scope sensitive actions such as debug-session output and get-random-key behavior. <br>
Mitigation: Review these endpoints before deployment, restrict access to administrative users, and monitor calls that retrieve session or key material. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/krishnakumarmahadevan-cmd/toolweb-the-linkedin-optimization-toolkit) <br>
- [API docs](https://api.mkkpro.com:8100/docs) <br>
- [API base route](https://api.mkkpro.com/career/linproopt) <br>
- [ToolWeb](https://toolweb.in) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown with JSON payloads and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote API operations can affect admin keys, session state, and managed API keys.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; API spec reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
