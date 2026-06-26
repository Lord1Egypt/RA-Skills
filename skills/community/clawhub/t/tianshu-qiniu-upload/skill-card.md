## Description: <br>
Uploads local files such as images, HTML pages, documents, and other artifacts to Qiniu Cloud storage, then returns a publicly accessible CDN URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangshengli0421](https://clawhub.ai/user/wangshengli0421) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when they need an agent to publish a selected local file to a configured Qiniu bucket and return a shareable URL. It is intended for Qiniu uploads only, not for other storage providers or file generation without sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can publish selected local files to a public or externally reachable Qiniu URL. <br>
Mitigation: Verify the exact local path and the bucket access policy before upload; do not upload private documents, credentials, or personal data unless the bucket policy is appropriate. <br>
Risk: The upload workflow requires Qiniu access credentials. <br>
Mitigation: Use least-privilege Qiniu keys stored in environment or skill configuration, and keep secrets out of chat transcripts and source files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangshengli0421/tianshu-qiniu-upload) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text URL with optional Markdown guidance and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns the uploaded file URL after the Node.js script completes.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release metadata and clawhub.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
