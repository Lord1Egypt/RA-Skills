## Description: <br>
Compress and accelerate vector search in memory and RAG systems using TurboQuant vector quantization with blockwise Hadamard rotation and Lloyd-Max scalar quantization. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunnyztj](https://clawhub.ai/user/sunnyztj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to reduce embedding storage size, speed up semantic search, validate quantization quality, and integrate compressed vector storage into SQLite or sqlite-vec-backed memory systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can mutate a selected SQLite memory database when migration is requested, creating or replacing quantized embedding records. <br>
Mitigation: Use the skill only on databases intentionally selected for quantization, back up the database before running migration, and validate results on a non-production copy first. <br>
Risk: The validation workflow can load a native sqlite-vec extension from --vec-ext or SQLITE_VEC_PATH. <br>
Mitigation: Use only sqlite-vec libraries from trusted local paths and avoid loading unverified native extensions. <br>
Risk: Embedding contents, validation statistics, paths, and database details may be processed locally and exposed through terminal or log output. <br>
Mitigation: Avoid sensitive production memory stores unless local processing and possible terminal/log exposure are acceptable, and limit output files to controlled locations. <br>


## Reference(s): <br>
- [TurboQuant Algorithm Reference](references/algorithm.md) <br>
- [TurboQuant Paper](https://arxiv.org/abs/2504.19874) <br>
- [PolarQuant Paper](https://arxiv.org/abs/2502.02617) <br>
- [ClawHub Skill Page](https://clawhub.ai/sunnyztj/turboquant-memory) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python snippets, shell command examples, tables, and JSON-oriented validation output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with Python 3.9+ and numpy; optional SQLite and sqlite-vec workflows read embeddings and can write quantized tables when migration is requested.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
