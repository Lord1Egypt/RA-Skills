## Description: <br>
Provides Douyin Open Platform API reference material for generating a client_token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lentiancn](https://clawhub.ai/user/lentiancn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to look up the Douyin Open Platform client_token endpoint, request parameters, response shape, and error codes when preparing API calls that do not require user authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release security verdict is suspicious and the server guidance recommends review before installation or credentialed use. <br>
Mitigation: Install only when the publisher is trusted, and review any proposed command or remote-state change before allowing credentials to be used. <br>
Risk: The API workflow uses client_key and client_secret values to request a client_token. <br>
Mitigation: Keep client_secret values out of prompts, logs, and shared files, and use the correct environment credentials to avoid invalidating production tokens. <br>


## Reference(s): <br>
- [Douyin API index](references/apidocs/apis.md) <br>
- [douyin.open.client.token API reference](references/apidocs/douyin.open.client.token.md) <br>
- [Douyin client_token endpoint](https://open.douyin.com/oauth/client_token/) <br>
- [ClawHub skill page](https://clawhub.ai/lentiancn/skill-douyin) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with API tables and curl and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes example client credentials placeholders; users should substitute their own Douyin application credentials.] <br>

## Skill Version(s): <br>
1.0.2 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
