## Description: <br>
API文档生成器 helps developers turn code, URLs, OpenAPI files, or API descriptions into OpenAPI 3.0/Swagger documentation with SDK examples, mock-server configuration, and integration test guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qqyougitcom](https://clawhub.ai/user/qqyougitcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and API teams use this skill to convert implementation code, interface definitions, URLs, or natural-language endpoint descriptions into readable API documentation and supporting examples for REST, GraphQL, WebSocket, SDK, mock, and test workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SDK examples, cURL commands, mock servers, or tests may call real services or mutate data if run with live credentials or create/update/delete endpoints. <br>
Mitigation: Safe to install for generating API documentation. Review any generated SDK, curl, mock-server, or test code before running it against real services, especially where real API tokens or create/update/delete endpoints are involved; request a different output language explicitly if needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qqyougitcom/qqyougit-api-doc-generator) <br>
- [Detailed API documentation generator reference](references/details.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation with OpenAPI YAML/JSON, SDK code examples, cURL commands, mock-server configuration, and integration test snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended for review before generated SDK, curl, mock-server, or test code is run against real services.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
