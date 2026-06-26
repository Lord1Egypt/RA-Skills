## Description: <br>
Uploads local files to Qiniu Object Storage and returns a deliverable public or signed private download link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[showtimewalker](https://clawhub.ai/user/showtimewalker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and workflow operators use this skill when an existing local file needs to be uploaded to Qiniu Object Storage and delivered as a public URL or time-limited signed URL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected local files leave the local environment when uploaded to Qiniu Object Storage. <br>
Mitigation: Use least-privilege Qiniu credentials and upload only files approved for external storage. <br>
Risk: Incorrect bucket privacy or public-domain settings can return a delivery link with unintended accessibility. <br>
Mitigation: Verify QINIU_PUBLIC_DOMAIN and QINIU_IS_PRIVATE before use, and prefer signed URLs for private buckets. <br>
Risk: Local logs may contain basic path, bucket, object key, or link details. <br>
Mitigation: Avoid sensitive filenames or object keys and manage local log retention according to the deployment environment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/showtimewalker/qiniu-object-storage) <br>
- [Usage Guide](references/usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [JSON containing storage provider, bucket, object key, access mode, and delivery URL fields.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv, Python, and Qiniu environment variables; private links include an expiration interval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
