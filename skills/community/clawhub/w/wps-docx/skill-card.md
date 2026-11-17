## Description:

WPS Word Document helps agents create or edit Word .docx documents, including HTML-to-DOCX generation, targeted text replacement, DOCX unpacking, validation, and repacking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xixihaha123123123123](https://clawhub.ai/user/xixihaha123123123123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an agent needs to deliver a Word document or make targeted edits to an existing DOCX file. It is most useful for generating DOCX files from Word-compatible HTML, replacing text in document bodies, headers, and footers, and inspecting or repacking DOCX XML structures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports under-disclosed network fetching during HTML-to-DOCX conversion.

Mitigation: Run the skill in a sandbox with limited network access and avoid converting HTML that contains remote images or other attacker-controlled remote resources.

Risk: The security evidence reports unsafe file and archive handling around DOCX unpacking and output paths.

Mitigation: Process only trusted DOCX files, write unpacked content to disposable directories, and avoid pointing outputs at existing important directories.

Risk: The security verdict is suspicious for this release.

Mitigation: Review the skill before deployment and install it only in environments with limited filesystem and network access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xixihaha123123123123/skills/wps-docx)
- [Publisher profile](https://clawhub.ai/user/xixihaha123123123123)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with Python snippets and generated DOCX files as the intended artifact]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill directs agents to create HTML, convert it to DOCX, edit DOCX XML content, and report structured success or validation results.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
