## Description:

This skill helps agents turn Chinese talking-head video cleanup requests into reviewable editing plans, deterministic ffmpeg commands, AI-HIVE generation steps, subtitles, timecodes, and vertical-video deliverables.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, training teams, sales teams, and short-video production teams use this skill to plan and execute Chinese talking-head video edits that remove repetition, pauses, and off-topic material while preserving argument flow and speaker voice. Developers or operators can use its scripts to create project briefs, inspect or reshape media with ffmpeg, and submit optional AI-HIVE image or video generation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an AI-HIVE API key and can upload selected media to a remote service.

Mitigation: Use the official HTTPS endpoint, prefer scoped or revocable credentials, avoid custom base URLs unless controlled, and upload only media the user is authorized to process.

Risk: The skill may overstate automatic editing coverage for pause removal, subtitles, and editorial timecodes.

Mitigation: Treat outputs as reviewable plans and helper commands; require human or agent review before accepting final cuts, subtitles, or timecodes.

Risk: Remote generation tasks may incur cost and produce outputs that need rights, brand, and factual review.

Mitigation: Confirm prompts, model, routing mode, pricing snapshot, input rights, and acceptance criteria before submitting paid or batch generation jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/talking-video-silence-cut-ai-hive)
- [AI-HIVE chat and API access](https://ai-hive.iclip.cn/chat)
- [AI-HIVE OpenAPI base endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline bash commands; helper scripts can produce JSON briefs and local media files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference AI-HIVE task IDs, routing modes, pricing snapshots, local file paths, and review checklists.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
