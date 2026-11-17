## Description:

Monitor website prices, inventory, and content changes using browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinanping-cpu](https://clawhub.ai/user/yinanping-cpu)

### License/Terms of Use:


## Use Case:

Developers, operators, and commerce teams use this skill to check product prices, stock status, and web content changes across monitored sites. It supports single-product checks, CSV-based multi-product monitoring, price history logging, and alert review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: CSV-supplied URLs can cause browser automation to open arbitrary destinations, including local or private resources.

Mitigation: Use only product lists you control, review URLs before execution, and restrict monitoring to trusted public retailer domains.

Risk: Generated CSV history can be unsafe to open in spreadsheet software if formula evaluation is enabled.

Mitigation: Inspect or sanitize CSV output before spreadsheet use, and avoid enabling formula evaluation for generated files.

Risk: External alert channels can disclose monitored URLs and price data to third-party services.

Mitigation: Configure email or webhook alerts only when sharing the monitored data with that service is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinanping-cpu/skills/yinan-price-monitor)
- [Publisher profile](https://clawhub.ai/user/yinanping-cpu)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with bash examples; CSV history files and console text from the monitoring script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce price-history.csv entries with timestamp, product name, URL, price, and status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
