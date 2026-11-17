## Description:

Downloads videos from YouTube, Twitter/X, TikTok, Douyin, Bilibili and other yt-dlp-supported sites, then uploads them to S3-compatible storage with quality selection and audio merging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiastia](https://clawhub.ai/user/aiastia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to archive, back up, or share videos from supported platforms through their own S3-compatible buckets. It helps configure storage, download media, upload files, and report resulting S3 access URLs and object paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe command handling could let a crafted video URL or S3 object path run commands on the user's machine.

Mitigation: Use only trusted video URLs and S3 object keys, review commands before execution, and prefer a maintained release that replaces shell-string execution with argument-array process execution.

Risk: The skill uses local S3 credentials and uploads media and metadata to configured storage.

Mitigation: Use least-privilege storage credentials, protect the local configuration file, and apply bucket policies and short-lived presigned URLs where appropriate.

Risk: Downloaded local copies may be deleted after successful upload unless kept by option.

Mitigation: Use the keep-local option when a local copy is required and verify the uploaded object before relying on cleanup behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aiastia/skills/youtube-s3-uploader)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Terminal output with S3 URLs and paths, plus YAML configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can upload media and metadata to configured S3-compatible storage and may delete downloaded local copies after successful upload unless kept by option.]

## Skill Version(s):

3.0.5 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
