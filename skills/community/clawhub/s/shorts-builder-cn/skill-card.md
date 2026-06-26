## Description: <br>
剧情生成管道流技能。支持多剧集连续生成、图谱管理、AI质检+人工确认的双控机制。自动管理人物、场景、钩子的关联关系。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hexidyg](https://clawhub.ai/user/hexidyg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External creators and agent users use this skill to plan and generate serialized short-drama episodes, manage story state, review episode quality, and continue or revise pipelines with human confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores full generated story drafts locally. <br>
Mitigation: Avoid sensitive or proprietary story material and clear bundled sample pipeline state before starting a fresh workspace. <br>
Risk: The skill documents sending story content to a third-party graph webhook. <br>
Mitigation: Use only if that data sharing is acceptable for the material being developed. <br>
Risk: Security evidence notes an unchecked file-path helper that can modify files outside its intended folder. <br>
Mitigation: Do not pass arbitrary pipeline IDs until the graph path validation issue is fixed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hexidyg/shorts-builder-cn) <br>
- [Documented graph webhook](https://framedream.art/n8n/webhook-test/open_frame_construct) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-like structured story pipeline content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces episode prompts, generated story drafts, quality review prompts or results, pipeline status, and graph-management guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
