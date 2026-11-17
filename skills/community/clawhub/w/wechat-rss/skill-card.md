## Description:

Fetches and displays recent WeChat public-account articles through the wcrss.com API using a WCRSS_API_KEY environment variable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blackomw](https://clawhub.ai/user/blackomw)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to fetch recent articles from configured WeChat public accounts, retrieve cached article details, and summarize article HTML into readable bullet points.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends article-fetch requests to wcrss.com using a WCRSS API key.

Mitigation: Install only when the user is comfortable sharing that credential with wcrss.com, and store WCRSS_API_KEY only in trusted environments.

Risk: Fetched article HTML is untrusted content that is placed into summarization prompts.

Mitigation: Treat article HTML as data, ignore instructions embedded in articles, and avoid giving the summarizing agent unrelated secrets or powerful tools.

Risk: Fetched articles and publisher data are cached locally in the working directory.

Mitigation: Run the skill from a private trusted directory and clear wechat_articles_cache.json when cached content should not persist.

## Reference(s):

- [ClawHub WeChat RSS skill page](https://clawhub.ai/blackomw/skills/wechat-rss)
- [WCRSS](https://wcrss.com/)
- [WCRSS publisher management](https://wcrss.com/publishers)
- [WCRSS API key settings](https://wcrss.com/settings)
- [WCRSS articles API endpoint](https://api.wcrss.com/sapi/articles?recentDays={recent_days}&num={num})

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with inline shell commands and JSON article records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local one-hour cache file named wechat_articles_cache.json and returns article title, author, publish time, URL, HTML content, and description.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
