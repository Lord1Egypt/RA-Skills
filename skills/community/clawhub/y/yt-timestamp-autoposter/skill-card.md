## Description:

Generate SEO-optimized YouTube timestamps from a YouTube URL or a raw transcript string, then optionally append them to the description of that specific video or your latest upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robj1925](https://clawhub.ai/user/robj1925)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, operators, and agents use this skill to generate YouTube chapter timestamps from a video transcript or URL. When explicitly requested with posting enabled, it can append the generated timestamp block to a target video description or the latest channel upload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Posting mode can automatically modify live YouTube video descriptions.

Mitigation: Run generation-only first, review the timestamp block and target video, and enable posting only after confirming the update is appropriate.

Risk: OAuth tokens are cached locally and grant reusable YouTube write access.

Mitigation: Store credentials outside the project with restrictive file permissions, keep token files out of version control, and revoke access when no longer needed.

Risk: Passing the Gemini API key as a command argument can expose the secret through shell history or process listings.

Mitigation: Use a safer secret path such as an environment variable or local secret manager instead of placing the key directly in command arguments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/robj1925/skills/yt-timestamp-autoposter)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Google AI Studio](https://aistudio.google.com/)
- [Google Account permissions](https://myaccount.google.com/permissions)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text timestamp block with supporting Markdown and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The generated timestamp block is intended to be reviewed before use and may be appended to a YouTube video description when posting is enabled.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
