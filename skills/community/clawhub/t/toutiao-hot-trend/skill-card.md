## Description:

Helps agents summarize and lightly analyze public Toutiao articles, videos, topic pages, searches, and channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codekungfu](https://clawhub.ai/user/codekungfu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create concise summaries and lightweight statistics from public Toutiao content by keyword, channel, or video page. It is intended for public-page analysis and reminders, not bulk scraping, interface reverse engineering, video downloading, or watermark removal.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automation could violate Toutiao platform rules if expanded into bulk scraping or interface reverse engineering.

Mitigation: Limit use to public pages, avoid bulk collection and interface reverse engineering, and follow Toutiao platform rules.

Risk: Dynamic rendering or anti-automation behavior can make extracted public metadata incomplete or stale.

Mitigation: Prefer human-opened pages when needed, keep request frequency low, and include collection timestamps in results.

Risk: Video workflows could drift beyond the intended boundary into downloading media or removing watermarks.

Mitigation: Use the skill only for public video metadata and summary extraction; do not download videos or remove watermarks.

## Reference(s):

- [Toutiao homepage](https://www.toutiao.com/)
- [Toutiao search](https://www.toutiao.com/search)
- [ClawHub skill page](https://clawhub.ai/codekungfu/skills/toutiao-hot-trend)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summaries and structured lists with public source links and collection timestamps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include titles, authors, sources, publish times, public interaction counts, channel names, summaries, tags, links, and collection timestamps.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
