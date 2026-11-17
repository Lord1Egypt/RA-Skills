## Description:

Fetches important news from Turkiye RSS feeds and helps an agent summarize recent items for manual or scheduled notification workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yalcindemir](https://clawhub.ai/user/yalcindemir)

### License/Terms of Use:


## Use Case:

Agents and users use this skill to fetch recent Turkiye news from RSS sources, select important items, and produce concise Turkish summaries for manual review or scheduled Telegram notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled notification workflows could send externally sourced news content without clear confirmation or recipient controls.

Mitigation: Require explicit configuration or confirmation for Telegram recipients before automatic sends.

Risk: RSS feed content is externally supplied and may contain untrusted or misleading text.

Mitigation: Limit fetching to approved RSS domains and treat all feed content as untrusted text before summarizing or forwarding.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yalcindemir/skills/turkey-news)
- [NTV RSS](https://www.ntv.com.tr/son-dakika.rss)
- [CNN Turk RSS](https://www.cnnturk.com/feed/rss/all/news)
- [TRT Haber RSS](https://www.trthaber.com/sondakika.rss)
- [Sozcu RSS](https://www.sozcu.com.tr/rss/all.xml)
- [Milliyet Gundem RSS](https://www.milliyet.com.tr/rss/rssnew/gundemrss.xml)
- [Haberturk RSS](https://www.haberturk.com/rss)
- [Hurriyet RSS](https://www.hurriyet.com.tr/rss/anasayfa)
- [Sabah RSS](https://www.sabah.com.tr/rss/anasayfa.xml)
- [Anadolu Ajansi RSS](https://www.aa.com.tr/tr/rss/default?cat=guncel)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON from the fetch script and concise Turkish text or Markdown summaries from the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches up to 20 newest items and marks items from the last three hours as recent.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
