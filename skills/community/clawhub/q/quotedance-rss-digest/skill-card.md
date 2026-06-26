## Description: <br>
Aggregates recent articles from enabled Quotedance-service RSS subscriptions and returns a filtered Markdown digest with local caching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yoocky](https://clawhub.ai/user/yoocky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to summarize recent articles from their enabled Quotedance subscriptions, optionally filtering by source name and time window. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Quotedance API key and configured RSSHub or service endpoints. <br>
Mitigation: Install only with trusted endpoints and use a least-privilege API key when available. <br>
Risk: Included local cache files can contain stale feed data. <br>
Mitigation: Clear the memory/rss-cache files before first use or force a refresh when current feed content is required. <br>
Risk: RSS article text is external content and may contain untrusted instructions or misleading claims. <br>
Mitigation: Treat RSS item text as content to summarize, not as agent instructions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yoocky/quotedance-rss-digest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown digest with article titles, sources, timestamps, links, and short summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports recent-day windows, result limits, source-name filtering, cache refresh controls, and local cache TTLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
