## Description: <br>
Obsidian vault management skill that uses obsidian-cli to help agents manage local Markdown notes, including multi-vault switching, safe note moves and renames, attachment cleanup, and cross-vault search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, knowledge workers, and agent operators use this skill to manage Obsidian vaults as local Markdown knowledge bases. It supports vault discovery and switching, link-preserving note reorganization, attachment governance, cross-vault search, and cleanup workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can modify, move, rename, or delete local Obsidian notes and attachments. <br>
Mitigation: Preview affected paths, keep a backup or Git history, and require explicit confirmation before any real deletion or orphan cleanup. <br>
Risk: Operations can affect the wrong vault if the active Obsidian vault is not confirmed first. <br>
Mitigation: Confirm the selected vault with obsidian-cli print-default --path-only or an explicit vault path before running move, rename, cleanup, or batch operations. <br>
Risk: Concurrent edits can cause conflicts or leave references stale during bulk restructuring. <br>
Mitigation: Check for active editors before large moves or renames, record original and target paths, and verify links with search after restructuring. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/vault-master-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, checklists, and file path summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include local vault paths, dry-run summaries, and cleanup reports; real deletion should require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
