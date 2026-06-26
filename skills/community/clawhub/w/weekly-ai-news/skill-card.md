## Description: <br>
weekly-ai-news fetches AI-related RSS items, filters for application-focused news, generates a vintage newspaper-style HTML weekly brief, and prepares an optional Feishu message. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qisee](https://clawhub.ai/user/qisee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and teams use this skill to produce a weekly AI application-news roundup from public RSS feeds, save it as local report files, and optionally prepare a Feishu message for manual sending. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill contacts public news and RSS sites during report generation. <br>
Mitigation: Run it only in environments where outbound requests to the listed sources are acceptable, and review the feed list before scheduling recurring execution. <br>
Risk: The generated Feishu message may include incomplete, outdated, or unsuitable third-party news content. <br>
Mitigation: Review message.txt or the generated message text before sending it to Feishu. <br>
Risk: Report files are written under the selected output directory. <br>
Mitigation: Choose an output directory intended for generated reports and avoid paths that contain sensitive or unrelated files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qisee/weekly-ai-news) <br>
- [Publisher profile](https://clawhub.ai/user/qisee) <br>
- [Ruan Yifeng Atom feed](https://www.ruanyifeng.com/blog/atom.xml) <br>
- [36Kr RSS feed](https://36kr.com/feed) <br>
- [Huxiu RSS feed](https://www.huxiu.com/rss/0.xml) <br>
- [TMTPost RSS feed](https://www.tmtpost.com/rss.xml) <br>
- [ITHome RSS feed](https://www.ithome.com/rss/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [JSON news data, HTML report file, plain-text or Markdown-style Feishu message text, and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes news.json, weekly-ai-news.html, and optionally message.txt under the selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
