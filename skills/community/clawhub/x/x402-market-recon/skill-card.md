## Description:

Measures live x402 endpoint discoverability, registry demand, payment-challenge delivery, directory checks, and router limits before changes are made.

This skill is ready for commercial/non-commercial use.

## Publisher:

[33ai-wq](https://clawhub.ai/user/33ai-wq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and endpoint operators use this skill to measure whether an x402 service can be discovered and purchased, then prioritize pricing, listing, or discovery-document fixes based on evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Allowing off-domain probes contacts public hosts beyond the documented list.

Mitigation: Review the host list before enabling --allow-any-host and use only intended public endpoints.

Risk: Local measurement reports may be written to an unintended directory.

Mitigation: Choose and review the --out directory before running the skill.

Risk: Unpaid endpoint probes still make public network requests.

Mitigation: Treat probes as external contact and obtain any required authorization before testing endpoints.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/33ai-wq/skills/x402-market-recon)
- [Decision rules and thresholds](artifact/references/decision-rules.md)
- [Dated market findings baseline](artifact/references/findings-baseline.md)
- [Coinbase x402 discovery registry](https://api.cdp.coinbase.com/platform/v2/x402/discovery/resources)

## Skill Output:

**Output Type(s):** [Text, Guidance, Files]

**Output Format:** [Markdown findings and local measurement reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report dates, sample sizes, sources, and unverified findings; reports are written under the selected --out directory.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
