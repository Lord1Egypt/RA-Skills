## Description:

Upload a local file to Astron Claw Bridge and return a public download URL.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to upload local files such as images, audio, video, documents, or other artifacts to Astron Claw Bridge and receive a public download URL for sharing or embedding.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded files and the authentication token may be sent over unencrypted HTTP.

Mitigation: Use only files intended for publication, require HTTPS for the Bridge URL, and use a least-privilege token.

Risk: The Python dependency is not pinned in a reproducible requirements file.

Mitigation: Pin the requests dependency before operational use.

## Reference(s):

- [File Uploader skill page](https://clawhub.ai/jpengcheng523-netizen/skills/uploader)
- [Publisher profile](https://clawhub.ai/user/jpengcheng523-netizen)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text upload result with file metadata and download URL]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local file path, optional session ID, the requests Python package, and Astron Claw Bridge configuration.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
