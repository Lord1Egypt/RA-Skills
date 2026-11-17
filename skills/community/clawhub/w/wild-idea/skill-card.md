## Description:

Injects concrete constraints from remote domains as "nails" and juxtaposes them with user-domain "counterparts" to generate intentionally unusual brainstorming outputs, with comfort and web-verification gates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liwenyu2002](https://clawhub.ai/user/liwenyu2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, product teams, and other creative practitioners use this skill when they are stuck on a product or design problem and need deliberately unfamiliar, concrete idea prompts. It produces nail-to-counterpart brainstorming tables and rerolls ideas that are too conventional or already implemented.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send search terms related to a user's brainstorming problem to Tavily.

Mitigation: Use it only when external search is approved, and avoid entering confidential product ideas unless the search workflow is explicitly permitted.

Risk: The artifact uses local API-key and home-directory helper patterns for Tavily search.

Mitigation: Review and replace the curl, .env, and home-directory helper examples with a scoped, reviewed API client before organizational deployment.

Risk: Generated ideas are intentionally unconventional and may be misleading if treated as validated product strategy.

Mitigation: Treat outputs as brainstorming prompts and require human review, feasibility checks, and independent validation before use.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/liwenyu2002/skills/wild-idea)
- [Paradigms reference](references/paradigms.md)
- [Mao seed library](references/mao-seeds.md)
- [Search integration reference](references/search-integration.md)
- [Tavily curl example](references/tavily-curl-example.md)
- [Output example](templates/output-example.md)

## Skill Output:

**Output Type(s):** [markdown, text, shell commands, code, guidance]

**Output Format:** [Markdown tables with concise text, optional HTML poster content, and inline shell or Python command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses random seed selection and optional external Tavily search; search failures are expected to be reported or skipped rather than filled from memory.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact package.json reports 5.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
