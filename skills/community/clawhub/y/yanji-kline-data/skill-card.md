## Description:

Yanji Kline Data fetches stock quote data, volume, price ranges, and demonstration moving-average estimates for supported China market stock codes.

This skill is for demonstration purposes and not for production usage.

## Publisher:

[caoling7878-arch](https://clawhub.ai/user/caoling7878-arch)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts can use this skill as a teaching or lightweight quote helper for checking supported stock codes and demonstrating basic price and moving-average workflows. It should not be used for trading, compliance, or automated financial decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may show estimated moving averages or demo fallback values that are not reliable historical K-line data.

Mitigation: Use it only for teaching or lightweight quote lookup, and verify financial data with an authoritative market data provider before making decisions.

Risk: The skill contacts Sina Finance with the requested stock code when network access is available.

Mitigation: Review network use before deployment and avoid using the skill where outbound market-data requests are not permitted.

Risk: The output could be mistaken for trading, compliance, or automated decision support.

Mitigation: Keep human review in the workflow and do not rely on this skill for trading, compliance, or automated financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caoling7878-arch/skills/yanji-kline-data)
- [Sina Finance](https://finance.sina.com.cn)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON returned from a command-line stock quote helper]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include live Sina Finance quote fields when network access works, or clearly marked failure/demo values when data cannot be fetched.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
