## Description:

Decides whether an agent should run `memory_search` before another skill or workflow, including when to retrieve, how to query, how much context to keep, and when to fall back.

This skill is ready for commercial/non-commercial use.

## Publisher:

[otweihan](https://clawhub.ai/user/otweihan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to decide when local memory retrieval is useful before continuing project work, following another skill, or relying on prior decisions. It helps build compact memory queries, keep only high-signal results, and fall back when retrieval is weak or unnecessary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may consult local memory when a task appears to depend on prior project context.

Mitigation: Use the skill's decision flow to retrieve only when the task depends on project history, prior decisions, local notes, or user-specific preferences.

Risk: Noisy, stale, or low-relevance memory results could add unnecessary context or influence later reasoning.

Mitigation: Start with the top 1-3 results, expand only clearly relevant hits, and fall back immediately when retrieval is weak, unavailable, or unnecessary.

## Reference(s):

- [Decision Flow](references/decision-flow.md)
- [Fallback Rules](references/fallback-rules.md)
- [Query Construction](references/query-construction.md)
- [Result Trimming](references/result-trimming.md)
- [Skill Tiering](references/skill-tiering.md)

## Skill Output:

**Output Type(s):** [guidance, text, markdown]

**Output Format:** [Markdown guidance with concise decision criteria and query recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces retrieval decisions, compact memory-search query guidance, result-limit guidance, and fallback guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
