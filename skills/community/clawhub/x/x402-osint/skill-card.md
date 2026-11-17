## Description:

Performs paid OSINT lookups on usernames or email addresses to find public profiles and footprint data, paid in USDC on Base via x402 with no API keys needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jienweng](https://clawhub.ai/user/jienweng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run public-profile OSINT lookups for legitimate recruiting research, prospecting, due diligence, trust and safety, brand protection, or personal exposure audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for a wallet private key and can make automatic paid USDC requests from a Base wallet.

Mitigation: Use a dedicated low-balance wallet, avoid primary wallet keys, and prefer a pinned reviewed version when available.

Risk: Repeated or unintended paid calls could accumulate charges.

Mitigation: Set per-call spend limits where supported, enforce external wallet limits where possible, and monitor usage for repeated paid requests.

Risk: OSINT lookup workflows can be misused for harassment, stalking, or profiling without a lawful basis.

Mitigation: Limit use to public-profile lookups for legitimate purposes such as due diligence, trust and safety, brand protection, or personal exposure audits.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jienweng/skills/x402-osint)
- [Publisher profile](https://clawhub.ai/user/jienweng)

## Skill Output:

**Output Type(s):** [text, guidance]

**Output Format:** [Natural-language text and JSON service responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses can summarize username, email, or identity-report lookups; paid calls require a configured Base wallet.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
