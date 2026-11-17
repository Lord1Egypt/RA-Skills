## Description:

Provides summaries of movie showtimes, prices, ratings, and basic public movie or cinema information from Taopiaopiao pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mike47512](https://clawhub.ai/user/mike47512)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to summarize public Taopiaopiao movie and cinema pages, including showtimes, theater details, price ranges, ratings, cast, runtime, and release information. It is intended for lightweight analysis and reminders, not booking or account actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Showtimes, prices, and availability may vary by time and region.

Mitigation: Include the collection time, region, and source link in summaries that use showtime or price information.

Risk: The skill could be misused for purchases, account actions, or attempts to bypass platform controls.

Mitigation: Keep usage limited to public-page summarization and do not perform booking, payment, account, reverse-engineering, or platform-bypass actions.

Risk: High-frequency collection could become bulk scraping.

Mitigation: Use frequency control, avoid bulk collection, and prefer human-opened public pages before parsing when dynamic rendering or location context matters.

## Reference(s):

- [Taopiaopiao Homepage](https://dianying.taobao.com/)
- [ClawHub Skill Page](https://clawhub.ai/mike47512/skills/taopiaopiao)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summaries should include collection time, region, and source links when showtime or price information is used.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence, created 2026-03-18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
