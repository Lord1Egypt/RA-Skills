## Description:

Web Insight helps agents run Feedax-powered public web content monitoring searches with keyword, sentiment, time, platform, domain, scene, and region filters, then summarize results and save normalized JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[longgggggg](https://clawhub.ai/user/longgggggg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to monitor public web, news, social, and information sources for brand management, market analysis, competitor tracking, and risk awareness. It supports filtered searches and produces concise result previews plus complete JSON exports for follow-up analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends API keys and search queries to a Feedax HTTP endpoint, which can expose sensitive credentials or query contents in transit.

Mitigation: Use a low-privilege or disposable Feedax API key, avoid sensitive searches unless approved, and treat the HTTP endpoint as a serious issue until it is replaced with HTTPS.

Risk: The skill documentation includes commands that can print `.env` contents during API key checks.

Mitigation: Do not run commands that print `.env` contents; verify key presence without displaying secret values.

Risk: Complete search results are saved locally, defaulting to a Desktop output directory.

Mitigation: Choose an approved output directory for sensitive work and review saved JSON files before sharing or retaining them.

## Reference(s):

- [Feedax](https://www.feedax.cn)
- [ClawHub Skill Page](https://clawhub.ai/longgggggg/skills/web-insight)
- [domains.json](references/domains.json)
- [media_names.json](references/media_names.json)
- [scenes.json](references/scenes.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with shell command examples, terminal result summaries, and normalized JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires FEEDAX_SEARCH_API_KEY; complete search results are saved to a local output directory, defaulting to the user's Desktop.]

## Skill Version(s):

1.0.4 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
