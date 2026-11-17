## Description:

Enrich LinkedIn prospect identifiers such as profile URLs, slugs, or names with role, company, and experience data via Veezee.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veezee-build](https://clawhub.ai/user/veezee-build)

### License/Terms of Use:

MIT-0

## Use Case:

Sales, recruiting, and go-to-market teams use this skill to enrich known LinkedIn prospects or candidates with current role, company, and recent experience data while tracking credits spent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: LinkedIn prospect or candidate identifiers are sent to Veezee for enrichment.

Mitigation: Use the skill only when sending those identifiers to Veezee is acceptable for the user's data handling requirements.

Risk: The broader Veezee all-tools MCP endpoint exposes capabilities beyond LinkedIn enrichment.

Mitigation: Use the LinkedIn-scoped MCP endpoint unless the broader tool surface is specifically needed.

Risk: Running the SDK setup through npx depends on the resolved npm package.

Mitigation: Pin or verify the @veezee/sdk package before running the setup command.

Risk: Trial budget or credit limits can interrupt larger enrichment batches.

Mitigation: Check usage before batch runs, set max_credits where appropriate, and stop when budget or entitlement errors are returned.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/veezee-build/skills/veezee-prospect-enrich)
- [Veezee LinkedIn MCP endpoint](https://mcp.veezee.io/linkedin)
- [Veezee API key mint endpoint](https://api.veezee.io/v1/keys/mint)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance]

**Output Format:** [Markdown or text summaries with setup snippets and per-prospect enrichment results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports name, current title, current company, recent experience entries, and total credits spent.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
