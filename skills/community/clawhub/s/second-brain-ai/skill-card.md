## Description:

Read, capture, search, relate, and assemble context from a user-specified local Markdown knowledge base (Obsidian/Logseq style). Supports controlled write operations with explicit approval and attribution. Use when the user wants a Second Brain / note-vault memory layer for Markdown notes, including saving ideas, searching past notes, finding related notes or backlinks, building context packs, appending to existing notes (with attribution), or getting smart link suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to maintain a local Markdown note vault: capturing notes, searching prior notes, finding related material, assembling context packs, and appending attributed updates after explicit write approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security summary reports that the vault boundary can be bypassed through symbolic links, which could expose or modify files outside the chosen vault.

Mitigation: Install only for vaults you control, avoid symbolic links inside the configured vault, and use write operations cautiously until realpath containment is enforced before every read and write.

Risk: Write tools can create or append Markdown files in the configured vault when approved.

Mitigation: Use a dedicated vault path, require explicit allow_write approval for each write action, and review proposed note content and append attribution before execution.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/second-brain-ai)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, files, configuration, guidance]

**Output Format:** [JSON command results and Markdown note content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SECOND_BRAIN_VAULT for a local Markdown vault; write operations require explicit allow_write approval and append attribution.]

## Skill Version(s):

2.3.3 (source: skill frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
