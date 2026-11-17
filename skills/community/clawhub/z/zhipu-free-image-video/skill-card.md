## Description:

智谱免费图片与视频生成技能，帮助用户使用智谱生成图片、批量出图、生成短视频、查询视频任务结果、等待视频完成，或优先使用免费/低成本模型快速产出创意内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[156554395](https://clawhub.ai/user/156554395)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate single images, batches of image candidates, and short videos with Zhipu models, then query or wait for asynchronous video task results. It is suited to creative drafting, concept validation, and low-cost iteration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends prompts and optional image URLs to Zhipu's external image and video generation APIs.

Mitigation: Avoid sensitive prompts, private image URLs, or confidential materials unless the user is comfortable sharing them with that external service.

Risk: Long video wait settings or malformed polling parameters could keep the process running and generate excess API traffic.

Mitigation: Use bounded wait times, reasonable polling intervals, and stop or retry explicitly when a task times out.

Risk: The skill requires a Zhipu API key for API-backed generation.

Mitigation: Provide credentials through IMAGE_VIDEO_GENERATION_API_KEY or ZHIPU_API_KEY and do not expose API keys in prompts, logs, or generated output.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/156554395/skills/zhipu-free-image-video)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API Calls]

**Output Format:** [Markdown guidance with JSON inputs and JSON API results from Node scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and npm plus IMAGE_VIDEO_GENERATION_API_KEY or ZHIPU_API_KEY for Zhipu API access.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
