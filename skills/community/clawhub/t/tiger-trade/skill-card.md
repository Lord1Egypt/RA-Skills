## Description:

Tiger Trade helps agents provide Tiger Brokers API setup guidance and example code for checking prices, managing portfolio context, and placing US or Hong Kong stock orders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[esanle](https://clawhub.ai/user/esanle)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to configure Tiger Brokers API access, check stock prices, and prepare buy or sell order code for US or Hong Kong stocks. Because the sample can operate on a live brokerage account, users should add review, confirmation, and credential safeguards before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe live-trading instructions could cause accidental real-money orders.

Mitigation: Add sandbox defaults, explicit order review and confirmation, trade limits, and contract verification before use.

Risk: Brokerage credentials are stored in a local plaintext configuration file.

Mitigation: Use secure credential storage with restrictive file permissions or a secret manager.

## Reference(s):

- [Tiger Brokers 02800 stock page](https://www.itiger.com/hant/stock/02800)
- [Tiger Brokers AAPL stock page](https://www.itiger.com/hant/stock/AAPL)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown with JSON and Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live-trading sample code and credential configuration guidance that require review before execution.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
