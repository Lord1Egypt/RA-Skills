## Description:

Manage and monitor a personal stock watchlist with support for adding, removing, listing stocks, and summarizing recent performance using data from 10jqka.com.cn.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robin797860](https://clawhub.ai/user/robin797860)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to maintain a personal Chinese A-share watchlist, run local watchlist management scripts, and summarize recent market performance for saved stock codes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clear and uninstall flows can erase saved watchlist entries.

Mitigation: Back up ~/.clawdbot/stock_watcher/watchlist.txt before clearing or uninstalling, and review destructive commands before execution.

Risk: Performance summaries require outbound network lookups to 10jqka.com.cn and may depend on delayed or unavailable market data.

Mitigation: Use the skill only when those network requests are acceptable, and treat returned market data as informational rather than investment advice.

Risk: Python dependencies may be installed from the ambient package environment.

Mitigation: Install requests and beautifulsoup4 in a virtual environment with pinned versions.

## Reference(s):

- [Stock Watcher on ClawHub](https://clawhub.ai/robin797860/skills/stock-watcher)
- [10jqka Stock Pages](https://stockpage.10jqka.com.cn/{stock_code}/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown or plain text with shell commands, watchlist entries, and stock performance summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local watchlist file under ~/.clawdbot/stock_watcher and outbound lookups to 10jqka.com.cn for performance summaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
