## Description:

Sushiro Skill helps agents check real-time queue status, store details, city rankings, area filters, nearby stores, and area lists for Sushiro locations in Mainland China.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitnapp](https://clawhub.ai/user/gitnapp)

### License/Terms of Use:

MIT

## Use Case:

Agents use this skill to answer user questions about Sushiro wait conditions, compare stores by city or area, and retrieve store details or raw JSON for low-frequency personal planning and monitoring.

### Deployment Geography for Use:

Mainland China

## Known Risks and Mitigations:

Risk: The skill sends requests to an unofficial Sushiro China integration using a bundled shared bearer token.

Mitigation: Install only after reviewing that behavior, and prefer a version that removes the hardcoded token or requires an operator-supplied token.

Risk: Broad raw API access and filter handling can increase exposure when inputs are untrusted.

Mitigation: Avoid the raw command, do not pass untrusted city or area text into filters, and prefer an allowlisted endpoint implementation with fixed jq argument handling.

## Reference(s):

- [Sushiro China API Reference](references/api.md)
- [Sushiro China Mini-Program API Base](https://crm-cn-prd.sushiro.com.cn/wechat/api/2.0)

## Skill Output:

**Output Type(s):** [text, shell commands, JSON, guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI results are tables, plain text, or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and jq. Results come from live Sushiro China endpoints and are limited to Mainland China stores.]

## Skill Version(s):

0.1.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
