## Description:

This skill helps agents use Qinghu AI's Ozon market data APIs to identify fast-growing, less-saturated category opportunities on the Russian Ozon marketplace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoagc](https://clawhub.ai/user/autoagc)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketplace analysts, and agent operators use this skill to research Ozon Russia category opportunities before opening a store, adding a product category, or comparing category growth and saturation.

### Deployment Geography for Use:

Global; analysis is specific to the Ozon Russia marketplace.

## Known Risks and Mitigations:

Risk: Qinghu tokens may be exposed or used outside an approved secret-management path.

Mitigation: Use an approved secret mechanism for the Qinghu token and avoid embedding credentials in prompts, files, or shared outputs.

Risk: API calls may consume Qinghu credits or trigger paid usage.

Mitigation: Confirm intended Qinghu API calls before execution and report actual pointCost-derived consumption when available.

Risk: Large market-analysis results may be exported to local spreadsheet or cache files.

Mitigation: Review generated files before sharing, store them in approved locations, and remove local exports when they are no longer needed.

Risk: Market recommendations can be misleading if category IDs, sites, or reporting periods are mixed.

Mitigation: Resolve category IDs through the Qinghu category APIs and label every conclusion with the Ozon site, period, cycle, and sample size used.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoagc/skills/qinghu-ozon-bluesea-hunter)
- [Qinghu MCP API endpoint](https://www.iqinghu.com/api/desktop/qh/mcp)
- [Qinghu API key dashboard](https://www.iqinghu.com/workbench/dashboard/api-keys)

## Skill Output:

**Output Type(s):** [guidance, markdown, API calls, configuration, files]

**Output Format:** [Concise Markdown recommendations with optional spreadsheet exports or links to cached local data files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should include Top 2-3 recommended category tracks, market-growth comparisons, saturation warnings, and clearly labeled site, period, cycle, and sample-size assumptions.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
