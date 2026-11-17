## Description:

Set up and optimize RAG pipelines for large datasets with document chunking, embedding benchmarking, vector indexing, and retrieval tuning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhinas90](https://clawhub.ai/user/abhinas90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to create or improve local RAG pipelines for large document collections, including chunking, embedding selection, vector index management, and retrieval parameter tuning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads chosen document folders and writes derived chunks, results, and index files.

Mitigation: Run it in dedicated working directories and avoid pointing outputs at important folders.

Risk: Using hosted embedding APIs in future extensions could send document chunks or queries to external providers.

Mitigation: Treat hosted embedding use as a separate privacy decision and prefer local models for sensitive data.

Risk: Retrieval and benchmark recommendations may be affected by simplified scoring paths and data-handling caveats.

Mitigation: Validate recommendations with representative queries and reviewed evaluation data before relying on them in production.

## Reference(s):

- [RAG Pipeline Starter ClawHub page](https://clawhub.ai/abhinas90/skills/rag-pipeline-starter)
- [Publisher profile](https://clawhub.ai/user/abhinas90)
- [Skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python command examples, console text, JSON results, and generated local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read user-selected document folders and write derived chunks, benchmark results, tuning results, and vector index files.]

## Skill Version(s):

1.0.1 (source: server release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
