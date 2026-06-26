## Description: <br>
QuiverAI Quickstart guides users through creating a QuiverAI account, configuring an API key, installing the Node.js SDK, and sending SVG generation requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[charmmm718](https://clawhub.ai/user/charmmm718) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to learn the basic QuiverAI SVG generation workflow, including account setup, API key configuration, SDK installation, REST calls, error handling, and credit usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: QuiverAI API keys could be exposed if copied into source control, chat logs, or shared transcripts. <br>
Mitigation: Store QUIVERAI_API_KEY in a secure environment variable or secrets manager and use revocable keys when possible. <br>
Risk: Installing @quiverai/sdk without verification could introduce package supply-chain risk. <br>
Mitigation: Verify the package name and source before installation and use normal dependency review controls. <br>
Risk: QuiverAI API calls may consume account credits. <br>
Mitigation: Review prompts and request volume before execution, and monitor account credit usage. <br>


## Reference(s): <br>
- [QuiverAI Homepage](https://quiver.ai) <br>
- [QuiverAI Start](https://quiver.ai/start) <br>
- [QuiverAI API Reference](https://docs.quiver.ai/api-reference/introduction) <br>
- [QuiverAI Pricing](https://docs.quiver.ai/api/pricing) <br>
- [Text to SVG Model](https://docs.quiver.ai/models/text-to-svg) <br>
- [Image to SVG Model](https://docs.quiver.ai/models/image-to-svg) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with shell commands, JavaScript snippets, REST examples, and JSON error examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires QUIVERAI_API_KEY for live API use; successful API calls may consume account credits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
