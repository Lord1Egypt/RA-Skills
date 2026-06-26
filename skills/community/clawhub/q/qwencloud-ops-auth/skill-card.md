## Description: <br>
Configures QwenCloud authentication, API key setup, endpoint selection, and 401 troubleshooting for agents and related QwenCloud skills. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cuixiaoyang123](https://clawhub.ai/user/cuixiaoyang123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users configuring QwenCloud-backed tools use this skill to set up standard DashScope API credentials, choose the correct endpoint and key type, verify authentication with curl, and avoid exposing secrets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles API keys and OSS credentials, so secrets could be exposed or persisted if users provide real values in chat or commit local configuration files. <br>
Mitigation: Use placeholders in generated .env examples, keep real secrets out of chat and version control, mask diagnostic output, and rotate any exposed credentials. <br>
Risk: The security evidence notes unrelated update and installation flows that can change local skill state. <br>
Mitigation: Only allow .env edits, diagnostic output, agent-config registration, update checks, npx skill installation, or reminder-state changes when the user intentionally requests those local changes. <br>
Risk: The skill can direct users toward paid QwenCloud resources and distinguishes key types that affect billing behavior. <br>
Mitigation: Confirm the intended key type, endpoint, and billing model before running API verification or usage workflows that may incur charges. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/cuixiaoyang123/qwencloud-ops-auth) <br>
- [Official Documentation URLs](references/sources.md) <br>
- [Coding Plan vs Standard API Key](references/codingplan.md) <br>
- [Custom OSS Storage](references/custom-oss.md) <br>
- [Agent Compatibility](references/agent-compatibility.md) <br>
- [QwenCloud API key management](https://home.qwencloud.com/api-keys) <br>
- [QwenCloud OpenAI compatibility documentation](https://docs.qwencloud.com/api-reference/preparation/install-sdk) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and environment-variable names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local .env placeholder changes, diagnostic status, and auth verification outputs when the user authorizes them.] <br>

## Skill Version(s): <br>
0.2.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
