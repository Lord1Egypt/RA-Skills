## Description:

Guides agents through Xiaohongshu analysis for popular note discovery, keyword monitoring, trend analysis, and creator research.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guohongbin-git](https://clawhub.ai/user/guohongbin-git)

### License/Terms of Use:

MIT

## Use Case:

Content creators, marketers, and researchers use this skill to analyze Xiaohongshu topics, monitor keywords, compare competing notes, identify KOLs, and understand content trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: External scraper code may change or contain unsafe behavior when cloned and run without pinning or integrity checks.

Mitigation: Review the scraper before execution, pin it to a trusted commit, and run it in a fresh virtual environment or container.

Risk: Scraping, packet capture, or automated access may create account, platform policy, or privacy compliance risk.

Mitigation: Confirm that collection methods comply with Xiaohongshu rules and applicable privacy obligations, and avoid exposing browser profiles or credentials.

## Reference(s):

- [Xiaohongshu CN skill page](https://clawhub.ai/guohongbin-git/skills/xiaohongshu-cn)
- [Xiaohongshu Explore](https://www.xiaohongshu.com/explore)
- [Xiaohongshu Search](https://www.xiaohongshu.com/search_result)
- [XiaohongshuSpider](https://github.com/Big-Buffer/XiaohongshuSpider)
- [xiaohongshu-spider reference](https://github.com/lonngxiang/xiaohongshu-spider)
- [xiaohongshu-spider Selenium reference](https://github.com/63can/xiaohongshu-spider)
- [Nanji](https://www.nanji.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with tables and inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include external scraper and third-party tool references for user review.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
