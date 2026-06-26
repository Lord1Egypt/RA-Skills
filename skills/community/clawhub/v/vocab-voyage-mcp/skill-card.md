## Description: <br>
Provides hosted MCP vocabulary tools for definitions, quizzes, word lists, study plans, and contextual explanations for academic and standardized test preparation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jaideepdhanoa](https://clawhub.ai/user/jaideepdhanoa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, educators, and agents use this skill to look up vocabulary, generate test-prep quizzes, list course words, explain words in context, and preview study plans for ISEE, SSAT, SAT, PSAT, GRE, GMAT, LSAT, and general academic vocabulary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Personal bearer tokens can expose profile or progress data if leaked. <br>
Mitigation: Use anonymous mode unless personalized features are needed; keep tokens out of source control and revoke or rotate exposed tokens. <br>
Risk: Hosted tool calls may be logged with referral, account, or IP-derived analytics. <br>
Mitigation: Review privacy expectations before enabling authenticated features or referral-tagged endpoints. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jaideepdhanoa/vocab-voyage-mcp) <br>
- [Vocab Voyage MCP Documentation](https://vocab.voyage/mcp) <br>
- [Authentication and Scopes Reference](https://vocab.voyage/developers/auth) <br>
- [MCP Server Card](https://vocab.voyage/.well-known/mcp/server-card.json) <br>
- [Agent Card](https://vocab.voyage/.well-known/agent-card.json) <br>
- [OpenAPI Specification](https://vocab.voyage/openapi.json) <br>
- [MCP Apps Manifest](https://vocab.voyage/.well-known/mcp/apps.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance, configuration] <br>
**Output Format:** [MCP tool responses with structured JSON, human-readable text, and optional MCP Apps UI resources.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Hosted streamable HTTP endpoint; anonymous use is supported, with optional bearer tokens for personalized features.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact manifests list 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
