## Description:

Track autonomous driving and Robotaxi sector intelligence with Pony.ai, Waymo, Tesla Robotaxi, and Baidu Apollo as core targets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangzhe1991](https://clawhub.ai/user/yangzhe1991)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external analysts use this skill to produce twice-daily incremental briefings on autonomous driving and robotaxi market developments. It focuses on fresh public-source reporting, prior-report delta comparison, source URL resolution, and competitive context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Briefings depend on public web, RSS, Reddit, and social-search sources that can be incomplete, stale, or misleading.

Mitigation: Require 24-hour freshness, resolved source URLs, source status reporting, and cross-verification for financial, licensing, permit, and safety-sensitive claims.

Risk: The workflow writes report files and removes old matching robotaxi report files in the OpenClaw memory directory.

Mitigation: Review the configured memory path and cleanup pattern before deployment, especially in shared or restricted environments.

Risk: The skill includes shell examples for direct public-source fetching and URL resolution.

Mitigation: Review shell execution policy before installation and follow the skill's single-command URL-resolution guidance in environments that restrict shell access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangzhe1991/skills/robotaxi-briefing)
- [Publisher profile](https://clawhub.ai/user/yangzhe1991)
- [TechCrunch RSS feed](https://techcrunch.com/feed/)
- [The Verge RSS feed](https://www.theverge.com/rss/index.xml)
- [Wired RSS feed](https://www.wired.com/feed/rss)
- [Ars Technica RSS feed](https://arstechnica.com/feed/)
- [Reuters technology feed](https://www.reutersagency.com/feed/?taxonomy=best-sectors&post_type=best&best-sectors=tech)
- [SelfDrivingCars Reddit feed](https://www.reddit.com/r/SelfDrivingCars/new.json?limit=15)
- [Reuters autos and transportation](https://www.reuters.com/technology/autos-transportation/)
- [36Kr robotaxi search](https://36kr.com/search/articles/robotaxi)
- [CLS robotaxi search](https://www.cls.cn/searchPage?keyword=robotaxi)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Chinese Markdown briefing with bare source URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes 24-hour delta comparison, source status reporting, resolved final-domain URLs, and scoped local report retention guidance.]

## Skill Version(s):

6.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
