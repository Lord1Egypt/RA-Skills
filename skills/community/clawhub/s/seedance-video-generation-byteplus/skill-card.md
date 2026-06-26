## Description: <br>
Generate AI videos using BytePlus Seedance API (International) from text prompts, images, first and last frames, or reference images, and query or manage video generation tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JackyCSer](https://clawhub.ai/user/JackyCSer) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers and external users use this skill to create, monitor, download, and manage BytePlus Seedance video generation tasks from an agent or terminal workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send prompts and selected local images or generated videos to external services including BytePlus and optionally Feishu. <br>
Mitigation: Use it only when that external sharing is approved, and avoid confidential local paths, sensitive media, and sensitive prompts. <br>
Risk: The scanner flags macOS auto-open behavior after downloads through an unsafe shell command. <br>
Mitigation: Review or disable the auto-open behavior before use, especially in workflows that handle untrusted task IDs, file paths, or generated media. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/JackyCSer/seedance-video-generation-byteplus) <br>
- [BytePlus Video Generation API](https://docs.byteplus.com/en/docs/ModelArk/Video_Generation_API) <br>
- [BytePlus API Key Management](https://console.byteplus.com/ark/region:ark+ap-southeast-1/apiKey) <br>
- [BytePlus Model List and Pricing](https://docs.byteplus.com/en/docs/ModelArk/1330310) <br>
- [BytePlus API Call Guide](https://docs.byteplus.com/en/docs/ModelArk/1366799) <br>
- [BytePlus Prompt Guide](https://docs.byteplus.com/en/docs/ModelArk/1587797) <br>
- [Feishu Video Sending Guide](how_to_send_video_via_feishu_app.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with Python CLI commands, curl examples, and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can create asynchronous video tasks, poll status, download MP4 outputs, and optionally route generated videos to Feishu.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
