## Description: <br>
V2EX API 2.0 integration for accessing V2EX forum data, notifications, topics, nodes, and member profiles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[timqian](https://clawhub.ai/user/timqian) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers use this skill to integrate agents and tooling with V2EX forum APIs for notifications, topics, nodes, token information, and member profile workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: V2EX Personal Access Tokens can expose account access if pasted into chat, code, or logs. <br>
Mitigation: Store the token in an environment variable or another secure store and avoid echoing it in shared outputs. <br>
Risk: Notification deletion is a destructive V2EX API action. <br>
Mitigation: Require explicit user approval before issuing DELETE requests for notifications. <br>
Risk: V2EX API requests can fail or be throttled when rate limits are reached. <br>
Mitigation: Check V2EX rate-limit headers, use pagination where supported, and back off or retry gracefully. <br>


## Reference(s): <br>
- [V2EX API Documentation](https://www.v2ex.com/help/api) <br>
- [V2EX Personal Access Tokens](https://www.v2ex.com/settings/tokens) <br>
- [V2EX API Node](https://www.v2ex.com/go/v2ex-api) <br>
- [ClawHub Skill Page](https://clawhub.ai/timqian/v2ex) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash, HTTP, and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes V2EX endpoint references, authentication guidance, error handling notes, rate-limit handling guidance, and example client code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
