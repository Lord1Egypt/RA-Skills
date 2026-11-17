## Description:

For AI short drama, comic, virtual IP, and long-form content teams, this skill checks continuity across character appearance, clothing, props, tone, relationships, and timelines, then can help prepare authorized AI-HIVE media generation or video-processing workflows when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External content teams, marketers, and developers use this skill to turn Chinese serialized-character consistency requests into reviewable continuity reports, production plans, prompts, runnable commands, and acceptance checklists. It is intended for authorized source material and keeps stable character anchors separate from plot-approved changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may upload user-provided media to AI-HIVE.

Mitigation: Use only media the user is authorized to process and require confirmation before any upload.

Risk: Image or video generation can create billable AI-HIVE tasks.

Mitigation: Show the final prompt, model, routing mode, and expected task setup before submission; use a small sample before batch generation.

Risk: AI-HIVE API keys may be stored locally or exposed in logs.

Mitigation: Use limited API keys where available, keep keys in environment or local config only, and never echo real keys into prompts, screenshots, logs, or repositories.

Risk: Changing the default API endpoint can redirect uploads and generation requests.

Mitigation: Keep the default AI-HIVE endpoint unless the user controls the alternate endpoint and explicitly approves the change.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/serialized-character-consistency-ai-hive)
- [AI-HIVE workspace](https://ai-hive.iclip.cn/chat)
- [AI-HIVE OpenAPI endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON, Guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON task or project records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include routing mode, model and price snapshots, task IDs, task status, downloaded file paths, evidence locations, risk levels, repair suggestions, and review checklist items.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
