## Description: <br>
Typeform API integration with managed OAuth for creating forms, managing responses, and accessing insights. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an agent needs to read or modify Typeform forms, responses, insights, and workspaces through a managed OAuth connection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Typeform API requests, response data, connection metadata, and the Maton API key are routed through api.maton.ai. <br>
Mitigation: Install only when that routing is acceptable, use the intended Typeform connection, and prefer least-privileged access. <br>
Risk: Create, update, and delete requests can change Typeform resources. <br>
Mitigation: Confirm the target resource and intended effect with the user before running any write operation. <br>


## Reference(s): <br>
- [Typeform API Overview](https://www.typeform.com/developers/get-started) <br>
- [Typeform Forms API](https://www.typeform.com/developers/create/reference/retrieve-forms) <br>
- [Typeform Responses API](https://www.typeform.com/developers/responses/reference/retrieve-responses) <br>
- [Typeform Workspaces API](https://www.typeform.com/developers/create/reference/retrieve-workspaces) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with HTTP, Python, JavaScript, and shell examples; API responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MATON_API_KEY, network access, and a connected Typeform OAuth account.] <br>

## Skill Version(s): <br>
1.0.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
