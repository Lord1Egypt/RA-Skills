## Description: <br>
RankClaw checks ClawHub, OpenClaw, nanobot, nanoclaw, picoclaw, and MCP server skills before installation and returns security scores, malicious flags, and AI-generated safety verdicts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tudoanh](https://clawhub.ai/user/tudoanh) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, security reviewers, and AI agents use RankClaw to check skills and MCP servers before installation, review verdicts and trust scores, and find safer alternatives when a package is risky or malicious. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Skill lookup queries and MCP request contents are sent to RankClaw's remote service. <br>
Mitigation: Use the skill only when sharing those requests with RankClaw is acceptable for the user's privacy and compliance requirements. <br>
Risk: Agents may over-rely on RankClaw scores when deciding whether to install or reject another skill. <br>
Mitigation: Keep user confirmation in the loop and review key findings before making installation decisions based solely on a score. <br>
Risk: The nanoclaw setup example downloads bridge code from an unpinned branch. <br>
Mitigation: Prefer a reviewed bundled bridge copy or a pinned version with a checksum before running the bridge. <br>


## Reference(s): <br>
- [ClawHub RankClaw listing](https://clawhub.ai/tudoanh/rankclaw) <br>
- [RankClaw homepage](https://rankclaw.com) <br>
- [RankClaw MCP endpoint](https://api.rankclaw.com/api/mcp/) <br>
- [RankClaw leaderboard API](https://api.rankclaw.com/api/leaderboard/?per_page=10&safe_only=1) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON configuration examples, shell commands, and MCP/API JSON responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns skill verdicts, scores, findings, leaderboard results, search results, and malicious-skill listings through remote RankClaw services.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
