## Description: <br>
Manage Vapi voice assistants, calls, phone numbers, tools, and webhooks via the Vapi REST API or CLI for voice agent operations and integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[colygon](https://clawhub.ai/user/colygon) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to manage Vapi voice assistants, calls, phone numbers, tools, and webhooks for voice agent operations and integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can manage a real Vapi account, including creating assistants, changing phone or webhook settings, and starting outbound calls. <br>
Mitigation: Require explicit user approval before mutating account resources or initiating calls. <br>
Risk: The VAPI_API_KEY secret could be exposed if pasted into logs or prompts. <br>
Mitigation: Keep VAPI_API_KEY in a secret store or trusted environment variable and avoid printing it. <br>
Risk: Changing VAPI_BASE_URL can direct authenticated requests to an untrusted endpoint. <br>
Mitigation: Leave VAPI_BASE_URL unset unless the endpoint is explicitly trusted. <br>
Risk: The optional Vapi CLI installer uses a curl-to-bash flow. <br>
Mitigation: Inspect the installer before running it or avoid the optional CLI path. <br>


## Reference(s): <br>
- [Vapi docs introduction](https://docs.vapi.ai/quickstart/introduction) <br>
- [Vapi API reference](https://api.vapi.ai/api) <br>
- [Vapi CLI](https://github.com/VapiAI/cli) <br>
- [Vapi MCP docs](https://docs.vapi.ai/cli/mcp) <br>
- [Vapi Node example server](https://github.com/VapiAI/example-server-javascript-node) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Code, Configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VAPI_API_KEY for authenticated API operations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
