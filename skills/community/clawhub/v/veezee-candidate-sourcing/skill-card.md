## Description:

Find LinkedIn candidates matching a role spec, shortlist them, and enrich the shortlist with current role and experience.

This skill is ready for commercial/non-commercial use.

## Publisher:

[veezee-build](https://clawhub.ai/user/veezee-build)

### License/Terms of Use:

MIT-0

## Use Case:

External recruiters, sourcers, and hiring teams use this skill to turn LinkedIn role criteria into ranked shortlists enriched with current title, company, location, and recent experience.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may use broader-than-needed remote tooling or an unpinned npm initialization command.

Mitigation: Prefer the LinkedIn-specific MCP endpoint or direct API-key minting, review the Veezee service and npm package, and pin @veezee/sdk before running npx in sensitive environments.

Risk: Candidate sourcing runs can consume trial or paid credits quickly when searches paginate or enrich many profiles.

Mitigation: Check usage before searching, set max_credits on batch calls, prefer one appropriately sized search over pagination, and stop when budget or credit errors are returned.

Risk: Private LinkedIn profiles cannot be enriched and contact details are outside the skill's scope.

Mitigation: Skip anonymous profiles during enrichment, report them only as private matches when useful, and state that the skill does not provide email addresses or phone numbers.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/veezee-build/skills/veezee-candidate-sourcing)
- [Publisher profile](https://clawhub.ai/user/veezee-build)
- [Veezee LinkedIn MCP endpoint](https://mcp.veezee.io/linkedin)
- [Veezee API key mint endpoint](https://api.veezee.io/v1/keys/mint)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown shortlist with candidate summaries and credit-usage notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes ranked fit, current role, current company, location, two recent experience entries, skipped private-profile notes, and total credits spent.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
