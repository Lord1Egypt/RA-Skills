## Description:

X Intelligence CLI helps agents search, monitor, analyze, and engage with X/Twitter from the terminal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xnyk](https://clawhub.ai/user/0xnyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, researchers, and agents use Xint to gather current X/Twitter discourse, monitor topics or accounts, analyze sentiment with xAI/Grok, and export findings for reports or workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation and optional server patterns require review before use.

Mitigation: Review install.sh or use Homebrew or manual source checkout, and set XINT_INSTALL_REQUIRE_CHECKSUM=1 when using the installer.

Risk: Broad, long-lived X/xAI credentials and OAuth scopes can expose account access.

Mitigation: Use least-privilege credentials, avoid tweet.write unless required, and keep secrets out of logs and shared exports.

Risk: Webhooks, SSE MCP, and the package API server can transmit data or expose local services.

Mitigation: Enable them only in trusted environments with explicit authentication, HTTPS or localhost-only endpoints, and host controls.

## Reference(s):

- [Xint Skill Page](https://clawhub.ai/0xnyk/skills/xint)
- [X API Reference Notes](references/x-api.md)
- [Xint README](README.md)
- [Xint Skill Instructions](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Terminal text, Markdown, JSON, JSONL, CSV, and shell commands depending on command options.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can write local cache, exports, snapshots, and OAuth token state under data/ when commands request or require local state.]

## Skill Version(s):

2026.2.26 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
