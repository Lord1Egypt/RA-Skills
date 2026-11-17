## Description: <br>
RSS阅读器免费版 helps an agent manage RSS/Atom subscriptions, filter feed items by category, keyword, and time range, and produce list, content-research, or JSON outputs for personal information monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, content creators, independent developers, and researchers use this skill to monitor public RSS/Atom feeds, organize subscriptions, collect competitive or industry updates, and generate content ideas from recent feed items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to run local Node.js commands and fetch configured RSS/Atom feed URLs. <br>
Mitigation: Install it only in environments where local command execution and network access to those feed URLs are acceptable. <br>
Risk: Cron and file-output examples may persist generated feed summaries or content ideas to local paths. <br>
Mitigation: Review scheduled command examples before use and choose non-sensitive output locations. <br>
Risk: Broad writing and marketing triggers could be applied beyond the feed-monitoring workflow. <br>
Mitigation: Limit use to content ideas and summaries derived from configured RSS/Atom feeds. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/rss-reader-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands, plain-text feed lists, content-idea Markdown, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include RSS item metadata, URLs, generated summaries, configured feed settings, and command examples.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
