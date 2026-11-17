## Description:

Backend retrieval skill for structured search of occupational health standards and documents, returning relevant text with source and clause details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loda666](https://clawhub.ai/user/loda666)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill as a backend retrieval component for occupational health regulation workflows. It returns source text and structured citation fields for downstream skills rather than direct end-user answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on mutable unpackaged Python code from a hard-coded workspace path.

Mitigation: Install and run it only in a controlled environment where the referenced RAG system path is trusted, reviewed, and read-only.

Risk: Queries may be processed by embedding or rerank components that are not clearly disclosed by the artifact.

Mitigation: Review data handling for the embedding and rerank components before using the skill with sensitive queries.

Risk: Unbounded result counts can increase operational load or expose more retrieved text than intended.

Mitigation: Fix the input schema and enforce a bounded top_k before broad deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/loda666/skills/rag-search)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON object containing results, error, query, count, and method fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Each result may include content, source, clause, regulation_level, and score.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
