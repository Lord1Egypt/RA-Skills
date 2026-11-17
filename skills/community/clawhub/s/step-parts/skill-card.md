## Description:

Find, evaluate, and download purchasable CAD part STEP files from step.parts, including off-the-shelf actuators, electronics, connectors, hardware, bearings, and other catalog components.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liubuq-sys](https://clawhub.ai/user/liubuq-sys)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to search step.parts for standard and off-the-shelf CAD components, compare candidate records, download canonical STEP files, and report part IDs, file paths, checksums, and source URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader can write downloaded STEP files outside the intended output folder in some user-directed cases.

Mitigation: Use trusted output directories, do not pass path components to --filename, avoid --overwrite except for intentional replacement, and verify checksums before treating downloaded CAD files as trusted.

Risk: A custom step.parts-compatible origin can serve unexpected or untrusted CAD data.

Mitigation: Use the default step.parts origin when possible and only use custom mirrors that the user trusts.

## Reference(s):

- [step.parts API Reference](references/step-parts-api.md)
- [step.parts API](https://api.step.parts)
- [step.parts Agent Guide](https://www.step.parts/llms.txt)
- [ClawHub Skill Page](https://clawhub.ai/liubuq-sys/skills/step-parts)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, files, guidance]

**Output Format:** [Markdown guidance, shell commands, JSON records, and STEP files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Downloader output can include selected part details, saved file paths, source URLs, SHA-256 values, and checksum status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
