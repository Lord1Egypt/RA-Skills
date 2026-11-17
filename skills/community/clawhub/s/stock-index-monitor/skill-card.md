## Description:

StockIndexMonitor helps agents configure and explain a Chinese-market stock alert workflow using cost, price movement, volume, moving-average, RSI, gap, and trailing-stop rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quant520](https://clawhub.ai/user/quant520)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to set up stock-index and securities monitoring alerts for Chinese-market conventions, including threshold tuning, technical-indicator signals, and tiered notification examples. Outputs are informational and should not be treated as professional investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock alerts and suggested actions could be mistaken for professional financial advice.

Mitigation: Treat alerts as informational, review decisions independently, and avoid trading solely from skill output.

Risk: The skill's run commands reference a control.sh script that was not included in the reviewed package.

Mitigation: Do not run any script from that path unless it has been separately inspected and trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/quant520/skills/stock-index-monitor)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python configuration examples, shell command examples, and alert-message templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language stock-monitoring guidance using red-up and green-down market color conventions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
