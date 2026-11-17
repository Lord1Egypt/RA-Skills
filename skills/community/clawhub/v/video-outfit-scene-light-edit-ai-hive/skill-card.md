## Description:

Helps short-video creators, advertising post-production teams, apparel brands, and social media teams turn video outfit, scene, and lighting edit requests into a reviewable workflow, runnable AI-HIVE commands, and continuity checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content teams use this skill to plan and execute authorized AI video outfit, background, and lighting edits for ecommerce, advertising, marketing, short drama, and social content. It produces reviewable briefs, prompts, commands, task records, and acceptance checks before submitting potentially billable generation jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential exposure or misuse through custom AI-HIVE endpoints.

Mitigation: Use the official AI-HIVE service, keep API keys out of logs and screenshots, and avoid custom --base-url or AI_HIVE_BASE_URL values with real credentials.

Risk: Sensitive or unauthorized media may be uploaded when generation or reference-video workflows are used.

Mitigation: Confirm rights and privacy clearance before using source media, and avoid sensitive media unless the upload destination and retention expectations are acceptable.

Risk: Generated media downloads may write files to an unexpected location.

Mitigation: Use --no-download for review-only runs or set a controlled output directory until download path handling is fixed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wubin1836/skills/video-outfit-scene-light-edit-ai-hive)
- [AI-HIVE entry point](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls, files]

**Output Format:** [Markdown with inline shell and Python commands, plus JSON task or blueprint files when scripts are used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include prompts, production briefs, task IDs, pricing snapshots, media upload references, local ffmpeg command output, and downloaded generated video or image files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
