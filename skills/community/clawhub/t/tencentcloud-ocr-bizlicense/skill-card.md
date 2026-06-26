## Description: <br>
Calls Tencent Cloud BizLicenseOCR to extract business-license fields from image URLs or Base64 image input, including company identity fields, validity period details, copy or reshoot warnings, electronic license detection, and optional business-certificate recognition. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zt1314p-design](https://clawhub.ai/user/zt1314p-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to submit authorized business-license images or URLs to Tencent Cloud OCR and receive structured company registration fields and warning signals for downstream review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses Tencent Cloud credentials and sends selected business-license images or URLs to Tencent Cloud OCR for recognition. <br>
Mitigation: Use a dedicated least-privilege Tencent key, protect the required environment variables, process only authorized documents, and review Tencent Cloud data-handling terms for sensitive business records. <br>


## Reference(s): <br>
- [Tencent Cloud BizLicenseOCR API documentation](https://cloud.tencent.com/document/api/866/36215) <br>
- [ClawHub skill page](https://clawhub.ai/zt1314p-design/tencentcloud-ocr-bizlicense) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON output from the helper script, with Markdown usage guidance and shell command examples in the skill documentation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tencent Cloud credentials via TENCENTCLOUD_SECRET_ID and TENCENTCLOUD_SECRET_KEY, and accepts either ImageUrl or ImageBase64 input.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
