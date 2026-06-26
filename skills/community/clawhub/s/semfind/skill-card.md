## Description: <br>
Semantic search over local text files using embeddings for cases where grep or ripgrep cannot find relevant results because the exact wording is unknown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PaperBoardOfficial](https://clawhub.ai/user/PaperBoardOfficial) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and other technical users use semfind to search local docs, logs, code, memory files, and notes by meaning when exact-text search is ineffective. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow depends on installing the semfind Python package and downloading a local embedding model. <br>
Mitigation: Install only when you trust the package and downloaded model used in your environment. <br>
Risk: Embedding caches may retain derived information from searched local files. <br>
Mitigation: Use narrow file paths for sensitive content, run with --no-cache when appropriate, and clear ~/.cache/semfind/ when cached embeddings should not persist. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash commands and grep-like text output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results include local file paths, line numbers, matched text, and similarity scores.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
