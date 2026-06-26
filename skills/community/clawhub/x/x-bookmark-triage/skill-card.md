## Description: <br>
Automatically triages X/Twitter bookmarks into structured knowledge cards and posts them to a Discord channel, using Claude Haiku to score relevance, assign tier, freshness, topic tags, and optionally remove captured bookmarks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeremyknows](https://clawhub.ai/user/jeremyknows) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and knowledge workers use this skill to turn X/Twitter bookmarks and manually dropped URLs into structured Discord knowledge cards, drain bookmark backlogs, and maintain a searchable intake stream. It supports standalone operation or optional OpenClaw scheduling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses persistent X, Discord, and Anthropic credentials. <br>
Mitigation: Store tokens in a real secret manager or protected environment, avoid printing secrets, and review any cron, launchd, or systemd setup before enabling unattended runs. <br>
Risk: Bookmark content and URLs are sent to third-party services for fetching, model triage, and Discord posting. <br>
Mitigation: Install only for accounts and channels where this data flow is acceptable, and test with non-sensitive bookmarks first. <br>
Risk: Automated polling and backlog sweeps can remove X/Twitter bookmarks after capture. <br>
Mitigation: Run with dry-run behavior first, prefer read-only OAuth scopes or no-unbookmark mode unless deletion is intentional, and confirm output quality before scheduled operation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jeremyknows/x-bookmark-triage) <br>
- [OAuth setup guide](references/oauth-setup.md) <br>
- [Cron setup guide](references/cron-setup.md) <br>
- [Adapting guide](references/adapting.md) <br>
- [X Developer Platform](https://developer.x.com) <br>
- [Discord Developer Portal](https://discord.com/developers/applications) <br>
- [Anthropic Console](https://console.anthropic.com) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown Discord knowledge cards with setup guidance and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Cards include tier, freshness, topic, tags, rationale, proposed action, and source link; local state tracks seen URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
