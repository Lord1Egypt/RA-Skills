## Description: <br>
Convert Word documents (.docx/.doc) to high-quality JPG images using Microsoft Word COM export to PDF and PyMuPDF rendering at 300 DPI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jerryxue185-png](https://clawhub.ai/user/jerryxue185-png) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing agents use this skill to convert Word documents into high-resolution JPG page images while preserving document formatting. It supports explicit document paths, directory-based latest-file selection, and the OpenClaw inbound media folder workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can process the most recent Word document from the inbound folder when no explicit path is provided. <br>
Mitigation: Use explicit file paths for sensitive documents so the agent converts the intended file. <br>
Risk: The converter deletes prior .jpg and .png files from its fixed output folder before writing new page images. <br>
Mitigation: Move or rename generated images that need to be retained before rerunning the skill. <br>
Risk: The workflow uses local Microsoft Word automation and creates a temporary source copy. <br>
Mitigation: Run it only where local Word automation is acceptable and delete the temporary source copy after conversion when the document is confidential. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jerryxue185-png/word-to-jpg) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Text] <br>
**Output Format:** [JPG image files with console status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes page_1.jpg, page_2.jpg, and subsequent page images to ~/.openclaw/media/outbound/word-images at JPG quality 95.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
