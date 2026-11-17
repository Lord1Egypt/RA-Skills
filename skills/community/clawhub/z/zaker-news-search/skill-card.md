## Description:

基于ZAKER权威资讯库进行关键词新闻检索，支持指定时间范围。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zaker-coder](https://clawhub.ai/user/zaker-coder)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search ZAKER news by keyword, topic, person, company, or event. It supports optional date filtering for recent or time-bounded news lookups and returns concise article titles, summaries, authors, and publication times.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: News search keywords and optional date filters are sent to ZAKER.

Mitigation: Use the skill only for explicit news-search requests and avoid submitting sensitive or private query terms.

Risk: Broad trigger wording may cause follow-up phrases such as "continue" to invoke search without enough context.

Mitigation: Clarify ambiguous follow-ups before searching and bind repeated searches to an explicit prior news topic.

Risk: Sample scripts do not enforce request timeouts.

Mitigation: Add or enforce HTTP request timeouts before running the scripts in an agent environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zaker-coder/skills/zaker-news-search)
- [ZAKER article search API endpoint](https://skills.myzaker.com/api/v1/article/search?v=1.0.6)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Text, Shell commands, Code]

**Output Format:** [Markdown or plain text news-result lists with optional Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to 20 news items with title, summary, author, and publication time; the API does not return original article URLs.]

## Skill Version(s):

1.0.9 (source: server release metadata; artifact frontmatter reports 1.0.8)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
