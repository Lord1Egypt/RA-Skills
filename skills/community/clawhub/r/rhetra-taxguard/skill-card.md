## Description: <br>
Silent tax advisor that checks every trade for wash sales, PDT triggers, and optimization, logs results, and delivers a daily tax risk and opportunity report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaronahadi23](https://clawhub.ai/user/aaronahadi23) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Trading agents and their operators use this skill to check planned trades for tax, wash-sale, pattern day trader, and holding-period issues before execution, then summarize accumulated findings in daily and year-end reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends detailed trade, account, portfolio, and tax context to Rhetra and creates local logs. <br>
Mitigation: Review Rhetra consent, storage, deletion, retention, and sharing terms before installation, and avoid sending account or tax details that are not needed for the check. <br>
Risk: If TaxGuard is unreachable, the skill proceeds with the trade and records the gap only in the daily report. <br>
Mitigation: Decide before use whether fail-open behavior is acceptable for the trading setup, and configure Guardian Mode or external controls for risks that should block execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aaronahadi23/rhetra-taxguard) <br>
- [Rhetra TaxGuard signup](https://rhetra.io/trading) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown reports and guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a Node.js helper command and Rhetra API responses to produce trade checks, blocking guidance in Guardian Mode, strategy assessments, CSV export guidance, and daily tax summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
