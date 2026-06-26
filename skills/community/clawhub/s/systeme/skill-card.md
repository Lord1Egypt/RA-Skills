## Description: <br>
Systeme.io API integration with managed OAuth for managing contacts, tags, courses, communities, and subscriptions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage Systeme.io account data through Maton-managed OAuth, including contacts, tags, course enrollments, community memberships, and subscriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, delete, enroll, remove memberships, and cancel subscriptions in a connected Systeme.io account. <br>
Mitigation: Confirm the exact account, resource, and intended effect before any write operation, and specify the intended connection when multiple Systeme.io connections exist. <br>
Risk: The skill requires a Maton API key and OAuth access to a Systeme.io account. <br>
Mitigation: Install only if you trust Maton.ai, keep MATON_API_KEY secret, and revoke unneeded keys or connections. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/systeme) <br>
- [Maton Homepage](https://maton.ai) <br>
- [Systeme.io API Reference](https://developer.systeme.io/reference) <br>
- [Systeme.io API Overview](https://developer.systeme.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline Python, JavaScript, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and MATON_API_KEY; write operations require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
