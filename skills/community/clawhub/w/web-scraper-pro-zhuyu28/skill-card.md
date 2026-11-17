## Description:

Browser automation skill for web interaction and data extraction. Enhanced version by zhuyu28.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhuyu28](https://clawhub.ai/user/zhuyu28)

### License/Terms of Use:


## Use Case:

Developers and automation users can use this skill for web scraping, data extraction, automated form filling, UI testing, and browser-based workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Form-filling workflows can expose submitted data through command arguments or output.

Mitigation: Avoid passwords, tokens, personal data, payment information, and authenticated workflows unless the skill is revised to redact form values and avoid command-line secret handling.

Risk: The package lacks documented safety controls for state-changing browser actions.

Mitigation: Review the skill before installing and require explicit confirmation before actions that submit forms or change remote state.

## Reference(s):

- [Web Scraper Pro Usage Guide](references/scraper_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional JSON examples and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce scraping or form-filling guidance that should be reviewed before use with sensitive or authenticated workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
