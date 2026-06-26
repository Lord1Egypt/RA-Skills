## Description: <br>
Local-first multimedia research library for hardware projects. Capture code, CAD, PDFs, images. Search with material-type weighting. Project isolation with cross-references. Async extraction. Backup + restore. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jonbuckles](https://clawhub.ai/user/Jonbuckles) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and hardware engineers use this skill to capture, index, search, link, export, and back up local research materials such as code, CAD files, PDFs, images, schematics, and project notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Imported private files, extracted text, and metadata can become searchable in the local library. <br>
Mitigation: Import only materials intended for local indexing and review the configured data directory before adding sensitive project files. <br>
Risk: Image EXIF fields, including GPS-related metadata when present, may be extracted and indexed. <br>
Mitigation: Strip sensitive image metadata before import or avoid adding images whose EXIF data should not become searchable. <br>
Risk: The CLI can add materials from URLs, including less trustworthy sources. <br>
Mitigation: Prefer trusted HTTPS sources and avoid FTP or unknown URLs when importing external documents. <br>
Risk: Restore and force operations can overwrite or hide local library state. <br>
Mitigation: Create a fresh backup before restore operations and review targets carefully before using --force. <br>


## Reference(s): <br>
- [Research Library ClawHub Page](https://clawhub.ai/Jonbuckles/research-library) <br>
- [CLI Reference](docs/CLI-REFERENCE.md) <br>
- [Extraction Guide](docs/EXTRACTION-GUIDE.md) <br>
- [Search Guide](docs/SEARCH-GUIDE.md) <br>
- [Worker Guide](docs/WORKER-GUIDE.md) <br>
- [Technical Notes](TECHNICAL-NOTES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell command examples, Python snippets, and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local CLI workflows and library-management guidance; the underlying tool stores indexed text, metadata, attachments, and backups on the user's machine.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
