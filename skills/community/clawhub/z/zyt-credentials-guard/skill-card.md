## Description: <br>
Guide users to configure local Chanjing credentials safely via local commands only, and validate local token status when needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zuoyuting214](https://clawhub.ai/user/zuoyuting214) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when a Chanjing workflow needs local AK/SK setup, token refresh, or credential status validation without asking the user to paste secrets into chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Chanjing AK/SK or access tokens may be exposed if the local credentials file is shared, committed, or pasted into chat. <br>
Mitigation: Keep ~/.chanjing/credentials.json private, avoid committing it, never request secrets in chat, and rotate keys if exposure occurs. <br>
Risk: Token refresh sends credential material to the Chanjing API endpoint. <br>
Mitigation: Verify the Chanjing API domain before refreshing tokens and use the documented local configuration path. <br>


## Reference(s): <br>
- [Credentials Guard Reference](reference.md) <br>
- [Chanjing Open API Homepage](https://open-api.chanjing.cc) <br>
- [Chanjing Documentation](https://doc.chanjing.cc) <br>
- [Chanjing OpenAPI Login](https://www.chanjing.cc/openapi/login) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with JSON configuration examples and local command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Focuses on local credential handling; does not require bundled helper scripts or elevated privileges.] <br>

## Skill Version(s): <br>
0.5.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
