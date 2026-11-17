## Description:

Download YouTube videos by URL in various resolutions using a pay-per-use API with credit-based authentication and no charge on failed downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jxyyjm](https://clawhub.ai/user/jxyyjm)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill when a user asks to download a YouTube video, choose a video resolution, or extract audio from a YouTube URL through the documented third-party API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the user's generated service API key and requested YouTube URLs to a third-party service.

Mitigation: Use a dedicated, rotatable API key and review the provider's terms, privacy practices, and pricing before use.

Risk: Successful downloads may be served from an external storage URL.

Mitigation: Review downloaded files and storage links before opening or sharing them, and confirm that the requested content may be downloaded under applicable rights and policies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jxyyjm/skills/youtube-downloader-skill)
- [Publisher profile](https://clawhub.ai/user/jxyyjm)
- [YouTube Video Downloader service](https://skill.lordest.cn)
- [API key management](https://skill.lordest.cn/?page=apikeys)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration]

**Output Format:** [Markdown instructions with JSON, bash, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include API requests that send the user's API key and requested YouTube URL to the third-party service.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
