## Description: <br>
RSS聚合工具免费版 helps an agent read configured RSS feeds, fetch article content, merge duplicate coverage, check history logs, and produce high-density incremental text or Markdown news briefs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and researchers use this skill to manually aggregate trusted RSS feeds into concise incremental news briefs. It is intended for lightweight personal or technical information tracking with duplicate detection through a local pushed-history log. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill text inconsistently references API, webhook, callback, and system-connection behavior that the free edition says it does not support. <br>
Mitigation: Use it only for manual RSS aggregation unless the publisher clarifies those integration behaviors and their data disclosure rules. <br>
Risk: Untrusted or overly broad RSS feed lists can introduce misleading, low-quality, or unwanted content into generated briefs. <br>
Mitigation: Limit feeds to trusted sources, review generated summaries before relying on them, and keep feed and history files in a known ~/rss-aggregator directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/rss-aggregator-tool-free) <br>
- [Skill source](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text or Markdown news brief with links, plus optional shell commands for local feed and history files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires trusted RSS feed lists, internet access, and a local ~/rss-aggregator history log when using incremental mode.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
