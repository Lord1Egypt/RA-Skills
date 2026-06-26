## Description: <br>
SlowMist AI Agent Security Review is a Claude Code security-review framework for skills, repositories, URLs, on-chain addresses, and products. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xcjl](https://clawhub.ai/user/0xcjl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to perform conservative reviews before installing or trusting skills, MCP servers, packages, repositories, URLs, on-chain addresses, products, APIs, or socially shared tools. It helps route requests to focused checklists and produce risk-rated review guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional review log can capture sensitive security, repository, or wallet context if users paste secrets or private URLs. <br>
Mitigation: Do not store seed phrases, private keys, tokens, private repository URLs, or sensitive wallet context in the log; redact before saving. <br>
Risk: The skill intentionally triggers on many install, review, repository, URL, product, and blockchain-related requests, which can interrupt normal workflows. <br>
Mitigation: Use it when conservative review is desired and scope each review to the external input under consideration. <br>
Risk: Manual clone or install workflows rely on an external source while server-resolved GitHub import provenance is unavailable. <br>
Mitigation: Verify the clone source and artifact hashes before installing manually. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xcjl/slowmist-security-cc) <br>
- [Publisher profile](https://clawhub.ai/user/0xcjl) <br>
- [Artifact metadata homepage](https://github.com/0xcjl/slowmist-security-cc) <br>
- [MistTrack skills optional integration](https://github.com/slowmist/misttrack-skills) <br>
- [Skill and MCP installation review](references/skill-mcp.md) <br>
- [GitHub repository review](references/repository.md) <br>
- [URL and document review](references/url-document.md) <br>
- [On-chain address and contract review](references/onchain.md) <br>
- [Product, service, and API review](references/product-service.md) <br>
- [Group chat and social sharing review](references/message-share.md) <br>
- [Code red-flag patterns](references/red-flags.md) <br>
- [Social engineering patterns](references/social-engineering.md) <br>
- [Supply-chain attack patterns](references/supply-chain.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Shell commands] <br>
**Output Format:** [Markdown security review guidance with checklists, risk ratings, and optional command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include LOW, MEDIUM, HIGH, or REJECT ratings and review-log entries when the user requests traceability.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
