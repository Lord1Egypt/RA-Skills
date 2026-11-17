## Description:

Explore zooidfund campaigns and assess public evidence; use when browsing charitable requests or proposing USDC donations on Base. Transfers and paid evidence require explicit authority.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ales375](https://clawhub.ai/user/ales375)

### License/Terms of Use:

MIT-0

## Use Case:

External operators use the skill to explore humanitarian campaigns, assess available public evidence, and prepare carefully bounded USDC donations on Base. It separates read-only exploration from paid evidence access, registration, and transfers that require explicit authority.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Donations are irreversible, and registration or confirmed donations can make identity and wallet-linked activity public.

Mitigation: Use a dedicated low-balance wallet, keep donations manually approved, and review the current terms and privacy information before registration.

Risk: Evidence retrieval may incur repeated fees and expose sensitive records.

Mitigation: Start with free public browsing and require explicit operator approval before any potentially paid evidence request.

Risk: The hosted server source is unavailable for public audit.

Mitigation: Start in read-only mode and escalate slowly; use enforced spending and stop controls before enabling scheduled donations.

## Reference(s):

- [Zooidfund](https://zooid.fund)
- [Zooidfund Skill on ClawHub](https://clawhub.ai/ales375/skills/zooidfund)

## Skill Output:

**Output Type(s):** [Markdown, Guidance, Configuration]

**Output Format:** [Plain-language and Markdown campaign assessments, recommendations, and optional policy or scheduling configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May suggest up to five campaigns or none; assessments and prepared configuration do not grant spending authority.]

## Skill Version(s):

1.9.3 (source: frontmatter; confirmed by server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
