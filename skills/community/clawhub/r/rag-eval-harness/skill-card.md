## Description:

Guides evaluation of RAG question-answering quality and hallucination resistance using positive retrieval tests, negative refusal tests, and local threshold scans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT (Python code); all rights reserved (skill text and methodology)

## Use Case:

Developers and engineers evaluate local knowledge-base RAG systems before release and after corpus or model changes, checking retrieval accuracy, refusal of unsupported questions, and citation-backed answers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local knowledge-base content is sent to a local embedding service and included in evaluation reports.

Mitigation: Review the knowledge-base path and content before running; protect the locally generated reports.

Risk: The evaluation suite executes scripts listed in its registry.

Mitigation: Treat the registry and referenced scripts as trusted code; review changes before running the suite.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/rag-eval-harness)
- [Local RAG evaluation script](references/local_rag_eval.py)
- [Capability evaluation suite](references/capability_eval_suite/run_suite.py)
- [Evaluation suite registry](references/capability_eval_suite/suite_registry.json)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bundled scripts can produce local JSON evaluation reports.]

## Skill Version(s):

1.1.5 (source: ClawHub release metadata; bundled frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
