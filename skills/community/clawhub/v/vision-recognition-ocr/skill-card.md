## Description:

Recognizes vehicles, animals, and plants and extracts text from screenshots, photos, invoices, handwriting, and tables using Baidu vision and OCR APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangziiiiii](https://clawhub.ai/user/wangziiiiii)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run Baidu-backed image classification and OCR workflows for local files, public image URLs, or base64 image input.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images and documents submitted through local paths, URLs, or base64 input are sent to Baidu vision or OCR services.

Mitigation: Use the skill only with files and URLs that are approved for Baidu processing, and avoid sensitive or regulated documents unless the deployment has reviewed the applicable data handling requirements.

Risk: User-specified local paths may upload any readable local file without file-type, path-scope, size, or confirmation safeguards.

Mitigation: Require explicit confirmation for local path inputs, restrict paths to approved folders, and add file type and size validation before broader deployment.

Risk: Shared or overly broad Baidu credentials could expand impact if misused.

Mitigation: Use dedicated least-privilege Baidu credentials for this skill and rotate or revoke them independently from other systems.

## Reference(s):

- [Baidu image classification API endpoint](https://aip.baidubce.com/rest/2.0/image-classify/v1)
- [Baidu OCR API endpoint](https://aip.baidubce.com/rest/2.0/ocr/v1)
- [Baidu OAuth token endpoint](https://aip.baidubce.com/oauth/2.0/token)
- [jisuapi.com](https://jisuapi.com)
- [jisuepc.com](https://jisuepc.com)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Configuration guidance, Text]

**Output Format:** [JSON API responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Baidu API credentials and accepts image_path, image_base64, or url input.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
