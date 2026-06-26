## Description: <br>
智谱免费图片与视频生成技能，帮助用户用智谱/BigModel 生成图片、批量出图、生成短视频、查询视频任务结果并等待视频完成。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[156554395](https://clawhub.ai/user/156554395) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and users use this skill to create single images, batches of images, short videos, and video task status updates through Zhipu/BigModel generation APIs. It is useful for fast creative drafts, concept exploration, cover art, illustrations, and simple video ideation where free or low-cost models are preferred. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Zhipu/BigModel API key and sends prompts or media URLs to that provider. <br>
Mitigation: Use a dedicated or limited API key where possible, do not expose the key in outputs, and avoid confidential prompts or private media. <br>
Risk: Batch size, model selection, and video waits can affect quota, cost, and completion time. <br>
Mitigation: Confirm model choices, batch sizes, concurrency, and wait limits before large runs or production use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/156554395/zhipu-free-image-video) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with JSON results from Node scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires node, npm, and either IMAGE_VIDEO_GENERATION_API_KEY or ZHIPU_API_KEY. Script outputs may include generated media URLs, task IDs, status values, errors, selected model names, and prompt text.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
