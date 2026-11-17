## Description:

Daily retrieves Trump-related news from official and major wire sources, then translates, edits, and delivers concise Chinese summaries to the user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wall-nut417](https://clawhub.ai/user/wall-nut417)

### License/Terms of Use:

MIT-0

## Use Case:

External users and OpenClaw operators use this skill to collect recent Trump-related items from selected public sources, translate them into Chinese, and receive a concise news digest by chat or optional Telegram delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Truth Social support may require sensitive credentials or a browser session token and uses an optional unpinned dependency.

Mitigation: Avoid browser session tokens when possible, pin and review truthbrush before enabling it, and keep credentials in a restricted environment.

Risk: The workflow makes outbound requests and can optionally send generated summaries to Telegram.

Mitigation: Enable Telegram or cron delivery only after verifying the destination, schedule, and operating environment.

Risk: Feed failures, access limits, or stale source data can produce incomplete news coverage.

Mitigation: Review source links in the generated digest and treat the result as a source snapshot rather than exhaustive real-time coverage.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wall-nut417/skills/trump-news)
- [Truthbrush Python Package](https://pypi.org/project/truthbrush/)
- [White House Briefing Room Feed](https://www.whitehouse.gov/briefing-room/feed/)
- [Federal Register Documents API](https://www.federalregister.gov/api/v1/documents.json)
- [SCOTUSblog Feed](https://www.scotusblog.com/feed/)
- [Reuters Political Feed](https://www.reutersagency.com/feed/?best-topics=political-general&post_type=best)
- [Associated Press Top News Feed](https://feeds.apnews.com/rss/ap_top_news)
- [AFP Feed](https://www.afp.com/en/actus/afp_communique/all/feed)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown news digest with source links, plus optional shell commands and configuration guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries are intended to be translated and edited into Chinese before chat or optional Telegram delivery.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
