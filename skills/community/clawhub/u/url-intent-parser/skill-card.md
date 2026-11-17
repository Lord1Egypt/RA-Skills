## Description:

Parse product and landing URLs into an executable ads brief for Meta (Facebook/Instagram), Google Ads, TikTok Ads, YouTube Ads, Amazon Ads, Shopify Ads, and DSP/programmatic.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danyangliu-sandwichlab](https://clawhub.ai/user/danyangliu-sandwichlab)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn a product, service, or landing page URL plus a business goal and market scope into an ads launch brief. It helps extract the offer, form audience and funnel hypotheses, recommend channels, and produce a launch hand-off payload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ads recommendations can affect budget, tracking, channel allocation, or campaign setup if copied directly into real ad platforms.

Mitigation: Review budget, tracking, and channel recommendations before acting, and preserve rollback or stop-loss conditions for spend decisions.

Risk: Broad ads-related prompts may activate the skill when the user wanted general marketing advice rather than a launch brief.

Mitigation: Confirm that the request includes a URL, business goal, and market scope before producing an ads launch brief.

Risk: The generated brief may contain assumptions about page intent, funnel stage, or platform fit when source information is incomplete.

Mitigation: Separate observed facts from assumptions, mark low-confidence claims, and ask a focused clarification question when critical inputs are missing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/danyangliu-sandwichlab/skills/url-intent-parser)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown ads brief with a structured launch hand-off JSON payload]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes intake summary, parsed offer and value proposition, audience and funnel hypothesis, channel rationale, and validation or escalation guidance when confidence is low.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
