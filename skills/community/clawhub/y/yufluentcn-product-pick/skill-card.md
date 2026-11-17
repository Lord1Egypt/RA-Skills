## Description:

选品分析 helps operators analyze Amazon, TikTok Shop, and AliExpress product candidates with BSR, sales, price, review, margin, competition, and IP-risk signals through the Yufluent cloud harness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metahuan](https://clawhub.ai/user/metahuan)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators and sourcing teams use this skill to turn authorized marketplace data or pasted candidate tables into go, watch, or no-go product-picking guidance. Developers and agents can also use it to orchestrate Browser Service discovery before invoking the Yufluent product-pick API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill imports an unbundled yufluent_api.py client from outside the reviewed package.

Mitigation: Verify which yufluent_api.py module will be imported before installation and run the skill in a limited environment.

Risk: Product-candidate files and Browser Service data can be sent to configurable cloud or browser services.

Mitigation: Use only trusted TOKENAPI_BASE_URL and BROWSER_SERVICE_URL values, and provide only authorized, relevant product-candidate data.

Risk: The skill may read local paths supplied to --product-candidates and submit that content for analysis.

Mitigation: Do not pass unrelated or sensitive files as product-candidate input.

Risk: Profit, sales, competition, and IP-risk outputs are estimates for sourcing decisions.

Mitigation: Manually review source data, intellectual-property concerns, and purchasing assumptions before acting on a go/watch/no-go verdict.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/metahuan/skills/yufluentcn-product-pick)
- [Yufluent product-pick homepage](https://www.changzhiai.com/skills/product-pick)
- [Yufluent console](https://claw.changzhiai.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or JSON/text returned from the Yufluent cloud analysis, with optional file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include product-picking scores, IP-risk notes, capital-impact context, and go/watch/no-go verdicts.]

## Skill Version(s):

1.0.2 (source: evidence release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
