## Description: <br>
Formats user-provided bibliography entries into specified citation styles such as APA, GB/T 7714, MLA, Chicago, or a user-supplied format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zyyfaith](https://clawhub.ai/user/zyyfaith) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, researchers, and academic writers use this skill to clean mixed bibliography lists, convert them to a selected citation style, and generate copy-ready reference files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Default file output can place bibliography files in an unintended or shared workspace location. <br>
Mitigation: Use explicit output filenames or locations, especially in shared workspaces, and review generated files before sharing. <br>
Risk: Private drafts, internal URLs, annotations, or unpublished bibliography data could be exposed during optional web lookup for missing citation details. <br>
Mitigation: Keep sensitive bibliography data offline unless the user intentionally approves web lookup, and redact private annotations before lookup. <br>


## Reference(s): <br>
- [Citation Format Reference](reference/formats.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Guidance] <br>
**Output Format:** [Formatted bibliography documents, usually DOCX with TXT or Markdown fallback, plus a concise change report.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Defaults to references.docx in the workspace root when no filename is specified; may use TXT or Markdown fallback if document conversion is unavailable.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
