## Description:

This skill should be used when the user asks to "analyze source code", "understand this codebase", "perform code analysis", "study this project", "explain this repository", or discusses source code learning, codebase comprehension, open source project analysis, understanding software architecture, or learning from existing code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[river-zhanglh](https://clawhub.ai/user/river-zhanglh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, technical leads, contributors, and software engineering students use this skill to understand unfamiliar source repositories, analyze architecture and core pathways, and create structured codebase analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages running unfamiliar code during analysis, which can expose users to unsafe build, test, install, or startup behavior.

Mitigation: Use the skill only with trusted code or inside an isolated sandbox, and inspect build, test, install, and startup commands before running them.

Risk: Using the skill on third-party repositories without review can lead an agent to follow unsafe repository-specific instructions or commands.

Mitigation: Review the skill before installing it and apply repository analysis steps selectively when working with untrusted projects.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/river-zhanglh/skills/source-code-analysis)
- [Publisher Profile](https://clawhub.ai/user/river-zhanglh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Markdown analysis reports with structured sections, file references, execution-flow notes, and learning recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prioritized reading lists, code pathway traces, and suggested commands for validating understanding.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
