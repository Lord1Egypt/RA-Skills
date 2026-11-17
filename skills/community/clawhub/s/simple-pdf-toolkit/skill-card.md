## Description:

PDF 工具箱 helps agents perform local PDF merging, splitting, rotation, compression, and text extraction with bundled Python scripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[changeworldy-cyber](https://clawhub.ai/user/changeworldy-cyber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, employees, and external users can use this skill to ask an agent to run local PDF file operations such as merging, splitting, rotating, compressing, and extracting text. It is best suited for non-confidential documents in environments where the Chinese-language interface and local file writes are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF operations read and write local files, and output paths could overwrite important documents if chosen carelessly.

Mitigation: Use copies of important PDFs and choose explicit output paths that do not replace originals.

Risk: Processing confidential documents in an untrusted environment can expose sensitive document contents.

Mitigation: Avoid using the skill on confidential PDFs unless the runtime environment is trusted.

Risk: The skill depends on pypdf and optionally Ghostscript for compression behavior.

Mitigation: Install dependencies from trusted, pinned sources before use.

Risk: Server security review notes some overstated or missing advertised features.

Mitigation: Rely on the bundled scripts for supported operations: merge, split, rotate, compress, and text extraction.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/changeworldy-cyber/skills/simple-pdf-toolkit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; helper scripts emit JSON status and write PDF or text files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local filesystem PDF operations require pypdf, with optional Ghostscript support for stronger compression.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
