## Description: <br>
Organizes PDFs by extracting metadata and classifying them into topics, then renaming files and sorting them into topic-based folders using AI analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yxl184](https://clawhub.ai/user/yxl184) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and developers with local PDF collections use this skill to extract document text and metadata, classify PDFs with a configured AI provider, and organize them into renamed topic and subtopic folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Extracted PDF text and metadata may be sent to the configured AI provider. <br>
Mitigation: Use only PDFs that the provider agreement permits, and avoid confidential, regulated, or proprietary documents unless that use is approved. <br>
Risk: The tool can rename and move local PDF files. <br>
Mitigation: Run with --dry-run or keep backups before processing important files. <br>
Risk: Configuration can contain an API key. <br>
Mitigation: Keep config.json private and avoid sharing or committing populated credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yxl184/skill-pdf-orgnizer) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [Markdown instructions, Python source files, JSON configuration, shell commands, console summaries, renamed PDFs, folder structures, and move logs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports dry-run previews, incremental processing, custom topic mappings, and configurable text extraction limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
