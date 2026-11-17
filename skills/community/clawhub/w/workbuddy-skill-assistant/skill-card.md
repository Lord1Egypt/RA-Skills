## Description:

WorkBuddy skill-assistant helps users choose, install, invoke, combine, troubleshoot, and maintain WorkBuddy skills for real tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huyujie2017-tech](https://clawhub.ai/user/huyujie2017-tech)

### License/Terms of Use:

MIT-0

## Use Case:

WorkBuddy users and operators use this skill to select a minimal skill set, apply reusable trigger prompts and workflows, diagnose skill usage issues, and record verified practices. It is intended for skill management guidance rather than general task execution or independent skill quality auditing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect local WorkBuddy state and propose changes to skills, automations, connectors, reports, and memory.

Mitigation: Install only for WorkBuddy skill management and require explicit user confirmation before installs, upgrades, automation creation, memory writes, connector changes, or external file writes.

Risk: The package includes an investment morning-briefing workflow and finance-oriented references that may be outside the core skill-management purpose.

Mitigation: Review or remove the investment workflow and require separate approval for any financial-analysis workflow before use.

Risk: Templates for private notes, contacts, connectors, and automations could affect personal or workspace configuration if applied without review.

Mitigation: Treat templates as examples until a user approves the exact target, authorization scope, and validation step.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huyujie2017-tech/skills/workbuddy-skill-assistant)
- [Runtime reference index](references/README.md)
- [Execution workflow](references/execution.md)
- [Skill usage guide](references/skill-usage-guide.md)
- [Skill sources](references/skill-sources.md)
- [System scan reference](references/system-scan.md)
- [Morning briefing workflow](references/workflows/morning-briefing.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional commands, templates, checklists, and workflow recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local diagnostics, automation changes, connector changes, memory writes, or skill installs only after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports source version 6.8.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
