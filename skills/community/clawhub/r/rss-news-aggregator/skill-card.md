## Description: <br>
Aggregate and filter multiple RSS feeds to fetch, summarize, deduplicate, and monitor news articles by keywords and sources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to combine RSS or Atom feeds into one stream, filter articles by keyword or source, and generate readable news reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: RSS feed content and article links may be untrusted or misleading. <br>
Mitigation: Only add feeds the user intends to contact, treat fetched summaries and links as untrusted content, and review reports before acting on them. <br>
Risk: Dependency ranges can resolve to different package versions over time. <br>
Mitigation: Use pinned dependencies or a lockfile for reproducible installs, especially in enterprise-controlled environments. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kaiyuelv/rss-news-aggregator) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [RSS engine](artifact/scripts/rss_engine.py) <br>
- [Basic usage example](artifact/examples/basic_usage.py) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Python data structures plus Markdown or plain-text reports] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetches user-selected RSS feeds, filters and deduplicates article records, and can emit summaries with source, link, author, and publication metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
