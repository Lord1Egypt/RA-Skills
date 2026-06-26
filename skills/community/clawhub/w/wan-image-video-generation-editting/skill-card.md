## Description: <br>
Generates and edits images and videos with Wan 2.6 models through Alibaba DashScope, including text-to-image, image editing, text-to-video, image-to-video, and reference-to-video workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krisyejh](https://clawhub.ai/user/krisyejh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creators use this skill to submit Wan media-generation jobs, edit images from prompts and source images, and retrieve asynchronous video results from DashScope. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected image or media references are sent to Alibaba DashScope for remote processing. <br>
Mitigation: Avoid submitting sensitive, private, regulated, or unauthorized media, and review data-handling requirements before use. <br>
Risk: DashScope API usage can consume quota or incur billing. <br>
Mitigation: Use a dedicated API key, monitor quota and billing, and limit access to the key. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/krisyejh/wan-image-video-generation-editting) <br>
- [Bailian model marketplace](https://bailian.console.aliyun.com/cn-beijing?tab=model#/model-market) <br>
- [Wan 2.6 text-to-image API reference](references/wan2.6-t2i-api-doc.md) <br>
- [Wan 2.6 image editing API reference](references/wan2.6-image-api-doc.md) <br>
- [Wan 2.6 text-to-video API reference](references/wan2.6-t2v-api-doc.md) <br>
- [Wan 2.6 image-to-video API reference](references/wan2.6-i2v-api-doc.md) <br>
- [Wan 2.6 reference-to-video API reference](references/wan2.6-r2v-api-doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, JSON, Files, Guidance] <br>
**Output Format:** [Command-line text with generated media URLs, task IDs, and full JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and DASHSCOPE_API_KEY; video generation uses asynchronous task submission and polling.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
