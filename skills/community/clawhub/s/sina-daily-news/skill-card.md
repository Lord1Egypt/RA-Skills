## Description: <br>
抓取新浪财经 7×24 实时新闻流，并按新闻类别生成包含时间、来源和阅读量的 Markdown 日报。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Analysts, operators, and agents use this skill to turn Sina Finance's public 7x24 news feed into a categorized daily briefing for finance, politics, technology, industrial, and social news review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The optional cron example can run daily public-web fetches and save generated reports to memory. <br>
Mitigation: Enable scheduled execution only when recurring Sina Finance fetching and stored daily report files are acceptable. <br>
Risk: Fetched page content may be blocked, too short, or otherwise fail to produce a complete report. <br>
Mitigation: Check fetch status and review generated reports before using them for decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/paudyyin/sina-daily-news) <br>
- [Sina Finance 7x24 news feed](https://finance.sina.com.cn/7x24/?tag=0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown daily report with categorized bullet lists, plus optional shell and cron configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Consumes fetched Sina Finance page text from stdin or argv[1]; optional cron usage may save daily reports to memory.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence release, SKILL.md frontmatter, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
