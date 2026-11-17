## Description:

公众号爆款封面AI设计工具。基于全网每日收录的10w+文章数据，获取同赛道爆款封面视觉元素，通过AI分析总结高转化视觉规律，生成贴合文章内容、符合平台流量审美的封面设计方案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanyi-github](https://clawhub.ai/user/yuanyi-github)

### License/Terms of Use:

MIT-0

## Use Case:

External WeChat creators, content operators, designers, and new media teams use this skill to analyze recent high-performing WeChat cover patterns, produce a visual HTML analysis report, and generate three cover design proposals with image-generation prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a RedFox API key and sends keyword queries to the RedFox service.

Mitigation: Install only when the publisher and RedFox service are trusted, keep REDFOX_API_KEY out of prompts and logs, and avoid sensitive client topics or private reference images in queries.

Risk: The security evidence marks the release suspicious because of unsafe command and report-generation instructions plus unsolicited runtime output.

Mitigation: Run the skill in an isolated environment, sanitize keywords before executing commands, and review generated report files before opening or sharing them.

Risk: The generated report embeds article and cover image URLs from API results.

Mitigation: Review report data for irrelevant, unsafe, private, or misleading links before using the report as design guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yuanyi-github/skills/wechat-cover-generator)
- [公众号爆款数据格式说明](references/gzh_trend_data_format.md)
- [爆款封面分析报告 HTML 模板](references/report_template.md)
- [Report template HTML](references/report_template.html)
- [RedFox hot article search API endpoint](https://redfox.hk/story/api/gzh/search/hotArticleNew)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Files, Shell commands, Code, Guidance]

**Output Format:** [Markdown guidance, shell commands, JSON report data, HTML report files, image-generation prompts, and generated cover images]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated report uses a fixed HTML template populated with JSON data and cover image URLs from the RedFox API.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact frontmatter says 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
