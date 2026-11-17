## Description:

RankClaw — AI Agent Trust Layer. Check any ClawHub, OpenClaw, nanobot, nanoclaw, picoclaw, or MCP server skill against 14,700+ indexed tools before installing. Get security scores, malicious flags, and AI-generated safety verdicts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tudoanh](https://clawhub.ai/user/tudoanh)

### License/Terms of Use:


## Use Case:

Developers and agent operators use RankClaw to check ClawHub, OpenClaw, nanobot, nanoclaw, picoclaw, and MCP server skills before installation. It provides security verdicts, trust scores, malicious-skill flags, leaderboard/search results, and installation guidance for safer agent tooling decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to use RankClaw service results when deciding whether to install other skills.

Mitigation: Treat RankClaw results as advisory evidence and keep user or operator review in the installation decision path.

Risk: The documented nanoclaw bridge download uses an unpinned GitHub main-branch URL.

Mitigation: Pin and verify the exact bridge script before use instead of downloading an unversioned main-branch file.

Risk: MCP requests sent through the bridge leave the local machine for api.rankclaw.com.

Mitigation: Avoid sending sensitive private data in RankClaw MCP requests and disclose the outbound service call to users.

## Reference(s):

- [RankClaw Homepage](https://rankclaw.com)
- [RankClaw MCP Endpoint](https://api.rankclaw.com/api/mcp/)
- [ClawHub Skill Page](https://clawhub.ai/tudoanh/skills/rankclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, JSON-RPC responses, shell command examples, and client configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory and may include external service results from api.rankclaw.com.]

## Skill Version(s):

2.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
