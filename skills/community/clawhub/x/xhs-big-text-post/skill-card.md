## Description: <br>
小红书大字图全流程制作技能。当用户需要制作小红书配图（带文字的大图、卖点图）时触发。完整流程：理解需求、精炼文案、用 AI 生成底图、叠加文字，并通过飞书发出。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cleanbinggmail](https://clawhub.ai/user/cleanbinggmail) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators and social media operators use this skill to turn short marketing or idea text into Xiaohongshu-style cover images with concise large-text copy. The workflow guides an agent through copy refinement, visual metaphor design, image generation, text overlay, and optional delivery through Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can send generated images through Feishu to a named recipient without an explicit confirmation step. <br>
Mitigation: Require confirmation that shows the exact generated file and Feishu destination before sending, or edit the skill so Feishu delivery is optional. <br>
Risk: Generated poster content may be used with private, client, business, or personal material. <br>
Mitigation: Review prompts, final image content, file path, and destination before delivery when sensitive or proprietary content is involved. <br>


## Reference(s): <br>
- [小红书大字图 — 详细工作流](artifact/references/workflow.md) <br>
- [ClawHub skill page](https://clawhub.ai/cleanbinggmail/xhs-big-text-post) <br>
- [Publisher profile](https://clawhub.ai/user/cleanbinggmail) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, files, guidance] <br>
**Output Format:** [Markdown guidance with image file paths and generated image assets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated images are stored under /workspace/xhs/ and final images may be sent through Feishu when that tool is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
