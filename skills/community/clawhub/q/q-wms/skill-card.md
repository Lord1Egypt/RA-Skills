## Description:

千易 WMS 智能查询技能。当前开放的一期场景：今日仓内总览、今日待办与异常、出库积压归因、昨日问题恢复情况，以及库存、订单、任务、绩效和仓库/货主上下文查询。所有查询必须通过 q-claw。

This skill is ready for commercial/non-commercial use.

## Publisher:

[ljqdh](https://clawhub.ai/user/ljqdh)

### License/Terms of Use:

MIT-0

## Use Case:

Warehouse managers, operators, and business users use this skill to query 千易 WMS for warehouse overviews, tasks, issues, outbound backlog causes, recovery status, inventory, orders, performance, warehouse context, and owner context through q-claw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorized use can expose operational WMS data such as inventory, orders, tasks, performance, warehouse, and owner context through q-claw.

Mitigation: Limit installation and authorization to users who should access that WMS data, and review q-claw authorization scope before deployment.

Risk: Warehouse decisions can be affected if responses reuse stale context or infer business data outside the current tool result.

Mitigation: Require business results, selections, pagination prompts, and fixed interactions to come only from the current q-claw response.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ljqdh/skills/q-wms)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Guidance]

**Output Format:** [Localized natural-language responses and Markdown links or tables when returned by q-claw]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs must be grounded in the current q-claw result and may include authorization links, warehouse or owner selections, business summaries, or necessary follow-up questions.]

## Skill Version(s):

1.0.73 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
