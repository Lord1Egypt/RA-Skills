## Description:

客户清单分析基于 Shop API customer list data to summarize customer type distribution, trial activity, sales-associate matching, and customer detail queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gwyang7](https://clawhub.ai/user/gwyang7)

### License/Terms of Use:

MIT-0

## Use Case:

Retail operators and store analytics teams use this skill to query customer lists, monitor customer type mix, review trial-to-purchase behavior, and check sales-associate matching for authorized store data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on an external local API client path that was not reviewed with the release artifact.

Mitigation: Install only in environments where the API client path is trusted, controlled, and packaged or reviewed with the skill.

Risk: The skill can expose detailed customer records from store customer-list data.

Mitigation: Use it only for authorized customer-data analysis, restrict access to raw lists or exports, and prefer aggregated output unless raw records are explicitly needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gwyang7/skills/retail-customer-list-analysis)

## Skill Output:

**Output Type(s):** [analysis, json, markdown, code]

**Output Format:** [JSON analysis results and human-readable report text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include detailed customer records when raw list output is requested.]

## Skill Version(s):

1.0.0 (source: server release metadata and package __version__)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
