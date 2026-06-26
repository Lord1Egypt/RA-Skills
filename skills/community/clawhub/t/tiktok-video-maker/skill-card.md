## Description: <br>
Generate TikTok-style talking videos from a script and image using the LovelyBots API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georgegally](https://clawhub.ai/user/georgegally) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, marketing teams, ecommerce brands, and developers use this skill to queue, monitor, and retrieve talking-video generation jobs from scripts and images through LovelyBots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-provided scripts and images to LovelyBots for video generation. <br>
Mitigation: Install only if you trust LovelyBots with that content and avoid sending sensitive scripts or images unless approved for that service. <br>
Risk: The LovelyBots API key can authorize credit-consuming video generation. <br>
Mitigation: Keep LOVELYBOTS_API_KEY secret, do not commit or log it, and confirm generation before using the skill at scale. <br>
Risk: Returned video_url and share_url values may allow others to access generated videos. <br>
Mitigation: Share or log returned URLs only when the generated video is intended to be accessible to those recipients. <br>


## Reference(s): <br>
- [TikTok Video Maker on ClawHub](https://clawhub.ai/georgegally/tiktok-video-maker) <br>
- [LovelyBots OpenClaw documentation](https://lovelybots.com/openclaw) <br>
- [LovelyBots developer API keys](https://lovelybots.com/developer) <br>
- [LovelyBots API base URL](https://api.lovelybots.com/api) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration instructions, API Calls] <br>
**Output Format:** [Markdown guidance with bash and JSON examples; completed jobs return a video URL.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires LOVELYBOTS_API_KEY, curl, python3, a LovelyBots account, and an active subscription plan.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
