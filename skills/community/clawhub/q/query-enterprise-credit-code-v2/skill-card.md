## Description:

通过企业名称模糊匹配查询企业统一社会信用代码，支持多结果选择和错误提示，适用于工商信息核验和尽调。

This skill is ready for commercial/non-commercial use.

## Publisher:

[daviddatamining](https://clawhub.ai/user/daviddatamining)

### License/Terms of Use:

MIT-0

## Use Case:

Business users and agents use this skill to look up a Chinese enterprise's unified social credit code from an enterprise name for investment attraction, due diligence, and business-registration checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Enterprise names, internal enterprise IDs, and returned company records may be sent to an external service and printed in local execution logs over plaintext HTTP.

Mitigation: Use only in approved environments until the integration uses HTTPS, response validation, and log redaction for sensitive business data.

Risk: The provided scripts do not fully match the documented command-line behavior, which can break automated or non-interactive use.

Mitigation: Verify and implement the documented parameters before production automation, including enterprise-name input and multi-result selection behavior.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/daviddatamining/skills/query-enterprise-credit-code-v2)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Text or JSON lookup results with enterprise name, unified social credit code, enterprise ID, or an error message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May prompt for a selection when an enterprise-name query returns multiple matches.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
