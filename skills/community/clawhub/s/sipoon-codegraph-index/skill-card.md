## Description:

CodeGraph Index helps agents prebuild tree-sitter-based symbol, call, import, and structure indexes so they can answer codebase exploration questions with fewer broad file scans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sipoon](https://clawhub.ai/user/sipoon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and coding agents use this skill to index large repositories and quickly inspect symbols, call relationships, imports, structure summaries, and potential dead code before reading source files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger broad workspace indexing and create repository-local .tree-sitter artifacts.

Mitigation: Confirm the intended project scope before repository-wide indexing and add generated .tree-sitter artifacts to .gitignore when appropriate.

Risk: The artifact suggests a global, unpinned npm install of tree-sitter-cli.

Mitigation: Prefer a pinned project-local tree-sitter-cli install and avoid elevated shells.

Risk: Static call graph output can miss dynamic calls, reflection, or eval-style behavior.

Mitigation: Treat dead-code findings as review candidates and manually verify dynamic code paths before deleting or refactoring code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sipoon/skills/sipoon-codegraph-index)
- [Publisher profile](https://clawhub.ai/user/sipoon)
- [Artifact skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries with tables, command snippets, and structured codebase findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include symbol tables, call graphs, import relations, file-structure summaries, and dead-code candidates.]

## Skill Version(s):

0.1.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
