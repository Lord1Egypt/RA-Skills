## Description:

社媒情报中心 - 多平台爬虫 + 数据分析 + AI洞察 + 词云 + 趋势追踪

This skill is ready for commercial/non-commercial use.

## Publisher:

[kk-kingkong](https://clawhub.ai/user/kk-kingkong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to collect public social-media search results, compare topics, track trends, generate word clouds, export CSV/XLSX files, and prepare concise LLM analysis prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms and note IDs may be sent to configured TikHub/mcporter services.

Mitigation: Use the skill only for queries you are comfortable disclosing to those services and review the configured services before execution.

Risk: Scraped public content can be cached locally under /tmp/social_intel_cache.

Mitigation: Clear /tmp/social_intel_cache on shared machines and use --no-cache when local caching is not appropriate.

Risk: Generated CSV/XLSX exports may contain untrusted social-media fields, including spreadsheet formulas.

Mitigation: Treat exported spreadsheets as untrusted and review or sanitize fields before opening them in spreadsheet software.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kk-kingkong/skills/social-intel)
- [Publisher profile](https://clawhub.ai/user/kk-kingkong)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Terminal text, Markdown-like analysis reports, LLM prompt text, PNG word clouds, and CSV/XLSX export files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can cache scraped public content in /tmp/social_intel_cache for 24 hours and write generated files under /tmp/social_intel or a user-specified output path.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
