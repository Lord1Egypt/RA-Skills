## Description:

Enrich a list of companies (names, domains, or LinkedIn URLs) with firmographic data like industry, employee count, headquarters, and founding year.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veezee-build](https://clawhub.ai/user/veezee-build)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and business research teams use this skill to enrich batches of company domains or LinkedIn identifiers with firmographic data and credit usage reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company lists, domains, LinkedIn URLs, and the Veezee API key are sent to Veezee.

Mitigation: Use the skill only for data the user is comfortable sharing with Veezee, and prefer the narrower LinkedIn MCP endpoint where it satisfies the task.

Risk: The optional npx setup command can introduce supply-chain exposure if used without pinning or review.

Mitigation: Pin and review the @veezee/sdk package version before using npx in sensitive environments, or use the MCP endpoint instead.

Risk: Batch runs can stop or incur unexpected cost when trial limits, paid credits, or realtime freshness settings are exceeded.

Mitigation: Check usage before a batch, set max_credits on calls, stop on credit-limit errors, and report total credits spent.

Risk: Approximate company names and unverifiable domains can return no company record or closest-match suggestions instead of a definitive enrichment result.

Mitigation: Ask for a website domain or LinkedIn company URL when the identifier is ambiguous, and flag INVALID_INPUT responses with suggested matches rather than guessing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/veezee-build/skills/veezee-company-enrichment)
- [Veezee LinkedIn MCP Endpoint](https://mcp.veezee.io/linkedin)
- [Veezee API Key Mint Endpoint](https://api.veezee.io/v1/keys/mint)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, shell commands, configuration, guidance]

**Output Format:** [Markdown report with per-company enrichment results, invalid-input flags, and credit usage totals.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include company name, industry, employee count, headquarters, website, founding year, and total credits spent when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
