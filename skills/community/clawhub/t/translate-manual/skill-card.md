## Description:

Translate DOCX manuals into target languages while preserving document structure; screenshot replacement is described as planned rather than implemented in this version.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qianzitech](https://clawhub.ai/user/qianzitech)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, document owners, and localization reviewers use this skill to translate DOCX product manuals into target languages while preserving paragraphs, tables, image placeholders, and overall structure for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Document text may be sent to the hardcoded api.deeplx.org translation service.

Mitigation: Use only documents whose contents are approved for that external service, especially when manuals contain confidential or customer information.

Risk: Supplying API keys through command-line arguments can expose credentials in process history or logs.

Mitigation: Prefer the documented environment variables or a secret manager for API keys.

Risk: Screenshot replacement is described by the skill but is not actually implemented in this version.

Mitigation: Treat translated DOCX output as requiring manual screenshot review and replacement before release.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qianzitech/skills/translate-manual)
- [DeepLX translation API endpoint](https://api.deeplx.org/{API_KEY}/translate)

## Skill Output:

**Output Type(s):** [text, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell command examples, and translated DOCX file outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a target language and source DOCX path; API key may be supplied by environment variable or command-line argument.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
