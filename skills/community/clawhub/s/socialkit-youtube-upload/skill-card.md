## Description:

Uploads an approved video to YouTube with the official Data API v3 - private by default, optional scheduled publish time, AI or synthetic content disclosure, and custom thumbnail - after the user approves the exact file and settings. Use when the user wants to upload, publish or schedule a YouTube video, or to connect their YouTube channel.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers use this skill to connect their YouTube channel, review an exact video and its publishing settings, then upload it privately or schedule publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The saved OAuth token grants access to the connected YouTube account.

Mitigation: Use your own OAuth client, protect the saved token, and revoke access and delete the token when finished.

Risk: A scheduled video may become public at its publish time, and YouTube may apply a different privacy setting than requested.

Mitigation: Review the exact video and settings before approval, then check the resulting privacy in YouTube Studio.

## Reference(s):

- [Setup guide](artifact/references/setup.md)
- [YouTube Data API video upload guide](https://developers.google.com/youtube/v3/guides/uploading_a_video)
- [YouTube Data API quota costs](https://developers.google.com/youtube/v3/determine_quota_cost)
- [YouTube altered or synthetic content disclosure](https://support.google.com/youtube/answer/14328491)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON upload result with setup guidance and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Upload results include video identifiers, URLs, requested and actual privacy, schedule, synthetic-media status, thumbnail status, and warnings.]

## Skill Version(s):

0.3.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
