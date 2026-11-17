## Description:

门店客流分析基于 AIoT customerFunnel 和 behaviorFunnel 数据，生成门店客流、转化漏斗、转化效率和人均指标的诊断分析。

This skill is ready for commercial/non-commercial use.

## Publisher:

[gwyang7](https://clawhub.ai/user/gwyang7)

### License/Terms of Use:

MIT-0

## Use Case:

Retail operations analysts, store managers, and agents use this skill to retrieve store funnel data and diagnose traffic drops, trial depth, and conversion efficiency across selected date ranges.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that the skill loads an unaudited external module from a developer-specific local path before fetching store data.

Mitigation: Review the skill before installation, ask the publisher to bundle or pin the API client, and confirm which service receives store IDs and date ranges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gwyang7/skills/retail-traffic-analysis)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Console-style analysis text and structured JSON result data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May fetch customerFunnel and behaviorFunnel data for a store ID and date range before calculating conversion diagnostics.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
