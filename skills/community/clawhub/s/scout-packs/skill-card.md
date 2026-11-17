## Description:

Scout Packs helps agents find published business contact emails and source URLs for companies through paid USDC lookups on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tigerops-win](https://clawhub.ai/user/tigerops-win)

### License/Terms of Use:

MIT-0

## Use Case:

Sales and outreach agents use this skill to find published business contact emails and source URLs for prospecting, lead enrichment, and CRM backfill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A lookup can trigger a real USDC payment without a clear per-transaction user approval gate.

Mitigation: Require user confirmation before each lookup, showing the company query, $0.01 USDC amount, Base network, USDC contract, live recipient address, and cumulative spend.

Risk: Company names or domains submitted for enrichment are sent to the vendor.

Mitigation: Do not submit confidential prospect lists unless the user accepts disclosure of the company names or domains to the vendor.

## Reference(s):

- [Scout Packs on ClawHub](https://clawhub.ai/tigerops-win/skills/scout-packs)
- [Scout Packs agent documentation](https://scout-packs-production.up.railway.app/llms.txt)
- [Scout Packs payment manifest](https://scout-packs-production.up.railway.app/.well-known/x402)
- [Scout Packs OpenAPI specification](https://scout-packs-production.up.railway.app/openapi.json)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [JSON contact details or a text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Business email, company name, source URL, and verification note; name, title, and location when available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
