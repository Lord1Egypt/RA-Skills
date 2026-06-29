## Description: <br>
Drafts on-brand social replies, social posts, and Markdown blog posts from a compact request plus an optional JSON context object through AgentPMT-hosted remote tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agentpmt](https://clawhub.ai/user/agentpmt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and content teams use this skill to generate review-ready social media replies, original social posts, and short or long Markdown blog drafts in a requested brand voice. It is intended for drafting only and does not publish content, browse the web, retrieve URLs, or accept media files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided topics, posts, brand guidance, examples, and source material are sent to AgentPMT for remote processing. <br>
Mitigation: Keep inputs scoped to the minimum content needed and do not provide confidential business material or regulated personal data unless policy permits it. <br>
Risk: The skill may require account, wallet, or payment-related setup for some routes. <br>
Mitigation: Use the referenced AgentPMT setup skills for credential handling and do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agentpmt/writing-agent-human-style) <br>
- [AgentPMT marketplace page](https://www.agentpmt.com/marketplace/writing-agent-human-style) <br>
- [Action schema](artifact/schema.md) <br>
- [AgentPMT account MCP/REST setup](https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup) <br>
- [AgentPMT no-account AgentAddress/x402 setup](https://clawhub.ai/agentpmt/agentpmt-no-account-agentaddress-x402) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown] <br>
**Output Format:** [JSON response containing generated text or Markdown content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Social response calls return a responses array; draft calls return content and may include OUTPUT_TRUNCATED_TO_CHARACTER_LIMIT warnings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
