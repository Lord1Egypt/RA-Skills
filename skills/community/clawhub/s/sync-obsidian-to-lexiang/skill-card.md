## Description:

Synchronizes an Obsidian vault to a Tencent Lexiang knowledge base with one-way full or incremental sync for Markdown, images, folders, and standalone attachments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajaxhe](https://clawhub.ai/user/ajaxhe)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, knowledge managers, and teams that maintain notes in Obsidian use this skill to publish or refresh a matching Tencent Lexiang knowledge base while preserving folder structure, Markdown content, images, and attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authentication fallback could use an unintended Lexiang credential.

Mitigation: Prefer an explicit Lexiang profile or credential file and verify authentication before running a sync.

Risk: Untrusted symlinks or traversal-style attachment references could cause uploads from outside the intended vault boundary.

Mitigation: Use only trusted vaults, remove untrusted symlinks or traversal-style references, and run a dry-run before syncing.

Risk: A non-dry-run sync can publish content to the wrong Lexiang space or folder if target identifiers are incorrect.

Mitigation: Confirm the target Lexiang space and folder before any non-dry-run sync.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ajaxhe/skills/sync-obsidian-to-lexiang)
- [Conflict Strategy Reference](references/conflict-strategy.md)
- [upload-markdown-to-lexiang Dependency](https://github.com/ajaxhe/upload-markdown-to-lexiang)
- [Lexiang Personal Credentials](https://lexiangla.com/ai/claw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash command examples, plus JSON status summaries and report files from sync runs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may write manifest, progress, configuration, and report files under the Obsidian vault state directory.]

## Skill Version(s):

2.1.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
