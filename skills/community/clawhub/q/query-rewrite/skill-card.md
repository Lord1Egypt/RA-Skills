## Description:

Query Rewrite helps agents preprocess Chinese-oriented RAG queries by detecting unclear, referential, comparative, multi-intent, rhetorical, or conditional queries and rewriting them for memory, wiki, or vector retrieval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dabin0927](https://clawhub.ai/user/dabin0927)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill before RAG, memory, wiki, or vector searches to decide whether a user query needs rewriting and to produce original-plus-rewritten retrieval queries without changing the user's intent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad query-rewrite triggers may cause extra rewritten searches when a user is only discussing query rewriting concepts.

Mitigation: Review triggers and apply the documented zero-rewrite and fallback rules before enabling the skill in workflows where extra searches could confuse retrieval results.

Risk: Query rewriting can change retrieval behavior if the agent adds unsupported context or changes the user's intent.

Mitigation: Only add entities present in recent context, always search the original query too, and fall back to the original query when the referent or intent is unclear.

## Reference(s):

- [Query rewrite patterns](references/rewrite-patterns.md)
- [ClawHub skill page](https://clawhub.ai/dabin0927/skills/query-rewrite)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown guidance with rewritten query strings or lists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return the original query plus one or more rewritten queries; falls back to the original query when rewriting is unsafe or unsupported.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
