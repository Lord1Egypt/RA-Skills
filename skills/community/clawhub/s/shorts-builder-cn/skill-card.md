## Description:

剧情生成管道流技能。支持多剧集连续生成、图谱管理、AI质检+人工确认的双控机制。自动管理人物、场景、钩子的关联关系。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hexidyg](https://clawhub.ai/user/hexidyg)

### License/Terms of Use:


## Use Case:

Creators and agents use this skill to build Chinese short-drama story pipelines that generate connected episodes, track characters and hooks, run AI quality review, and wait for human approval before continuing. It supports pause, resume, modification, and multi-pipeline workflows through JSON-backed state.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Graph storage can access or delete JSON files outside its intended graph directory if a crafted pipeline ID is accepted.

Mitigation: Validate pipeline IDs before use and confine resolved graph paths to the graph storage directory before granting write or delete access.

Risk: The skill writes local JSON state and graph data for generated story pipelines.

Mitigation: Review the skill before installing it in workspaces that contain important JSON files, and run it with limited filesystem permissions where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hexidyg/skills/shorts-builder-cn)
- [Artifact skill definition](artifact/SKILL.md)
- [AI quality review template](artifact/templates/review_template.md)
- [Graph interface endpoint](https://framedream.art/n8n/webhook-test/open_frame_construct)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown story-generation prompts and previews, JSON review/state objects, and Python API guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language workflow with per-pipeline state, AI review scoring, user confirmation actions, and graph-backed continuity tracking.]

## Skill Version(s):

1.0.0 (source: server release metadata and scripts/__init__.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
