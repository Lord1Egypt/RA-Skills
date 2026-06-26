## Description: <br>
VMake helps agents submit image and video watermark removal or quality restoration jobs to the paid Vmake media API and return the resulting media. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wemayiiii](https://clawhub.ai/user/wemayiiii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and external users use this skill when a user asks to remove watermarks or restore quality on images or videos. It guides credential checks, job submission, polling, and optional delivery through configured chat platforms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media may be uploaded to Vmake for processing. <br>
Mitigation: Require explicit user confirmation before processing and avoid submitting sensitive media unless the user accepts Vmake handling. <br>
Risk: Processing uses a paid, quota-consuming API. <br>
Mitigation: Confirm paid processing with the user and rely on official billing or administrator guidance instead of guessing prices. <br>
Risk: The skill can deliver media through configured chat-platform accounts. <br>
Mitigation: Use scoped chat credentials, validate recipients before delivery, and avoid sending results to unconfirmed destinations. <br>
Risk: Backend task invocation may exceed the four advertised operations. <br>
Mitigation: Restrict allowed task names to eraser_watermark, videoscreenclear, image_restoration, and hdvideoallinone. <br>
Risk: Unpinned dependencies can change behavior in production. <br>
Mitigation: Pin and review dependencies before production deployment. <br>


## Reference(s): <br>
- [ClawHub VMake release page](https://clawhub.ai/wemayiiii/vmake-skill) <br>
- [Vmake Developers API Key](https://vmake.ai/developers#api-key) <br>
- [README.md](README.md) <br>
- [docs/multi-platform.md](docs/multi-platform.md) <br>
- [docs/errors-and-polling.md](docs/errors-and-polling.md) <br>
- [docs/im-attachments.md](docs/im-attachments.md) <br>
- [docs/feishu-send-video.md](docs/feishu-send-video.md) <br>
- [sdk/README.md](sdk/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Text, Files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON CLI results, media result URLs, and chat delivery instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Vmake credentials and may use configured chat-platform credentials for delivery.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
