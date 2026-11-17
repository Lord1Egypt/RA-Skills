## Description:

Find, evaluate, and recommend AI products using the watcha.cn platform API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charipoter](https://clawhub.ai/user/charipoter)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to find, compare, and evaluate AI products for specific needs, including products available in China or globally. It guides agents to combine watcha.cn product, review, and discussion data with external web sources before making recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User queries may be sent to watcha.cn when the agent uses the platform API.

Mitigation: Avoid sharing sensitive or confidential requirements, and ask the agent not to use watcha.cn when those queries should not be sent there.

Risk: watcha.cn popularity signals, review counts, and unrevealed scores may be mistaken for product quality.

Mitigation: Compare watcha.cn results with external sources and weigh detailed review content more heavily than popularity metrics.

## Reference(s):

- [Watcha](https://watcha.cn)
- [Watcha Products](https://watcha.cn/products)
- [Watcha API](https://watcha.cn/api/v2/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, API Calls]

**Output Format:** [Markdown recommendations with product summaries, comparisons, review analysis, and cited external context]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product shortlists, comparison tables, caveats about review reliability, and follow-up questions for ambiguous requests.]

## Skill Version(s):

0.1.0 (source: server release metadata and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
