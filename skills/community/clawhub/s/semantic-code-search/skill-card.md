## Description:

Semantic search engine for codebases that understands intent and finds functionally similar code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[evezart](https://clawhub.ai/user/evezart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to search codebases by intent, find functionally similar implementations, discover duplicate logic, and navigate unfamiliar code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Indexing can persist raw source snippets and docstrings locally in .code_index.json.

Mitigation: Treat generated indexes as sensitive project artifacts and do not commit or share them until their contents are reviewed.

Risk: Directory traversal during indexing can follow symlinks outside the intended project.

Mitigation: Run the skill only on trusted directories and inspect or constrain symlinks before indexing private or untrusted repositories.

## Reference(s):

- [Semantic Code Search on ClawHub](https://clawhub.ai/evezart/skills/semantic-code-search)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or describe a local code index containing source snippets, docstrings, file paths, line numbers, and similarity scores.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
