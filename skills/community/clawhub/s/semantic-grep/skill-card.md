## Description:

Offline local semantic code search using embeddings to find and index code by meaning with llama.cpp, ONNX, or Ollama backends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rizperdana](https://clawhub.ai/user/rizperdana)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to index local codebases and run offline semantic searches by meaning. It helps locate related code using embeddings with local backend options.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documentation exposes a credential-like ClawHub token.

Mitigation: Do not reuse the embedded token; revoke it and require user-provided authentication before installation.

Risk: Installation commands fetch an unpinned remote package.

Mitigation: Install a pinned, reviewed semgrepll version with hashes from a trusted package source.

Risk: Indexing source code creates local cached embeddings of project content.

Mitigation: Avoid indexing sensitive code unless cache storage, access controls, and retention are understood.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rizperdana/skills/semantic-grep)
- [Publisher profile](https://clawhub.ai/user/rizperdana)
- [Artifact README](artifact/README.md)
- [Artifact skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and environment configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is oriented around local execution; indexing code creates cached embeddings of project content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
