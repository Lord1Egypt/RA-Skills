## Description: <br>
Star Search gives agents MCP and HTTP/SSE tools for web, news, finance, academic/code, and deep-research search with optional LLM-generated answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muchenhengxin](https://clawhub.ai/user/muchenhengxin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can use this skill to give an LLM agent real-time search, news, finance, source lookup, and answer-generation capabilities. It is most relevant when an agent needs Chinese and English web results, structured search output, or MCP-accessible search tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes credentials, account/payment logic, upload handling, persistence, and server administration behavior beyond a lightweight search wrapper. <br>
Mitigation: Install only from a trusted publisher, review configuration before use, and deploy with restricted credentials and least-privilege service accounts. <br>
Risk: LLM, Cloudflare, server deployment, OCR upload, account, and payment configuration can expose sensitive data or operational access if misconfigured. <br>
Mitigation: Restrict API keys and tokens, avoid running deployment or root scripts unless administering the full service, and do not expose HTTP/SSE endpoints without intentional access controls. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/muchenhengxin/star-search) <br>
- [v16-v17 legacy archive](references/v16-v17-legacy-archive.md) <br>
- [Frontend answer card](references/v17-frontend-answer-card.md) <br>
- [LLM answer quality strategy](references/v17-llm-answer-quality-strategy.md) <br>
- [MCP server zero dependencies](references/mcp-server-zero-deps.md) <br>
- [Honest LLM answer prompt](references/llm-answer-honest-prompt.md) <br>
- [AI-native search transformation](references/ai-native-search-transformation.md) <br>
- [Intent understanding test bench](references/intent-understanding-test-bench.md) <br>
- [Intent detection rule priority](references/intent-detection-rule-priority.md) <br>
- [Cloudflare bot protection](references/cloudflare-bot-protection.md) <br>
- [Source credibility 4D formula](references/source-credibility-4d-formula.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, JSON, tables, Mermaid diagrams, and MCP tool result text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return search results, citations, LLM answers, engine lists, and deployment or integration guidance.] <br>

## Skill Version(s): <br>
20.39.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
