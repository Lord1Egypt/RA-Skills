## Description:

Crawls TikTok video metadata via Apify or Playwright, analyzes hotspot signals with heat and coverage scoring, and generates static HTML trend reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tandongtaotao](https://clawhub.ai/user/tandongtaotao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to collect TikTok public metadata for configurable keywords, hashtags, creators, or music sources, then analyze emerging trend signals and produce local reports. It is oriented toward fashion hotspot monitoring by default, but the sources can be adapted to other domains.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Apify access and TikTok session data.

Mitigation: Use a dedicated low-privilege TikTok account and Apify token, keep tokens in the environment, and protect or delete data/tiktok_session.json after use.

Risk: Broad crawling or scheduled runs can create unexpected Apify billing or platform-use exposure.

Mitigation: Review source limits and provider configuration before running, set external billing limits, and avoid --schedule unless continuous monitoring is intended.

Risk: The artifact includes a video downloader that can save local media from TikTok URLs.

Mitigation: Do not run the downloader unless input URLs have been validated and local media downloads are explicitly desired.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tandongtaotao/skills/tiktok-hotspot-monitor)
- [English README](artifact/readme-en.md)
- [Skill Instructions](artifact/skill.md)
- [Sample HTML Report](artifact/examples/report.html)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands; generated artifacts are JSONL snapshots, JSON analysis, and static HTML reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require an Apify token or saved TikTok session; optional media downloads should be run only after URL and retention review.]

## Skill Version(s):

2.0.0 (source: server evidence, artifact metadata, and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
