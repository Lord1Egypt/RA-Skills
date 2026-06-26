## Description: <br>
Transform document photos into clean scanned-looking pages with automatic edge detection, cropping, and perspective correction. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and end users use this skill to turn document photos, receipts, forms, pages, or papers into cropped, perspective-corrected scan-style images for easier reading, sharing, archiving, or downstream OCR. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Browser workflows may load mutable CDN dependencies for OpenCV.js or jscanify. <br>
Mitigation: For sensitive or production document cleanup, pin dependency versions or use local dependencies instead of mutable CDN URLs. <br>
Risk: Generated scans can differ from the original photo if edge detection or perspective correction selects the wrong document corners. <br>
Mitigation: Keep original photos separate from generated scans and visually review outputs before sharing, archiving, or passing them to OCR. <br>


## Reference(s): <br>
- [ClawHub Scanner skill page](https://clawhub.ai/ivangdavila/scanner) <br>
- [Scanner homepage](https://clawic.com/skills/scanner) <br>
- [OpenCV.js documentation](https://docs.opencv.org/) <br>
- [jscanify browser bundle](https://cdn.jsdelivr.net/gh/ColonelParrot/jscanify@master/src/jscanify.min.js) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JavaScript or HTML snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend browser-first document scanning workflows using jscanify, OpenCV.js, local preview commands, and manual-corner fallback guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
