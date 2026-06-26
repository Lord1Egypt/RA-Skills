## Description: <br>
Fast X Intelligence CLI for searching, monitoring, analyzing, and engaging with X/Twitter from the terminal. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[0xNyk](https://clawhub.ai/user/0xNyk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to run terminal-based X/Twitter search, monitoring, profile lookup, trend discovery, sentiment analysis, intelligence reports, and selected account actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can request broad X account authority through OAuth for actions such as bookmarks, likes, follows, lists, blocks, and mutes. <br>
Mitigation: Prefer read_only policy mode, avoid OAuth setup unless account actions are required, and review requested X scopes before authorizing. <br>
Risk: Collection and bookmark knowledge-base features can upload selected local files or bookmark-derived content to xAI. <br>
Mitigation: Do not run collection upload, directory sync, or bookmark cloud sync on private material; review paths and files before use. <br>
Risk: Webhook and network-facing modes can send data to external services or expose a server mode. <br>
Mitigation: Use only webhook endpoints you control and require explicit approval before network-facing modes such as watch webhooks or MCP SSE. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/0xNyk/xint-rs) <br>
- [X API access documentation](https://developer.x.com) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, CSV, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and optional JSON, JSONL, CSV, or report file outputs from xint commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write cache, exports, snapshots, and OAuth token data under the skill data directory when those commands are used.] <br>

## Skill Version(s): <br>
2026.2.26 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
