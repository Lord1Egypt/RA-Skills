## Description: <br>
Generates images with Alibaba Cloud Model Studio's Wan text-to-image API, including asynchronous task submission, status polling, and local image downloads. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouweico](https://clawhub.ai/user/zhouweico) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate images from prompts through DashScope Wan models, test low-cost drafts, poll existing tasks, and save generated images locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Review before execution as proposals could introduce incorrect or misleading guidance into skills. <br>
Mitigation: Review and scan skill before deployment. <br>

## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhouweico/wan-image-gen) <br>
- [Wan Image Generation API Notes](references/api.md) <br>
- [Alibaba Cloud Model Studio text-to-image v2 API reference](https://help.aliyun.com/zh/model-studio/text-to-image-v2-api-reference) <br>
- [Alibaba Cloud Model Studio text-to-image guide](https://help.aliyun.com/zh/model-studio/text-to-image) <br>
- [Alibaba Cloud Model Studio regions](https://help.aliyun.com/zh/model-studio/regions/) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, files] <br>
**Output Format:** [CLI text output, dry-run JSON, and downloaded image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js >= 18 and DASHSCOPE_API_KEY; sends prompts and request details to Alibaba Cloud DashScope and writes generated images to the selected output directory.] <br>

## Skill Version(s): <br>
0.1.1 (source: ClawHub release evidence; package.json reports 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
