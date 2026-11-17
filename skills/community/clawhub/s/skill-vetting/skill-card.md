## Description:

Vet ClawHub skills for security and utility before installation. Use when considering installing a ClawHub skill, evaluating third-party code, or assessing whether a skill adds value over existing tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eddygk](https://clawhub.ai/user/eddygk)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to vet ClawHub skills before installation by combining a local regex scanner with manual review guidance for security, prompt-injection, and utility concerns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner can over-direct agents toward automatic rejection based on scanner results.

Mitigation: Treat scanner output as advisory and require contextual review before making installation or rejection decisions, except where organizational policy explicitly requires rejection.

Risk: Archive inspection can expose the workspace to unsafe or unexpected files if ZIP contents are trusted before extraction.

Mitigation: Use a private temporary directory, validate archive contents before extraction, and keep reviewed skill files outside active workspaces.

Risk: Regex scanning can miss semantic prompt injection, delayed behavior, context-aware logic, and obfuscation split across files.

Mitigation: Combine automated scanning with manual code review and monitor installed skills for unexpected network or file activity.

## Reference(s):

- [Skill Vetting ClawHub Page](https://clawhub.ai/eddygk/skills/skill-vetting)
- [Prompt-Injection-Resistant Security Review Architecture](artifact/ARCHITECTURE.md)
- [Malicious Code Patterns Database](artifact/references/patterns.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with bash examples and optional scanner text or JSON output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scanner findings are advisory and should be reviewed in context.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
