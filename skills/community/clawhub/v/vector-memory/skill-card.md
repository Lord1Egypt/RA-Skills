## Description:

Smart memory search with automatic vector fallback. Uses semantic embeddings when available, falls back to built-in search otherwise. Zero configuration - works immediately after ClawHub install. No setup required - just install and memory_search works immediately, gets better after optional sync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluepointdigital](https://clawhub.ai/user/bluepointdigital)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to search local memory files through a smart wrapper that uses semantic vector search after sync and keyword fallback before sync or when vector search fails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports unsafe command execution that could run unintended commands.

Mitigation: Review and fix command construction before installing or using the skill in a workspace with secrets or sensitive files.

Risk: The security evidence reports file-reading flaws that could expose local files.

Mitigation: Restrict memory file access to the intended workspace paths and review path handling before deployment.

Risk: The security guidance advises against installing through a curl-to-shell path.

Mitigation: Install only from a trusted, pinned ClawHub release or reviewed source archive.

## Reference(s):

- [Integration Guide](artifact/vector-memory/references/integration.md)
- [pgvector Version](artifact/vector-memory/references/pgvector.md)
- [ClawHub skill page](https://clawhub.ai/bluepointdigital/skills/vector-memory)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [JSON search results, Markdown guidance, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search output includes matching file paths, line ranges, scores, and snippets.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
