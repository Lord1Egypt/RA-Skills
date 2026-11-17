## Description:

Calls Tencent Cloud AdvertiseOCR to extract text from image URLs, local image files, or Base64 image input and return detected text with confidence and position metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zt1314p-design](https://clawhub.ai/user/zt1314p-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run Tencent Cloud OCR on image inputs and receive structured OCR results, including detected text, confidence scores, text coordinates, image size, and request ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload any readable local file supplied as an image path to Tencent Cloud without confirming it is an intended image input.

Mitigation: Use only approved image files or URLs, avoid sensitive documents, and add image-type validation plus explicit upload confirmation before deployment.

Risk: OCR requests send image content to Tencent Cloud under the configured Tencent account.

Mitigation: Use this skill only for images permitted for Tencent Cloud processing and manage Tencent Cloud credentials through environment variables.

Risk: The dependency is documented without a pinned Tencent Cloud SDK version.

Mitigation: Pin and review tencentcloud-sdk-python before installation.

## Reference(s):

- [Tencent Cloud AdvertiseOCR API documentation](https://cloud.tencent.com/document/api/866/49524)
- [ClawHub skill page](https://clawhub.ai/zt1314p-design/skills/tencentcloud-ocr-general)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [JSON response with Markdown usage guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Tencent Cloud credentials and sends provided image URL or Base64 image content to Tencent Cloud OCR.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
