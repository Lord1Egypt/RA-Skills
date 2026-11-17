## Description:

Optimizes RAG pipeline chunking strategy by analyzing documents and recommending chunk sizes, splitting methods, overlap settings, and metadata enrichment for retrieval quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to profile document corpora and choose chunking, overlap, metadata, and evaluation strategies for RAG applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Example profiling commands may inspect private or regulated documentation if pointed at the wrong corpus.

Mitigation: Run commands only against the intended documentation set and apply the organization's data-handling controls before sharing outputs.

Risk: Chunking recommendations can affect retrieval quality and may produce misleading results if accepted without validation.

Mitigation: Evaluate recommendations with representative queries and metrics such as recall, precision, MRR, answer accuracy, and latency before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/charlie-morrison/skills/rag-chunking-optimizer)
- [ClawHub publisher profile](https://clawhub.ai/user/charlie-morrison)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with tables, code blocks, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations may include document profiles, chunking strategy comparisons, evaluation metrics, and expected retrieval-quality improvements.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
