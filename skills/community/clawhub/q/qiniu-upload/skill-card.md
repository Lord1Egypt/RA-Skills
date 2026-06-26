## Description: <br>
Upload local files to Qiniu Cloud and return a publicly accessible URL or signed private URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenggongdu](https://clawhub.ai/user/chenggongdu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to upload selected local files to Qiniu Cloud, receive a hosted URL, and pass that URL into downstream workflows such as transcription or document processing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads selected local files to external Qiniu Cloud storage, which can expose sensitive content if the wrong file or bucket policy is used. <br>
Mitigation: Use dedicated least-privilege Qiniu credentials, confirm the file path before upload, and avoid uploading sensitive files unless external storage is intended. <br>
Risk: Returned URLs may be public or signed private URLs depending on bucket and configuration. <br>
Mitigation: Confirm whether the configured bucket and domain produce public URLs or signed private URLs, and verify URL accessibility before passing it to downstream services. <br>


## Reference(s): <br>
- [Qiniu Cloud homepage](https://www.qiniu.com/) <br>
- [Qiniu environment variables](references/env-example.md) <br>
- [ClawHub Qiniu Upload release page](https://clawhub.ai/chenggongdu/qiniu-upload) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, JSON, Guidance] <br>
**Output Format:** [JSON upload result with key, URL, size, privacy mode, MIME type, and source path] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Qiniu credentials and bucket/domain environment variables.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
