## Description: <br>
Upscale videos to 720p, 1080p, 2K, or 4K resolution using WaveSpeed AI's Ultimate Video Upscaler. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chengzeyi](https://clawhub.ai/user/chengzeyi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation agents use this skill to prepare WaveSpeed AI API calls that upscale publicly accessible videos or uploaded video assets to a selected target resolution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video files or publicly accessible video URLs are sent to WaveSpeed AI for processing. <br>
Mitigation: Use the skill only when that data-sharing posture is acceptable for the video content. <br>
Risk: User-provided video URLs can introduce privacy and URL-validation concerns. <br>
Mitigation: Validate URLs and use trusted video sources before submitting them to the API. <br>
Risk: The skill requires a WaveSpeed API key. <br>
Mitigation: Store the API key in an environment variable or secret manager and do not hardcode or commit it. <br>
Risk: Video upscaling can incur usage-based costs. <br>
Mitigation: Monitor costs and choose target resolution intentionally before running upscaling jobs. <br>


## Reference(s): <br>
- [WaveSpeed API Key Access](https://wavespeed.ai/accesskey) <br>
- [ClawHub Skill Page](https://clawhub.ai/chengzeyi/wavespeed-ultimate-video-upscaler) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with JavaScript and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include WaveSpeed model ID, video URL input, target resolution, API-key setup, pricing notes, and error-handling guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
