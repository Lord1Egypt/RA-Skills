## Description:

Tracks selected TikTok creators and reports new videos and follower-count changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[memeanalyst](https://clawhub.ai/user/memeanalyst)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, social media managers, and analysts can monitor a TikTok creator watchlist for new videos and follower-count changes, or request one-off creator and video lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Actor usage is billed at $0.001 per returned record on the user's Apify account, so backfills and recurring checks can add up.

Mitigation: Review the expected record volume, backfill choice, and schedule against the per-record charge before enabling recurring checks.

Risk: The security review could not assess the referenced tracking state file, so its findings have medium confidence.

Mitigation: Review the state file's location, permissions, and stored watchlist before running the skill.

## Reference(s):

- [Apify TikTok Scraper](https://apify.com/magnova/tiktok-scraper)
- [ClawHub release](https://clawhub.ai/memeanalyst/skills/tiktok-creator-tracker)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON state file]

**Output Format:** [Markdown alerts and summaries, with a JSON file for the watchlist and tracking state]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scheduled checks fetch up to 20 recent videos per creator by default; one-off requests can ask for up to 50.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
