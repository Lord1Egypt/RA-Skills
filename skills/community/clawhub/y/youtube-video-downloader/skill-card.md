## Description:

YouTube Video Downloader parses a YouTube video link through the redfox.hk API and returns direct video or audio download URLs in available formats and resolutions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, editors, collectors, and researchers use this skill to submit one YouTube video, Shorts, or youtu.be link and receive direct resource URLs for permitted offline saving, editing, backup, or analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Submitted URLs and the RedFox API key are sent to redfox.hk.

Mitigation: Use a revocable RedFox API key, avoid private or tokenized URLs, and install only when third-party processing by redfox.hk is acceptable.

Risk: The skill may be used to download videos without sufficient authorization.

Mitigation: Use it only with YouTube content you own or are authorized to download, and confirm that the intended use complies with applicable platform terms and law.

Risk: Long or unexpected API responses may be printed without output limits.

Mitigation: Review output before sharing it, avoid pasting sensitive URLs, and prefer controlled terminal or JSON handling when processing large responses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/youtube-video-downloader)
- [RedFox API key settings](https://redfox.hk/settings/api-keys?source=clawhub)
- [RedFox YouTube video download API endpoint](https://redfox.hk/story/api/parseWork/videoDownload/youtube)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style terminal text with full download and cover URLs, optional JSON output, and setup commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REDFOX_API_KEY; processes one video link per request; prints each returned resource without URL truncation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
