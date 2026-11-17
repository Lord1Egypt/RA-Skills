## Description:

Provides paid API-style lottery number recommendations for Shuangseqiu and Daletou, described by the skill as historical-data analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinboh68-prog](https://clawhub.ai/user/jinboh68-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External users or agents can request Shuangseqiu or Daletou number suggestions for entertainment and comparison, with payment information disclosed by the skill. Recommendations should not be treated as financial or gambling advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The paid service is described as historical-data lottery analysis, while the reviewed behavior appears to return simulated random picks.

Mitigation: Present recommendations as entertainment-only suggestions and avoid claims that they improve lottery outcomes unless supported by verifiable analysis.

Risk: The payment flow description may not prove that payment is enforced correctly.

Mitigation: Review payment enforcement before paying for or deploying the service.

Risk: Unpinned dependencies can change behavior or introduce supply-chain risk.

Mitigation: Pin dependency versions and review updates before release or installation.

## Reference(s):

- [Rich Lottery ClawHub Skill Page](https://clawhub.ai/jinboh68-prog/skills/rich-lottery)
- [Rich Lottery API Endpoint](https://rich-lottery.vercel.app)

## Skill Output:

**Output Type(s):** [JSON, API Calls, Guidance]

**Output Format:** [JSON responses with lottery type, draw date, and recommendation arrays]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are generated per request for either the ssq or dlt endpoint.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, skill.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
