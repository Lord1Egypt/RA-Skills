## Description: <br>
Work with Obsidian-style Markdown vaults and local knowledge bases to organize notes, add frontmatter, repair links, design vault workflows, create templates, migrate Markdown, and automate safe local note maintenance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kyro-ma](https://clawhub.ai/user/kyro-ma) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agent users, skill authors, maintainers, and teams use this skill to plan safe organization, metadata cleanup, link repair, template creation, and migration workflows for local Obsidian-style Markdown vaults. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger metadata may activate the skill for unrelated work or general note-management requests. <br>
Mitigation: Invoke the skill explicitly by name and use it only for Obsidian or Markdown-vault tasks. <br>
Risk: Bulk edits to local notes can damage frontmatter, links, embeds, attachments, or existing formatting. <br>
Mitigation: Require a dry-run, patch plan, backup, or rollback path before any bulk vault changes. <br>
Risk: Personal notes may contain sensitive content. <br>
Mitigation: Limit the skill to a specific vault path, define folders it must not edit, and summarize structure without exposing private note text unnecessarily. <br>
Risk: Generated scripts or shell commands may change local files. <br>
Mitigation: Review commands before execution and validate changed notes by checking unresolved wiki links, duplicate tags, malformed frontmatter, and attachment references. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/work-productivity-obsidian-vaults-workflow-helper) <br>
- [Requirement Plan](artifact/references/requirement-plan.md) <br>
- [Popular ClawHub Skill Demand: Obsidian](https://clawhub.ai/skills/obsidian) <br>
- [Markdown Workflow Demand Signal](https://news.ycombinator.com/item?id=48601134) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with optional templates, checklists, patch plans, scripts, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should separate read-only analysis from file-changing steps and prefer dry-run or reversible plans for bulk vault changes.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
