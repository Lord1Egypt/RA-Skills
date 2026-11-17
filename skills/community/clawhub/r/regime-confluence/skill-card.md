## Description:

This paid x402 endpoint on Base returns a multi-timeframe regime agreement score for evaluating potential entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kynto2001-ctrl](https://clawhub.ai/user/kynto2001-ctrl)

### License/Terms of Use:

MIT-0

## Use Case:

Crypto traders and agent developers use the score to assess agreement across market timeframes before considering a potential entry. Each request is a paid x402 call.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid calls authorize USDC transfers using an EVM private key, so unintended or repeated requests can incur charges.

Mitigation: Keep EVM_PRIVATE_KEY in a secure secret store, set a strict x402 maximum payment policy, and check the per-call price before enabling repeated calls.

## Reference(s):

- [Regime Confluence endpoint](https://apexrunner.ai/signals/regime-confluence)
- [Regime signal](https://apexrunner.ai/signals/regime)
- [Regime Transition signal](https://apexrunner.ai/signals/regime-transition)
- [ClawHub release page](https://clawhub.ai/kynto2001-ctrl/skills/regime-confluence)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [JSON response containing a confluence score, aligned timeframe count, and dominant regime]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A paid x402 request returns a market signal; it is not a guarantee of trading outcomes.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
