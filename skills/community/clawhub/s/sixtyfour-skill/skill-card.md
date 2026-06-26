## Description: <br>
People and company intelligence via the Sixtyfour AI API for live-web lead enrichment, company research, contact discovery, lead qualification, search, and batch enrichment workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rxhxm](https://clawhub.ai/user/rxhxm) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to call Sixtyfour AI APIs for people and company enrichment, contact discovery, lead scoring, search, and batch workflow execution. It is intended for enrichment and research workflows that require structured, confidence-scored output from live web research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to look up personal emails, phone numbers, and other sensitive contact data. <br>
Mitigation: Confirm a lawful and authorized basis before enrichment or contact-discovery requests, and limit requested fields to data needed for the approved workflow. <br>
Risk: API keys are required for authenticated Sixtyfour requests. <br>
Mitigation: Store SIXTYFOUR_API_KEY securely, avoid exposing it in prompts or logs, and rotate it if it may have been disclosed. <br>
Risk: Paid, bulk, workflow, webhook, or CSV enrichment actions can process many records or incur cost. <br>
Mitigation: Require explicit approval before running paid, bulk, workflow, webhook, or CSV actions, and avoid uploading confidential or unnecessary CSV fields. <br>
Risk: The artifact mentions an optional sixtyfour-mcp package. <br>
Mitigation: Review the package separately before installing or running it in an MCP client. <br>


## Reference(s): <br>
- [Sixtyfour Skill on ClawHub](https://clawhub.ai/rxhxm/sixtyfour-skill) <br>
- [Sixtyfour API Detailed Reference](references/api-details.md) <br>
- [Sixtyfour Documentation](https://docs.sixtyfour.ai) <br>
- [Sixtyfour OpenAPI Spec](https://api.sixtyfour.ai/openapi.json) <br>
- [Sixtyfour App](https://app.sixtyfour.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls, JSON] <br>
**Output Format:** [Markdown with curl commands, JSON payloads, response examples, and setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to make authenticated Sixtyfour API calls that return structured enrichment data, confidence scores, references, CSV downloads, job identifiers, or webhook results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
