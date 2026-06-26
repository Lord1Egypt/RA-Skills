## Description: <br>
Provides API marketplace access for AI agents to discover and call external services including web search, image generation, code execution, text-to-speech, translation, financial data, weather, academic papers, email, and document conversion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ucmai](https://clawhub.ai/user/ucmai) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to discover UCM services and invoke external APIs from an agent through curl or another HTTP client when native capabilities are insufficient. It is suited for tasks that need current data, media generation, document conversion, sandboxed code execution, email, or other marketplace capabilities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Paid marketplace calls, email sends, and sandbox code execution can spend credits or perform external actions. <br>
Mitigation: Ask for confirmation before paid calls, email sends, or sandbox code execution; check balance and history when cost matters. <br>
Risk: Inputs sent through UCM may be processed by UCM and downstream providers. <br>
Mitigation: Do not send secrets, credentials, or confidential documents unless the user accepts that processing; redact sensitive inputs where possible. <br>
Risk: The UCM API key or terminal logs containing it could expose account access. <br>
Mitigation: Keep UCM_API_KEY private, avoid printing it unnecessarily, and protect logs that include credentials. <br>


## Reference(s): <br>
- [UCM Service Catalog](references/service-catalog.md) <br>
- [UCM Website](https://ucm.ai) <br>
- [UCM Source Repository](https://github.com/ucmai/skills) <br>
- [ClawHub Skill Page](https://clawhub.ai/ucmai/ucm) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, API Calls] <br>
**Output Format:** [Markdown guidance with curl commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access and UCM_API_KEY for authenticated paid service calls.] <br>

## Skill Version(s): <br>
1.1.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
