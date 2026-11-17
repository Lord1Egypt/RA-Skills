## Description:

Research Library is a local-first multimedia research library for hardware projects that captures code, CAD, PDFs, images, and schematics with project-scoped search, extraction, backup, and restore.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jonbuckles](https://clawhub.ai/user/jonbuckles)

### License/Terms of Use:

MIT

## Use Case:

Developers and hardware engineers use this skill to operate a local research library for project documents, extracted metadata, cross-reference links, and CLI-driven search.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: URL import can fetch untrusted content or unsafe network locations.

Mitigation: Prefer the ClawHub-reviewed package path, avoid untrusted URLs and FTP links, and review imported sources before extraction.

Risk: Project-path handling can affect where local research data and attachments are organized.

Mitigation: Run as a normal user, use simple safe project IDs, and keep data directories scoped to the intended workspace.

Risk: Indexed metadata and exports may include sensitive file contents, GPS, author, or device information.

Mitigation: Review extracted metadata and exported JSON or Markdown before sharing outside the local environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jonbuckles/skills/research-library)
- [CLI Reference](artifact/docs/CLI-REFERENCE.md)
- [Extraction Pipeline Guide](artifact/docs/EXTRACTION-GUIDE.md)
- [Research Library Search Guide](artifact/docs/SEARCH-GUIDE.md)
- [Extraction Worker Guide](artifact/docs/WORKER-GUIDE.md)
- [Technical Notes](artifact/TECHNICAL-NOTES.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON or Markdown exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local SQLite data, extracted text indexes, backups, and export files when its CLI is used.]

## Skill Version(s):

0.1.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
