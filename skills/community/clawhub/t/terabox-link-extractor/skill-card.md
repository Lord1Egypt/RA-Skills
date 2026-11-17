## Description:

Direct link extraction from TeraBox URLs using the XAPIverse protocol. Extracts high-speed download and stream links for all resolutions without browser session requirements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abdul-karim-mia](https://clawhub.ai/user/abdul-karim-mia)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to extract direct download and stream links from user-provided TeraBox URLs after explicit consent. It requires Node.js and a TERABOX_API_KEY for the XAPIverse service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the full TeraBox URL and TERABOX_API_KEY to xapiverse.com.

Mitigation: Ask for explicit user consent before extraction and use only non-sensitive links unless the user accepts third-party processing.

Risk: Security evidence warns that download mode can write untrusted remote files outside the intended folder.

Mitigation: Avoid CLI --download mode until output-path containment, filenames, allowed download hosts, redirect limits, and size/time limits are fixed.

Risk: Security evidence rates the release suspicious because third-party data sharing is inconsistently disclosed.

Mitigation: Disclose xapiverse.com processing and API-key use before running the extractor.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abdul-karim-mia/skills/terabox-link-extractor)
- [TeraBox API Reference](references/api-reference.md)
- [Skill changelog](references/changelog.md)
- [XAPIverse TeraBox Pro API](https://xapiverse.com/apis/terabox-pro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text report with extracted file metadata, stream links, download links, and remaining credits; CLI mode can also emit JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TERABOX_API_KEY and sends the target URL to xapiverse.com for processing.]

## Skill Version(s):

1.4.0 (source: server release, package.json, _meta.json, references/changelog.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
