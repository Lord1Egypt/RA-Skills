## Description:

Extracts, normalizes, and deduplicates candidate indicators of compromise from existing reports, logs, and other text, with text, JSON, CSV, and STIX-lite output options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yottameta](https://clawhub.ai/user/yottameta)

### License/Terms of Use:

MIT-0

## Use Case:

Security analysts and developers can extract and normalize candidate indicators from existing threat reports, phishing messages, and logs for review or sharing. The skill processes local text and does not verify indicator reputation or scan systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hostile report text can become active spreadsheet formulas in CSV exports.

Mitigation: Prefer JSON for untrusted reports. If CSV is needed, import cells as text and disable formula interpretation until formula protection is added.

Risk: Output snippets and URLs may contain credentials or live indicators that should not be shared as-is.

Mitigation: Review snippets and embedded URL credentials before sharing, and use defanged indicators to reduce accidental activation.

Risk: Extracted indicators are candidates and do not establish that an indicator is malicious.

Mitigation: Verify indicators with authorized, trusted sources before drawing conclusions or taking action.

Risk: An installer may use an unintended release or destination if invoked with the wrong selection.

Mitigation: Use an exact reviewed installer version and select the intended destination.

## Reference(s):

- [Project homepage](https://github.com/YottaMeta/yotta-intel)
- [ClawHub skill page](https://clawhub.ai/yottameta/skills/yotta-intel)
- [IOC specification](references/ioc-spec.md)
- [Defang rules](references/defang-rules.md)
- [STIX-lite specification](references/stix-lite-spec.md)

## Skill Output:

**Output Type(s):** [Text, JSON, CSV, STIX 2.1 Bundle]

**Output Format:** [Plain text, JSON, CSV, or STIX-lite JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normalized and deduplicated candidate indicators with counts, first-seen line numbers, context snippets, and defanged forms.]

## Skill Version(s):

0.2.4 (source: frontmatter, CHANGELOG.md, package.json; released 2026-11-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
