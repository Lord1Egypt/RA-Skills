## Description:

This skill helps short-drama directors, art teams, post-production teams, and continuity managers turn scripts, references, blocking, timelines, visual style, and adjacent shots into scene bibles, spatial relationships, lighting continuity, prop positions, camera-axis notes, AI-HIVE generation commands, and review checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, creative operations teams, and developers use this skill to plan short-drama scene continuity and generate auditable AI-HIVE image, video, and editing tasks. It is intended for authorized commercial, advertising, ecommerce, social, and short-drama workflows where scene, lighting, prop, character, and timeline consistency must be reviewed before paid generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scripts can store an AI-HIVE API key locally and use it for media generation requests.

Mitigation: Use a limited-scope API key, review ~/.ai-hive/config.json before running the skill, and avoid placing keys in prompts, scripts, logs, or shared repositories.

Risk: A user-configured base URL can redirect API-key-bearing requests away from the default AI-HIVE endpoint.

Mitigation: Use --base-url or AI_HIVE_BASE_URL only when the endpoint is controlled and trusted.

Risk: Image and video generation tasks may incur cost or upload authorized media to AI-HIVE.

Mitigation: Confirm prompt, model, routing mode, pricing snapshot, media rights, and batch size before submitting paid or bulk generation tasks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/short-drama-scene-continuity-ai-hive)
- [AI-HIVE chat entry](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands, JSON task records, and checklist sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include AI-HIVE task IDs, routing mode, model and pricing snapshots, generated file paths, and continuity review results.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
