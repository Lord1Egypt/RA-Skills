## Description:

Helps Taiwan fashion brands plan social posts, ad copy, hashtag mixes, publishing schedules, funnel strategy, localized marketing, and Meta/Threads analytics reviews using embedded fashion advertising benchmarks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shangweilin7](https://clawhub.ai/user/shangweilin7)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing teams, brand operators, and agents use this skill to create Taiwan-localized fashion social media plans, ad copy, hashtags, schedules, and funnel recommendations for Facebook, Instagram, TikTok, and Threads. Developers or operators can also use the included setup guidance and Python helper to fetch Meta and Threads post analytics into an Excel report for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad long-lived Meta and Threads credentials could expose business analytics if they are over-privileged or mishandled.

Mitigation: Use the narrowest read-only permissions Meta allows, avoid administrator or full-control tokens where possible, keep .env out of version control with strict file permissions, and rotate tokens regularly.

Risk: The included script reads business social analytics through external APIs and writes a local report.

Mitigation: Review the fetch script before running it and execute it only in an environment where the destination report path and API credentials are acceptable.

Risk: Marketing recommendations are grounded in Taiwan fashion benchmarks and may not fit other industries or markets.

Mitigation: Treat the embedded benchmarks as fashion-specific guidance and adjust recommendations when the brand, audience, or market differs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shangweilin7/skills/tw-fashion-social-manager)
- [Publisher Profile](https://clawhub.ai/user/shangweilin7)
- [README.md](artifact/README.md)
- [Brand Context](artifact/references/brand-context.md)
- [Meta Ads Data](artifact/references/meta-ads-data.md)
- [Meta Business Manager](https://business.facebook.com)
- [Meta for Developers](https://developers.facebook.com)
- [Graph API Explorer](https://developers.facebook.com/tools/explorer/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with optional shell commands and Python-generated XLSX reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The fetch helper can create weekly_insights_YYYY-MM-DD.xlsx after the user supplies Meta and Threads credentials.]

## Skill Version(s):

1.0.8 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
