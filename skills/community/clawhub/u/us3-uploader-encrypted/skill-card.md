## Description: <br>
Uploads files to UCloud US3 (UFile) object storage and generates signed download URLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qianjunye](https://clawhub.ai/user/qianjunye) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill when generated files need to be uploaded to UCloud US3 and shared as time-limited signed download links instead of local sandbox paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated files may be uploaded to external UCloud US3 storage without a clear consent or sensitivity check. <br>
Mitigation: Use the skill only when external sharing is intended, review file contents before upload, and avoid uploading sensitive or private files. <br>
Risk: Signed download links can remain usable for the configured validity period. <br>
Mitigation: Use a dedicated least-privilege bucket and keep deletion, revocation, or credential-rotation procedures available when links should no longer work. <br>
Risk: The uploader can install the ufile dependency at runtime. <br>
Mitigation: Preinstall or pin the ufile dependency in the execution environment instead of relying on runtime installation. <br>


## Reference(s): <br>
- [US3 CLI Configuration Guide](references/us3_config.md) <br>
- [UCloud US3 CLI documentation](https://docs.ucloud.cn/ufile/tools/us3cli/prepare) <br>
- [UCloud us3cli releases](https://github.com/ucloud/us3cli/releases) <br>
- [ClawHub skill page](https://clawhub.ai/qianjunye/us3-uploader-encrypted) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and generated signed URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs signed UCloud US3 download URLs valid for 7 days; uploads require US3 credentials and a configured bucket.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
