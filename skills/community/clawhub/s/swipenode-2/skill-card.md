## Description:

Swipenode is a web extraction skill for AI agents that extracts structured JSON from Next.js, Nuxt.js, Gatsby, and Remix pages without headless browsers while reducing raw HTML token overhead.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nefas11](https://clawhub.ai/user/nefas11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use Swipenode to extract structured data or clean text from modern web pages for e-commerce, news, market research, and other API-less data collection workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses WAF-bypass and TLS spoofing behavior for web scraping.

Mitigation: Use it only on sites where you have permission to automate access and where this access pattern complies with site terms and applicable policy.

Risk: The skill directs users to build and run an external binary and MCP server.

Mitigation: Review the exact source to be built, pin a trusted commit or release, confirm the canonical repository, and inspect MCP configuration changes before enabling the server.

Risk: Extraction commands can accept custom headers that may contain sensitive values.

Mitigation: Avoid passing secrets in headers unless required, and scope any credentials to the minimum permissions and lifetime needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nefas11/skills/swipenode-2)
- [Publisher profile](https://clawhub.ai/user/nefas11)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and extracted JSON or text examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce structured JSON from framework data, clean visible text fallback output, batch extraction commands, and MCP setup guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
