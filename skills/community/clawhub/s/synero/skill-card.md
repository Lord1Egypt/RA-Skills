## Description:

Synero asks four contrasting AI advisors a terminal-submitted question and returns a synthesized answer for judgment-heavy decisions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blovett80](https://clawhub.ai/user/blovett80)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and decision makers use this skill to get multiple AI perspectives and a final synthesis for strategy, research, architecture, hiring, positioning, and other ambiguous decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and the Synero API key are sent over the network.

Mitigation: Use the skill only for prompts approved for Synero, avoid secrets or regulated/confidential data unless approved, and keep SYNERO_API_KEY narrowly scoped and revocable.

Risk: SYNERO_API_URL can redirect authenticated requests to a different endpoint.

Mitigation: Leave SYNERO_API_URL unset for the default Synero endpoint, or set it only to an exact trusted HTTPS endpoint.

## Reference(s):

- [Prompt Patterns](references/prompt-patterns.md)
- [Synero](https://synero.ai)
- [ClawHub Skill Page](https://clawhub.ai/blovett80/skills/synero)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Terminal text; normal mode prints a Markdown-style synthesis, quiet mode prints only the final answer, and raw mode prints SSE event lines.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SYNERO_API_KEY and python3; optional settings control endpoint, timeout, advisor models, synthesizer model, and thread continuity.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence, released 2026-03-09)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
