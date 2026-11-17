## Description:

A complete Chinese novel writing studio with 15 specialized AI agents covering the full creative workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weihfei](https://clawhub.ai/user/weihfei)

### License/Terms of Use:

MIT-0

## Use Case:

External writers and creative teams use Novel Studio to plan, draft, revise, and manage continuity for Chinese web novels, including market positioning, worldbuilding, character design, outlining, chapter drafting, editing, platform compliance, and genre-specific support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read and update project-configured files with broad file access.

Mitigation: Install it only in a dedicated novel project workspace and keep configured paths relative and inside that workspace.

Risk: Untrusted project.md files can steer which files the agents read or update.

Mitigation: Use only trusted project.md files and review intended file creations or updates before allowing the skill to proceed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weihfei/skills/weihefei-novel-studio)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown documents, structured checklists, and project file updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update novel project files when file write access is enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
