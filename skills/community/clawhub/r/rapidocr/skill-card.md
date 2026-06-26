## Description: <br>
Extract text from local image files with RapidOCR. Use when the user wants OCR on a JPG, PNG, WEBP, BMP, or TIFF image and may want plain text or JSON output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rapidai](https://clawhub.ai/user/rapidai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and end users use this skill to extract OCR text from local image files and receive either plain text or structured JSON with recognized lines, boxes, scores, and source path. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill executes local Node.js and Python code and depends on local RapidOCR and ONNX Runtime packages. <br>
Mitigation: Review before installing, use only with local images you intentionally provide, and install dependencies in the intended Python environment. <br>
Risk: Runtime instructions include an unrelated ClawHub publishing step. <br>
Mitigation: Remove or ignore the publish step unless deliberately publishing the skill. <br>


## Reference(s): <br>
- [RapidOCR Documentation](https://rapidai.github.io/RapidOCRDocs) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [Plain text or JSON, with Markdown guidance for dependency or execution issues] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON mode includes text, lines, boxes, scores, and source.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
