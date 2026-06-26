## Description: <br>
Calls Tencent Cloud VehicleLicenseOCR to extract structured vehicle-license fields from front, back, double-sided, electronic, and tractor vehicle-license images supplied by URL or Base64 input. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zt1314p-design](https://clawhub.ai/user/zt1314p-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to submit vehicle-license images to Tencent Cloud OCR and receive normalized vehicle-registration fields, warning codes, and request metadata as JSON. It is suited for workflows that are authorized to process vehicle-license images through Tencent Cloud. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vehicle-license images can contain sensitive personal and vehicle data, and this skill sends those images to Tencent Cloud OCR. <br>
Mitigation: Use only with authorization, avoid third-party documents without consent, and ensure the deployment is approved for Tencent Cloud processing. <br>
Risk: Cloud OCR usage depends on Tencent Cloud credentials, billing state, regional service availability, and SDK behavior. <br>
Mitigation: Use dedicated Tencent Cloud credentials with appropriate permission and billing controls, and review or pin the Tencent Cloud SDK dependency in the runtime environment. <br>


## Reference(s): <br>
- [Tencent Cloud VehicleLicenseOCR API documentation](https://cloud.tencent.com/document/api/866/36209) <br>
- [ClawHub skill page](https://clawhub.ai/zt1314p-design/tencentcloud-ocr-vehiclelicense) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/zt1314p-design) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON from the OCR script, with Markdown usage guidance in the skill documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tencent Cloud credentials and either an image URL or Base64 image input; image content is sent to Tencent Cloud OCR.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
