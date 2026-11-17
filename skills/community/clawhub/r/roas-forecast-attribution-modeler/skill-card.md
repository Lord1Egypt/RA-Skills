## Description:

Build ROAS forecasting and attribution-model assumptions for Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, Shopify Ads, and DSP/programmatic planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danyangliu-sandwichlab](https://clawhub.ai/user/danyangliu-sandwichlab)

### License/Terms of Use:


## Use Case:

Marketing, growth, and ecommerce teams use this skill to forecast ROAS, CPA, or revenue scenarios, compare attribution-window assumptions, and choose risk-adjusted budget paths across major advertising channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may influence ad budget planning advice and campaign-spend decisions.

Mitigation: Treat recommendations as planning assumptions, review confidence bounds, and require human approval before changing campaign budgets.

Risk: Incomplete or uncertain performance inputs can produce misleading ROAS, CPA, or revenue forecasts.

Mitigation: Separate observed facts from assumptions, widen forecast intervals when inputs are uncertain, and validate scenarios before acting on them.

Risk: Large scenario spread or attribution-window variance can lead to overconfident allocation decisions.

Mitigation: Use phased budget release, dual-plan decisions where attribution windows materially differ, and explicit rollback or stop-loss conditions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danyangliu-sandwichlab/skills/roas-forecast-attribution-modeler)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with model inputs, scenario outputs, sensitivity analysis, attribution impact notes, and budget recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory planning output; no code execution, credential access, persistence, or hidden execution behavior.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
