## Description:

Compresses and accelerates vector search in memory/RAG systems using TurboQuant vector quantization with blockwise Hadamard rotation and Lloyd-Max scalar quantization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyztj](https://clawhub.ai/user/sunnyztj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to evaluate, integrate, and run TurboQuant compression for embedding stores, especially SQLite/sqlite-vec memory databases and RAG search systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validation workflows can load a local native sqlite-vec extension through SQLITE_VEC_PATH or --vec-ext.

Mitigation: Use only trusted, absolute extension paths and avoid untrusted environment variables or command-line values.

Risk: Migration workflows can modify a local memory database by creating and populating quantized embedding tables.

Mitigation: Run migration first on backup copies or disposable test databases and inspect results before using production data.

Risk: Validation and benchmark output can expose details about local memory stores in terminal or CI logs.

Mitigation: Avoid running benchmarks or validation against sensitive stores in shared terminals, shared logs, or CI output.

## Reference(s):

- [TurboQuant Algorithm Reference](references/algorithm.md)
- [TurboQuant paper](https://arxiv.org/abs/2504.19874)
- [PolarQuant paper](https://arxiv.org/abs/2502.02617)
- [ClawHub skill page](https://clawhub.ai/sunnyztj/skills/turboquant-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and Python snippets, plus optional JSON validation reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of compressed vector artifacts and SQLite quantized embedding tables when the migration script is run.]

## Skill Version(s):

2.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
