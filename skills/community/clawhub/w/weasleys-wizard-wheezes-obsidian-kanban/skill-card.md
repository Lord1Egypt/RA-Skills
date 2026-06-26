## Description: <br>
Creates, normalizes, and reorganizes Obsidian Kanban plugin Markdown boards from ledgers, tables, checklists, audit notes, and issue lists while preserving content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[child2d](https://clawhub.ai/user/child2d) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and Obsidian users use this skill to convert ledgers, tables, review notes, and issue lists into readable Kanban boards. It also helps clean up existing Obsidian Kanban Markdown while preserving plugin structure and detailed source content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bulk board rewrites can unintentionally change or lose important Obsidian Kanban content. <br>
Mitigation: Limit use to the intended notes or vault folders, keep backups for bulk reorganizations, and review diffs before accepting large board rewrites. <br>
Risk: Changing plugin-recognized frontmatter or settings can prevent a board from parsing as an Obsidian Kanban board. <br>
Mitigation: Preserve the kanban-plugin marker and settings block unless the user explicitly asks to change board behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/child2d/weasleys-wizard-wheezes-obsidian-kanban) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, guidance] <br>
**Output Format:** [Obsidian Kanban plugin Markdown with task-list cards and nested detail bullets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Preserves frontmatter, Kanban settings blocks, columns, and full source details when requested.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
