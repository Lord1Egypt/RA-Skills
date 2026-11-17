## Description:

Publish content to saved.md and return a public shareable URL for Markdown, HTML, or JSX pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anboias](https://clawhub.ai/user/anboias)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to create, validate, and publish shareable saved.md pages from Markdown, HTML, or JSX content. It supports quick one-shot publishing, scaffolded page generation, existing-page remixing, and markdown enhancement with supported chart widgets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Publishing may expose sensitive, confidential, personal, or third-party material at a public saved.md URL.

Mitigation: Review and redact content before publishing, and use the skill only when public sharing is intended.

Risk: Deletion phrases may be stored in a local plaintext entries.json log.

Mitigation: Disable or modify deletion-phrase logging before use, and avoid committing or sharing entries.json.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anboias/skills/saved-markdown)
- [saved.md](https://saved.md)
- [saved.md page API](https://saved.md/api/pages)
- [Template index](templates/INDEX.md)
- [Validation guide](templates/validation.md)
- [Chart guide](templates/charts.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, HTML, JSX, API payload guidance, and public saved.md URLs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Published pages are immutable; edits are performed by fetching source, applying changes, and publishing a new page.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
