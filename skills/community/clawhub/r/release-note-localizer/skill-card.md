## Description:

Release Note Localizer converts release notes into Chinese, English, customer-facing, and technical variants while keeping terminology consistent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[52yuanchangxing](https://clawhub.ai/user/52yuanchangxing)

### License/Terms of Use:

MIT-0

## Use Case:

Documentation, release, and localization teams use this skill to turn release-note input and terminology requirements into reviewable localized drafts, audience-specific variants, glossaries, and terms needing confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The support script may behave more like a restructuring and audit helper than a full localization engine.

Mitigation: Treat script output as a draft or report, then review terminology, tone, and completeness before relying on it.

Risk: Pointing the script at broad local directories may include unintended local file content in generated reports.

Mitigation: Run it only on intended, non-sensitive release-note inputs and redact sensitive material before processing.

Risk: Sensitive contracts or legal translation requests may require professional review beyond this skill's scope.

Mitigation: Use the skill for product and technical release-note drafts, and route legal or contract language to qualified translators or counsel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/52yuanchangxing/skills/release-note-localizer)
- [Skill specification](resources/spec.json)
- [Output template](resources/template.md)
- [Smoke test](tests/smoke-test.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Structured Markdown, with optional JSON output from the local helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are intended as reviewable drafts and checklists; users should confirm terminology and sensitive content before use.]

## Skill Version(s):

1.0.0 (source: release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
