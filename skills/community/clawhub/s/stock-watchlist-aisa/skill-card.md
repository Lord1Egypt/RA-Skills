## Description:

Manage a stock and crypto watchlist with target and stop alerts using live AISA price checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to maintain a local stock and crypto watchlist, set target and stop alerts, and run live checks through AISA with an AISA API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A custom AISA_BASE_URL can redirect API-key-authenticated ticker checks to an untrusted endpoint.

Mitigation: Leave AISA_BASE_URL unset unless the endpoint is intentionally trusted, and use a limited AISA key with spending controls.

Risk: Dependency resolution can install an unpinned openai package version.

Mitigation: Pin and review dependencies before running the script in production or other sensitive environments.

Risk: Watchlist tickers, targets, stops, and recent signals are stored in a local JSON state file.

Mitigation: Run in a controlled workspace and set CLAWDBOT_STATE_DIR to an appropriate local state location when needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bibaofeng/skills/stock-watchlist-aisa)
- [Publisher Profile](https://clawhub.ai/user/bibaofeng)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Plain text command output and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; stores watchlist state in a local JSON file by default.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
