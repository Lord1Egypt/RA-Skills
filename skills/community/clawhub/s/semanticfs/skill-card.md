## Description:

SemanticFS helps agents search a local filesystem or codebase semantically and return exact file paths, line ranges, and snippets for relevant files, functions, symbols, or code patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[navneeth08k](https://clawhub.ai/user/navneeth08k)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to navigate unfamiliar repositories, find implementation details, and replace manual grep/find/ls/cat exploration with semantic search over an indexed workspace.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The install instructions pipe a mutable GitHub-hosted script directly into Bash.

Mitigation: Review the installer before running it and prefer a pinned release or checksum-verified installer.

Risk: The skill relies on local workspace indexing and a local search server.

Mitigation: Index only workspaces intended to be searchable and start the local server only when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/navneeth08k/skills/semanticfs)
- [SemanticFS project homepage](https://github.com/Navneeth08k/semanticFS)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search guidance expects the semanticfs binary, an indexed target directory, and a local SemanticFS server when using HTTP search examples.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
