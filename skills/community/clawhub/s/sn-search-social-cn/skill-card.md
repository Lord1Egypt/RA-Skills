## Description:

Searches Chinese social platforms with script entry points for Bilibili, Zhihu, and Douyin, plus public-web fallback guidance for Xiaohongshu and Weibo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sensenova-skills](https://clawhub.ai/user/sensenova-skills)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and agents use this skill to retrieve structured search results from Chinese social platforms for social listening, source discovery, and trend review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cookie values for Zhihu and Douyin can expose user sessions if copied into logs, reports, or shell history.

Mitigation: Prefer environment variables, avoid passing cookies on the command line, and do not include secrets in skill outputs or reports.

Risk: Zhihu searches can persist full content to local temporary files without an automatic cleanup path.

Mitigation: Review and delete temporary content files after use, especially after sensitive searches.

Risk: The dependency list includes an unused unpinned package.

Mitigation: Install in an isolated virtual environment, remove the unused dependency where possible, and pin approved package versions before deployment.

Risk: Internal or unofficial platform search APIs may fail or return incomplete results when platforms change.

Mitigation: Verify returned results before relying on them and disclose when browser-use or public-web fallback was used.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sensenova-skills/skills/sn-search-social-cn)
- [ClawHub publisher profile](https://clawhub.ai/user/sensenova-skills)
- [Bilibili](https://www.bilibili.com)
- [Zhihu search](https://www.zhihu.com/search)
- [Douyin search](https://www.douyin.com/search/)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples; scripts emit JSON search results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Script JSON follows {success, query, provider, items, error}; public-web fallbacks may require manual notes instead.]

## Skill Version(s):

2026.8.19 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
