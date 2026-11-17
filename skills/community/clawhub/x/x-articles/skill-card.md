## Description:

Creates and publishes X (Twitter) Articles with AI-assisted long-form formatting, viral hook patterns, and browser automation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nextfrontierbuilds](https://clawhub.ai/user/nextfrontierbuilds)

### License/Terms of Use:


## Use Case:

External creators, marketers, and developers use this skill to draft, format, review, and publish long-form X Articles with platform-specific formatting guidance and optional browser-assisted publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate against a logged-in X browser session and may reach publishing controls.

Mitigation: Use a dedicated browser profile or test account, keep the session scoped to X, and require human review before any publish action.

Risk: Formatted output may alter source article structure while converting markdown into X-friendly plain text.

Mitigation: Keep backups of source articles and compare the generated X-ready text before loading it into the editor.

Risk: The provided security verdict is suspicious because final human approval is not consistently enforced by the skill materials.

Mitigation: Treat browser automation commands as proposals unless a human explicitly approves the final publish step.

## Reference(s):

- [Viral X Article Patterns](references/viral-patterns.md)
- [X Article Editor](https://x.com/compose/article)
- [ClawHub Skill Page](https://clawhub.ai/nextfrontierbuilds/skills/x-articles)
- [Publisher Profile](https://clawhub.ai/user/nextfrontierbuilds)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with plain-text article drafts and bash command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce X-ready plain-text files and browser automation commands that require user review before publishing.]

## Skill Version(s):

1.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
