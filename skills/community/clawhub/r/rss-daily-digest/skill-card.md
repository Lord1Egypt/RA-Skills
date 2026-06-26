## Description: <br>
Fetch RSS feeds, parse articles, generate AI summaries, and compile a daily digest report in Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renchengxiang](https://clawhub.ai/user/renchengxiang) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to fetch configured RSS feeds, summarize recent articles, and create a daily Markdown news digest for briefings or feed-reader workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches configured RSS feeds and stores digest output locally. <br>
Mitigation: Review the configured feeds and output path before running the workflow, especially where local files may contain sensitive reading interests or article metadata. <br>
Risk: The workflow may install the unpinned feedparser Python dependency if it is missing. <br>
Mitigation: Install dependencies from a trusted package index in a controlled environment and pin versions for repeatable deployments. <br>
Risk: The fetch script writes to a fixed temporary file at /tmp/openclaw-rss-articles.json. <br>
Mitigation: Use a unique or user-scoped temporary path before deploying unchanged on shared or multi-user systems. <br>


## Reference(s): <br>
- [RSS Feed Sources](references/feed-sources.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/renchengxiang/rss-daily-digest) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/renchengxiang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown digest with JSON feed results and a completion summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses RSS_FEEDS_CONFIG, writes a temporary JSON file at /tmp/openclaw-rss-articles.json, saves digests under ~/openclaw-output/digests/, and limits the digest to 50 articles.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
