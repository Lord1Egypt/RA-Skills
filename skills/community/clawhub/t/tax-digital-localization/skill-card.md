## Description:

Localizes Chinese in-product copy for tax, invoicing, filing, and compliance systems into market-appropriate UI text for Vietnam, Malaysia, Singapore, Poland, Italy, and Germany.

This skill is ready for commercial/non-commercial use.

## Publisher:

[munich949](https://clawhub.ai/user/munich949)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and localization reviewers use this skill to translate Chinese UI labels, buttons, messages, and tax or invoice terms into deployment-ready product copy for six target markets while preserving keys, placeholders, markup, and structural formatting.

### Deployment Geography for Use:

Global, with localization guidance for Vietnam, Malaysia, Singapore, Poland, Italy, and Germany.

## Known Risks and Mitigations:

Risk: Tax, invoice, and compliance terminology can have jurisdiction-specific meanings that may not be fully determined from UI copy alone.

Mitigation: Review high-risk localized terms against product context and local requirements before release.

Risk: Ambiguous or missing country and language targets can produce unsuitable localization, especially for multilingual markets.

Mitigation: Confirm the intended target country and language before using the output in a product.

Risk: Translated strings may become too long or awkward when placeholders or UI constraints limit word order.

Mitigation: Check generated strings in the target interface while preserving placeholders, keys, and markup exactly.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/munich949/skills/tax-digital-localization)
- [UI Patterns](references/ui-patterns.md)
- [Tax Terms](references/tax-terms.md)
- [Vietnam Locale](references/locales/vietnam.md)
- [Malaysia Locale](references/locales/malaysia.md)
- [Singapore Locale](references/locales/singapore.md)
- [Poland Locale](references/locales/poland.md)
- [Italy Locale](references/locales/italy.md)
- [Germany Locale](references/locales/germany.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text or Markdown preserving the user's input structure; final translation only, with an optional note for ambiguity or semantic risk.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves code keys, placeholders, ICU placeholders, markup, numeric/date/currency tokens, line breaks, and list or key-value structure.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
