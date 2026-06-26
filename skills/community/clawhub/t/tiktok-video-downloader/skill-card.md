## Description: <br>
Downloads TikTok videos without watermark in HD quality via savefbs.com when a user provides a TikTok URL, with a documented free tier and paid unlimited downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frankchen622](https://clawhub.ai/user/frankchen622) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to fetch download-link options for public TikTok videos when they need offline access or watermark-free variants. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: TikTok URLs are sent to savefbs.com, and the security evidence says privacy and payment claims do not match the code closely enough for automatic trust. <br>
Mitigation: Review before installing and use the skill only when the user is comfortable sharing the TikTok URL with savefbs.com. <br>
Risk: The skill includes an embedded crypto payment link without a server-verified payment and unlock process in the evidence. <br>
Mitigation: Do not use the embedded payment link unless the publisher provides a verifiable payment and unlock process. <br>
Risk: The downloader writes a local quota-tracking file in the OpenClaw skills directory. <br>
Mitigation: Inform users to expect local quota tracking and review or remove that file according to their local data-retention expectations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/frankchen622/tiktok-video-downloader) <br>
- [savefbs.com](https://savefbs.com) <br>
- [savefbs.com pricing](https://savefbs.com/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, guidance] <br>
**Output Format:** [JSON from the downloader script, typically summarized as Markdown download options by the agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes download URLs, quality labels, media extension, usage counts, and error details when a video is unavailable.] <br>

## Skill Version(s): <br>
1.2.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
