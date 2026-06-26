## Description: <br>
Uploads a local file to Tencent Cloud COS and returns presigned URLs for browser preview and file download. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hoyt-tian](https://clawhub.ai/user/hoyt-tian) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to upload selected local files to Tencent Cloud COS buckets and share time-limited view or download links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Presigned view and download links can expose uploaded COS objects if they are shared too broadly or remain valid too long. <br>
Mitigation: Confirm the file, bucket, object key, and expiration before running; keep signed links short-lived, prefer HTTPS, and delete uploaded objects when they are no longer needed. <br>
Risk: Tencent Cloud credentials used by the script can grant upload and signing access to a bucket. <br>
Mitigation: Use least-privilege or temporary credentials and avoid passing long-lived secrets unless the execution environment protects them. <br>


## Reference(s): <br>
- [Tencent COS Uploader on ClawHub](https://clawhub.ai/hoyt-tian/tencent-cos-uploader) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Tencent COS credentials, region, bucket, local file path, optional object key, expiration seconds, and HTTPS scheme by default.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
