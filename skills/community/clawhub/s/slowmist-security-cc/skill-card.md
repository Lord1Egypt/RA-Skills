## Description:

SlowMist AI Agent Security Review provides a security review framework for skills, repositories, URLs, on-chain addresses, products, and social shares in Claude Code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xcjl](https://clawhub.ai/user/0xcjl)

### License/Terms of Use:

MIT

## Use Case:

Developers and security reviewers use this skill to route security reviews, inspect external inputs, apply risk ratings, and produce review reports before installing or trusting tools, repositories, documents, on-chain assets, products, or social-share recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the skill recommends writing review results from untrusted sources into Claude memory without enough controls.

Mitigation: Disable or ignore the optional memory-log behavior unless records are stored outside agent memory in a structured, sanitized format with content hashes.

Risk: The security evidence advises care around local MCP or Claude configuration review.

Mitigation: Require explicit user direction before reading local MCP or Claude configuration files and keep review scope limited to the requested files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xcjl/skills/slowmist-security-cc)
- [Skill README](README.md)
- [Skill / MCP installation review](references/skill-mcp.md)
- [GitHub repository review](references/repository.md)
- [URL / document review](references/url-document.md)
- [On-chain address / contract / DApp review](references/onchain.md)
- [Product / service / API / SDK review](references/product-service.md)
- [Social share review](references/message-share.md)
- [Code red flag patterns](references/red-flags.md)
- [Social engineering and prompt injection patterns](references/social-engineering.md)
- [Supply chain attack patterns](references/supply-chain.md)
- [SlowMist Agent Security original framework](https://github.com/slowmist/slowmist-agent-security)
- [OpenClaw Security Practice Guide](https://github.com/slowmist/openclaw-security-practice-guide)
- [Optional MistTrack skills integration](https://github.com/slowmist/misttrack-skills)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown review reports, checklists, ratings, and recommendations, with inline command or configuration snippets when relevant.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces conservative security guidance and may recommend human approval for high-risk findings.]

## Skill Version(s):

1.0.0 (source: frontmatter, artifact metadata, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
