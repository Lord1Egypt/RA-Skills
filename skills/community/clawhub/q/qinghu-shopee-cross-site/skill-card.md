## Description:

青虎AI Shopee 跨站点拓客帮助卖家查看品牌和类目在 Shopee 各站点的分布、店铺、商品和趋势，用于判断一店多开时优先拓展哪个站点。

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External Shopee sellers and ecommerce operators use this skill to compare cross-site demand signals before opening additional Shopee stores. The skill guides an agent to query Qinghu market-data APIs, rank up to three target sites, summarize site-by-site evidence, and flag weak or unsuitable expansion options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use Qinghu API credentials from user input or QINGHU_TOKEN / QHKIT_TOKEN environment variables.

Mitigation: Confirm user authorization before API use, keep credentials out of generated output, and avoid installing the skill where those environment variables should not be accessed.

Risk: Qinghu API calls may consume Qinghu credits after user confirmation.

Mitigation: Request approval before calls, report actual Qinghu credit consumption from the response envelope when available, and stop when authorization is denied.

Risk: Large market-data result sets may be exported to local files.

Mitigation: Tell the user when data is exported, provide the local file link, and treat exported market data as retained local data subject to the user's handling requirements.

Risk: External market-data API results can be incomplete, unavailable, or tied to a specific site and accounting period.

Mitigation: Label site, period, cycle, and sample size in summaries, and avoid mixing cross-site or cross-period figures without context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/qinghu-shopee-cross-site)
- [Qinghu API endpoint](https://www.iqinghu.com/api/desktop/qh/mcp)
- [Qinghu API key dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown recommendations with concise comparison tables and links to exported local files when result sets are large.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should state data scope and accounting period, present conclusions before supporting data, and avoid pasting large raw datasets into chat.]

## Skill Version(s):

0.1.3 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
