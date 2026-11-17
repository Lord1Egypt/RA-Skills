## Description:

Fast X Intelligence CLI (Rust) for searching, monitoring, analyzing, and engaging with X/Twitter from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xnyk](https://clawhub.ai/user/0xnyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and operators use this skill to run X/Twitter search, monitoring, profile, thread, trend, follower-tracking, and Grok-assisted analysis workflows from a CLI or optional MCP server. It is suitable for intelligence reports, social listening, and structured exports when the required X and xAI credentials are available.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer execution may run code retrieved over the network.

Mitigation: Review the installer first, prefer a trusted package manager, or build from a reviewed source tag.

Risk: OAuth and engagement commands can mutate an X account or expose broad account scopes.

Mitigation: Use read_only policy by default and run OAuth setup only when account actions are intentional.

Risk: Webhooks, collections, bookmark knowledge-base sync, and package API features can share data with remote services.

Mitigation: Use only endpoints and workspaces you control, and review exported or synced content before sharing.

Risk: Local caches, exports, snapshots, media, and OAuth tokens may contain sensitive search queries or account data.

Mitigation: Keep local data paths private, preserve restrictive token permissions, and review generated files before distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xnyk/skills/xint-rs)
- [X API access](https://developer.x.com)
- [Rust language](https://www.rust-lang.org)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, JSONL, CSV, shell commands, configuration, guidance]

**Output Format:** [Terminal output, Markdown reports, structured JSON/JSONL, CSV exports, and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write cache, exports, snapshots, OAuth tokens, and downloaded media under local data paths when commands request it.]

## Skill Version(s):

2026.2.26 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
