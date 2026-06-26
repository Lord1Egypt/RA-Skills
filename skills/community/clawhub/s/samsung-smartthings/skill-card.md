## Description: <br>
Control Samsung TVs via SmartThings (OAuth app + device control). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[regenrek](https://clawhub.ai/user/regenrek) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and smart-home users use this skill to provision SmartThings OAuth credentials for Clawdbot, identify a Samsung TV device, and guide SmartThings CLI actions for status checks, device control, and app launch. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The default OAuth redirect uses httpbin, which can expose the authorization code outside the user's controlled environment. <br>
Mitigation: Use a localhost or user-controlled OAuth redirect URI before completing the SmartThings login flow. <br>
Risk: The skill requests read and execute device scopes and stores SmartThings credentials and OAuth tokens in a local .env file. <br>
Mitigation: Use the minimum practical scopes or a dedicated SmartThings account, protect or delete the .env file when finished, and rotate credentials if they appear in logs or were used through the default redirect. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/regenrek/samsung-smartthings) <br>
- [SmartThings Developer Documentation](https://developer.smartthings.com/docs) <br>
- [SmartThings Personal Access Tokens](https://account.smartthings.com/tokens) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration] <br>
**Output Format:** [Plain text guidance and local environment configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update SmartThings OAuth credentials and tokens in ~/.clawdbot/.env or CLAWDBOT_STATE_DIR/.env.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
