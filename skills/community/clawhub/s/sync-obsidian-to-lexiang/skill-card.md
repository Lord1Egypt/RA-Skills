## Description: <br>
Syncs an Obsidian vault one way to a Tencent Lexiang knowledge base, including directory structure, Markdown notes, images, and attachments, with full and incremental modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ajaxhe](https://clawhub.ai/user/ajaxhe) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, external users, and developers who maintain notes in Obsidian use this skill to preview and run a one-way sync into Tencent Lexiang knowledge bases while preserving folders, Markdown content, images, and attachments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reuses an existing local Lexiang connector OAuth token. <br>
Mitigation: Install it only in the intended agent profile and trust boundary, and avoid using it on machines where connector tokens belong to another user or workspace. <br>
Risk: The skill can upload selected Obsidian notes and attachments to Tencent Lexiang. <br>
Mitigation: Run dry-run first, limit the vault or source directories, verify the target space and folder, and review the generated report after sync. <br>


## Reference(s): <br>
- [Conflict Strategy](references/conflict-strategy.md) <br>
- [Obsidian](https://obsidian.md/) <br>
- [Tencent Lexiang](https://lexiangla.com/) <br>
- [ClawHub Skill Page](https://clawhub.ai/ajaxhe/skills/sync-obsidian-to-lexiang) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; sync execution returns a JSON summary and a Markdown report path.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill can create local sync configuration, manifest, lock, and report files inside the selected Obsidian vault.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
