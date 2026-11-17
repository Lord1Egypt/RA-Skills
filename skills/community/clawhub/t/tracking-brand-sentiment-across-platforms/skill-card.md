## Description:

Tracks brand sentiment across Twitter, Reddit, and TikTok using Apify-hosted Apidojo scrapers, returning per-platform sentiment distribution, a cross-platform health score, top positive and negative posts, and theme analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apidojo-io](https://clawhub.ai/user/apidojo-io)

### License/Terms of Use:

MIT-0

## Use Case:

Brand managers, CMOs, PR teams, and reputation monitoring teams use this skill to compare brand sentiment across Twitter, Reddit, and TikTok. It helps produce a unified social-listening report with per-platform sentiment, themes, impactful posts, and an overall brand health score.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Reddit workflow is reported by security evidence as pointing to a Twitter scraper, which may make cross-platform reporting inaccurate.

Mitigation: Review or correct the Reddit actor before relying on the skill for cross-platform sentiment reports.

Risk: Fallback examples place the Apify token in request URLs, which can expose credentials through logs or browser and proxy history.

Mitigation: Use a least-privilege Apify token in authorization headers rather than URL parameters.

Risk: Brand search terms, scraped social content, and exported CSV or JSON files may contain sensitive or reputation-relevant information.

Mitigation: Use the skill only when Apify-hosted processing is acceptable and store exported results in an appropriately protected location.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/apidojo-io/skills/tracking-brand-sentiment-across-platforms)
- [Publisher Profile](https://clawhub.ai/user/apidojo-io)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown report with tables, scored summaries, theme lists, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include exported CSV or JSON result files when the optional runner workflow is used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
