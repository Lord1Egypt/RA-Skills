## Description: <br>
Build, configure, and deploy conversational video agents using the Trugen AI platform API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AjayK47](https://clawhub.ai/user/AjayK47) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and teams use this skill to create and manage Trugen conversational video agents, including avatars, knowledge bases, webhooks, embeds, LiveKit integrations, tools, MCPs, multilingual settings, and bring-your-own LLM configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trugen API keys can be exposed if copied into client-side embeds or browser-visible code. <br>
Mitigation: Use a dedicated Trugen API key where possible and keep it in protected server-side configuration or agent environment variables. <br>
Risk: Recordings, transcripts, memory, uploaded knowledge bases, embeds, and external tool calls may involve personal or sensitive data. <br>
Mitigation: Review privacy controls before deployment, minimize sensitive data in embed URLs and uploaded content, and restrict external tool, MCP, webhook, and LLM-token access to the intended workflow. <br>
Risk: Delete endpoints can remove Trugen agents, knowledge bases, documents, templates, tools, or MCP resources. <br>
Mitigation: Confirm destructive actions and target identifiers before running delete requests. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/AjayK47/trugenai) <br>
- [Publisher Profile](https://clawhub.ai/user/AjayK47) <br>
- [Trugen AI Documentation](https://docs.trugen.ai/docs/overview) <br>
- [Trugen API Reference](https://docs.trugen.ai/api-reference/overview) <br>
- [Developer Portal](https://app.trugen.ai) <br>
- [GitHub Examples](https://github.com/trugenai/trugen-examples) <br>
- [Agents API Reference](references/agents.md) <br>
- [Embedding & Integration Reference](references/embedding.md) <br>
- [Knowledge Base API Reference](references/knowledge-base.md) <br>
- [Tools & MCPs Reference](references/tools-and-mcps.md) <br>
- [Webhooks & Callbacks Reference](references/webhooks.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with API examples, curl commands, JSON payloads, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRUGEN_API_KEY for authenticated Trugen API operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
