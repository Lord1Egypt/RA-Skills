## Description: <br>
Calls Tencent Cloud LicensePlateOCR to identify Mainland China vehicle license plates from an image URL or base64 image and return plate number, color, confidence, category, coordinates, and multi-plate results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zt1314p-design](https://clawhub.ai/user/zt1314p-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when they need an agent to call Tencent Cloud OCR for vehicle-license-plate recognition from an image URL, image file, or base64 image. It is intended for workflows that need structured plate number, color, confidence, category, bounding-box, and multi-plate results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Vehicle images, plate images, or image URLs are sent to Tencent Cloud for OCR processing. <br>
Mitigation: Submit only images the user is authorized to process, avoid unnecessary sensitive plate data, and confirm the relevant Tencent Cloud privacy and retention controls before use. <br>
Risk: Tencent Cloud credentials can incur usage, quota, or billing impact if over-permissioned or exposed. <br>
Mitigation: Use a least-privilege Tencent Cloud key, store it in environment variables or a secret manager, rotate it as needed, and monitor quota and billing. <br>
Risk: OCR results may be incorrect, incomplete, or low-confidence. <br>
Mitigation: Review the confidence score and source image before relying on recognized plate details in operational or compliance-sensitive workflows. <br>


## Reference(s): <br>
- [Tencent Cloud LicensePlateOCR API documentation](https://cloud.tencent.com/document/api/866/36211) <br>
- [ClawHub skill release](https://clawhub.ai/zt1314p-design/tencentcloud-ocr-licenseplate) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands] <br>
**Output Format:** [JSON object printed to stdout by a Python command-line script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes recognized plate number, confidence, color, category, bounding rectangle, multi-plate list, plate count, and request ID when returned by Tencent Cloud.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
