## Description:

Helps agents obtain XRP Ledger telemetry and ledger or account reads through metered XRP payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fudge144](https://clawhub.ai/user/fudge144)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to check XRP Ledger fee pressure, transaction queues, and ledger liveness, or to retrieve ledger and account details through paid HTTP requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Signed XRPL transaction fees are not clearly included in the advertised per-request or daily spend limits.

Mitigation: Use only a dedicated low-balance hot wallet and do not treat the daily budget as a complete loss limit until transaction fees are capped and audited.

Risk: Payment requests use a wallet seed and depend on external services.

Mitigation: Start with NO_PAY, keep the seed out of chats and repositories, and review dependency versions and the WS_URL endpoint before signing.

Risk: Telemetry can become stale and proxied reads are best-effort.

Mitigation: Check the response's freshness flags and age before presenting data as live; plan for rate limits and outages.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/fudge144/skills/xrp-fleet-data)
- [Service API documentation](https://d5e7fd5a.xrplclaw.com/site/nodes/API.md)
- [Live pricing contract](https://d5e7fd5a.xrplclaw.com/app/nodes/api/v1/pricing)
- [Agent product description](https://d5e7fd5a.xrplclaw.com/site/nodes/llms.txt)

## Skill Output:

**Output Type(s):** [JSON data, Guidance, Shell commands]

**Output Format:** [JSON responses and Markdown instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns telemetry or ledger/account reads; paid calls can include payment and settlement details.]

## Skill Version(s):

1.0.2 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
