## Description: <br>
Enhances user-provided images and document photos through Quark Scan services, including quality improvement, cleanup, crop correction, watermark or handwriting removal, shadow removal, sketch conversion, line-art extraction, and contract or exam-paper enhancement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yescan-ai](https://clawhub.ai/user/yescan-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to route a single image URL, local image file, or base64 image into the appropriate Quark Scan enhancement scene and receive the processed image result. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images are uploaded to Quark's remote service for processing. <br>
Mitigation: Use the skill only when external processing is acceptable, and avoid highly sensitive IDs, contracts, medical records, or financial documents unless the user has approved that data flow. <br>
Risk: Processed image files are written to the local temporary directory and can remain until cleaned up. <br>
Mitigation: Periodically remove generated files from the temporary image output directory when local retention is not desired. <br>
Risk: The skill requires SCAN_WEBSERVICE_KEY credentials. <br>
Mitigation: Store the API key in the configured environment, keep it out of prompts and logs, and rotate or revoke it if exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yescan-ai/yescan-scan-universal) <br>
- [Quark Scan business platform](https://scan.quark.cn/business) <br>
- [Quark Scan vision endpoint](https://scan-business.quark.cn/vision) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [JSON text with a local image path when processing succeeds] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and SCAN_WEBSERVICE_KEY; successful image responses are saved under the system temporary directory.] <br>

## Skill Version(s): <br>
1.0.16 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
