## Description:

This skill helps video editors, post-production teams, and short-video directors turn authorized reference videos into shot-duration tables, rhythm peaks and valleys, transition logic, B-roll lists, remake plans, prompts, runnable AI-HIVE commands, and quality checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, video editors, post-production teams, and short-video directors use this skill to analyze viral commercial video pacing and produce original, auditable plans for e-commerce, advertising, marketing, short drama, comic-video, social selling, and recommendation content. The skill can prepare reviewable plans first, then generate or edit media through AI-HIVE and ffmpeg workflows when the user confirms authorization, budget, and parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed or sent to an untrusted endpoint if users override the AI-HIVE base URL or share commands and logs.

Mitigation: Use only the official AI-HIVE endpoint unless a custom server is fully trusted, keep keys out of shared logs and screenshots, and store local configuration with restrictive permissions.

Risk: Video or image generation can create billable tasks and batch retries can duplicate costs.

Mitigation: Confirm prompts, routing mode, model, budget, and pricing snapshot before submission; run small samples before batch generation and keep a task ledger with task IDs.

Risk: Reference-video analysis can drift into unauthorized copying, misleading product claims, or platform-rule evasion.

Mitigation: Require authorized source materials, keep only abstract structure from references, rewrite characters, scenes, dialogue, visual style, and claims, and review factual statements before publication.

Risk: Local media processing depends on ffmpeg and writes transformed output files that may overwrite existing paths.

Mitigation: Install and review dependencies in an isolated Python environment, preserve original media files, and choose explicit output paths before running edit commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/viral-video-shot-rhythm-analyzer-ai-hive)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [AI-HIVE chat and API access](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands, JSON task records, generated configuration, and media file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include shot tables, rhythm analysis, transition plans, B-roll lists, prompts, AI-HIVE task IDs, pricing snapshots, status records, and ffmpeg output paths.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
