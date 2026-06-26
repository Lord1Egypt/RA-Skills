## Description: <br>
根据用户提示词，实现文生图、文生视频、图生视频，制作的素材用于地震应急数字化演练。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[daixihu2026](https://clawhub.ai/user/daixihu2026) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to generate realistic 16:9 disaster-response images and videos for earthquake emergency digital drills, optionally using one prepared asset image as input. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected assets, prompts, and generation metadata may be sent to Alibaba Cloud OSS and api.wuyinkeji.com. <br>
Mitigation: Use non-sensitive media and prompts, and verify third-party retention and access settings before use. <br>
Risk: The source notes that requests with uploaded asset images may intermittently fail with server errors. <br>
Mitigation: Treat generation as asynchronous and retry after a short wait when the external API returns a transient failure. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/daixihu2026/wenshengtu) <br>
- [Wuyinkeji generation API documentation](https://api.wuyinkeji.com/doc/60) <br>
- [Wuyinkeji result query API documentation](https://api.wuyinkeji.com/doc/36) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Files] <br>
**Output Format:** [Text guidance with API calls and generated media file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Asynchronous media generation; default output is a 15-second large 16:9 video or a 16:9 image, with files saved to the configured output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
