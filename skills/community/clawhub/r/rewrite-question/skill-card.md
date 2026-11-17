## Description:

Rewrites user questions into self-contained queries by resolving context, pronouns, time references, and omitted entities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovenervermore](https://clawhub.ai/user/lovenervermore)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn follow-up business questions into standalone queries before downstream intent recognition, SQL generation, or answer workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Business questions, SQL templates, or credentials may be sent to external LLM endpoints.

Mitigation: Use only an approved HTTPS endpoint, restrict outbound access, and avoid providing production credentials or sensitive business data.

Risk: Caller-supplied endpoint and token settings can redirect sensitive prompts or authorization material.

Mitigation: Fix endpoint configuration in deployment policy and rotate or remove embedded or broadly scoped tokens before use.

Risk: Milvus, SQL, and workflow-file behavior may expose or persist sensitive query context.

Mitigation: Document data flows, limit accessible collections and workflow directories, and review generated JSON and SQL before downstream execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lovenervermore/skills/rewrite-question)
- [ClawHub publisher profile](https://clawhub.ai/user/lovenervermore)

## Skill Output:

**Output Type(s):** [text, JSON, code, shell commands, configuration, guidance]

**Output Format:** [JSON object containing the final query, rewrite status, confidence, optional reasoning, and optional matched SQL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a confidence threshold before adopting an LLM rewrite and may return matched SQL when a supplied QA pair exactly matches the query.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
