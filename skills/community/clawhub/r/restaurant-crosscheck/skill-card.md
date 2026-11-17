## Description:

Cross-checks restaurant recommendations from Xiaohongshu and Dianping by location and cuisine, then scores recommendation confidence from ratings, engagement, sentiment, and cross-platform consistency.

This skill is for research and development only.

## Publisher:

[liyang2016](https://clawhub.ai/user/liyang2016)

### License/Terms of Use:

MIT

## Use Case:

Developers, agents, and end users use this skill to query restaurants by city or district and cuisine, then compare Dianping ratings with Xiaohongshu engagement and sentiment before making personal dining decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated scraping can save Dianping and Xiaohongshu browser sessions on disk.

Mitigation: Use a dedicated low-privilege account, keep the session directory private, and reset saved sessions when they are no longer needed.

Risk: Server and mock outputs can resemble real recommendations while not using live platform data.

Mitigation: Treat mock/server output as demonstration data and rely on results only after explicitly running the real Playwright-based path.

Risk: The setup script performs broad Python package and Playwright browser installation.

Mitigation: Review the installer first and prefer an isolated virtual environment over system-level installation.

Risk: Scraping restaurant platforms may conflict with platform terms, rate limits, or permitted use.

Mitigation: Review platform terms before use, keep usage to personal research, and apply conservative rate limits and caching.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liyang2016/skills/restaurant-crosscheck)
- [Data schema documentation](references/data_schema.md)
- [Sentiment analysis guide](references/sentiment_analysis.md)
- [API limitations](references/api_limitations.md)
- [Dianping](https://www.dianping.com)
- [Xiaohongshu](https://www.xiaohongshu.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown-style restaurant recommendation report with ranked entries, recommendation scores, platform comparisons, consistency labels, warnings, and optional command or Python usage guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Server mode can produce mock recommendation output; the real-data path uses Playwright with locally saved browser sessions.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact publish metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
