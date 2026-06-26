## Description: <br>
基于ZAKER权威资讯库进行关键词新闻检索，支持指定时间范围。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zaker-coder](https://clawhub.ai/user/zaker-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to search ZAKER news articles by keyword, topic, person, event, or optional date range. It is suited for retrieving article titles, summaries, authors, and publish times from ZAKER's news corpus during news lookup or follow-up research workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: News search keywords and optional date ranges are sent to skills.myzaker.com. <br>
Mitigation: Avoid sensitive private queries and disclose external API use before running the skill in privacy-sensitive contexts. <br>
Risk: Retrieved articles may be incomplete, stale, biased, or unsuitable as the only source for high-stakes fact-checking. <br>
Mitigation: Treat ZAKER results as retrieved articles rather than verified truth and corroborate important claims with additional authoritative sources. <br>
Risk: Skill wording overstates result reliability according to the authoritative security summary. <br>
Mitigation: Present results with source attribution and avoid claiming that the search eliminates misinformation risk. <br>


## Reference(s): <br>
- [ClawHub release page for ZAKER news search](https://clawhub.ai/zaker-coder/zaker-news-search) <br>
- [ZAKER article search API endpoint](https://skills.myzaker.com/api/v1/article/search?v=1.0.6) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Code] <br>
**Output Format:** [Markdown or plain text article list with title, summary, author, and publish time; scripts may print JSON-backed API results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to 20 results per request; article URLs are not returned by the API.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release evidence; artifact frontmatter is 1.0.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
