## Description: <br>
Recognizes vehicles, animals, and plants and extracts OCR text from screenshots, photos, invoices, handwriting, and tables using Baidu vision APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangziiiiii](https://clawhub.ai/user/wangziiiiii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to classify cars, animals, and plants or extract OCR text from selected image inputs supplied as local paths, URLs, or base64 payloads. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images and document screenshots are sent to Baidu for OCR or recognition. <br>
Mitigation: Use only approved images, avoid highly sensitive or regulated documents unless approved, and disclose the external processing path where required. <br>
Risk: Baidu API credentials are required through environment variables. <br>
Mitigation: Use dedicated, least-privileged Baidu credentials and rotate or revoke them according to local credential policy. <br>
Risk: The scripts read local image files and make outbound network requests. <br>
Mitigation: Review requested image paths or URLs before execution and run the skill only in environments where Baidu network access is expected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangziiiiii/vision-recognition-ocr) <br>
- [Baidu image classification API endpoint](https://aip.baidubce.com/rest/2.0/image-classify/v1) <br>
- [Baidu OCR API endpoint](https://aip.baidubce.com/rest/2.0/ocr/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration] <br>
**Output Format:** [JSON API responses with command-line usage examples and credential configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Baidu credential environment variables and network access; accepts local image path, URL, or base64 image input.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
