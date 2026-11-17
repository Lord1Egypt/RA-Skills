## Description:

AI-powered mutual fund evaluation tool for Indian retail investors using web search and investor profiling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[krishnakumarmahadevan-cmd](https://clawhub.ai/user/krishnakumarmahadevan-cmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users, especially Indian retail investors and financial advisors, use this skill to evaluate a named mutual fund against investor age, goals, time horizon, risk tolerance, portfolio context, volatility preference, and tax sensitivity.

### Deployment Geography for Use:

India

## Known Risks and Mitigations:

Risk: The hosted service receives personal financial context, and the evidence does not provide enough privacy, retention, or third-party processing detail.

Mitigation: Use generic portfolio descriptions where possible, avoid account numbers, PAN or tax IDs, exact holdings, and other identifiers, and review the publisher's privacy terms before production use.

Risk: The skill produces investment suitability guidance that may be incomplete, outdated, or inappropriate for a user's full financial situation.

Mitigation: Treat outputs as decision-support only and review fund facts, tax assumptions, and recommendations with qualified financial advice before acting.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/krishnakumarmahadevan-cmd/skills/toolweb-mutual-fund-evaluator)
- [Mutual Fund Evaluator API Route](https://api.toolweb.in/tools/mutual-fund-evaluator)
- [Mutual Fund Evaluator API Docs](https://api.toolweb.in:8205/docs)
- [ToolWeb](https://toolweb.in)
- [ToolWeb OpenClaw](https://toolweb.in/openclaw/)

## Skill Output:

**Output Type(s):** [API Calls, Analysis, Guidance]

**Output Format:** [JSON API response with suitability scores, fund analysis, tax implications, comparative context, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a target mutual fund name and investor profile fields; the skill may use web search to add current market context.]

## Skill Version(s):

1.0.0 (source: server release metadata and OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
