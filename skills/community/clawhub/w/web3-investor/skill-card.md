## Description:

AI-native DeFi investment intelligence for discovering, analyzing, and comparing yield opportunities across protocols using intent-aware search, risk scoring, security scanning, smart money signals, and server-side analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bevanding](https://clawhub.ai/user/bevanding)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to research DeFi yield opportunities, compare products, and generate risk-aware analysis from natural language or structured preferences. The skill is for investment research support, not custody or trade execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted DeFi queries, risk preferences, product IDs, session IDs, and optional feedback are sent to Antalpha's remote MCP server.

Mitigation: Do not submit wallet seed phrases, private keys, personally identifying details, or full private portfolio records; provide only the minimum investment context needed for research.

Risk: Investment research outputs may be affected by delayed APY data, incomplete market context, or limits in server-side analysis.

Mitigation: Review returned data quality and freshness fields, treat recommendations as research support, and perform independent due diligence before making investment decisions.

Risk: Reference material includes optional unpinned npx MCP examples that could execute third-party packages.

Mitigation: Pin and verify package sources before running those examples, or use the bundled Python client path instead.

## Reference(s):

- [ClawHub Web3 Investor skill page](https://clawhub.ai/bevanding/skills/web3-investor)
- [Antalpha MCP server endpoint](https://mcp-skills.ai.antalpha.com/mcp)
- [Antalpha homepage](https://www.antalpha.com/)
- [MCP servers reference](artifact/references/mcp-servers.md)
- [Protocol registry reference](artifact/references/protocols.md)
- [Risk assessment framework](artifact/references/risk-framework.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-formatted text with structured JSON-derived result summaries and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include ranked recommendations, product analysis, comparison summaries, clarification prompts, suggested next actions, and raw JSON fallback responses.]

## Skill Version(s):

3.8.2 (source: ClawHub release metadata; artifact frontmatter is 3.8.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
