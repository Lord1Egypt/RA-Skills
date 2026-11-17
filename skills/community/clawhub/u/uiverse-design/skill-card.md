## Description:

UI component design learning library with 165 curated CSS/Tailwind components from Uiverse Galaxy for finding, studying, and adapting component examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cmyang-it](https://clawhub.ai/user/cmyang-it)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and design-focused agents use this skill to search curated UI component examples and extract CSS, Tailwind, layout, animation, color, and interaction patterns for web interfaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional setup script can replace reviewed local component examples with unverified content downloaded from GitHub.

Mitigation: Use the bundled curated examples by default; run scripts/setup.sh only after trusting the current upstream repository and accepting that reviewed local assets will be replaced.

Risk: Copied UI snippets may be inappropriate for sensitive workflows such as login, payment, upload, or externally linked components.

Mitigation: Review copied components before production use, especially for authentication, payment, upload, or external-link behavior.

## Reference(s):

- [UI Design Patterns Reference](references/patterns.md)
- [Uiverse](https://uiverse.io/)
- [ClawHub skill page](https://clawhub.ai/cmyang-it/skills/uiverse-design)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with component paths, search results, and CSS/Tailwind/HTML snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local curated HTML component files and optional shell commands for searching or setup.]

## Skill Version(s):

2.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
