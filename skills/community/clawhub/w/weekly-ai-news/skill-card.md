## Description:

Generates a weekly AI application-news digest by fetching RSS feeds, filtering out highly technical items, creating a vintage newspaper-style HTML report, and optionally preparing a Feishu message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qisee](https://clawhub.ai/user/qisee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content operators, and automation users use this skill to produce a weekly AI application-news report from configured RSS feeds and prepare a Feishu-ready summary for sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An attacker-controlled output path may cause arbitrary Python code execution in the report workflow.

Mitigation: Use only trusted, simple output paths and do not pass paths supplied by others.

Risk: Scheduled execution or Feishu sharing can amplify unsafe output-path behavior before review.

Mitigation: Avoid enabling cron or Feishu sending until the output-path issue is fixed and the skill has been reviewed.

Risk: Generated reports include external links collected from RSS feeds.

Mitigation: Treat report links as untrusted external links and review them before sharing or clicking.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qisee/skills/weekly-ai-news)
- [Ruanyifeng RSS feed](https://www.ruanyifeng.com/blog/atom.xml)
- [36Kr RSS feed](https://36kr.com/feed)
- [Huxiu RSS feed](https://www.huxiu.com/rss/0.xml)
- [TMTPost RSS feed](https://www.tmtpost.com/rss.xml)
- [ITHome RSS feed](https://www.ithome.com/rss/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [JSON data, HTML report, and Markdown/plain-text Feishu message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes news.json, weekly-ai-news.html, and optionally message.txt to the selected output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
