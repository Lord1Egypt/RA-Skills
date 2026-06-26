## Description: <br>
Use TestTau when an AI agent needs disposable email inboxes, private API-key protected test inboxes, webhook capture, request inspection, replay, or JSON Schema assertions for QA, CI, signup, checkout, and integration testing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[manojkottam](https://clawhub.ai/user/manojkottam) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and integration-test agents use TestTau to create disposable or private email inboxes and webhook capture endpoints, inspect captured messages or requests, replay webhook traffic, and run JSON Schema assertions during test workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public disposable inboxes and webhook captures are name-based and may be visible to anyone who knows the identifier. <br>
Mitigation: Use private inboxes or private hooks with bearer-token authentication for sensitive test data. <br>
Risk: Production secrets, PII, or credentials could be exposed if sent to public captures. <br>
Mitigation: Keep TestTau use to testing workflows and avoid sending production secrets, PII, or credentials to public inboxes or hooks. <br>
Risk: Webhook replay or wipe operations can affect test evidence or send captured payloads to another endpoint. <br>
Mitigation: Require explicit user confirmation before replaying requests or wiping inboxes and hooks. <br>


## Reference(s): <br>
- [TestTau API Reference For Agents](references/api.md) <br>
- [TestTau homepage](https://testtau.com/) <br>
- [ClawHub skill page](https://clawhub.ai/manojkottam/testtau) <br>
- [Publisher profile](https://clawhub.ai/user/manojkottam) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks and URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns inbox or hook identifiers, inspection URLs, captured message or request IDs, timeout status, and API usage guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
