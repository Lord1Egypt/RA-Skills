## Description:

Quark Scan enhances single image or document-photo inputs by improving clarity, removing visual artifacts such as handwriting, watermarks, shadows, screen patterns, and background color, and producing an optimized local image output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yescan-ai](https://clawhub.ai/user/yescan-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to enhance individual scanned documents, screenshots, receipts, certificates, contracts, study materials, and photos through Quark Scan's remote image service. It is not intended for OCR, document conversion to Word, Excel, or PDF, video processing, batch processing, or AI image generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images or document photos are sent to Quark's remote service for processing.

Mitigation: Use the skill only with images you are authorized to upload and avoid highly sensitive documents unless consent and policy approval are clear.

Risk: Weak local-file validation could expose unintended files when paths are ambiguous or symlinked.

Mitigation: Provide explicit image file paths, avoid symlinks, and verify the selected file before invoking the skill.

Risk: Redirect handling could expose image data or SCAN_WEBSERVICE_KEY unexpectedly.

Mitigation: Use trusted image URLs, avoid cross-origin redirects, and rotate SCAN_WEBSERVICE_KEY if exposure is suspected.

Risk: Enhanced image outputs are saved in the system temporary directory and may persist after use.

Mitigation: Manually clean temporary output images after retrieval, especially for confidential scans.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yescan-ai/skills/alibaba-quark-scan)
- [Quark Scan business platform](https://scan.quark.cn/business)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, files]

**Output Format:** [JSON response with error details or a saved local image path; setup guidance may include Markdown and bash commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and SCAN_WEBSERVICE_KEY; successful image responses are saved under the system temporary directory.]

## Skill Version(s):

1.0.18 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
