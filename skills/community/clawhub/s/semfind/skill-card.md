## Description:

Semantic search over local text files using embeddings for cases where grep or ripgrep cannot find relevant results because the exact wording is unknown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paperboardofficial](https://clawhub.ai/user/paperboardofficial)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to search local logs, project documentation, notes, memory files, and code-adjacent text by semantic meaning when exact keyword search is insufficient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The semfind package and local embedding model are installed and run in the user's environment.

Mitigation: Install in a virtual environment, avoid sudo pip install, and pin or review the semfind package version when strict supply-chain control is required.

Risk: Embeddings for selected local files may be retained in the semfind cache between runs.

Mitigation: Use --no-cache or clear ~/.cache/semfind/ when cached embeddings of local files should not be retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paperboardofficial/skills/semfind)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and grep-like result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs semfind command guidance and result lines with similarity scores.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
