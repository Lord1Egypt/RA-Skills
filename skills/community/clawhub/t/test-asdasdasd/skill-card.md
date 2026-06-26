## Description: <br>
Structured field extraction tool that extracts text, table, and paragraph fields from documents based on a user-defined schema. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cf990801-commits](https://clawhub.ai/user/cf990801-commits) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and document-processing agents use this skill to turn a requested extraction task into a schema and extract structured fields from PDFs, Word files, Excel files, images, and other documents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local or sensitive documents may be uploaded to remote DPA services over plain HTTP, with unclear retention handling for uploaded files, task IDs, and extracted results. <br>
Mitigation: Use only approved DPA endpoints, prefer HTTPS overrides through DPA_BASE_URL and DPA_UPLOAD_URL, avoid confidential documents until retention is confirmed, and review task IDs and extracted results as sensitive data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cf990801-commits/test-asdasdasd) <br>
- [DPA simulation document endpoint](http://imsfz.gjzq.cn:18087/ismp/yx-dpa/document) <br>
- [DPA production document endpoint](http://ims.gjzq.cn:18087/ismp/yx-dpa/document) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [JSON extraction schema guidance and structured JSON extraction results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return a taskId and status when asynchronous extraction does not complete within the default wait period.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
