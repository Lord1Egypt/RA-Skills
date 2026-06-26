## Description: <br>
Convert YouTube videos into 9:16 vertical clips with burned-in captions and hook titles, optimized for TikTok, Reels, and Shorts using the MakeAIClips API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nosselil](https://clawhub.ai/user/nosselil) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, social media teams, and agents use this skill to submit YouTube URLs or video uploads to MakeAIClips, monitor clip generation, and retrieve captioned vertical clips for TikTok, Instagram Reels, and YouTube Shorts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a MakeAIClips API key. <br>
Mitigation: Keep the key in an environment variable, avoid pasting it into shared logs or prompts, and rotate it if it is exposed. <br>
Risk: YouTube URLs or uploaded video files are sent to makeaiclips.live for processing. <br>
Mitigation: Avoid confidential or restricted video content unless the user trusts that service and has reviewed its terms. <br>
Risk: Clip generation may consume service quotas or paid plan capacity. <br>
Mitigation: Review the service pricing, plan limits, and intended batch size before running bulk clipping jobs. <br>


## Reference(s): <br>
- [ClawHub skill release](https://clawhub.ai/nosselil/youtube-to-viral-clips-with-captions) <br>
- [MakeAIClips homepage](https://makeaiclips.live) <br>
- [MakeAIClips sign-up](https://makeaiclips.live/sign-up) <br>
- [MakeAIClips API key dashboard](https://makeaiclips.live/dashboard/api-key) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown guidance with JSON request examples, shell commands, and downloaded MP4 files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MAKEAICLIPS_API_KEY and sends YouTube URLs or uploaded video files to makeaiclips.live for processing.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
