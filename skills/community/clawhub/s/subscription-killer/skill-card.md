## Description: <br>
Analyse a bank transactions CSV to detect recurring subscriptions, score cancellation priority, and surface actionable savings recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexwong27](https://clawhub.ai/user/alexwong27) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and personal-finance agents use this skill to inspect a local bank transaction CSV, identify recurring subscriptions, and prioritize cancellation or downgrade actions. It can also support company or contractor expense review where the user provides an appropriate account export. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads bank transaction exports, which may contain sensitive financial data. <br>
Mitigation: Run it locally on a narrow or redacted CSV export and review the report before sharing any output. <br>
Risk: Subscription detection and savings prioritization can be incomplete or misleading if the CSV format, merchant names, or recurring-payment patterns are unusual. <br>
Mitigation: Treat the output as decision support, manually review flagged merchants and cancellation links, and avoid relying on it as sole financial advice. <br>
Risk: The release evidence notes version and documentation mismatches that could affect expectations about available options or output. <br>
Mitigation: Check the installed release version and current command help before depending on documented invocation examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/alexwong27/subscription-killer) <br>
- [Cancellation URL lookup table](artifact/cancel_urls.json) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, text, shell commands, guidance] <br>
**Output Format:** [Terminal text report with subscription rankings, confidence indicators, savings estimates, flags, and cancellation links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a local CSV or TSV transaction export and Python 3; currency display can be configured with SUBSCRIPTION_KILLER_CURRENCY or --currency.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
