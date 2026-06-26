## Description: <br>
用于中文小说人物蒸馏、关系抽取、关系图谱导出与角色对话准备；当宿主需要基于小说内容生成结构化人物档案、关系结果或多角色对话上下文时使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wkbin](https://clawhub.ai/user/wkbin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and host-agent developers use this skill to turn Chinese novel text into structured character profiles, relationship artifacts, graph exports, and host-driven roleplay context. It is useful when an agent needs prompt payloads, local helper scripts, and schemas rather than direct model calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads source text and writes generated project outputs such as profiles, status files, and relationship graph artifacts. <br>
Mitigation: Run it in the intended project directory and review generated file changes before keeping or publishing them. <br>
Risk: Character profiles, relationship extraction, and dialogue context can be misleading when the source evidence is thin or contradictory. <br>
Mitigation: Use the included validation and safety policies, preserve evidence notes, and mark low-confidence results for revision. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wkbin/zaomeng-skill) <br>
- [Capability Index](references/capability_index.md) <br>
- [Output Schema](references/output_schema.md) <br>
- [Dialogue Handoff Contract](references/chat_contract.md) <br>
- [Safety Policy](references/safety_policy.md) <br>
- [Validation Policy](references/validation_policy.md) <br>
- [Scene Recommendation Context Example](examples/scene_recommendation_context.example.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown, JSON, Mermaid, HTML/SVG files, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Host performs model calls; helper scripts prepare prompt payloads, status files, persona bundles, and graph artifacts.] <br>

## Skill Version(s): <br>
4.1.8 (source: server evidence, SKILL.md frontmatter, .metadata.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
