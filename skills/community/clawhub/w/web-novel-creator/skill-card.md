## Description:

Coordinates Chinese web-novel projects by standardizing project directories, archiving chapter outputs from compatible writing skills, and handing index updates to Memory Manager Pro.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guojiuben](https://clawhub.ai/user/guojiuben)

### License/Terms of Use:

MIT-0

## Use Case:

External writers and agent users use this skill after a web-novel writing skill has produced chapters to align outputs under one project, update title and planning artifacts, and request Memory Manager Pro indexing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chapter or planning files may be moved or renamed in the wrong project path.

Mitigation: Confirm the target novel project path and review proposed migrations before applying them to an existing workspace.

Risk: Persistent project indexes may be updated with incorrect chapter metadata.

Mitigation: Verify the chapter number, title, word count, project name, and source skill before requesting Memory Manager Pro index updates.

Risk: Other writing skills may depend on their original output layout.

Mitigation: Check the detected source skill and preserve non-indexed review or auxiliary outputs unless the user confirms a migration.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/guojiuben/skills/web-novel-creator)
- [README](README.md)
- [External Skill Integration Specification](references/对接规范.md)
- [Chapter Planning Template](references/规划模板.md)
- [Keyword Mapping Table](references/关键词映射.md)
- [Fanqie Novel Platform Guidelines](references/番茄小说规范.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown prose with file paths, templates, and command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or reorganize project directories, move chapter files, update planning and title-library files, and prepare Memory Manager Pro handoff requests.]

## Skill Version(s):

2.0.0 (source: release evidence and README changelog, released 2026-04-26)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
