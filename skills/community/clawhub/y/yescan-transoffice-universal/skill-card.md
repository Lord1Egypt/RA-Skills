## Description: <br>
Converts user-selected images, screenshots, or scans into editable Word or Excel documents or PDFs using Quark Scan's OCR conversion service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mozhihuidage](https://clawhub.ai/user/mozhihuidage) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to convert a single explicitly provided image, screenshot, or scan into a Word, Excel, or PDF file while preserving document structure where the upstream service supports it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images or image URLs are sent to Quark's scanning service for processing. <br>
Mitigation: Use the skill only with documents suitable for Quark's terms and avoid sensitive content unless that data handling is acceptable. <br>
Risk: The SCAN_WEBSERVICE_KEY credential is required for execution. <br>
Mitigation: Keep the key private, scope it appropriately, and rotate or revoke it if exposed. <br>
Risk: Converted documents are saved locally in the system temp directory and may contain private data. <br>
Mitigation: Delete generated files from the temp directory after use when outputs contain sensitive information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mozhihuidage/yescan-transoffice-universal) <br>
- [Quark Scan business portal](https://scan.quark.cn/business) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Files, Shell commands, Configuration] <br>
**Output Format:** [JSON response with local output file paths for successful conversions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SCAN_WEBSERVICE_KEY and accepts one image input by URL, local path, or base64 data.] <br>

## Skill Version(s): <br>
1.1.16 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
