## Description:

Plan which search provider to use before multi-provider skills run by scoring query signals, choosing Serper, Tavily, Exa, Brave, or Firecrawl, defining a fallback chain, and documenting the rationale.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruti3](https://clawhub.ai/user/ruti3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create an explicit, auditable routing plan before using multi-provider web search skills or search APIs. It helps select a primary search provider, fallback chain, provider-specific query phrasing, and post-route quality checks without executing searches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat the skill as a live search tool or assume it fetched current results.

Mitigation: Use the output only as a routing plan; execute selected providers separately and verify retrieved results.

Risk: Sensitive or personal query text could be routed to an external provider if the plan is followed without review.

Mitigation: For sensitive queries, confirm consent, minimize logging, and prefer available privacy-preserving or internal search options.

Risk: Users may provide API keys even though the skill does not need credentials.

Mitigation: Do not give API keys to this prompt-only skill; configure credentials only in approved downstream executor tools.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ruti3/skills/search-auto-routing-plan)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown routing plan with scoring tables and optional YAML executor hints]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only planning output; no live API calls, network access, code execution, credential handling, or persistence.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
