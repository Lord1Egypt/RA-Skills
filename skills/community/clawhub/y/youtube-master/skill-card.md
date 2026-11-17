## Description:

Get YouTube video info, statistics, descriptions, thumbnails, and optionally transcripts. Uses YouTube Data API (free) for basic info and Apify (optional) for transcripts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tevfikgulep](https://clawhub.ai/user/tevfikgulep)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to retrieve YouTube video metadata, statistics, thumbnails, descriptions, and optional transcripts from a video URL or ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires API credentials for YouTube metadata and optional Apify transcript retrieval.

Mitigation: Use dedicated, revocable, least-privilege credentials and protect the local credentials file.

Risk: Transcript requests send the requested video URL to Apify.

Mitigation: Request transcripts only when sharing the video URL with Apify is acceptable for the use case.

Risk: The documented environment variables may not work as expected because the script reads credentials from the local credentials file.

Mitigation: Configure credentials in the documented local credentials file or verify runtime credential loading before deployment.

## Reference(s):

- [Google Cloud Console](https://console.cloud.google.com/)
- [Apify](https://apify.com/)
- [ClawHub Skill Page](https://clawhub.ai/tevfikgulep/skills/youtube-master)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text output with video metadata and optional transcript lines, plus Markdown usage examples in the skill documentation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a YouTube Data API key for metadata; transcript retrieval requires an Apify token and sends the video URL to Apify.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
