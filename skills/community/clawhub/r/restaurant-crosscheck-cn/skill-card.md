## Description:

Cross-reference restaurant recommendations from Xiaohongshu and Dianping by location and cuisine to compare ratings, engagement, matching confidence, and consistency scores.

This skill is for research and development only.

## Publisher:

[zhongrenfei1-hub](https://clawhub.ai/user/zhongrenfei1-hub)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users can use this skill to investigate Chinese local-service and restaurant recommendations across Dianping and Xiaohongshu, especially when they want cross-platform consistency checks before making a dining or venue decision. Its real-data mode depends on authenticated browser sessions and third-party site access, so it is best suited for research and review workflows rather than unattended production use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated scraping uses logged-in browser sessions and stores session data locally.

Mitigation: Use a dedicated account or browser profile, keep the environment isolated, and delete ~/.local/share/restaurant-crosscheck/sessions after use or on shared machines.

Risk: Third-party platform access may conflict with platform terms or trigger rate limits and account controls.

Mitigation: Review Dianping and Xiaohongshu terms before use, keep requests limited, and prefer official or licensed data sources for commercial workflows.

Risk: Installation and publishing guidance includes practices that need review before reuse.

Mitigation: Inspect setup scripts before running them, install dependencies in a virtual environment, and avoid command-line token login examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhongrenfei1-hub/skills/restaurant-crosscheck-cn)
- [Data schema documentation](artifact/references/data_schema.md)
- [Sentiment analysis guide](artifact/references/sentiment_analysis.md)
- [API and data source limitations](artifact/references/api_limitations.md)
- [Dianping](https://www.dianping.com)
- [Xiaohongshu](https://www.xiaohongshu.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration guidance]

**Output Format:** [Markdown-style recommendation summaries, command examples, and optional JSON result files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include ranked restaurant matches, platform-only results, ratings, review counts, engagement indicators, consistency levels, and confidence scores.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
