## Description:

Vibe Coding Rules is a six-skill AI coding workflow that guides agents through pre-change checks, safe command execution, post-change self-review, automated web testing, changelog writing, and self-growing project rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ron-dali](https://clawhub.ai/user/ron-dali)

### License/Terms of Use:

Apache-2.0

## Use Case:

Developers, solo builders, small teams, and heavy AI-agent users use this skill to add a disciplined coding workflow around AI-assisted development, including pre-change reasoning, safer command execution, regression testing, and changelog discipline. It is especially aimed at projects that want agent-readable memory through breadcrumbs and self-growing quality rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist agent instructions and auto-grow blocking quality rules that influence future agent behavior.

Mitigation: Require review before accepting .ai-pipeline changes, breadcrumb/file-header edits, changelog writes, and .codebuddy memory updates.

Risk: The workflow allows broad file and package operations, including commands such as rm, git push, npm, and npx.

Mitigation: Use it only in intended repositories, require explicit review for destructive or publishing commands, and pin package versions where practical.

Risk: Optional share-contact settings can expose contact details if populated.

Mitigation: Keep shareContact.phone empty unless the user intentionally wants the contact information published.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/ron-dali/skills/vibe-coding-rules)
- [Project Website](https://tangbuping.com)
- [Vibe Coding Rules Repository](https://github.com/Ron-dali/vibe-coding-rules)
- [Complete Self-Check Rules](self-check/references/self-check-full.md)
- [Growth Detection Rule Definitions](changelog/references/growth-rules.md)
- [Project Initialization Dialog](pipeline-init/references/init-dialog.md)
- [Technical Stack Dependency Checklist](pipeline-init/references/tech-stack-checklist.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands, generated code snippets, configuration files, changelog entries, and test reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update project-local pipeline files, agent memory, file-header breadcrumbs, changelogs, and automated test scripts when the user enables those workflows.]

## Skill Version(s):

2.5.3 (source: server release metadata; artifact frontmatter reports 2.5.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
