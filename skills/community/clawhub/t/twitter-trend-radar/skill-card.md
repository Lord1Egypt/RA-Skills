## Description:

Find early product, tool, game, and SEO opportunity signals from X/Twitter using the local bird CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kevin-free](https://clawhub.ai/user/kevin-free)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, SEO researchers, and product builders use this skill to find early X/Twitter launch signals, rank linked domains, and turn promising trends into manual research or landing-page ideas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on a third-party bird CLI that may access X/Twitter through browser-profile credentials.

Mitigation: Use a pinned and reviewed bird version with a dedicated browser profile or low-privilege X/Twitter account.

Risk: Search topics, cached results, and browser-profile access may expose sensitive research intent.

Mitigation: Avoid sensitive private topics unless external service exposure is acceptable, and review cached files under .cache/twitter-trend-radar.

Risk: X/Twitter web search behavior can rate-limit, block, or change, which may make results incomplete or inconsistent.

Mitigation: Keep searches low frequency, use caching, avoid concurrency, and manually verify top opportunities before acting.

Risk: Trend scores can be misleading if a linked site is old, inaccessible, legally sensitive, or not backed by real search demand.

Mitigation: Manually check the site, demand signals, competition, and brand or trademark risk before creating pages or products.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kevin-free/skills/twitter-trend-radar)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Shell commands, Guidance]

**Output Format:** [Markdown or JSON reports with command-line guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include candidate domains, scores, engagement signals, domain-age details when available, source links, suggested pages, and next actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
