## Description:

TikTok视频下载 helps an agent parse one or more TikTok video links through RedFox and return watermark-free download URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[redfox-data](https://clawhub.ai/user/redfox-data)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, editors, content collectors, and operations or research users use this skill to validate TikTok links, parse single or batch URLs, and obtain downloadable video, cover, audio, and description details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: TikTok URLs and the RedFox API key are sent to redfox.hk.

Mitigation: Use the skill only when that disclosure is acceptable, confirm the key source, scope, expiry, and revocation process, and rotate the key if it may have been exposed.

Risk: The security summary notes that URL validation is weaker than advertised.

Mitigation: Avoid submitting private or sensitive links until hostname validation is tightened, and review links before running the downloader.

Risk: The artifact supports saving the API key to a local configuration file.

Mitigation: Prefer the REDFOX_API_KEY environment variable over saving the key on disk.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/redfox-data/redfox-community/tree/main/skills/tiktok-video-downloader)
- [ClawHub skill page](https://clawhub.ai/redfox-data/skills/tiktok-video-downloader-2)
- [Core workflow](references/core_workflow.md)
- [RedFox API keys](https://redfox.hk/settings/api-keys?source=github)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown or plain text status output with optional JSON from the downloader script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns parsed media details such as download URL, cover URL, optional audio URL, description, duration, and batch success or failure counts; download links are described as expiring after about 5 minutes.]

## Skill Version(s):

0.1.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
