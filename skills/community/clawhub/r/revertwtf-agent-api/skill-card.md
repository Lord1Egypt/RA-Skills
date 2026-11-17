## Description:

Use revert.wtf safely from agents, tools, browsers, or integrations through bounded HTTP APIs, MCP tools, and lightweight package subpaths without downloading the full catalog into client bundles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrtdlgc](https://clawhub.ai/user/mrtdlgc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to explain EVM, RPC, provider, wallet, account abstraction, and x402 errors, resolve selectors, search revert.wtf catalog entries, and integrate revert.wtf through bounded APIs or lightweight packages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hosted API requests may include error text that contains secrets, unreleased exploit details, or personal data.

Mitigation: Send only error text appropriate for revert.wtf processing, avoid secrets and personal data, or keep analysis local through package subpaths when needed.

Risk: Broad catalog fetching or server-oriented package imports in browser clients can increase exposure and bundle size.

Mitigation: Use bounded search and explain flows, lightweight browser helpers, or a server/API boundary for full parser and catalog-backed functionality.

## Reference(s):

- [revert.wtf Explain API](https://revert.wtf/api/explain)
- [ClawHub Skill Page](https://clawhub.ai/mrtdlgc/skills/revertwtf-agent-api)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown guidance with inline bash and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance emphasizes bounded API and MCP use, precise package imports, and avoiding secrets or personal data in hosted requests.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
