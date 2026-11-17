## Description:

A股每日新闻 searches Xiaohongshu, Douyin, and WeChat Official Accounts for A-share market discussions, filters non-stock content, compares cross-platform sentiment, and produces structured research reports with an optional interactive HTML view.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

Retail investors, financial researchers, institutional analysts, and financial content creators use this skill to gather recent A-share sentiment signals across Chinese social and publishing platforms and turn them into concise market discussion reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a RedFox API key and sends A-share query terms to redfox.hk.

Mitigation: Use only a scoped, revocable API key, avoid placing secrets in prompts or output files, and confirm that sending the intended query data to RedFox is acceptable.

Risk: Generated HTML reports are local files built from external and user-influenced data.

Mitigation: Review the generated HTML path and source content before opening or sharing the report, and avoid untrusted keywords, JSON files, or report inputs.

Risk: Reports include built-in promotional subscription links.

Mitigation: Treat subscription links as promotional material and separate them from the requested market analysis when reviewing outputs.

Risk: The skill produces social-media sentiment analysis about securities, which can be incomplete or misleading.

Mitigation: Use outputs as research context only, verify material claims against primary financial sources, and do not treat the report as investment advice.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/redfox-data/skills/stock-feed-redfox)
- [RedFox API Key Settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFox Website](https://redfox.hk?source=clawhub)
- [Output Rules and Report Template](references/output-rules.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with clickable source links, JSON result files, and optional local HTML reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a RedFox API key for live data retrieval; default queries cover the past 7 days and can be adjusted up to 30 days.]

## Skill Version(s):

1.0.4 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
