## Description: <br>
Gets short-lived Ravi identity verification tokens for third-party services that support Login with Ravi. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raunaksingwi](https://clawhub.ai/user/raunaksingwi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External Ravi users and their agents use this skill to obtain a fresh Ravi SSO token and pass it to a trusted third-party service for identity verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A third-party service that verifies a token can receive Ravi identity details such as name, email, and phone. <br>
Mitigation: Share tokens only with trusted services and only for login flows the user intentionally starts. <br>
Risk: Cached or stored SSO tokens may be reused outside the intended login flow. <br>
Mitigation: Generate tokens immediately before use and do not store them. <br>


## Reference(s): <br>
- [SSO Token API Reference](https://ravi.id/docs/schema/sso.json) <br>
- [ClawHub skill page](https://clawhub.ai/raunaksingwi/ravi-sso) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [SSO tokens are short-lived and should be generated immediately before use, not cached or stored.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
