## Description: <br>
Convert documents between PDF, Word, Excel, PPT, and image formats using the Textin API with OCR-based conversion and layout preservation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[intsig-textin](https://clawhub.ai/user/intsig-textin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, employees, developers, and document-workflow agents use this skill to convert user-selected local files, submitted URLs, or a non-recursive batch folder between supported office, PDF, and image formats through Textin. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents, images, or submitted URLs are sent to Textin for conversion under the user's Textin account. <br>
Mitigation: Run the skill only for files or URLs that are appropriate to share with Textin, and review the Textin account, API credentials, and privacy terms before conversion. <br>
Risk: The skill writes converted results to a local output path, which could affect existing files or sensitive directories if chosen incorrectly. <br>
Mitigation: Review the requested input path, batch folder, and output path before running; use a dedicated output folder for batch conversion. <br>


## Reference(s): <br>
- [Textin File Conversion API Documentation](https://www.textin.com/document/pdf-to-word) <br>
- [Textin Platform](https://www.textin.com) <br>
- [Textin Privacy Policy](https://www.textin.com/privacy) <br>
- [ClawHub Skill Page](https://clawhub.ai/intsig-textin/textin-file-converter-pro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown with inline bash commands and local output file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce converted local document, image, spreadsheet, presentation, PDF, or ZIP files after Textin API processing.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
