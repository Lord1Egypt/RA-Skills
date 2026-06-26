## Description: <br>
Solo File Transfer converts Word documents to Markdown with extracted images and uploads files, webpages, or notes to an IMA knowledge base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[meta-evo-creator](https://clawhub.ai/user/meta-evo-creator) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content operators use this skill to convert .docx material into Markdown and move selected files, webpages, or notes into an IMA knowledge base through authenticated upload steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected documents or generated Markdown may be uploaded to an external IMA knowledge base. <br>
Mitigation: Upload only content approved for that knowledge base and avoid confidential or sensitive documents unless the upload is explicitly authorized. <br>
Risk: The helper can make broad authenticated IMA requests using supplied credentials. <br>
Mitigation: Use least-privilege, temporary credentials where possible and review the requested API path and JSON body before running commands. <br>
Risk: The COS upload command accepts temporary secrets on the command line. <br>
Mitigation: Avoid exposing shell history or process listings, rotate temporary credentials after use, and prefer short-lived upload tokens. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/meta-evo-creator/solo-file-transfer) <br>
- [IMA service endpoint](https://ima.qq.com) <br>
- [Tencent COS authorization reference](https://cloud.tencent.com/document/product/436/7778) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires IMA credentials and can perform authenticated uploads to IMA and Tencent COS.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
