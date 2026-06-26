## Description: <br>
Provides expert OAuth 2.0 implementation, troubleshooting, and token management guidance for Twenty CRM with Google and Microsoft OAuth plus email and calendar sync integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[avirweb](https://clawhub.ai/user/avirweb) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill when implementing, debugging, testing, or deploying OAuth authentication and sync behavior in Twenty CRM. It is intended for work on provider setup, token handling, redirect loops, domain restrictions, and Gmail or Calendar sync integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review states that some production authentication guidance could expose user sessions if followed as written. <br>
Mitigation: Review OAuth fixes with a security engineer before applying them, and prefer server-side or HttpOnly session designs where possible. <br>
Risk: OAuth troubleshooting may involve sensitive secrets, token values, or raw environment output. <br>
Mitigation: Do not paste live OAuth secrets, token values, or raw docker environment output into chats, tickets, logs, or documentation. <br>


## Reference(s): <br>
- [Twenty CRM OAuth Mastery on ClawHub](https://clawhub.ai/avirweb/twenty-oauth-mastery) <br>
- [Publisher profile: avirweb](https://clawhub.ai/user/avirweb) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with TypeScript, SQL, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only troubleshooting reference; users should review OAuth security implications before applying recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
