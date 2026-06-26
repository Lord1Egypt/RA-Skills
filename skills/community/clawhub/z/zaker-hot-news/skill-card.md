## Description: <br>
获取ZAKER聚合权威媒体的最新头条新闻与热点资讯. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zaker-coder](https://clawhub.ai/user/zaker-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch and summarize current ZAKER hot headlines for news, breaking-events, and broad current-affairs requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation wording may cause vague prompts such as "what's new" to be treated as news requests. <br>
Mitigation: Invoke the skill explicitly with news-oriented phrases such as "latest news" or "headlines" when deterministic routing is needed. <br>
Risk: News and current-events outputs may become stale or incomplete between endpoint updates. <br>
Mitigation: Treat results as a current headline snapshot and preserve links to original articles so users can verify details. <br>


## Reference(s): <br>
- [ZAKER Hot Articles API](https://skills.myzaker.com/api/v1/article/hot?v=1.0.3) <br>
- [ClawHub skill page](https://clawhub.ai/zaker-coder/zaker-hot-news) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, text, API Calls, shell commands, code] <br>
**Output Format:** [Markdown list of linked headlines with summaries and source names; helper scripts can emit console text or raw JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns up to 20 hot articles from the configured ZAKER endpoint.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence; artifact frontmatter remains 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
