## Description: <br>
Generate accurate Volcengine SDK examples by locating an API with the bundled local ranker, fetching its API Explorer swagger, and calling api/common/explorer/make-code with user-provided Params. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[volc-sdk-team](https://clawhub.ai/user/volc-sdk-team) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to generate Volcengine SDK examples and configuration guidance for Python, Go, Java, PHP, cURL, and Node.js API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API queries and user Params are sent to Volcengine services. <br>
Mitigation: Avoid pasting real secrets unless sharing them with Volcengine is intended; prefer environment variables, temporary credentials, and least-privilege accounts. <br>
Risk: Broad aliases or ambiguous requests can lead to generated code for destructive, security-sensitive, or account-level cloud API actions. <br>
Mitigation: Verify the selected service, API action, region, and Params before running generated code, especially for create, delete, security, and account operations. <br>
Risk: Some reference examples disable or weaken transport security. <br>
Mitigation: Do not copy SSL-disabling or HTTP examples into production; keep TLS verification enabled unless there is a reviewed exception. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/volc-sdk-team/skills/volcengine-sdk-generator) <br>
- [Query aliases](references/query_aliases.json) <br>
- [Go SDK integration reference](references/sdk-integration-go.md) <br>
- [Java SDK integration reference](references/sdk-integration-java.md) <br>
- [Node.js SDK integration reference](references/sdk-integration-nodejs.md) <br>
- [PHP SDK integration reference](references/sdk-integration-php.md) <br>
- [Python SDK integration reference](references/sdk-integration-python.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with generated SDK code blocks and concise guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include mocked required top-level parameters when the user omits them; generated examples should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
