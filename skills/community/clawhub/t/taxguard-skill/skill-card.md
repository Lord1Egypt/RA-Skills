## Description: <br>
Monitors proposed trades for tax risks and optimization opportunities, supports opt-in blocking through Guardian Mode, and prepares daily tax reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaronahadi23](https://clawhub.ai/user/aaronahadi23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Trading-agent users and developers use this skill to check trades for wash sales, pattern day trader triggers, holding-period considerations, estimated tax impact, and tax-loss harvesting opportunities before execution. It can run in silent monitor mode, produce daily summaries, or ask for confirmation when opt-in Guardian Mode blocks a configured risk. <br>

### Deployment Geography for Use: <br>
United States <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive trading, holdings, tax, and income-related context may be sent to Rhetra and stored or logged with unclear privacy controls. <br>
Mitigation: Use the skill only when that data sharing is acceptable, start in monitor-only mode, store API keys in a secrets manager rather than a plain .env file when possible, and decide log retention and deletion practices before enabling it on real accounts. <br>
Risk: If TaxGuard is unreachable, the artifact behavior allows trades to proceed without a compliance check. <br>
Mitigation: Treat outage gaps as material, review them in the daily report, and require an explicit operating policy for whether trading should pause when checks cannot be completed. <br>
Risk: The host override option can redirect checks away from the default Rhetra endpoint. <br>
Mitigation: Avoid using the host override unless the destination is intentionally configured and trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aaronahadi23/taxguard-skill) <br>
- [Rhetra website](https://rhetra.io) <br>
- [Release README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown daily reports and plain-text command output with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses trade, holdings, tax, and income context supplied by the agent; Guardian Mode may return a blocking result that requires confirmation before execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: release evidence and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
