## Description: <br>
Upload files to UCloud US3 object storage and generate public URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qianjunye](https://clawhub.ai/user/qianjunye) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and agents use this skill to upload selected local files, such as images, videos, documents, audio, or archives, to a configured UCloud US3 bucket and return shareable public URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local files may be uploaded to a public US3 bucket and become directly accessible by URL. <br>
Mitigation: Review file paths and batch patterns before upload, and avoid uploading secrets, private documents, or other sensitive content. <br>
Risk: UCloud credentials with broad permissions could allow unintended bucket access. <br>
Mitigation: Use a least-privilege UCloud key limited to the intended bucket. <br>


## Reference(s): <br>
- [UCloud UFile Product Page](https://www.ucloud.cn/site/product/ufile.html) <br>
- [ClawHub skill page](https://clawhub.ai/qianjunye/us3) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Text, Configuration] <br>
**Output Format:** [JSON upload result or direct URL string, with Markdown usage guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uploads selected local files to a configured public UCloud US3 bucket and returns directly accessible URLs.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
