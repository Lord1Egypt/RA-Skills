## Description: <br>
Captures forecast errors, supplier risks, logistics delays, inventory mismatches, quality deviations, and demand signal shifts to support continuous supply chain improvement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jose-compu](https://clawhub.ai/user/jose-compu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Supply chain teams and agent users use this skill to record disruptions, forecast misses, supplier risks, inventory mismatches, quality issues, and feature requests as local Markdown learnings. Recurring patterns can be promoted into scorecards, safety stock policies, routing playbooks, demand planning models, quality criteria, or reusable skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional Bash output detection may inspect command output that contains sensitive operational data. <br>
Mitigation: Enable Bash output detection only where command output will not include sensitive data, and prefer targeted project-level hook matchers. <br>
Risk: A user-level global hook can display supply chain reminders in sessions where they are not relevant. <br>
Mitigation: Use project-level hooks with supply-chain-specific matchers unless reminders are intentionally wanted in all sessions. <br>
Risk: Learning logs may capture proprietary supplier pricing, negotiated contract terms, or customer-identifiable order data if users include raw operational details. <br>
Mitigation: Record aggregated metrics and redacted summaries instead of raw purchase order numbers, customer names, negotiated terms, or proprietary pricing. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/jose-compu/self-improving-supply-chain) <br>
- [OpenClaw Integration](references/openclaw-integration.md) <br>
- [Hook Setup Guide](references/hooks-setup.md) <br>
- [Entry Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and hook configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local learning logs when an agent follows the workflow; optional hooks emit reminder text and can inspect Bash output for supply chain disruption terms.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
