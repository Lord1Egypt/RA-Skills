## Description: <br>
Generate short product videos from images using Runway Gen4 Turbo for TikTok ads, UGC-style product demos, Reels, and YouTube Shorts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and creators use this skill to turn product images and motion prompts into short vertical MP4 videos for social advertising and video pipelines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends the selected image and prompt to Runway and may incur Runway generation costs. <br>
Mitigation: Use a dedicated Runway API key, confirm content-handling expectations before submitting confidential inputs, and monitor generation duration and spend. <br>
Risk: The skill can read credentials from a shared ~/tiktok-api.json file if RUNWAY_API_KEY is not set. <br>
Mitigation: Prefer RUNWAY_API_KEY or a dedicated Runway-only secret instead of storing broader credentials in a shared config file. <br>
Risk: Generated video downloads depend on the URL returned by the Runway task response. <br>
Mitigation: Review outputs before downstream use and keep normal network and file handling controls in place for generated media. <br>


## Reference(s): <br>
- [Skill Runway Video Gen on ClawHub](https://clawhub.ai/Zero2Ai-hub/skill-runway-video-gen) <br>
- [Runway image-to-video API endpoint](https://api.dev.runwayml.com/v1/image_to_video) <br>
- [Runway task polling API endpoint](https://api.dev.runwayml.com/v1/tasks/{task_id}) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [MP4 video file with terminal status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv, Python 3.10 or newer, requests, and a Runway API key; duration is limited to 5 or 10 seconds.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter, artifact metadata, and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
