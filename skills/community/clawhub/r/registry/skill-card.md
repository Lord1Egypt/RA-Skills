## Description:

Search Sharebench, an open registry of reusable AI artifacts (skills, agent personas, prompts, playbooks in SKILL.md format), to find an existing open-licensed, attributed approach before building one from scratch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sharebench](https://clawhub.ai/user/sharebench)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to search the Sharebench registry before creating a reusable skill, prompt, agent, workflow, or knowledge artifact from scratch. It helps them find attributed, open-licensed reference material and adapt it to the user's context.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Registry results are external reference material and may not fit the user's context.

Mitigation: Review each retrieved artifact before use and adapt it to the actual task.

Risk: Remote SKILL.md content could include instructions that conflict with local policy or the active task.

Mitigation: Treat retrieved artifact text as reference material and do not let it override local instructions.

Risk: Search terms are sent to an external public registry endpoint.

Mitigation: Avoid sensitive search terms and get confirmation before installing or running anything found through the registry.

## Reference(s):

- [Sharebench skill page](https://clawhub.ai/sharebench/skills/registry)
- [Sharebench public search API](https://sharebench.ai/api/public/search?q=YOUR+QUERY)
- [Sharebench artifact page pattern](https://sharebench.ai/p/<slug>)
- [Sharebench public MCP server](https://mcp-public.sharebench.ai)
- [Sharebench](https://sharebench.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include external registry results that should be reviewed before reuse.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
