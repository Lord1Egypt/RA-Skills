## Description:

Translate documents and text between multiple languages with support for glossaries, translation memory, and common office file formats via the Xdoc Translation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangsongbai1](https://clawhub.ai/user/yangsongbai1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and localization teams use this skill to translate documents or text through Xdoc's cloud API, including workflows that use glossaries or translation memory for consistent terminology.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents or text are sent to Xdoc's cloud translation service.

Mitigation: Use the skill only when Xdoc's privacy, retention, and data-handling terms are acceptable for the content being translated.

Risk: The Xdoc API key could expose account access or usage quota if logged or shared.

Mitigation: Store XDOC_API_KEY as a secret, avoid including it in logs or shared files, and rotate or revoke it if exposure is suspected.

Risk: Glossaries and translation memories may retain reusable terminology or translated content.

Mitigation: Review stored glossary and memory entries, remove outdated or sensitive content, and avoid uploading highly sensitive material without approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yangsongbai1/skills/xdoc-translationx)
- [Xdoc Translation API portal](https://translation.x-doc.ai/)
- [Xdoc website](https://x-doc.ai)
- [Xdoc privacy policy](https://x-doc.ai/privacy)

## Skill Output:

**Output Type(s):** [Text, Markdown, API Calls, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON and HTTP request examples, text translation results, and document download links when translations complete.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XDOC_API_KEY for authenticated HTTPS requests; document translation may upload files to Xdoc's cloud service.]

## Skill Version(s):

1.0.0 (source: server release metadata, artifact manifest, skill.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
