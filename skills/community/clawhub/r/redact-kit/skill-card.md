## Description:

Scan your data before sending it to AI. Detect and redact PII, secrets, and sensitive info. Reversible, local, zero network calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[theshadowrose](https://clawhub.ai/user/theshadowrose)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users use this skill to redact sensitive text, files, logs, and code before sharing them with AI tools or other third parties, then optionally restore originals from a local mapping file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext mapping files can restore redacted sensitive values if exposed.

Mitigation: Store mappings outside shared, synced, or source-controlled folders; restrict file permissions and encrypt the files or containing volume.

Risk: Verified redaction bugs can leave phone numbers and standalone tokens exposed.

Mitigation: Review redacted output before sharing, add custom patterns for expected formats, and do not treat this release as a complete privacy scrubber.

Risk: Report mode can print sensitive matches into terminal or job logs.

Mitigation: Avoid report mode in logged environments or run it only where console output is protected.

Risk: Regex-based, text-only detection can miss obfuscated, non-standard, encoded, image, audio, video, or PDF-only sensitive data.

Mitigation: Extract and normalize text before scanning, audit outputs, and use specialized tools for regulated or high-assurance redaction workflows.

## Reference(s):

- [RedactKit Skill Page](https://clawhub.ai/theshadowrose/skills/redact-kit)
- [RedactKit README](artifact/README.md)
- [RedactKit Limitations](artifact/LIMITATIONS.md)

## Skill Output:

**Output Type(s):** [Text, Files, JSON, Shell commands, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell command examples; redacted text or files, report text, and JSON restoration mappings when the tool is run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local processing only; reversible redaction depends on preserving the generated mapping file.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
