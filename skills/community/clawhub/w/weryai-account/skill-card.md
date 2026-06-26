## Description: <br>
Check WeryAI account credits and API balance through the official WeryAI account endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WeryAI-Developer](https://clawhub.ai/user/WeryAI-Developer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to check remaining WeryAI API credits, verify that WERYAI_API_KEY can access the account endpoint, and decide whether credits are available before paid generation work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires WERYAI_API_KEY access and sends authenticated requests to WeryAI. <br>
Mitigation: Provide the key only through the runtime environment, use a least-privileged or short-lived key where available, and avoid storing the secret in skill files or prompts. <br>
Risk: Bundled but undeclared vendor helper code can query generation status endpoints and retrieve generation outputs, even though the public skill purpose is account balance checking. <br>
Mitigation: Review the package before deployment and remove or block unused vendor status/polling helpers if strict account-only behavior is required. <br>
Risk: WERYAI_BASE_URL can redirect API requests if overridden. <br>
Mitigation: Leave the default WeryAI API host in place or override it only with a trusted endpoint under an approved deployment policy. <br>


## Reference(s): <br>
- [WeryAI Account API](references/account-api.md) <br>
- [WeryAI documentation index](https://docs.weryai.com/llms.txt) <br>
- [Query API Account Credits](https://docs.weryai.com/api-reference/account/query-api-account-credits.md) <br>
- [WeryAI Account on ClawHub](https://clawhub.ai/WeryAI-Developer/weryai-account) <br>
- [WeryAI-Developer publisher profile](https://clawhub.ai/user/WeryAI-Developer) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, text] <br>
**Output Format:** [JSON command output with concise Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WERYAI_API_KEY, Node.js 18 or newer, and network access to the WeryAI API.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
