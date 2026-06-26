## Description: <br>
Download videos from YouTube, Twitter/X, TikTok, Douyin, Bilibili and upload to S3-compatible storage. Universal video downloader with smart quality selection and audio merging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aiastia](https://clawhub.ai/user/aiastia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and media operators use this skill to download videos from supported public platforms, upload them to S3-compatible storage, and produce access URLs or S3 paths for archiving, backup, and team sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports unsafe shell command construction with user-supplied video URLs. <br>
Mitigation: Review the local script before execution, avoid untrusted or attacker-supplied video URLs, and prefer a fixed version that avoids shell-string execution. <br>
Risk: The skill reads S3 credentials and uploads media plus metadata to the configured bucket. <br>
Mitigation: Use dedicated least-privilege S3 credentials limited to the required bucket or prefix, and avoid granting list or delete permissions unless those commands are needed. <br>
Risk: The security verdict is suspicious because the workflow downloads remote media and handles cloud storage credentials with limited safeguards. <br>
Mitigation: Install only after reviewing the code path and configuration, then run it in an environment appropriate for downloading remote media and handling storage secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aiastia/youtube-s3-uploader) <br>
- [README](README.md) <br>
- [Skill instructions](SKILL.md) <br>
- [Example configuration](example-config.yml) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Text, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, YAML configuration, status text, S3 URLs, and S3 object paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local video files temporarily, uploads media and metadata to configured S3-compatible storage, and may generate presigned access URLs.] <br>

## Skill Version(s): <br>
3.0.5 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
