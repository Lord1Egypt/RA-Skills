## Description: <br>
Audit traffic quality beyond surface GA4 or Meta reports by mapping source and medium weight to behavioral depth, flagging likely invalid or low-intent clicks, and recommending budget cuts or exclusions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rijoyai](https://clawhub.ai/user/rijoyai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketers, analysts, and commerce operators use this skill to audit GA4 and Meta traffic quality, compare engagement depth against conversion paths, and identify sources, campaigns, placements, or referrals to pause, cap, exclude, or monitor. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can produce forceful pause, cap, exclusion, or reallocation recommendations from incomplete analytics context. <br>
Mitigation: Confirm GA4 and Meta data, attribution window, sample size, and business impact before changing budgets or placements. <br>
Risk: Traffic-quality hypotheses may be mistaken when engagement, key-event, or attribution data is missing or misconfigured. <br>
Mitigation: Treat recommendations as hypotheses and validate tracking definitions, date ranges, and conversion paths before acting. <br>


## Reference(s): <br>
- [Traffic Quality Audit Skill](https://clawhub.ai/rijoyai/traffic-quality-audit) <br>
- [Traffic Quality Playbook](references/traffic_quality_playbook.md) <br>
- [Rijoy Brand Context](references/rijoy_brand_context.md) <br>
- [Rijoy](https://www.rijoy.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown diagnostic tables, narrative analysis, and prioritized recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a source/medium comparison table, a dwell-time versus conversion-path section, and at least two shutoff or pause recommendations when in scope.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
