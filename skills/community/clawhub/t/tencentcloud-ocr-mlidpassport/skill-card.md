## Description: <br>
Calls Tencent Cloud's MLIDPassportOCR API to extract passport fields, MRZ data, optional portrait crops, and international warning signals from passport images or image URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zt1314p-design](https://clawhub.ai/user/zt1314p-design) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run Tencent Cloud passport OCR on authorized passport images, extracting identity fields, MRZ information, and optional warning signals for document-processing workflows. <br>

### Deployment Geography for Use: <br>
Global, subject to Tencent Cloud OCR regional availability and user compliance requirements. <br>

## Known Risks and Mitigations: <br>
Risk: Passport images, image URLs, returned OCR fields, and optional portrait crops are sensitive data sent to Tencent Cloud OCR. <br>
Mitigation: Use only documents you are authorized to process, avoid RetImage unless the portrait crop is required, and review Tencent Cloud data handling and retention terms before deployment. <br>


## Reference(s): <br>
- [Tencent Cloud MLIDPassportOCR API Documentation](https://cloud.tencent.com/document/api/866/37657) <br>
- [ClawHub Skill Page](https://clawhub.ai/zt1314p-design/tencentcloud-ocr-mlidpassport) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [JSON API results and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return extracted passport fields, MRZ data, warning codes, request IDs, and optional portrait image data when RetImage is enabled.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
