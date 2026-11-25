## Description:

按已确认的日期和状态筛选，只读汇总当前可见的本人订单（最多 20 单），并提供状态计数、商家待办和可见证据位置。

This skill is ready for commercial/non-commercial use.

## Publisher:

[xxjrq](https://clawhub.ai/user/xxjrq)

### License/Terms of Use:

MIT-0

## Use Case:

店铺经营者可用它巡检本人或有权查看的订单列表，核对已确认范围内的订单状态、待处理事项和页面证据；订单归属或筛选不明确时会停止汇总。

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan flags the external skill installation source as unpinned, with some analysis incomplete.

Mitigation: Review the external skill and its source before installation, and pin the CLI and skill revision to audited versions.

Risk: Some scripts were only partly inspected, and binary assets were outside the analyzer scope.

Mitigation: Review the uncovered scripts and binary assets before use.

## Reference(s):

- [Easy WebBridge (GitHub)](https://github.com/xxjrq/easy-webbridge)
- [Easy WebBridge (Gitee mirror)](https://gitee.com/xxjrq/easy-webbridge)
- [EasyBR official download page](https://www.ebrower.com/down.html)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown order status digest with counts, merchant follow-ups, visible evidence locations, and missing information]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [At most 20 visible orders; masks buyer-sensitive details; read-only.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
