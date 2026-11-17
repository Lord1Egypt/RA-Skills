## Description:

Automates Xiaohongshu search, browsing, likes, and favorites for Singapore study-related topics, with history tracking to reduce repeated interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luckychay](https://clawhub.ai/user/luckychay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers or operators use this skill to configure and run Xiaohongshu account automation under a logged-in user account. It supports searching Singapore private university and study-abroad topics, browsing feeds, liking and favoriting posts, and maintaining local logs and interaction history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automates likes and favorites under a logged-in Xiaohongshu account and may perform account actions the user did not manually review.

Mitigation: Run manually or with a dry-run/review step first, keep execution frequency low, and confirm the account owner approves each automation scope.

Risk: The package normalizes recurring unattended execution through cron.

Mitigation: Avoid enabling the cron schedule unless recurring automation is intentional, document any installed cron entry, and remove it when the automation is no longer needed.

Risk: Local log and history files can accumulate account activity details over time.

Mitigation: Inspect and clear logs and history periodically, and protect the workspace path where the scripts write those files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luckychay/skills/xhs-auto-interaction)
- [Publisher profile](https://clawhub.ai/user/luckychay)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and script configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a running Xiaohongshu MCP service, an authenticated Xiaohongshu account, curl, and jq.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
