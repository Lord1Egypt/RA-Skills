## Description:

Download videos from Xiaohongshu (XHS) pages by extracting the real CDN video URL and saving it with the required headers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hviktortsoi](https://clawhub.ai/user/hviktortsoi)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to download videos from Xiaohongshu pages they are allowed to save, especially when the page exposes only a browser blob URL and the agent needs to locate the playable CDN URL.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled script can fetch arbitrary URLs and write to unsafe output paths.

Mitigation: Review before installing, restrict use to expected Xiaohongshu and CDN URLs, and add URL allowlisting plus output-path sanitization before accepting untrusted input.

Risk: Downloading authenticated, private, or unauthorized videos may violate permissions or platform expectations.

Mitigation: Use only for videos the user is allowed to download, and avoid authenticated or private pages unless explicit permission is available.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance, files]

**Output Format:** [Markdown guidance with inline JavaScript, Bash, and Python command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create an MP4 file in the configured download directory when the bundled script succeeds.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
