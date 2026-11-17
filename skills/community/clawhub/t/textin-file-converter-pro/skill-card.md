## Description:

Convert documents between PDF, Word, Excel, PPT, and image formats using the Textin API with OCR-based layout preservation for single-file and batch folder workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[intsig-textin](https://clawhub.ai/user/intsig-textin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert user-specified documents, images, folders, or supported source URLs into office, PDF, image archive, or OCR-restored Word outputs through Textin's cloud conversion API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uploads selected documents, image contents, source URLs, and Textin API credentials to Textin for server-side processing.

Mitigation: Use only with files your organization permits sending to Textin, and avoid confidential or regulated documents unless that transfer is approved.

Risk: The security evidence reports automatic redirect following despite the skill describing a single fixed destination.

Mitigation: Review outbound requests before use and prefer a version that removes automatic redirect following or enforces same-origin HTTPS redirects.

Risk: Single-file conversion can overwrite the requested output path if the caller chooses an existing file.

Mitigation: Choose a new output path or confirm the path is unused before running single-file conversion.

## Reference(s):

- [Textin PDF to Word API Documentation](https://www.textin.com/document/pdf-to-word)
- [Textin API Key Documentation](https://docs.textin.com/xparse/api-key)
- [Textin Conversion Pricing and Specifications](https://www.textin.com/product/textin_conversion#Specifications)
- [Textin xParse Product](https://www.textin.com/market/detail/xparse)
- [Textin xParse API Reference](https://docs.textin.com/api-reference/endpoint/xparse/v1/parse-sync)
- [Textin Privacy Policy](https://www.textin.com/privacy)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown with inline bash commands and generated file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces converted document files and reports output paths, file sizes, batch counts, and failed conversions when applicable.]

## Skill Version(s):

1.0.2 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
