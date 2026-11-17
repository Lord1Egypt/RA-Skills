## Description:

SnapChat Ads CLI helps agents analyze Snapchat Ads data, inspect account structure, pull performance statistics, debug delivery issues, estimate bids and audience size, review creatives and audiences, manage AR lenses, and retrieve billing information through the snapchat-ads-cli tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bin-huang](https://clawhub.ai/user/bin-huang)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers, analysts, and developers use this skill to query Snapchat Ads organizations, accounts, campaigns, ad squads, ads, creatives, audiences, pixels, billing records, and performance statistics. It supports reporting, troubleshooting, conversion tracking checks, and account exploration when the user has an appropriate Snapchat Ads OAuth token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a third-party CLI package installed globally and handled with a Snapchat Ads OAuth token.

Mitigation: Use a pinned, reviewed, local or sandboxed install before granting access to production accounts.

Risk: Snapchat Ads OAuth tokens can expose sensitive campaign, audience, billing, member, and account records.

Mitigation: Use narrowly scoped and short-lived tokens, avoid logging sensitive records, and rotate tokens if package behavior is unexpected.

Risk: Billing, audience, member, and performance outputs may contain commercially sensitive information.

Mitigation: Limit shared transcripts and exported CLI output to the minimum data needed for the task.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/bin-huang/skills/snapchat-ads-cli)
- [snapchat-ads-cli documentation](https://github.com/Bin-Huang/snapchat-ads-cli)
- [Snapchat Marketing API overview](https://developers.snap.com/api/marketing-api/Ads-API)
- [Snapchat Marketing API authentication](https://developers.snap.com/api/marketing-api/Ads-API/authentication)
- [Snapchat Measurement API](https://developers.snap.com/api/marketing-api/Ads-API/measurement)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs use of a read-only CLI whose commands output pretty-printed JSON by default.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
