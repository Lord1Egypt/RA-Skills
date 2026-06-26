## Description: <br>
Word Parser helps agents parse Word documents (.docx and .doc) with mineru-open-api, producing structured content such as headings, paragraphs, tables, images, lists, and metadata. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[veeicwgy](https://clawhub.ai/user/veeicwgy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and automation agents use this skill to extract structured data from Word documents for document analysis, content indexing, form data extraction, automated report processing, and document search systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Word document contents may be processed through the MinerU service and written to local output files. <br>
Mitigation: Avoid confidential documents unless MinerU data handling is acceptable, choose the output directory deliberately, and delete generated files when they are no longer needed. <br>
Risk: The workflow depends on the third-party mineru-open-api package and CLI behavior. <br>
Mitigation: Install and run the package only in environments where the package and service are trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/veeicwgy/word-parser) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Files, JSON] <br>
**Output Format:** [Markdown guidance with inline shell commands and MinerU-generated output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Deep extraction can request JSON output, table recognition, and formula recognition; generated files are written to a local output directory.] <br>

## Skill Version(s): <br>
0.2.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
