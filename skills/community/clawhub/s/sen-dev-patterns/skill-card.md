## Description:

Sen Dev Patterns helps agents reuse a personal development library of UI styles, coding standards, algorithms, module templates, performance guidance, Git workflow notes, and pitfalls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[the13ai](https://clawhub.ai/user/the13ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to apply a reusable set of personal development conventions, UI patterns, algorithm recipes, module templates, and troubleshooting notes when building Python desktop, web, and data-processing tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bundled publishing scripts may use repository credentials, create public repositories, push local code, and persist access tokens in Git remotes.

Mitigation: Review the scripts before execution, avoid running publish_skill.py or publish_gitee.py unless publishing is intended, inspect git remote URLs after use, and rotate any exposed GitHub or Gitee tokens.

Risk: The skill is a personal pattern library, so its coding conventions, formulas, and UI styles may not match every project's requirements.

Mitigation: Treat generated guidance and snippets as project-specific recommendations and review them against local engineering, security, and product requirements before applying changes.

## Reference(s):

- [Algorithm Library](references/algorithm-library.md)
- [Code Modules](references/code-modules.md)
- [Coding Standards](references/coding-standards.md)
- [Development Context](references/development-context.md)
- [Evaluation Report](references/evaluation-report.md)
- [Git Workflow](references/git-workflow.md)
- [Icon Library](references/icon-library.md)
- [Performance Guide](references/performance-guide.md)
- [Pitfalls Record](references/pitfalls-record.md)
- [UI Style Guide](references/ui-style-guide.md)
- [Web Guide](references/web-guide.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include reusable snippets, module skeleton guidance, formulas, UI styling recommendations, and development workflow advice.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata; artifact declares 1.3.0 in SKILL.md and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
