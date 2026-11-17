## Description:

Organizes PDF files by extracting metadata, classifying documents into topic-based folders, and renaming files with AI-assisted analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yxl184](https://clawhub.ai/user/yxl184)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-heavy users use this skill to organize local PDF collections into topic and subtopic folders, with extracted titles, authors, and publication venues used for descriptive filenames.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF text may be sent to external AI providers during title, author, venue, and topic analysis.

Mitigation: Use only on PDFs whose content may be shared with the configured provider, and avoid confidential or regulated documents unless that transfer is approved.

Risk: The skill moves and renames local files by default.

Mitigation: Run with dry-run mode first, review the planned destinations, and keep backups of input PDFs before allowing file moves.

Risk: API keys may be stored in config.json.

Mitigation: Protect the configuration file, avoid committing it, and rotate keys if the file is exposed.

Risk: Existing output folders and folder cache data may affect where documents are placed.

Mitigation: Inspect .folder_cache.json and use private, dedicated input and output folders before processing a collection.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yxl184/skills/skill-pdf-orgnizer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and Python code behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local folder structures, renamed PDF files, processing logs, and dry-run previews when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
