## Description: <br>
Fetches and summarizes important news from Türkiye using RSS feeds and can support scheduled notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yalcindemir](https://clawhub.ai/user/yalcindemir) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to collect recent Turkish news from public RSS feeds, choose the most important items, and produce concise Turkish summaries. It can also be run on a schedule for Telegram delivery when the user's Telegram setup is configured intentionally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts multiple public Turkish news feeds when the fetch script runs. <br>
Mitigation: Install it only when those outbound feed requests are expected and acceptable for the deployment environment. <br>
Risk: Scheduled Telegram delivery could send news summaries to an unintended recipient or continue longer than intended. <br>
Mitigation: Enable cron and Telegram alerts deliberately, confirm the Telegram recipient mapping, and provide an easy way to disable the schedule. <br>
Risk: News summaries can omit context or reflect source-feed errors. <br>
Mitigation: Keep summaries concise, include source links when practical, and review important items before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yalcindemir/turkey-news) <br>
- [Publisher profile](https://clawhub.ai/user/yalcindemir) <br>
- [NTV RSS feed](https://www.ntv.com.tr/son-dakika.rss) <br>
- [CNN Turk RSS feed](https://www.cnnturk.com/feed/rss/all/news) <br>
- [TRT Haber RSS feed](https://www.trthaber.com/sondakika.rss) <br>
- [Sozcu RSS feed](https://www.sozcu.com.tr/rss/all.xml) <br>
- [Milliyet RSS feed](https://www.milliyet.com.tr/rss/rssnew/gundemrss.xml) <br>
- [Haberturk RSS feed](https://www.haberturk.com/rss) <br>
- [Hurriyet RSS feed](https://www.hurriyet.com.tr/rss/anasayfa) <br>
- [Sabah RSS feed](https://www.sabah.com.tr/rss/anasayfa.xml) <br>
- [Anadolu Ajansi RSS feed](https://www.aa.com.tr/tr/rss/default?cat=guncel) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [JSON from the fetch script, followed by concise Turkish news summaries in text or Markdown] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Limits script output to the 20 newest collected items and marks items from the last three hours as recent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
