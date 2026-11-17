## Description:

Fast local PDF parsing with PyMuPDF (fitz) for Markdown/JSON outputs and optional images/tables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to parse local PDF files quickly into Markdown or JSON, with optional embedded image extraction and rough table output. It is best suited for fast text extraction when layout fidelity is less important than speed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Parsed PDF content is written to local Markdown, JSON, image, or table files and may contain sensitive source-document text.

Mitigation: Use a fresh private output directory, treat generated files as copies of the original document contents, and avoid transmitting parsed output to external services.

Risk: Batch or recursive parsing can expose many documents as cleartext on disk.

Mitigation: Confirm the intended file set before batch processing and review whether the target directory may contain sensitive documents.

Risk: Unpinned parser dependencies or elevated execution privileges can increase host risk during local parsing.

Mitigation: Install in a dedicated virtual environment, pin and review the PyMuPDF version, and run as a non-privileged user.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/snazar-faberlens/skills/pymupdf-pdf-parser-clawdbot-skill-hardened)
- [PyMuPDF Documentation](https://pymupdf.readthedocs.io/)
- [Clawdbot](https://github.com/clawdbot/clawdbot)
- [PyMuPDF Notes](references/pymupdf-notes.md)
- [Faberlens Safety Evaluation](https://faberlens.ai/explore/pymupdf-pdf-parser-clawdbot-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON files, optional PNG images, optional table JSON, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a per-document output directory containing output.md, output.json when requested, optional images/, and optional tables.json.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
