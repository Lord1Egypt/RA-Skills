## Description:

A Chinese-oriented query planning skill that decomposes complex research tasks into identity, event, action, and counter-evidence search queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[z1one0415](https://clawhub.ai/user/z1one0415)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and agent builders use this skill before web research or multi-step analysis to turn a complex task into a structured query plan. It is especially oriented toward Chinese-language search phrase generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad research-like tasks and produce query plans when the user expected direct analysis.

Mitigation: Use it as a planning step before research, and confirm whether the next agent should search, analyze, or answer.

Risk: The templates are Chinese-oriented and may be less suitable for users who need another language.

Mitigation: Adapt or translate generated search phrases before using them in non-Chinese research workflows.

Risk: The skill generates queries only and does not verify facts or draw conclusions.

Mitigation: Route generated queries to search and analysis steps before presenting findings as evidence-backed answers.

## Reference(s):

- [Query Patterns](references/query-patterns.md)
- [Examples](references/examples.md)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [Structured JSON query plan with arrays of search phrases]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates four fixed query categories and requires at least two counter_queries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
