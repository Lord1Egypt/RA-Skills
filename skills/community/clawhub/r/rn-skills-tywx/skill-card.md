## Description: <br>
小红书爆款内容全自动创作助手，专注时尚穿搭与新中式美学赛道，自动完成素材收集、选题筛选、文案生成、AI配图和本地归档。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ykabps1314](https://clawhub.ai/user/ykabps1314) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators and marketing operators use this skill to generate Xiaohongshu fashion and neo-Chinese aesthetics posts, including trend-informed topics, captions, image prompts or images, metadata, and local output folders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The image helper can initiate fixed paid DashScope image generation outside the documented interactive workflow. <br>
Mitigation: Require explicit user confirmation for topic, image count, model, and estimated cost before invoking image generation. <br>
Risk: The helper uses shell-based curl and cp commands while interpolating prompt and path data. <br>
Mitigation: Replace shell execution with native Python HTTP requests and file operations before trusted deployment. <br>
Risk: The helper reads DASHSCOPE_API_KEY from ~/.zshrc and writes to hard-coded local output paths. <br>
Mitigation: Accept the API key and output directory through explicit configuration and avoid reading shell profile files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ykabps1314/rn-skills-tywx) <br>
- [Claude Code](https://claude.com/claude-code) <br>
- [Alibaba Cloud Bailian console](https://bailian.console.aliyun.com/) <br>
- [DashScope text-to-image API endpoint](https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Files, Configuration, Shell commands, API calls] <br>
**Output Format:** [Markdown copy, JSON metadata, image files, and concise run summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local output folders and call DashScope image generation when configured with DASHSCOPE_API_KEY.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
