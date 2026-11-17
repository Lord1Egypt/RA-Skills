## Description:

Generates a Chinese-language, browser-openable travel app checklist for a destination, with categorized recommendations, iOS App Store and Android Google Play links, platform switching, category filters, and search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lmercy](https://clawhub.ai/user/lmercy)

### License/Terms of Use:

MIT-0

## Use Case:

Chinese-speaking travelers use this skill to generate a destination-specific app toolkit before international trips. The agent collects destination, travel style, platform, and payment preferences, then produces an interactive local HTML page with app recommendations and store links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated HTML can include unescaped destination, app, or tip text, which may run unwanted script or present misleading links.

Mitigation: Avoid untrusted or adversarial destination and app text; inspect generated HTML and download links before opening or sharing; add text escaping and URL validation before broad deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lmercy/skills/travel-app-toolkit)
- [Skill instructions](artifact/SKILL.md)
- [App database](artifact/app-database.json)
- [HTML template](artifact/template.html)

## Skill Output:

**Output Type(s):** [code, files, guidance]

**Output Format:** [Single-file HTML with embedded CSS and JavaScript]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes platform tabs, category filters, search, priority labels, download links, and usage tips.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
