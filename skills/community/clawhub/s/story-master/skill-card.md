## Description:

剧情生成管道流技能。支持多剧集连续生成、图谱管理、AI质检+人工确认的双控机制。自动管理人物、场景、钩子的关联关系。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hexidyg](https://clawhub.ai/user/hexidyg)

### License/Terms of Use:


## Use Case:

Writers, creative teams, and agent developers use this skill to run multi-episode story generation pipelines that preserve story state, query prior context, review episode quality, and wait for human confirmation before continuing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crafted pipeline IDs could cause local graph JSON reads, writes, or deletion outside the intended data folder.

Mitigation: Validate pipeline IDs, enforce storage-directory containment, and require explicit confirmation before graph deletion in any workspace with important local JSON files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hexidyg/skills/story-master)
- [Graph interface endpoint](https://framedream.art/n8n/webhook-test/open_frame_construct)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown story-generation prompts and JSON status or review payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains local pipeline state and graph JSON files for pause, resume, and multi-pipeline workflows.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
