## Description: <br>
Call APIs through Keychains without exposing real credentials to the agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smarcombes](https://clawhub.ai/user/smarcombes) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to route API calls through Keychains, replacing credential values with placeholders while Keychains injects approved tokens server-side. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Approved providers may grant agents broad ongoing ability to call third-party APIs through Keychains. <br>
Mitigation: Use narrowly scoped provider permissions, avoid approving high-risk accounts unless required, and revoke machine or provider access when the task is complete. <br>
Risk: API calls routed through the credential proxy can perform writes, billing changes, or account actions if the approved provider token allows them. <br>
Mitigation: Require explicit user confirmation before writes, billing actions, or account changes, and review activity in the Keychains dashboard. <br>
Risk: Installing the skill depends on trust in keychains.dev and the keychains npm package. <br>
Mitigation: Install only after reviewing the publisher, package, and Keychains documentation, and keep the installed CLI or SDK version under normal dependency review. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/smarcombes/secure-api-calls) <br>
- [Keychains](https://keychains.dev) <br>
- [Keychains Dashboard](https://keychains.dev/dashboard) <br>
- [Keychains Security Whitepaper](https://keychains.dev/api/whitepaper) <br>
- [Keychains Python SDK](https://pypi.org/project/keychains/) <br>
- [Keychains Client SDK](https://www.npmjs.com/package/@keychains/client-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include approval links, polling steps, provider-specific API examples, and setup requirements for the keychains CLI or SDKs.] <br>

## Skill Version(s): <br>
1.0.3 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
