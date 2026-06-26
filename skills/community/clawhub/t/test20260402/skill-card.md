## Description: <br>
Extracts text from multiple uploaded images and organizes the results by image in a structured Markdown document. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asiangiantduck](https://clawhub.ai/user/asiangiantduck) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to turn batches of document screenshots, presentation images, or other image files into editable text while preserving basic structure by image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded images may contain sensitive text. <br>
Mitigation: Use the skill only with images that are appropriate to process through the agent's image-reading tool. <br>
Risk: OCR results can be incomplete or inaccurate for blurry, low-contrast, or complex images. <br>
Mitigation: Review the generated Markdown against the source images before relying on or sharing the extracted text. <br>
Risk: When asked to create a file, the skill may write a Markdown document in the current workspace. <br>
Mitigation: Confirm the requested output mode and review any generated file before distributing it. <br>


## Reference(s): <br>
- [Output Format Reference](references/output-format.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/asiangiantduck/test20260402) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files] <br>
**Output Format:** [Markdown document with one section per image] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May be returned directly in chat or written as a .md file in the current workspace when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
